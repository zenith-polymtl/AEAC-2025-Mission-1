from pymavlink import mavutil
import time
from helper_func import *
mission_height = 20

nav = pymav()
nav.connect('udp:<ip_ubuntu>:14551')

want_to_set_guided_auto= False
input(f"The job of the pilot is now to takeoff, ans set into guided mode if {not want_to_set_guided_auto} ")

if want_to_set_guided_auto:
    mode = 'GUIDED'
    input(f"Press enter to set mode {mode}")
    nav.set_mode(mode)
    nav.arm()
    nav.takeoff(mission_height)

nav.local_target([10, 10,-mission_height], acceptance_radius = 2)
nav.local_target([-10, -10,-mission_height], acceptance_radius = 2)
nav.local_target( [0,0,-mission_height], acceptance_radius = 2)


rtl_wanted = True
if rtl_wanted:
    mode = 'RTL'
    input(f"Press enter to set mode {mode}")
    nav.RTL()

