import os
import sys


def handler(event, context):
    return "&".join(
        [
            f"AWS_EXECUTION_ENV={os.getenv('AWS_EXECUTION_ENV')}",
            f"VERSION={sys.version}",
        ]
    )
