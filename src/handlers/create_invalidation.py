from utils.create_client import create_client
from utils.create_logger import create_logger
from utils.decorate_handler import decorate_handler
from utils.load_environment import load_environment
from datetime import datetime, timezone

logger = create_logger(__name__)


@decorate_handler(logger)
def handler(_event, _context, cloudfront_client=create_client("cloudfront")):
    env = load_environment()
    option = {
        "DistributionId": env.distribution_id,
        "InvalidationBatch": {
            "Paths": {"Quantity": 1, "Items": ["/*"]},
            "CallerReference": str(datetime.now(timezone.utc).timestamp()),
        },
    }
    logger.info(
        "create_invalidation",
        extra={
            "command_info": {
                "service": "cloudfront",
                "api": "create_invalidation",
                "option": option,
            }
        },
    )
    cloudfront_client.create_invalidation(**option)
