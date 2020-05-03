import os
from dotenv import load_dotenv
import pathlib

_PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
PROJECT_ROOT = str(_PROJECT_ROOT)

load_dotenv(dotenv_path=_PROJECT_ROOT / '.env')

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
DJANGO_SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'ffffffffffffffffffffffffffffffffffffffffffffffffff')
_DJANGO_DEBUG = os.environ.get('DJANGO_DEBUG', 'true') or ''
DJANGO_DEBUG = _DJANGO_DEBUG.lower() == 'true'
DJANGO_LOG_LEVEL = os.environ.get('DJANGO_LOG_LEVEL', 'DEBUG').upper()
SENTRY_DSN = os.environ['SENTRY_DSN']
