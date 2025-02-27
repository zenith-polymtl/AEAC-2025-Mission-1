from pymavlink import mavutil
import time
from helper_func import *
nav = pymav()

mission_height  = 20

#nav.connect('udp:<ip_ubuntu>:14551')

nav.connect('tcp:127.0.0.1:5763')
want_to_set_guided_auto= False
input(f"The job of the pilot is now to set into guided mode if {not want_to_set_guided_auto}. Enter if done ")
if want_to_set_guided_auto:
    mode = 'GUIDED'
    input(f"Press enter to set mode {mode}")
    nav.set_mode(mode)


input("Enter if ready to arm and takeoff")
'''
possible de passer fibonnacci.fibbo comme paramètre while _moving pour démontrer les capacités de gestion de tâches en simultanné de l'approche (dans les temps morts)
class fibo():
    def __init__(self):
        self.fib = 1
        self.last_fib = 1
    
    def fibbo(self):
        result = self.fib+self.last_fib
        self.last_fib = self.fib
        self.fib = result
        print(result)

fibonnacci = fibo()'''

nav.arm()
nav.takeoff(mission_height)


    

input("Press enter to make small waypoint")
nav.local_target([100,100,-mission_height], acceptance_radius = 2)

rtl_wanted = False
if rtl_wanted:
    mode = 'RTL'
    input(f"Press enter to set mode {mode}")
    nav.RTL()

