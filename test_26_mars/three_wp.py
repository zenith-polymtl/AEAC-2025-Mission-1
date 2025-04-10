from pymavlink import mavutil
import time
from MAIN_MISSION.helper_func import *
mission_height = 7

nav = pymav()
nav.connect('udp:127.0.0.1:14551')


input(f"Set to GUIDED, ARM, press ENTER for Takoeff")


nav.takeoff(mission_height)

nav.local_target([10, 0,-mission_height], acceptance_radius = 1)
input(f"Press enter to pass")
nav.local_target([0, 0,-mission_height], acceptance_radius = 1)
input(f"Press enter to pass")
nav.local_target( [0,10,-mission_height], acceptance_radius = 1)


rtl_wanted = True
if rtl_wanted:
    mode = 'RTL'
    input(f"Press enter to set mode {mode}")
    nav.RTL()

input(f"Press enter to close")