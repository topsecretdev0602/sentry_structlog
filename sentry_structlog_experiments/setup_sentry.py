import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger

from .env_vars import ENVIRONMENT, SENTRY_DSN
from .setup_logs import StructlogAwareMessageFormatter

IGNORE_LOGGERS = [
    'django_structlog.middlewares.request'
]


def configure(**sentry_sdk_init_kwargs):
    for logger in IGNORE_LOGGERS:
        ignore_logger(logger)

    logging_integration = LoggingIntegration()
    attr_map = [
        StructlogAwareMessageFormatter.AttrMapItem(record_attr_name='request_id',
                                                   event_dict_key='request_id',
                                                   default_value=None)
    ]

    # We attach our structlog aware formatter to sentry logging handlers
    for attr_name, attr_value in vars(logging_integration).items():
        if isinstance(attr_value, logging.Handler):
            # we have to pass copy_record False because Sentry handler expects inplace formatting
            # Fortunately, Sentry's handlers are called last in chain
            attr_value.setFormatter(StructlogAwareMessageFormatter(copy_record=False, attr_map=attr_map))

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), logging_integration],
        environment=ENVIRONMENT,
        **sentry_sdk_init_kwargs
    )
