from pymavlink import mavutil
import math
import time
from helper_func import *  # Assuming this contains the connect(), set_mode(), get_global_position(), etc.

def ack(connection, keyword):
    """ Waits for acknowledgment message from the autopilot. """
    print(f" Message received: {connection.recv_match(type=f'{keyword}', blocking=True)}")

class MissionItem:
    def __init__(self, seq, current, x, y, z):
        self.seq = seq
        self.frame = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT  # Global coordinates in degrees * 1e7
        self.command = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT  # Command for waypoint navigation
        self.current = current
        self.autocontinue = 1
        self.param1 = 0.0
        self.param2 = 2.0  # Accept radius (may need adjusting)
        self.param3 = 20
        self.param4 = math.nan
        self.x = x
        self.y = y
        self.z = z
        self.mission_type = 0  # Standard mission type
        print(f"Position request: {x}, {y}, {z}")

def upload_mission(the_connection, mission_items):
    n = len(mission_items)
    print("--- Sending Mission Items ---")

    # Send mission count.
    the_connection.mav.mission_count_send(
        the_connection.target_system, the_connection.target_component, n, 0
    )
    ack(the_connection, "MISSION_REQUEST")

    # Send each mission item.
    for waypoint in mission_items:
        print(f"-- Creating waypoint {waypoint.seq} --")
        the_connection.mav.mission_item_int_send(
            the_connection.target_system,
            the_connection.target_component,
            waypoint.seq,
            waypoint.frame,
            waypoint.command,
            waypoint.current,
            waypoint.autocontinue,
            waypoint.param1,
            waypoint.param2,
            waypoint.param3,
            waypoint.param4,
            waypoint.x,
            waypoint.y,
            waypoint.z,
            waypoint.mission_type
        )

    ack(the_connection, "MISSION_ACK")

def start_mission(the_connection):
    print("-- Mission Start --")
    the_connection.mav.command_long_send(
        the_connection.target_system, the_connection.target_component,
        mavutil.mavlink.MAV_CMD_MISSION_START,
        0, 0, 0, 0, 0, 0, 0, 0
    )
    ack(the_connection, "COMMAND_ACK")

# Start mission
connection = connect()
set_mode(connection, "GUIDED")

home = get_global_pos(connection)
print(f"Home position: {home}")

# Define waypoints with unique sequence numbers
wps = [
    MissionItem(0, 1, int((home[0] + 0.005) * 1e7), int((home[1] - 0.005) * 1e7), 20),  # First waypoint
    MissionItem(1, 0, int((home[0] + 0.005) * 1e7), int((home[1] + 0.005) * 1e7), 20),  # Second waypoint
    MissionItem(2, 0, int((home[0] - 0.005) * 1e7), int((home[1] - 0.005) * 1e7), 20)   # Third waypoint
]


arm(connection)
takeoff(connection, 10)
upload_mission(connection, wps)
input("Please confirm mission status...")
input("Press enter to send into mission...")

set_mode(connection, "AUTO")

start_mission(connection)
