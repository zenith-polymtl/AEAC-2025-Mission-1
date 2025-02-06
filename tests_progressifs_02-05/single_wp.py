from pymavlink import mavutil
import time
from helper_func import *


master = connect('udp:<ip_ubuntu>:14551')

print(f"Local position : {get_local_pos()}/ Global position : {get_global_pos()}")


want_to_set_guided_auto= False
input(f"The job of the pilot is now to takeoff, ans set into guided mode if {not want_to_set_guided_auto}. Enter if done ")
if want_to_set_guided_auto:
    
    mode = 'GUIDED'
    input(f"Press enter to set mode {mode}")
    set_mode(master, mode)

local_target(master, [10,10,-20], acceptance_radius = 2)