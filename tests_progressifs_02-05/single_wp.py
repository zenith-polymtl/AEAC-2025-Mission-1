from pymavlink import mavutil
import time
from helper_func import *

nav = pymav()
#nav.connect('udp:<ip_ubuntu>:14551')

nav.connect('udp:127.0.0.1:14551')

want_to_set_guided_auto= False
input(f"The job of the pilot is now to takeoff, and set into guided mode if {not want_to_set_guided_auto}. Enter if done ")
if want_to_set_guided_auto:
    
    mode = 'GUIDED'
    print(f"Local position : {nav.get_local_pos()}/ Global position : {nav.get_global_pos()}")
    input(f"Press enter to set mode {mode}")
    nav.set_mode(mode)


nav.local_target([-5,5,-20], acceptance_radius = 2)