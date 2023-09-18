import json
from dataclasses import asdict
from typing import Dict

from utils.create_client import create_client
from utils.create_logger import create_logger
from utils.decorate_handler import decorate_handler
from utils.event_parser import parse_version_event
from utils.load_environment import load_environment
from utils.models import RuntimeVersion

logger = create_logger(__name__)

JSON_FILE_NAME = "runtime_summary.json"


@logger.inject_lambda_context(log_event=True)
@decorate_handler(logger)
def handler(event, context, s3_client=create_client("s3")):
    env = load_environment()
    runtime_version = parse_version_event(event)
    summary = get_summary_data(bucket=env.bucket_name_content, s3_client=s3_client)
    summary[runtime_version.aws_execution_env] = runtime_version
    put_summary_data(
        bucket=env.bucket_name_content, summary=summary, s3_client=s3_client
    )


def get_summary_data(bucket: str, s3_client) -> Dict[str, RuntimeVersion]:
    option = {"Bucket": bucket, "Key": JSON_FILE_NAME}
    logger.info(
        "get previous data",
        exc_info={
            "additional_data": {
                "service": "s3",
                "command": "get_object",
                "option": option,
            }
        },
    )
    try:
        resp = s3_client.get_object(**option)
        return {
            (y := RuntimeVersion(**x)).aws_execution_env: y
            for x in json.loads(resp["Body"].read())
        }
    except s3_client.exceptions.NoSuchKey:
        return {}


def put_summary_data(bucket: str, summary: Dict[str, RuntimeVersion], s3_client):
    option = {
        "Bucket": bucket,
        "Key": JSON_FILE_NAME,
        "Body": json.dumps(
            [summary[k] for k in sorted(summary.keys())],
            default=asdict,
            ensure_ascii=False,
        ).encode(),
        "ContentType": "application/json",
    }
    logger.info(
        "put_summary_data",
        exc_info={
            "additional_data": {
                "service": "s3",
                "command": "put_object",
                "option": option,
            }
        },
    )
    s3_client.put_object(**option)
