from functools import wraps
from typing import Callable

from aws_lambda_powertools import Logger


def decorate_handler(logger: Logger) -> Callable:
    def wrapper(handler: Callable):
        @wraps(handler)
        def process(*args, **kwargs):
            try:
                result = handler(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(
                    f"error occurred in handler: [{type(e)}] {e}", exc_info=True
                )
                raise

        return process

    return wrapper
