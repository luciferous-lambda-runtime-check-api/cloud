import os
from dataclasses import dataclass, fields

from utils.create_logger import create_logger


@dataclass
class EnvironmentVariables:
    bucket_name_content: str
    distribution_id: str


logger = create_logger(__name__)


def load_environment() -> EnvironmentVariables:
    env = EnvironmentVariables(
        **{k.name: os.environ[k.name.upper()] for k in fields(EnvironmentVariables)}
    )
    logger.info("load_environment", extra={"env": env})
    return env
