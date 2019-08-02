import logging
from settings import celery_app

log = logging.getLogger('scripts')


@celery_app.task()
def add(a, b):
    c = a + b
    print('{}'.format(c))
    log.info('{}'.format(c))
    return c
