from helper_func import *

drone = pymav()
drone.set_mode("GUIDED")
drone.arm()
drone.takeoff(20)

drone.set_mode("ACRO")

drone.connection.mav.rc_channels_override_send(
    drone.connection.target_system,
    drone.connection.target_component,
    1500,   # CH1: roll
    1000,   # CH2: pitch (full back)
    1900,   # CH3: throttle
    1500,   # CH4: yaw
    0, 0, 0, 0  # CH5–CH8
)
print("Backflip burst sent")
time.sleep(0.5)  # Short burst (adjust timing if needed)

# Clear RC override (return to neutral)
drone.connection.mav.rc_channels_override_send(
    drone.connection.target_system,
    drone.connection.target_component,
    0, 0, 0, 0, 0, 0, 0, 0
)

# Switch to LOITER to stabilize
drone.set_mode("ALT_HOLD")
