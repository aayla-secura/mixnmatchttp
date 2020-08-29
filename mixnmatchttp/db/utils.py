import logging
from contextlib import contextmanager
import re
import os.path

from sqlalchemy import create_engine, inspect, and_, event
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.engine import Engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import Session, \
    scoped_session, sessionmaker, joinedload
from sqlalchemy.orm.util import class_mapper

from .exc import ObjectConversionError, ObjectNotFoundError, \
    ObjectExistsError, ServerDBError, MetadataMistmatchError
from .is_db_sane import is_db_sane
from ..utils import is_seq_like, is_map_like, is_time_like, \
    date_from_timestamp


logger = logging.getLogger(__name__)


class DBConnection:
    '''Holds the current engine, scoped session maker and inspector

    The configure method sets or changes those
    '''

    __instances = {}  # by DB engine

    def __init__(self,
                 base,
                 url,
                 session_kargs={},
                 engine_kargs={}):
        '''Binds the session maker and base, and creates the inspector

        Also clears the current maps and checks the database for
        consistency.
        - base is a declarative base
        - For SQLite databases:
          - url should be sqlite:///<file>, where file can be
            :memory:, or sqlite://
          - If the database uses a file (rather than in memory) and
            the file does not exist, it and all tables are created.
        - For other databases:
          - url should contain the database, i.e.
            dialect://[username:password@]host/db
          - If the database specified in the URL does not exists, it
            and all tables are created.
        Returns the DBConnection instance itself.
        '''

        self.__base = base
        engine = self._get_engine(url)
        if engine is None:
            engine = self._create_engine(url, engine_kargs)
        self.__instances[engine] = self
        self.__engine = engine
        self.__session = scoped_session(sessionmaker(
            bind=engine, **session_kargs))
        self.__base.metadata.bind = engine
        self._create_db(engine_kargs)
        self._ensure_is_sane()
        self.__inspector = Inspector.from_engine(engine)
        self.__maps = {}
        self.__listeners = {}

    @property
    def base(self):
        '''Declarative base as passed to __init__'''

        return self.__base

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        '''Thread-local session registry

        All calls to DBConnectionInstance.session() within the same
        thread will get a handle on the same session.
        '''

        return self.__session

    @property
    def inspector(self):
        '''Inspector from the engine'''

        return self.__inspector

    @property
    def maps(self):
        '''Per-class mappings, populated by object_from_dict'''

        return self.__maps

    @property
    def url(self):
        '''Engine URL as a string'''

        engine = self.__engine
        if engine is None:
            return None
        return str(engine.url)

    @property
    def listeners(self):
        '''Event listeners'''

        return self.__listeners

    @classmethod
    def get(cls, key):
        '''key is an engine, session or a declarative base'''

        logger.debug('Looking up DBConnection based on {}'.format(
            key))
        if isinstance(key, (Session, scoped_session)):
            engine = key.bind
        elif isinstance(key, DeclarativeMeta):
            engine = key.metadata.bind
        elif isinstance(key, Engine):
            engine = key
        else:
            raise TypeError(
                'Looking up DBConnection is done using either '
                'an engine, session or a declarative base, '
                'not {}'.format(type(key)))
        logger.debug('Found engine {}'.format(engine))
        try:
            return cls.__instances[engine]
        except KeyError:
            return None

    def listen(self, event_name, handler):
        '''Register a handler for an event

        TODO: ability to remove the current one for this event
        '''

        try:
            current_handler = self.listeners[event_name]
        except KeyError:
            self.listeners[event_name] = handler
        else:
            if current_handler is handler:
                return

        @event.listens_for(self.session, event_name)
        def listener(*args):
            return handler(*args)

    def populate_maps(self, cls):
        tbl = cls.__tablename__
        if tbl in self.maps:
            return

        columns = {}
        uniq_column_sets = []
        relationships = {}
        primary_key = None
        for c in cls.__mapper__.columns:
            columns[c.name] = c.type
            if c.primary_key or c.unique:
                uniq_column_sets.append([c.name])
                if c.primary_key:
                    primary_key = c.name
        for i in self.inspector.get_indexes(tbl):
            if i['unique']:
                uniq_column_sets.append(i['column_names'])
        for u in self.inspector.get_unique_constraints(tbl):
            uniq_column_sets.append(u['column_names'])
        for r in cls.__mapper__.relationships:
            relationships[r.key] = {
                'class': r.mapper.class_,
                'keys': None}
            if len(r.local_remote_pairs) != 1:
                continue
            lrpair = r.local_remote_pairs[0]
            if lrpair[0].foreign_keys:
                if len(lrpair[0].foreign_keys) > 1 or \
                        len(lrpair[1].foreign_keys) > 1:
                    raise NotImplementedError(
                        ('Multiple foreign keys on {}.{} '
                         'relationship').format(tbl, r.key))
                relationships[r.key]['keys'] = \
                    keys = (lrpair[0].name, lrpair[1].name)

        self.maps[tbl] = {}
        self.maps[tbl]['primary_key'] = primary_key
        self.maps[tbl]['columns'] = columns
        self.maps[tbl]['relationships'] = relationships
        self.maps[tbl]['uniq_column_sets'] = uniq_column_sets
        logger.debug('primary_key for {} = {}'.format(
            tbl, primary_key))
        logger.debug('columns for {} = {}'.format(tbl, columns))
        logger.debug('relationships for {} = {}'.format(
            tbl, relationships))
        logger.debug('uniq_column_sets for {} = {}'.format(
            tbl, uniq_column_sets))

    def _create_db(self, engine_kargs):
        exists = False
        dbname = self.engine.url.database
        if self.url.startswith('sqlite'):
            if dbname is not None and os.path.isfile(dbname):
                exists = True
        else:
            baseurl = self.url
            if dbname:
                baseurl = baseurl.replace('/{}'.format(dbname), '')
            engine = create_engine(baseurl, **engine_kargs)
            insp = Inspector.from_engine(engine)
            if dbname in insp.get_schema_names():
                exists = True
            else:
                logger.debug('Creating database')
                with engine.connect() as connection:
                    # TODO detect error
                    connection.execute(
                        'CREATE DATABASE {}'.format(dbname))
        if not exists:
            logger.debug('Creating tables')
            self.base.metadata.create_all(self.engine)
        return exists

    def _get_engine(self, url):
        for e in self.__instances:
            if str(e.url) == url:
                return e
        return None

    def _create_engine(self, url, engine_kargs):
        engine = create_engine(url, **engine_kargs)
        return engine

    def _ensure_is_sane(self):
        '''Checks the database for consistency

        The database must exist.
        '''

        with self.session_context() as session:
            if not is_db_sane(self.base, session):
                error = MetadataMistmatchError(
                    'Metadata has changed since database '
                    'creation. Delete the database if you '
                    'want it to be recreated.')
                logger.error(str(error))
                raise error

    @contextmanager
    def session_context(self,
                        reraise=True,
                        commit_at_end=True,
                        close_at_end=True,
                        **kargs):
        '''Creates a context with an open SQLAlchemy session.'''

        session = self.session()
        for k, v in kargs.items():
            setattr(session, k, v)
        try:
            yield session
            if commit_at_end:
                session.commit()
        except (DatabaseError, ServerDBError) as e:
            logger.error(str(e))
            session.rollback()
            if reraise:
                raise
        finally:
            if close_at_end:
                #  session.expunge_all()
                session.close()


def parse_db_url(url):
    '''Returns a dictionary

    with dialect, user, password, host, port, database, query
    '''

    # TODO detect invalid SQLite?

    m = re.search((
        '^(?P<dialect>[^:/]+)://'
        '('
        '((?P<user>[^@/:]+)(:(?P<password>.*))?@)?'
        '(?P<host>[^@:/]+)(:(?P<port>[0-9]+))?'
        ')?'
        '(/(?P<database>[^?]+)(\?(?P<query>.+))?)?$'), url)
    if not m:
        return None
    return m.groupdict()

def is_base(cls):
    '''Returns True if cls is a declarative base'''

    return isinstance(cls, DeclarativeMeta) and not is_mapper(cls)

def is_mapper(cls):
    '''Returns True if cls is a mapper class'''

    try:
        class_mapper(cls)
    except UnmappedClassError:
        return False
    return True

def filter_results(db,
                   cls,
                   fparams,
                   expect_one=False,
                   load=[],
                   joining=and_):
    '''Returns the filtered result of a query on the given class

    - db is a database session
    - cls is a table object
    - fparams is a dictionary of column names and comparison values
      - it supports a nested dictionary up to one level, i.e. the
        top-most values can be dictionaries, but their values have to
        be flat
    - If expect_one is True, then one() is called finally, otherwise
      all()
    - load is a list of attributes (as names) which should be loaded
      eagerly
    - joining is an expression operator determining how to join
      clauses
    '''

    def get_attrs(attrnames):
        return [getattr(cls, k) for k in attrnames]

    def get_filter():
        return joining(*[
            getattr(cls, k).has(**v) if isinstance(v, dict)
            else getattr(cls, k) == v
            for k, v in fparams.items()])

    options = []
    if load:
        options = [joinedload(*get_attrs(load))]
    res = db.query(cls).filter(get_filter()).options(*options)
    if expect_one:
        return res.one()
    return res.all()

def object_to_dict(obj,
                   skip='_id$',
                   no_skip=None,
                   max_depth=None,
                   convert_timestamp=date_from_timestamp,
                   short_mappings={}):
    '''Returns a dictionary of the mapper object's columns

    Supports relationships (converts these to dictionaries).
    - skip is a regex of keys to be skipped. If None, nothing is
      skipped.
    - noskip is a regex of keys to be included and overrides any match
      in skip.
    - If max_depth is given, then it specifies the maximum depth of
      the dictionary. At the last level, objects are converted to
      strings via a predefined format containing one or more columns.
      - The format is controlled by short_mappings: a dictionary where
        each key is a table name and each value is a list of
        format_string, [value_1, [value_2]], i.e. the string value
        will be format_string.format(value_1, ...).
        - Default is:
          short_mappings = {
              'user': ['{}', 'username'],
              'session': ['{}', 'token'],
              'role': ['{}', 'name']}
        If the table name is not found in short_mappings, then the id
        column is returned (which must exist).
        The dictionary given in short_mappings adds to the default,
        rather than replacing it.
      - If max_depth is 0, then this function returns a string, rather
        than a dictionary
    - If convert_timestamp is not None, it must be a callable which
      takes a single argument (the timestamp) and returns a formatted
      date. It is used for values which look like timestamps.
      We guess by looking for values which are non-negative numbers up
      to the current timestamp (in seconds or milliseconds) + 10 years
      and with keys containing the word "time" or "date" (non-case
      sensitive). Both conditions have to match for the value to be
      converted. Local timezone is assumed.
    '''

    if max_depth is not None and max_depth < 0:
        raise ValueError('max_depth must be non-negative')

    return _object_to_dict(obj,
                           skip=skip,
                           no_skip=no_skip,
                           max_depth=max_depth,
                           convert_timestamp=convert_timestamp,
                           short_mappings=short_mappings)

def _object_to_dict(obj,
                    skip,
                    no_skip,
                    max_depth,
                    convert_timestamp,
                    short_mappings,
                    seen=None):
    def transform_value(key, val, seen):
        if is_seq_like(val):
            result = []
            first = True
            for e in val:
                v = transform_value(key, e, seen)
                result.append(v)
                first = False
            return result
        elif convert_timestamp is not None and is_time_like(val) \
                and re.search('time|date', key, re.IGNORECASE):
            return convert_timestamp(val)
        elif is_mapper(val.__class__):
            logger.debug('tansforming {}, seen: {}'.format(
                val.__tablename__, seen))
            if val.__tablename__ in seen:
                this_max_depth = 0
                logger.debug(
                    '{} already seen'.format(val.__tablename__))
            elif max_depth is None:
                this_max_depth = None
            else:
                this_max_depth = max_depth - 1
            seen = seen.union([val.__tablename__])
            return _object_to_dict(
                val,
                skip=skip,
                no_skip=no_skip,
                short_mappings=short_mappings,
                max_depth=this_max_depth,
                convert_timestamp=convert_timestamp,
                seen=seen)
        # assume it's a simple value like int or string
        # should we check here if it's JSON serializable and ommit
        # if not?
        return val

    def get_short_value(obj):
        _short_mappings = {
            'user': ['{}', 'username'],
            'session': ['{}', 'token'],
            'role': ['{}', 'name']}
        _short_mappings.update(short_mappings)
        try:
            fmt = _short_mappings[obj.__tablename__]
        except KeyError:
            fmt = ['{}', 'id']
        vals = []
        for attr in fmt[1:]:
            val = getattr(obj, attr)
            while is_mapper(val.__class__):
                val = get_short_value(val)
            vals.append(val)
        return fmt[0].format(*vals)

    if max_depth == 0:
        return get_short_value(obj)
    insp = inspect(obj)
    data = {}
    if seen is None:
        seen = set([obj.__tablename__])
    for attr in insp.attrs:
        if (skip is not None and re.search(skip, attr.key)) \
                and (no_skip is None
                     or not re.search(no_skip, attr.key)):
            continue
        val = transform_value(attr.key, attr.value, seen)
        data[attr.key] = val
    return data

def object_from_dict(db, cls, dic,
                     must_not_exist=False,
                     children_must_not_exist=False,
                     must_exist=False,
                     children_must_exist=False,
                     idprops={},
                     add=False):
    '''Creates or updates an object from a dictionary

    - If the dictionary describes uniquely an object already in the
      database, then it is retrieved and updated.
      Otherwise, the object is created.
    - The object is added to the session unless add is False.
      - NOTE: setting add to False will cause problems when creating
        an object which has a *ToMany relationship with another table
        (call it B), since in those cases it's possible to create many
        identical objects B which violate a unique constraint.
    - If idprops is given, they key--values in it are used to identify
      an existing object, but not used to update.
      E.g. if idprops = {'name': 'foo'} and dic = {'name': 'bar'},
      this will rename foo to bar
    - If must_not_exist is True, the object is only created, not
      updated and an ObjectExistsError is raised if it exists.
    - If children_must_not_exist is True, then any children of the
      object must be newly created, otherwise the same exception is
      raised.
    - If must_exist is True, then the object is only updated, not
      created and an ObjectNotFoundError is raised if it does not
      exist.
    - If children_must_exist is True, then any children of the object
      must exist, otherwise the same exception is raised.
    - Returns the object.
    '''

    def uniq_props():
        uprops = idprops.copy()
        required_cols_supplied = \
            not dbconn.maps[tbl]['uniq_column_sets']
        for ucset in dbconn.maps[tbl]['uniq_column_sets']:
            this_set_supplied = True
            for c in ucset:
                if c in props:
                    # don't overwrite value from idprops
                    if c == primary_key:
                        return {c: uprops.get(c, props[c])}
                    uprops.setdefault(c, props[c])
                else:
                    this_set_supplied = False
            required_cols_supplied = required_cols_supplied or \
                this_set_supplied
        if required_cols_supplied:
            return uprops

    tbl = cls.__tablename__
    dbconn = DBConnection.get(db)
    assert dbconn is not None

    if must_exist:
        logger.debug('Updating {} from dict'.format(tbl))
    elif must_not_exist:
        logger.debug('Creating {} from dict'.format(tbl))
    else:
        logger.debug('Creating or updating {} from dict'.format(tbl))
    logger.debug('idprops for {} = {}'.format(tbl, idprops))
    dbconn.populate_maps(cls)
    primary_key = dbconn.maps[tbl]['primary_key']
    columns = dbconn.maps[tbl]['columns']
    relationships = dbconn.maps[tbl]['relationships']
    uniq_column_sets = dbconn.maps[tbl]['uniq_column_sets']

    props = {}

    for key, val in dic.items():
        if key in columns:
            logger.debug('{}.{} = {}'.format(tbl, key, val))
            props[key] = val
        elif key in relationships:
            logger.debug('{} is a relationship'.format(key))
            if is_seq_like(val):
                props[key] = [
                    object_from_dict(
                        db, relationships[key]['class'], d,
                        must_not_exist=children_must_not_exist,
                        children_must_not_exist=must_not_exist,
                        must_exist=children_must_exist,
                        children_must_exist=children_must_exist,
                        add=add)
                    for d in val]
            elif is_map_like(val):
                lrkeys = relationships[key]['keys']
                # If the object we are about to create is a child and
                # requires the foreign key of that relationship set,
                # it should not be added to the database now. It
                # should be added along with the parent. So set
                # add=False if lrkeys is not None.
                # For example, when creating a Participant where an
                # Ownage has been provided, _object_from_dict will
                # create the Ownage before querying the database to
                # see if the Participant exists. In that case, if
                # the object is added, an exception will be raised
                # when the session is flushed since the required
                # attributes of hacker_id and victim_id for the Ownage
                # object are not populated.
                props[key] = object_from_dict(
                    db, relationships[key]['class'], val,
                    must_not_exist=children_must_not_exist,
                    children_must_not_exist=must_not_exist,
                    must_exist=children_must_exist,
                    children_must_exist=children_must_exist,
                    add=(lrkeys is None))
                if lrkeys is not None:
                    # get the value on the remote side of this foreign
                    # key and add it to the object we are creating
                    # here, as it may be used to look up an existing
                    # object below
                    rval = getattr(props[key], lrkeys[1])
                    if rval is not None:
                        props[lrkeys[0]] = rval
                        logger.debug(
                            '{}.{} = {} from relationship'.format(
                                tbl, lrkeys[0], rval))
            else:
                raise ObjectConversionError(
                    ('{} should be a dictionary or a'
                     'list of dictionaries').format(key))
        else:
            raise ObjectConversionError(
                '{} is not a column of {}'.format(key, tbl))

    # check if the object has unique column sets, and if so, try to
    # look it up
    uprops = uniq_props()
    if uprops:
        logger.debug('Looking for {} based on {}'.format(
            tbl, uprops))
        res = filter_results(db, cls, uprops)
        assert len(res) <= 1
        if res:
            logger.debug('Found {} in DB'.format(tbl))
            if must_not_exist:
                raise ObjectExistsError(
                    ('A new {} object requested, '
                     'but one already exists').format(tbl))
            obj = res[0]
            for k, v in props.items():
                setattr(obj, k, v)
            return obj

    if must_exist:
        raise ObjectNotFoundError(
            '{} object must exist but not found'.format(tbl))
    logger.debug('Creating {} object'.format(tbl))
    try:
        obj = cls(**props)
    except (ValueError, TypeError) as e:
        raise ServerDBError(str(e))
    if add:
        logger.debug('Adding {} object'.format(tbl))
        db.add(obj)
    return obj

def bulk_objects_from_dicts(db, cls, dics, **kargs):
    '''Creates or updates objects from a list of dictionaries

    Keyword arguments are same as object_from_dict
    '''

    result = []
    for dic in dics:
        obj = object_from_dict(db, cls, dic, **kargs)
        result.append(obj)
    return result

def delete_from_dict(db, cls, dic):
    '''Deletes an object from a dictionary

    - Returns True if object was found (and deleted), False otherwise.
    '''

    try:
        obj = object_from_dict(
            db, cls, dic, must_exist=True, add=False)
    except ObjectNotFoundError:
        return False
    db.delete(obj)
    return True

def update_from_dict(db, cls, dic, idprops={}):
    '''Updates an object from a dictionary

    Same as object_from_dict, except it requires it to exist
    '''

    return object_from_dict(db, cls, dic,
                            idprops=idprops,
                            must_exist=True)

def bulk_update_from_dicts(db, cls, dics, idprops={}):
    '''Updates objects from a list of dictionaries

    Same as bulk_objects_from_dicts, except it requires them to exist
    '''

    return bulk_objects_from_dicts(db, cls, dics,
                                   idprops=idprops,
                                   must_exist=True)
