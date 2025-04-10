from pymavlink import mavutil
import time
import numpy as np
from helper_func import *

nav = pymav()
nav.connect()

# Set mode to GUIDED
nav.set_mode( "GUIDED")


nav.arm()
nav.takeoff( 10)

input("Press enter to send current coordinates as source of fire...")
nav.insert_coordinates_to_csv("fire_coordinates.csv", nav.get_global_pos())

desc = input("Please enter description of source...")
nav.append_description_to_last_line("fire_coordinates.csv", desc)


input("Press enter to get position of the eye of the spiral")

pos = nav.get_local_pos()
print(f"Current position: {pos}")

input("Press Confirm local pos...")
# Circle parameters
theta_circle = np.linspace(0, 2 * np.pi, 100)
radius = 100
x_circle = radius * np.cos(theta_circle)
y_circle = radius * np.sin(theta_circle)

espacement = 10
nombre_de_tours = radius / espacement


# Spiral parameters
theta_spiral = np.linspace(0, 2 * np.pi*nombre_de_tours, 100)
a = 0
b = espacement/(2*np.pi)
r_spiral = a + b * theta_spiral
x_spiral = r_spiral * np.cos(theta_spiral) + pos[0]
y_spiral = r_spiral * np.sin(theta_spiral) + pos[1]

start_time = time.time()

for i in range(len(x_spiral)):
    wp = [x_spiral[i], y_spiral[i], -10]
    nav.local_target(wp, acceptance_radius=10)

total_time = time.time() - start_time
print(f"Total time: {total_time} seconds")
# Land

nav.RTL()
