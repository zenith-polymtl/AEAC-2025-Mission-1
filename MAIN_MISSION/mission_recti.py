import time
import numpy as np
from helper_func import *
from helper_func import *
from geopy.distance import distance
from geopy import Point


nav = pymav(gps_thresh=1.6, ip = 'udp:127.0.0.1:14551')
mission_height = 10

#ip vol = 'udp:127.0.0.1:14551'

input('Enter when mode set to GUIDED')
# Set mode to GUIDED

input("Now arm the drone, and press enter to takeoff...")
nav.takeoff(mission_height)

desc = input("Enter the description to send current coordinates and coordinates as source of fire...")
nav.insert_coordinates_to_csv("/home/colin/AEAC-2025-Mission-1/MAIN_MISSION/csvs/fire_coordinates.csv", nav.get_global_pos(), desc)

input("Free to fly in LOITER. Press enter to get position of the center of scan zone. Make sure to then be in GUIDED")

pos = nav.get_local_pos()
global_pos = nav.get_global_pos()
print(f"Current position: {pos}")

entree = input("Press 'y', and enter, to send drone in autonomous scan \n")
while entree != 'y':
    entree = input("Press 'y' to send drone in autonomous scan")
    if entree == 'y':
        print("Drone will now be sent to autonomous scan")
    else:
        print("Invalid input. Please enter 'y' to proceed.")

e = 6
radius = 102
x = []
y = []
high = True
n_passes = int(2*radius/e)
for n in range(n_passes):
    w = e*(1/2 + n)
    h = np.sqrt(radius**2 - (radius - w)**2)
    if high:
        y.append(-radius + w)
        x.append(h)
        y.append(-radius + w)
        x.append(-h)
        high = False
    else:
        y.append(-radius + w)
        x.append(-h)
        y.append(-radius + w)
        x.append(h)
        high = True

start_time = time.time()

x,y = y, x

reference_point = Point(global_pos[0], global_pos[1])
for i in range(len(x)):
    point_north = distance(meters=y[i]).destination(reference_point, bearing=0)
    point_final = distance(meters=x[i]).destination(point_north, bearing=90)
    nav.global_target([point_final.latitude, point_final.longitude, mission_height])
    print(f"Point Reached, aiming to next point")

total_time = time.time() - start_time
print(f"Total time: {total_time} seconds")
# Land

input('Press enter to return to launch site')
nav.RTL()
print("Returning")
