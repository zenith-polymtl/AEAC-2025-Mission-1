from pymavlink import mavutil
import time
from helper_func import *
nav = pymav()

nav.connect('udp:<ip_ubuntu>:14551')


while True:
    print(f"Local position : {nav.get_local_pos()}/ Global position : {nav.get_global_pos()}")
    time.sleep(0.1)