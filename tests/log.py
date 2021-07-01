from mixnmatchttp.log import get_loggers

logger = get_loggers(
    {
        'DEBUG': [['']],
        'INFO': [['', None, 'info.log']],
        'WARNING': [['', None]],
    }, logdir='log', color=True)['']

logger.critical('critical')
logger.error('error')
logger.warning('warning')
logger.info('info')
logger.debug('debug')
