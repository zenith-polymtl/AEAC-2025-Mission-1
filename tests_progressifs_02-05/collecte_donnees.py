from pymavlink import mavutil
import time
from helper_func import *
nav = pymav()

nav.connect('udp:127.0.0.1:14551')

print("Connected")

while True:
    print(f"Local position : {nav.get_local_pos()}/ Global position : {nav.get_global_pos()}")
    time.sleep(0.1)