from pymavlink import mavutil
import time
import numpy as np
from helper_func import *

nav = pymav()
mission_height = 10

nav.connect('udp:<ip_ubuntu>:14551')

input('Enter to set to GUIDED')
# Set mode to GUIDED
nav.set_mode( "GUIDED")


input("Press enter to takeoff...")
nav.arm()
nav.takeoff(mission_height)


"""
input("Press enter to send current coordinates as source of fire...")
insert_coordinates_to_csv("fire_coordinates.csv", get_global_pos(connection))

desc = input("Please enter description of source...")
append_description_to_last_line("fire_coordinates.csv", desc)
"""

input("Press enter to get position of the eye of the spiral")

pos = nav.get_local_pos()
print(f"Current position: {pos}")

input("Press Confirm local pos...")

e = 2
radius = 10
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
    nav.local_target(wp, acceptance_radius=1.5)

total_time = time.time() - start_time
print(f"Total time: {total_time} seconds")
# Land

nav.RTL()
