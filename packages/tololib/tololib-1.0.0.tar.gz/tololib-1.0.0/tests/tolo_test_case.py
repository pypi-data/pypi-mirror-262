import logging
from os import getenv
from sys import stderr
from typing import Any
from unittest import TestCase


class ToloTestCase(TestCase):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        logging.basicConfig(
            level=logging.getLevelName(getenv("LOG_LEVEL", "INFO")), handlers=[logging.StreamHandler(stderr)]
        )

        super().__init__(*args, **kwargs)
