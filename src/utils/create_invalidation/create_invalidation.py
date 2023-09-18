from typing import List

from botocore.client import BaseClient

from utils.create_logger import create_logger

logger = create_logger(__name__)


def create_invalidation(
    files: List[str], distribution_id: str, cloudfront_client: BaseClient
):
    option = {
        "DistributionId": distribution_id,
        "InvalidationBatch": {
            "Paths": {
                "Quantity": len(files),
                "Items": [f"/{filename}" for filename in files],
            }
        },
    }
