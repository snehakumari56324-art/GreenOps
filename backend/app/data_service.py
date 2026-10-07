import os

from .data_sources.demo_provider import (
    get_current_resources as get_demo_resources
)

from .data_sources.aws_provider import (
    get_current_resources as get_aws_resources
)


def get_current_resources():

    source = os.getenv(
        "DATA_SOURCE",
        "demo"
    ).lower()

    if source == "aws":
        return get_aws_resources()

    return get_demo_resources()