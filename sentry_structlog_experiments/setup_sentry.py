import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration  # , EventHandler, BreadcrumbHandler

from .env_vars import ENVIRONMENT, SENTRY_DSN


def configure():
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), LoggingIntegration()],
        environment=ENVIRONMENT
    )
