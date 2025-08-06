import obd

# Example with manually specifying the port (for Windows):
connection = obd.OBD(portstr="COM4")  # Replace with your actual COM port

# Or on Linux:
# connection = obd.OBD(portstr="/dev/rfcomm0")

if connection.is_connected():
    print("Connected to ELM327")
    rpm = connection.query(obd.commands.RPM)
    oiltemperature = connection.query(obd.commands.OIL_TEMP)
    print("Engine RPM:", rpm.value)
else:
    print("Connection failed")
