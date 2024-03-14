from argparse import ArgumentParser, Namespace

from ..const import DEFAULT_PORT
from ..device_simulator import ToloDeviceSimulator
from .common import Command


class DeviceSimulatorCommand(Command):
    def __init__(self, argument_parser: ArgumentParser) -> None:
        super().__init__(argument_parser)
        argument_parser.add_argument("-l", "--listen", default="localhost", dest="address", type=str)
        argument_parser.add_argument("-p", "--port", default=DEFAULT_PORT, type=int)

    def __call__(self, args: Namespace) -> int:
        tolo_test_server = ToloDeviceSimulator(args.address, args.port)
        tolo_test_server.start()
        tolo_test_server.join()
        return 0
