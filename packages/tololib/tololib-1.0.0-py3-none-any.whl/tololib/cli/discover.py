from argparse import ArgumentParser, Namespace

from tololib.const import DEFAULT_PORT, DEFAULT_RETRY_COUNT, DEFAULT_RETRY_TIMEOUT

from ..client import ToloClient
from .common import Command


class DiscoverCommand(Command):
    def __init__(self, argument_parser: ArgumentParser) -> None:
        super().__init__(argument_parser)
        argument_parser.add_argument("-p", "--port", default=DEFAULT_PORT, type=int)
        argument_parser.add_argument("--broadcast-address", default="255.255.255.255", type=str)
        argument_parser.add_argument("--retry-count", default=DEFAULT_RETRY_COUNT, type=int)
        argument_parser.add_argument("--retry-timeout", default=DEFAULT_RETRY_TIMEOUT, type=float)

    def __call__(self, args: Namespace) -> int:
        for remote, status in ToloClient.discover(
            broadcast_address=args.broadcast_address,
            port=args.port,
            timeout=args.retry_timeout,
            max_retries=args.retry_count,
        ):
            print(f"Found TOLO device at {remote[0]}:{remote[1]}")

        return 0
