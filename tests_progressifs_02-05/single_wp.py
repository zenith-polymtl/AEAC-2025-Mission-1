from pymavlink import mavutil
import time
from helper_func import *

nav = pymav()
#nav.connect('udp:<ip_ubuntu>:14551')

nav.connect('tcp:127.0.0.1:5762')

want_to_set_guided_auto= False
input(f"The job of the pilot is now to takeoff, ans set into guided mode if {not want_to_set_guided_auto}. Enter if done ")
if want_to_set_guided_auto:
    
    mode = 'GUIDED'
    print(f"Local position : {nav.get_local_pos()}/ Global position : {nav.get_global_pos()}")
    input(f"Press enter to set mode {mode}")
    nav.set_mode(mode)

nav.arm()
nav.takeoff(altitude=20)
nav.local_target( [-200,10,-20], acceptance_radius = 2)