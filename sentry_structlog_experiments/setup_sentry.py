import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger

from .env_vars import ENVIRONMENT, SENTRY_DSN
from .setup_logs import StructlogAwareMessageFormatter

IGNORE_LOGGERS = [
    'django_structlog.middlewares.request'
]


def configure():
    for logger in IGNORE_LOGGERS:
        ignore_logger(logger)

    logging_integration = LoggingIntegration()
    attr_map = StructlogAwareMessageFormatter.DEFAULT_ATTR_MAP + (('request_id', 'request_id', None),)
    for attr_name, attr_value in vars(logging_integration).items():
        if isinstance(attr_value, logging.Handler):
            attr_value.setFormatter(StructlogAwareMessageFormatter(copy_record=False, attr_map=attr_map))

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), logging_integration],
        environment=ENVIRONMENT
    )
