from pymavlink import mavutil
import time
import numpy as np
from helper_func import *

nav = pymav()
mission_height = 10

nav.connect('udp:127.0.0.1:14551')
#nav.connect('tcp:127.0.0.1:5763')
input('Enter when mode set to GUIDED')
# Set mode to GUIDED

input("Now arm the drone, and press enter to takeoff...")
nav.takeoff(mission_height)


"""
input("Press enter to send current coordinates as source of fire...")
insert_coordinates_to_csv("fire_coordinates.csv", get_global_pos(connection))

desc = input("Please enter description of source...")
append_description_to_last_line("fire_coordinates.csv", desc)
"""

input("Free to fly in LOITER. Press enter to get position of the center of scan zone. Make sure to then be in GUIDED")

pos = nav.get_local_pos()
print(f"Current position: {pos}")

input("Press Confirm local pos...")

e = 2
radius = 13
x = []
y = []
high = True
n_passes = int(2*radius/e)
for n in range(n_passes):
    w = e*(1/2 + n)
    h = np.sqrt(radius**2 - (radius - w)**2)
    if high:
        x.append(-radius + w)
        y.append(h)
        x.append(-radius + w)
        y.append(-h)
        high = False
    else:
        x.append(-radius + w)
        y.append(-h)
        x.append(-radius + w)
        y.append(h)
        high = True

start_time = time.time()

for i in range(len(x)):
    wp = [x[i] + pos[0], y[i] + pos[1], -mission_height]
    nav.local_target(wp, acceptance_radius=1.7)
    print(f"Next target : {wp}")

total_time = time.time() - start_time
print(f"Total time: {total_time} seconds")
# Land

input('Press enter to return to launch site')
nav.RTL()
print("Returning")
