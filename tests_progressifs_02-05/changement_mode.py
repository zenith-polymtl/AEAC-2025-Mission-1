from pymavlink import mavutil
import time
from helper_func import *

nav = pymav()

format_ip_en_vrai = 'udp:<ip_ubuntu>:14551'

nav.connect('udp:<ip_ubuntu>:14551')

print(f"Local position : {nav.get_local_pos()}/ Global position : {nav.get_global_pos()}")

mode = 'LOITER'
input(f"Press enter to set mode {mode}")
nav.set_mode( mode)

mode = 'GUIDED'
input(f"Press enter to set mode {mode}")
nav.set_mode(mode)

mode = 'LOITER'
input(f"Press enter to set mode {mode}")
nav.set_mode(mode)


