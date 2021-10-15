import logging
import logging.config
import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
        },
        'collect': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        }
    },

    'handlers': {
        # 打印到终端的日志
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'collect'
        },
        # 打印到文件的日志:收集错误及以上的日志
        'info': {
            'level': 'info'.upper(),
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'filename': os.path.dirname(os.path.realpath(__file__)) + '/log',
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 5M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': 'utf-8',
        },
    },

    'loggers': {
        '': {
            'handlers': ['console','info'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


def logger():
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger(__name__)
    return logger

