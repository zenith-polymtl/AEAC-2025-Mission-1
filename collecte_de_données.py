#Idée de fonctionnement pour l'interpolation des données GPS à plus haute fréquence

from pymavlink import mavutil
import time
from helper_func import *

# Function to interpolate between two GPS points
def interpolate_gps(p1, p2, fraction):
    lat = p1["lat"] + (p2["lat"] - p1["lat"]) * fraction
    lon = p1["lon"] + (p2["lon"] - p1["lon"]) * fraction
    alt = p1["alt"] + (p2["alt"] - p1["alt"]) * fraction
    return {"lat": lat, "lon": lon, "alt": alt}

# Connect to the vehicle
master = connect()

# Wait for a heartbeat
master.wait_heartbeat()
print("Connected to vehicle")

# Data storage for interpolation
last_gps = None
current_gps = None
last_time = None
current_time = None

target_frequency = 60  # Desired frequency in Hz
interval = 1 / target_frequency  # Time interval in seconds

# Listener loop
while True:
    # Receive the latest GPS_RAW_INT message
    msg = master.recv_match(type='GPS_RAW_INT', blocking=True)

    if msg:
        # Extract GPS data
        gps_data = {
            "lat": msg.lat / 1e7,  # Convert to degrees
            "lon": msg.lon / 1e7,  # Convert to degrees
            "alt": msg.alt / 1e3   # Convert to meters
        }
        timestamp = time.time()  # Record the current system time

        # Update GPS points for interpolation
        last_gps, current_gps = current_gps, gps_data
        last_time, current_time = current_time, timestamp

        # Skip interpolation if there is no previous point
        if last_gps is None or last_time is None:
            continue

        # Interpolate at 60 Hz
        t = last_time
        while t < current_time:
            fraction = (t - last_time) / (current_time - last_time)
            interpolated_gps = interpolate_gps(last_gps, current_gps, fraction)
            print(f"Interpolated GPS at {t:.2f}: {interpolated_gps}")
            t += interval

    # Sleep for a short while to avoid unnecessary CPU usage
    time.sleep(0.01)
