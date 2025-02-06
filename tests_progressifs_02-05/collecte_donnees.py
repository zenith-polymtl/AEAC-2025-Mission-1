from pymavlink import mavutil
import time
from helper_func import *

master = connect('udp:<ip_ubuntu>:14551')


while True:
    print(f"Local position : {get_local_pos()}/ Global position : {get_global_pos()}")