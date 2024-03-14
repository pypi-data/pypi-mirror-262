import subprocess
from argparse import ArgumentParser
from threading import Thread
from time import sleep

from tests.tolo_test_case import ToloTestCase
from tololib.cli.common import Command
from tololib.cli.device_simulator import DeviceSimulatorCommand


class CommandTest(ToloTestCase):
    def test_device_simulator_and_discovery(self) -> None:
        argument_parser = ArgumentParser()
        command = DeviceSimulatorCommand(argument_parser)
        self.assertRaises(SystemExit, argument_parser.parse_args, ["-h"])

        args = argument_parser.parse_args(["-l", "127.0.0.1", "-p", "51503"])
        process = Thread(target=command, args=(args,), daemon=True)
        process.start()
        sleep(1)

        result = subprocess.run(
            ["tolo-cli", "discover", "--broadcast-address", "127.0.0.1", "--port", "51503"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stdout, "Found TOLO device at 127.0.0.1:51503\n")


class CommonCommandTest(ToloTestCase):
    def test_common_command_call(self) -> None:
        argument_parser = ArgumentParser()
        common_command = Command(argument_parser)
        args = argument_parser.parse_args([])
        self.assertRaises(NotImplementedError, common_command, args)
