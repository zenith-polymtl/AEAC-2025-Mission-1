from pymavlink import mavutil
import time
from helper_func import *


format_ip_en_vrai = 'udp:<ip_ubuntu>:14551'

master = connect('udp:<ip_ubuntu>:14551')

print(f"Local position : {get_local_pos(master)}/ Global position : {get_global_pos(master)}")

mode = 'LOITER'
input(f"Press enter to set mode {mode}")
set_mode(master, mode)

mode = 'GUIDED'
input(f"Press enter to set mode {mode}")
set_mode(master, mode)

mode = 'LOITER'
input(f"Press enter to set mode {mode}")
set_mode(master, mode)


