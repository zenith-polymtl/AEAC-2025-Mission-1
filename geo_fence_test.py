from helper_func import *
from pymavlink import mavutil

nav = pymav()
nav.connect('tcp:127.0.0.1:5763')
nav.set_mode("GUIDED")

nav.arm()
nav.takeoff(10)



nav.local_target([-130, 50, -10], acceptance_radius=3)
