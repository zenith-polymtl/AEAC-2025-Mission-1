from pymavlink import mavutil
import time
from helper_func import *


master = connect('udp:<ip_ubuntu>:14551')

print(f"Local position : {get_local_pos(master)}/ Global position : {get_global_pos(master)}")


want_to_set_guided_auto= False
input(f"The job of the pilot is now to set into guided mode if {not want_to_set_guided_auto}. Enter if done ")
if want_to_set_guided_auto:
    mode = 'GUIDED'
    input(f"Press enter to set mode {mode}")
    set_mode(master, mode)


input("Enter if ready to arm and takeoff")

arm(master)
takeoff(master, 20)

want_to_set_guided_auto = True
if want_to_set_guided_auto:
    input(f"Press enter to set mode LOITER")
    set_mode(master, 'LOITER')