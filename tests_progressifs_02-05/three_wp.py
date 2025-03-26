from pymavlink import mavutil
import time
from helper_func import *
mission_height = 20

nav = pymav()
nav.connect('udp:127.0.0.1:14551')


input(f"The job of the pilot is to arm and set guided ")


nav.takeoff(mission_height)

nav.local_target([10, 10,-mission_height], acceptance_radius = 1)
input(f"Press enter to pass")
nav.local_target([5, 5,-mission_height], acceptance_radius = 1)
input(f"Press enter to pass")
nav.local_target( [5,10,-mission_height], acceptance_radius = 1)


rtl_wanted = True
if rtl_wanted:
    mode = 'RTL'
    input(f"Press enter to set mode {mode}")
    nav.RTL()

input(f"Press enter to close")