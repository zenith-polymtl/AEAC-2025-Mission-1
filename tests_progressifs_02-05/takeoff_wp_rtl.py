from pymavlink import mavutil
import time
from helper_func import *
nav = pymav()

mission_height  = 20

#nav.connect('udp:<ip_ubuntu>:14551')

nav.connect('udp:127.0.0.1:14551')
want_to_set_guided_auto= True

input("ARM DRONE, and press Enter if ready to takeoff")
if want_to_set_guided_auto:
    mode = 'GUIDED'
    nav.set_mode(mode)
    
input("Confirm guided")
nav.takeoff(mission_height)


input("Press enter to make small waypoint")
nav.local_target([5,5,-mission_height], acceptance_radius = 2)

rtl_wanted = True
if rtl_wanted:
    mode = 'RTL'
    input(f"Press enter to set mode {mode}")
    nav.RTL()

