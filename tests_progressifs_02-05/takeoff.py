from pymavlink import mavutil
import time
from helper_func import *

nav = pymav()
nav.connect('udp:<ip_ubuntu>:14551')

print(f"Local position : {nav.get_local_pos(nav.master)}/ Global position : {nav.get_global_pos()}")


want_to_set_guided_auto= False
input(f"The job of the pilot is now to set into guided mode if {not want_to_set_guided_auto}. Enter if done ")
if want_to_set_guided_auto:
    mode = 'GUIDED'
    input(f"Press enter to set mode {mode}")
    nav.set_mode(mode)


input("Enter if ready to arm and takeoff")

nav.arm()
nav.takeoff( 20)

want_to_set_guided_auto = True
if want_to_set_guided_auto:
    input(f"Press enter to set mode LOITER")
    nav.set_mode('LOITER')