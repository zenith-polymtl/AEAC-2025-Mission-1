from pymavlink import mavutil
import time

# Establish connection to MAVLink
connection = mavutil.mavlink_connection('tcp:127.0.0.1:5762')
print('Waiting for heartbeat...')
connection.wait_heartbeat()
print("Heartbeat received!")

# Request GLOBAL_POSITION_INT message at 2 Hz (500 ms interval)
message_type = mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT  # Message type ID for global position
frequency_hz = 2  # Frequency in Hz
interval_us = int(1e6 / frequency_hz)  # Interval in microseconds

# Send the command to set the message interval
connection.mav.command_long_send(
    connection.target_system,  # Target system ID
    connection.target_component,  # Target component ID
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,  # Command to set message interval
    0,  # Confirmation
    message_type,  # Message ID for GLOBAL_POSITION_INT
    interval_us,  # Interval in microseconds
    0, 0, 0, 0, 0  # Unused parameters
)

print("Requested GLOBAL_POSITION_INT messages at 2 Hz.")

# Fetch the current global position
while True:
    msg = connection.recv_match(blocking=True)
    if msg.get_type() == "GLOBAL_POSITION_INT":
        # Extract latitude, longitude, and relative altitude
        lat = msg.lat / 1e7  # Convert from int32 to degrees
        lon = msg.lon / 1e7  # Convert from int32 to degrees
        alt = msg.relative_alt / 1000.0  # Convert from mm to meters (relative altitude)

        print(f"Position: Lat = {lat}°, Lon = {lon}°, Alt = {alt} meters")
        break  # Stop after receiving the position
    time.sleep(0.1)  # Prevent busy-waiting and overload
