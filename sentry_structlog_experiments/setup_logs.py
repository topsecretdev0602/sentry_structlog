import logging.config
import os
from typing import Dict, Any, Union

import structlog

from .env_vars import PROJECT_ROOT, DJANGO_LOG_LEVEL
from .structlog_sentry_util import SentryJsonProcessor

LOG_FILTER_PATHS = []


def add_module_and_lineno(logger: Union[logging.Logger, structlog.stdlib.BoundLogger],
                          name: str,
                          event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add module and line number to the event dict
    Args:
        logger(structlog.stdlib.BoundLogger): stuctlog logger
        name(str): logger method (info/debug/..)
        event_dict(dict): log event dict
    Returns:
        event_dict (dict)
    """
    # see https://github.com/hynek/structlog/issues/253 for a feature request to get this done better
    # noinspection PyProtectedMember,PyUnresolvedReferences
    frame, module_str = structlog._frames._find_first_app_frame_and_name(additional_ignores=[__name__, 'logging'])
    event_dict['modline'] = f'{module_str}:{frame.f_lineno}'
    return event_dict


def filter_logs(logger: structlog.stdlib.BoundLogger, method_name: str, event_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Drop log events based on the request path
    Args:
        logger(structlog.stdlib.BoundLogger): stuctlog logger
        method_name(str): logger method (info/debug/..)
        event_dict(dict): log event dict
    Returns:
        event_dict (dict)
    """
    event_path = event_dict.get('request_path', '')
    for filter_path in LOG_FILTER_PATHS:
        if filter_path in event_path:
            raise structlog.DropEvent
    return event_dict


FOREIGN_PRE_CHAIN_PROCESSORS = (  # For logs being emitted from logging.Logger but use structlog's ProcessFormatter
    structlog.processors.TimeStamper(fmt='iso'),
    structlog.stdlib.add_log_level,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
    add_module_and_lineno,
)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json_formatter': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(),
            'foreign_pre_chain': FOREIGN_PRE_CHAIN_PROCESSORS,
        },
        'colored': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.dev.ConsoleRenderer(colors=True),
            'foreign_pre_chain': FOREIGN_PRE_CHAIN_PROCESSORS,
        },
        'key_value': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.KeyValueRenderer(key_order=['timestamp', 'level', 'event', 'logger']),
            'foreign_pre_chain': FOREIGN_PRE_CHAIN_PROCESSORS,
        }
    },
    'handlers': {
        'app': {
            'level': DJANGO_LOG_LEVEL,
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'logs', 'app.log'),
            'formatter': 'json_formatter'
        },
    },
    'loggers': {
        'app': {
            'handlers': ['app'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


def configure():
    structlog.configure(
        processors=[
            filter_logs,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(remove_positional_args=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            add_module_and_lineno,
            SentryJsonProcessor(level=logging.ERROR)
            # structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
