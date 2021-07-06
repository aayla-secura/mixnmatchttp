from mixnmatchttp.log import get_loggers, clear_loggers

loggers = get_loggers(
    {
        #  'DEBUG': [set('')],
        'DEBUG': [['']],
        'INFO': [['', None, 'info.log']],
        'WARNING': [['', None], ['dup', None]],
    },
    logdir='log',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'bold',
        'WARNING': 'purple',
        'ERROR': 'bold,red',
        'CRITICAL': 'bold,fg_white,bg_red',
    },
    dbgfmt='%(foo_log_color)sFOO%(reset_log_color)s%(log_color)s%(message)s',
    secondary_log_colors={
        'foo': {
            'DEBUG': 'bg_blue,fg_black',
            'INFO': 'bg_white,fg_black',
            'WARNING': 'bg_yellow,fg_black',
            'ERROR': 'bg_purple,fg_white',
            'CRITICAL': 'bold,fg_white,bg_red',
        },
        'reset': {
            'DEBUG': 'reset',
            'INFO': 'reset',
            'WARNING': 'reset',
            'ERROR': 'reset',
            'CRITICAL': 'reset',
        },
    }
)

loggers[''].critical('critical')
loggers[''].error('error')
loggers[''].warning('warning')
loggers[''].info('info')
loggers[''].debug('debug')
loggers['dup'].error('dup error')

clear_loggers(
    loggers,
    {
        'INFO': [['', 'info.log']]
    },
    logdir='log'
)

loggers[''].critical('! critical')
loggers[''].error('! error')
loggers[''].warning('! warning')
loggers[''].info('! info')
loggers[''].debug('! debug')

clear_loggers(
    loggers,
    {
        'DEBUG': [set('')],
        #  'DEBUG': [['']],
        'INFO': [['', None]],
        'WARNING': [['', None]],
        'ERROR': [['', None]],
        'CRITICAL': [['', None]],
    },
    logdir='log'
)
loggers[''].critical('!! critical')
loggers[''].error('!! error')
loggers[''].warning('!! warning')
loggers[''].info('!! info')
loggers[''].debug('!! debug')
