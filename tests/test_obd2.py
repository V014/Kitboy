import sys
import types
import unittest
from unittest.mock import patch

import obd2


class FakeResponse:
    def __init__(self, value):
        self.value = value

    def is_null(self):
        return self.value is None


class ObdReaderTests(unittest.TestCase):
    def make_obd_module(self, connected=True):
        commands = types.SimpleNamespace(
            RPM="rpm",
            SPEED="speed",
            COOLANT_TEMP="coolant",
            ENGINE_LOAD="load",
            OIL_TEMP="oil",
            GET_DTC="dtc",
        )
        fake_connection = types.SimpleNamespace(
            is_connected=lambda: connected,
            supports=lambda _command: True,
            query=lambda command: FakeResponse(
                [("P0101", "Mass air flow range/performance")]
                if command == "dtc"
                else command
            ),
            close=lambda: setattr(fake_connection, "closed", True),
            closed=False,
        )
        obd_module = types.ModuleType("obd")
        obd_module.commands = commands
        obd_module.OBD = lambda **_kwargs: fake_connection
        return obd_module, fake_connection

    def test_reads_supported_values_and_codes_then_closes_adapter(self):
        obd_module, fake_connection = self.make_obd_module()
        with patch.dict(sys.modules, {"obd": obd_module}):
            readings, codes = obd2.read_vehicle_data("COM8")

        self.assertEqual(len(readings), 5)
        self.assertEqual(readings[0], ("Engine speed", "rpm"))
        self.assertEqual(codes[0][0], "P0101")
        self.assertTrue(fake_connection.closed)

    def test_closes_adapter_when_connection_fails(self):
        obd_module, fake_connection = self.make_obd_module(connected=False)
        with patch.dict(sys.modules, {"obd": obd_module}):
            with self.assertRaises(ConnectionError):
                obd2.read_vehicle_data("COM8")

        self.assertTrue(fake_connection.closed)


if __name__ == "__main__":
    unittest.main()
