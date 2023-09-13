from dataclasses import asdict, is_dataclass
from decimal import Decimal
from typing import Type

from aws_lambda_powertools import Logger
from boto3.dynamodb.conditions import ConditionBase


def custom_default(obj: object):
    if isinstance(obj, Decimal):
        return num if (num := int(obj)) == obj else float(str(obj))
    if is_dataclass(obj):
        return str(obj) if isinstance(obj, Type) else asdict(obj)
    if isinstance(obj, ConditionBase):
        return obj.get_expression()
    try:
        return {"type": str(type(obj)), "value": str(obj)}
    except Exception as e:
        return {"type": str(type(obj)), "err": {"type": str(type(e)), "msg": str(e)}}


def create_logger(service: str) -> Logger:
    return Logger(service=service, json_default=custom_default, use_rfc3339=True)
