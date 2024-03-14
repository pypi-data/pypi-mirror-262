from server_communication_test_case import ServerCommunicationTestCase

from tololib.const import TARGET_TEMPERATURE_MAX, TARGET_TEMPERATURE_MIN
from tololib.enums import AromaTherapySlot, LampMode


class ToloClientTest(ServerCommunicationTestCase):
    def test_get_status(self) -> None:
        client = self.get_client()
        client.get_status()

    def test_get_settings(self) -> None:
        client = self.get_client()
        client.get_settings()

    def test_set_power_on(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_power_on(True))
        status = client.get_status()
        self.assertTrue(status.power_on)

        self.assertTrue(client.set_power_on(False))
        status = client.get_status()
        self.assertFalse(status.power_on)

    def test_set_fan_on(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_fan_on(True))
        status = client.get_status()
        self.assertTrue(status.fan_on)

        self.assertTrue(client.set_fan_on(False))
        status = client.get_status()
        self.assertFalse(status.fan_on)

    def test_set_aroma_therapy_on(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_aroma_therapy_on(True))
        status = client.get_status()
        self.assertTrue(status.aroma_therapy_on)

        self.assertTrue(client.set_aroma_therapy_on(False))
        status = client.get_status()
        self.assertFalse(status.aroma_therapy_on)

    def test_set_lamp_on(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_lamp_on(True))
        status = client.get_status()
        self.assertTrue(status.lamp_on)

        self.assertTrue(client.set_lamp_on(False))
        status = client.get_status()
        self.assertFalse(status.lamp_on)

    def test_set_sweep_on(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_sweep_on(True))
        status = client.get_status()
        self.assertTrue(status.sweep_on)

        self.assertTrue(client.set_sweep_on(False))
        status = client.get_status()
        self.assertFalse(status.sweep_on)

    def test_set_salt_bath_on(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_salt_bath_on(True))
        status = client.get_status()
        self.assertTrue(status.salt_bath_on)

        self.assertTrue(client.set_salt_bath_on(False))
        status = client.get_status()
        self.assertFalse(status.salt_bath_on)

    def test_set_target_temperature(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_target_temperature(40))
        settings = client.get_settings()
        self.assertEqual(settings.target_temperature, 40)
        self.assertTrue(client.set_target_temperature(50))
        settings = client.get_settings()
        self.assertEqual(settings.target_temperature, 50)
        self.assertTrue(client.set_target_temperature(60))
        settings = client.get_settings()
        self.assertEqual(settings.target_temperature, 60)

        self.assertRaises(ValueError, client.set_target_temperature, TARGET_TEMPERATURE_MIN - 1)
        self.assertRaises(ValueError, client.set_target_temperature, TARGET_TEMPERATURE_MAX + 1)

    def test_set_target_humidity(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_target_humidity(70))
        settings = client.get_settings()
        self.assertEqual(settings.target_humidity, 70)

    def test_set_power_timer(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_power_timer(42))
        settings = client.get_settings()
        self.assertEqual(settings.power_timer, 42)

        self.assertTrue(client.set_power_timer(None))
        settings = client.get_settings()
        self.assertEqual(settings.power_timer, None)

    def test_set_salt_bath_timer(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_salt_bath_timer(42))
        settings = client.get_settings()
        self.assertEqual(settings.salt_bath_timer, 42)

        self.assertTrue(client.set_salt_bath_timer(None))
        settings = client.get_settings()
        self.assertEqual(settings.salt_bath_timer, None)

    def test_set_aroma_therapy(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_aroma_therapy_slot(AromaTherapySlot.B))
        settings = client.get_settings()
        self.assertEqual(settings.aroma_therapy_slot, AromaTherapySlot.B)
        self.assertEqual(client.get_aroma_therapy_slot(), AromaTherapySlot.B)

        self.assertTrue(client.set_aroma_therapy_slot(AromaTherapySlot.A))
        settings = client.get_settings()
        self.assertEqual(settings.aroma_therapy_slot, AromaTherapySlot.A)
        self.assertEqual(client.get_aroma_therapy_slot(), AromaTherapySlot.A)

    def test_set_sweep_timer(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_sweep_timer(7))
        settings = client.get_settings()
        self.assertEqual(settings.sweep_timer, 7)

        self.assertTrue(client.set_sweep_timer(None))
        settings = client.get_settings()
        self.assertEqual(settings.sweep_timer, None)

    def test_set_lamp_mode(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_lamp_mode(LampMode.AUTOMATIC))
        settings = client.get_settings()
        self.assertEqual(settings.lamp_mode, LampMode.AUTOMATIC)
        self.assertEqual(client.get_lamp_mode(), LampMode.AUTOMATIC)

        self.assertTrue(client.set_lamp_mode(LampMode.MANUAL))
        settings = client.get_settings()
        self.assertEqual(settings.lamp_mode, LampMode.MANUAL)
        self.assertEqual(client.get_lamp_mode(), LampMode.MANUAL)

    def test_set_fan_timer(self) -> None:
        client = self.get_client()

        self.assertTrue(client.set_fan_timer(30))
        settings = client.get_settings()
        self.assertEqual(settings.fan_timer, 30)

        self.assertTrue(client.set_fan_timer(None))
        settings = client.get_settings()
        self.assertEqual(settings.fan_timer, None)

    def test_lamp_change_color(self) -> None:
        client = self.get_client()
        self.assertTrue(client.lamp_change_color())

    def test_get_fan_timer(self) -> None:
        client = self.get_client()
        self.assertTrue(client.set_fan_timer(30))
        self.assertTrue(client.set_fan_on(True))
        self.assertEqual(client.get_fan_timer(), 30)
        self.assertTrue(client.set_fan_on(False))
        self.assertTrue(client.set_fan_timer(None))
        self.assertTrue(client.set_fan_on(True))
        self.assertEqual(client.get_fan_timer(), None)

    def test_salt_bath_timer(self) -> None:
        client = self.get_client()
        self.assertTrue(client.set_salt_bath_timer(30))
        self.assertTrue(client.set_salt_bath_on(True))
        self.assertEqual(client.get_salt_bath_timer(), 30)
        self.assertTrue(client.set_salt_bath_on(False))
        self.assertTrue(client.set_salt_bath_timer(None))
        self.assertTrue(client.set_salt_bath_on(True))
        self.assertEqual(client.get_salt_bath_timer(), None)

    def test_sweep_timer(self) -> None:
        client = self.get_client()
        self.assertTrue(client.set_sweep_timer(7))
        self.assertTrue(client.set_sweep_on(True))
        self.assertEqual(client.get_sweep_timer(), 7)
        self.assertTrue(client.set_sweep_on(False))
        self.assertTrue(client.set_sweep_timer(None))
        self.assertTrue(client.set_sweep_on(True))
        self.assertEqual(client.get_sweep_timer(), None)
