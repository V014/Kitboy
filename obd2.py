"""Read-only OBD-II queries for paired Bluetooth Classic ELM327 adapters."""


def available_ports():
    from serial.tools import list_ports

    return sorted(port.device for port in list_ports.comports())


def read_vehicle_data(port):
    import obd

    connection = obd.OBD(portstr=port, fast=False, timeout=2)
    try:
        if not connection.is_connected():
            raise ConnectionError(
                "Could not connect. Confirm the adapter is paired and its COM port is correct."
            )

        commands = (
            ("Engine speed", obd.commands.RPM),
            ("Vehicle speed", obd.commands.SPEED),
            ("Coolant temperature", obd.commands.COOLANT_TEMP),
            ("Engine load", obd.commands.ENGINE_LOAD),
            ("Oil temperature", obd.commands.OIL_TEMP),
        )
        readings = []
        for label, command in commands:
            if not connection.supports(command):
                continue
            response = connection.query(command)
            if not response.is_null():
                readings.append((label, str(response.value)))

        dtc_response = connection.query(obd.commands.GET_DTC)
        trouble_codes = [] if dtc_response.is_null() else list(dtc_response.value)
        return readings, trouble_codes
    finally:
        connection.close()
