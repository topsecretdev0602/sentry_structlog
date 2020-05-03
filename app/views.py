import logging

import structlog
from django.http import HttpRequest, HttpResponse

structlog_logger: structlog.stdlib.BoundLogger = structlog.getLogger('app').bind()
logging_logger: logging.Logger = logging.getLogger('app')

MODE_TO_LOGGER = {
    'structlog': structlog_logger,
    'stdlib': logging_logger,
}


def home(request: HttpRequest, mode: str) -> HttpResponse:
    if mode not in MODE_TO_LOGGER:
        return HttpResponse(f'Mode should be one of {list(MODE_TO_LOGGER.keys())}', status=500)
    logger = MODE_TO_LOGGER[mode]
    logger.info(f'{mode} - home requested')
    logger.info(f'{mode} - breadcrumb 1')
    logger.info(f'{mode} - breadcrumb 2')
    logger.info(f'{mode} - breadcrumb 3')
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception(f'{mode} - We divided by zero and handled it! Now we will crash')

    raise Exception(f'{mode} - Shout! Shout! Let it all out!')

    return HttpResponse('How did we get here?', status=200)
