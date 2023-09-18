import json
from urllib.parse import parse_qsl

from utils.create_logger import create_logger
from utils.models import RuntimeVersion

logger = create_logger(__name__)


def parse_version_event(event: dict) -> RuntimeVersion:
    record = event["Records"][0]
    body_raw = record["body"]
    body_data = json.loads(body_raw)
    message_raw = body_data["Message"]
    message_data = json.loads(message_raw)
    payload_raw = message_data["responsePayload"]
    query = {k: v for k, v in parse_qsl(payload_raw)}
    return RuntimeVersion(
        aws_execution_env=query["AWS_EXECUTION_ENV"],
        version=query["VERSION"],
        time=message_data["timestamp"],
    )
