from utils.create_logger import create_logger
from utils.decorate_handler import decorate_handler

logger = create_logger(__name__)


@logger.inject_lambda_context(log_event=True)
@decorate_handler(logger)
def handler(event, context):
    pass
