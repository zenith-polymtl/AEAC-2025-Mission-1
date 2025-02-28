##Test script qui n'a jamais fonctionné, projet de faire des missions conventionnelles abandonnées, même si ça contient un potentiel
##La gestion des tâches et du processus en guided est plus facile


from pymavlink import mavutil
import numpy as np
import time
import math
from helper_func import get_global_position

# Function to convert NED to global coordinates
def ned_to_global(x, y, z, lat_ref, lon_ref, alt_ref):
    R_E = 6378137.0  # Earth's radius in meters
    lat_ref_rad = math.radians(lat_ref)

    lat_global = lat_ref + (x / R_E) * (180 / math.pi)
    lon_global = lon_ref + (y / (R_E * math.cos(lat_ref_rad))) * (180 / math.pi)
    alt_global = alt_ref - z  # NED Z is negative above reference

    return lat_global, lon_global, alt_global


# Establish connection to MAVLink
connection = mavutil.mavlink_connection('tcp:127.0.0.1:5762')
print('Waiting for heartbeat...')
connection.wait_heartbeat()
print("Heartbeat received!")

# Set mode to GUIDED
def set_mode(mode):
    mode_id = connection.mode_mapping()[mode]
    connection.mav.set_mode_send(
        connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id
    )
    print(f"Setting mode to {mode}...")

set_mode("GUIDED")

# Arm the vehicle
print("Arming motors...")
connection.mav.command_long_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0
)

# Wait for arming confirmation
connection.motors_armed_wait()
print("Motors armed!")

# Takeoff
altitude = 20  # Target altitude in meters
print(f"Taking off to {altitude} meters...")
connection.mav.command_long_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,
    0, 0, 0, 0, 0, 0, altitude
)
time.sleep(10)  # Allow time for the drone to ascend

# Fetch reference global position
print("Fetching reference global position...")
lat_ref, lon_ref, alt_ref = get_global_position(connection)
print(f"Reference Position: Lat = {lat_ref}, Lon = {lon_ref}, Alt = {alt_ref}")

# Generate spiral points in LOCAL_NED
theta_spiral = np.linspace(0, 2 * np.pi * 5, 100)  # 5 rotations
radius = 100  # Maximum radius in meters
espacement = 20
a = radius + espacement / 2
b = -espacement / (2 * np.pi)
r_spiral = a + b * theta_spiral
x_spiral = r_spiral * np.cos(theta_spiral)
y_spiral = r_spiral * np.sin(theta_spiral)
z_spiral = np.full_like(x_spiral, -10)  # Constant altitude

# Convert spiral points to global coordinates
global_waypoints = [
    ned_to_global(x, y, z, lat_ref, lon_ref, alt_ref)
    for x, y, z in zip(x_spiral, y_spiral, z_spiral)
]

# Upload the mission items (waypoints)
seq = 0  # Start from sequence number 0
frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT  # Use global relative altitude
command = mavutil.mavlink.MAV_CMD_NAV_SPLINE_WAYPOINT  # Spline waypoint command
autocontinue = 1  # Continue to next waypoint automatically

print("Uploading mission...")
for lat, lon, alt in global_waypoints:
    # Send the mission item (spline waypoint)
    connection.mav.mission_item_send(
        connection.target_system,  # Target system ID
        connection.target_component,  # Target component ID
        seq,  # Sequence number
        frame,  # Coordinate frame
        command,  # Command ID
        0, 0,  # Current item, autocontinue
        0, 0, 0, 0,  # Params 1, 2, 3, 4 (unused)
        int(lat * 1e7),  # Latitude (scaled to int32 for precision)
        int(lon * 1e7),  # Longitude (scaled to int32 for precision)
        alt  # Altitude in meters
    )
    seq += 1

# End the mission with a return-to-launch command
connection.mav.mission_item_int_send(
    connection.target_system,
    connection.target_component,
    seq,  # Sequence number for the last item
    frame,
    mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,  # Return to launch after mission completion
    0, 0,  # Current item, autocontinue
    0, 0, 0, 0, 0, 0, 0
)

# Notify vehicle that the mission is uploaded
connection.mav.mission_count_send(
    connection.target_system,
    connection.target_component,
    seq + 1  # Total number of waypoints including return-to-launch
)

# Start the mission by setting the mode to AUTO
print("Starting mission in Auto Mode...")
# Set mode to Auto Mode (ArduPilot custom mode ID for Auto is typically 0)
# Function to set flight mode to Auto Mode
def set_mode_auto():
    mode_id = 3  # Auto Mode ID for ArduPilot (as per your documentation)
    
    # Send the command to set the flight mode
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,  # Command to set mode
        0,  # Confirmation
        1,  # MAV_MODE_FLAG_CUSTOM_MODE_ENABLED = 1 (Enable custom mode)
        mode_id,  # Set to Auto Mode (mode 3 for Copter)
        0, 0, 0, 0, 0  # Unused parameters
    )
    print(f"Switched to Auto Mode (Mode ID: {mode_id})")

# Now you can call this function after uploading the mission
for i in range(10):
    print(10-i)
    time.sleep(1)
    
set_mode_auto()

# Monitor mission progress
while True:
    msg = connection.recv_match(type="MISSION_CURRENT", blocking=True)
    print(f"Current Mission Item: {msg.seq}")
    if msg.seq == seq:  # End of mission
        break

# Close connection after mission completion
print("Mission complete. Disconnecting...")
connection.close()