from dataclasses import dataclass


@dataclass
class RuntimeVersion:
    aws_execution_env: str
    version: str
    time: str
