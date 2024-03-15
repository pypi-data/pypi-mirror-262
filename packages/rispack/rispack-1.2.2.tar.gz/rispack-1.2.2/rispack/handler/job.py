from functools import wraps

from rispack.logger import logger

from .record import RecordBuilder


def job(func):
    @wraps(func)
    def wrapper(event, context):
        logger.mask_info(event)

        items = event.get("Records") or [event]

        for item in items:
            record = RecordBuilder(item).build()

            func(record)

    return wrapper
