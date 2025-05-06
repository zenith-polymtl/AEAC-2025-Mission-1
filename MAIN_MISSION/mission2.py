from helper_func import *

source_loc = (45.5059483, -73.6085258)

buckets = [(45.5060538, -73.6085946), 
           (45.5060293, -73.6084046), 
           (45.5059397, -73.6084479), 
           (45.5059294, -73.6086254)]

nav = pymav(gps_thresh=1.8, ip = 'tcp:127.0.0.1:5763')
mission_height = 15

#ip vol = 'udp:127.0.0.1:14551'

input('Enter when mode set to GUIDED')
# Set mode to GUIDED

val = input("Now arm the drone, and press enter to takeoff... s to skip")
if val != 's':
    nav.takeoff(mission_height)

all = [source_loc] + buckets

current = 0

while True:
    entry = input("Press a number corresponding to the bucket you want to go to, or 'rtl' to quit: ")
    if entry == 'a':

        if current >= len(all):
            print("All targets have been visited. Returning to launch...")
            nav.RTL()
            break

        target_loc = all[current]
        current += 1

        nav.global_target([target_loc[0], target_loc[1], mission_height])
        print(f"Reached autonomous target at {target_loc}")

    if entry.strip().lower() == 'rtl':
        print("Returning to launch...")
        nav.RTL()
        break
    elif entry.strip().startswith('so'):
        target_loc = source_loc
        print(f"Going to source at {target_loc}")
        nav.global_target([target_loc[0], target_loc[1], mission_height])
    else:
        try:
            bucket_index = int(entry)
            if 0 <= bucket_index < len(buckets):
                target_loc = buckets[bucket_index]
                print(f"Going to bucket {bucket_index} at {target_loc}")
                nav.global_target([target_loc[0], target_loc[1], mission_height])

                print(f"Reached bucket {bucket_index} at {target_loc}")
            else:
                print("Invalid bucket number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the bucket number, 'source, or 'rtl'.")