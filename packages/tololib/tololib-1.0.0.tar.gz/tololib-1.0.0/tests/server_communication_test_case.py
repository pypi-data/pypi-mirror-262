from __future__ import annotations

from os import getenv
from time import sleep
from typing import Any, Tuple

from tests.tolo_test_case import ToloTestCase
from tololib.client import DEFAULT_PORT, ToloClient
from tololib.device_simulator import ToloDeviceSimulator


class ServerCommunicationTestCase(ToloTestCase):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        if getenv("SERVER_ADDRESS") or getenv("SERVER_PORT"):
            self._test_server_address = getenv("SERVER_ADDRESS", "localhost")
            self._test_server_port = int(getenv("SERVER_PORT", DEFAULT_PORT))
            self._test_server = None
        else:
            self._test_server_address = "localhost"
            self._test_server_port = DEFAULT_PORT
            self._test_server = ToloDeviceSimulator()

    def setUp(self) -> None:
        if self._test_server is not None:
            self._test_server.start()
            sleep(0.1)

    def tearDown(self) -> None:
        if self._test_server is not None:
            sleep(0.1)
            self._test_server.stop()
            self._test_server.join()

    def get_server_address_and_port(self) -> Tuple[str, int]:
        return self._test_server_address, self._test_server_port

    def get_client(self) -> ToloClient:
        address, port = self.get_server_address_and_port()
        client = ToloClient(address, port)
        self.assertEqual(address, client.address)
        self.assertEqual(port, client.port)
        return client
