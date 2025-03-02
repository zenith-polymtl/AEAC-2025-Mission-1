from pymavlink import mavutil
import time
import numpy as np
from helper_func import *

nav = pymav()
connection = nav.connect('tcp:127.0.0.1:5763')

# Set mode to GUIDED
nav.set_mode("GUIDED")


nav.arm()
nav.takeoff(10)


input("Press enter to get position of the eye of the spiral")

pos = nav.get_local_pos()
print(f"Current position: {pos}")

input("Press Confirm local pos...")

e = 10
radius = 100
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
    wp = [x[i] + pos[0], y[i] + pos[1], -10]
    nav.local_target(wp, acceptance_radius=3)

total_time = time.time() - start_time
print(f"Total time: {total_time} seconds")
# Land

nav.RTL(connection)
