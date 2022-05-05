import sensor, image, time,
import green_and_red as cfunc       # camera functions

# === variables ===
B = None                            # pin B
tim = None                          # timer
motor = None                        # pwm for motor
Motor_speed = 0                     # motor speed
cur_ang = 0                         # servo angle
ang = 10                            # servo angle on detour
turn = 15                           # servo angle on rotation
cur_com = "None"                    # current command
past = False                        # is box already behind
flag = True                         # main loop flag
speed_of_servo = 1500               # servo rotation speed
cfunc.set_debug(True)               # set debug mode
cfunc.set_near_dist_area(4000)      # set minimum distance to box for trigger
cfunc.set_saw_interval(1000)        # set time (in millis) for box behind
cfunc.set_wall_diff_normal(500)     # set maximum wall difference

def main_init():
    # set global variables
    global B, tim, motor, ser
    cfunc.camera_init()                                         # init camera
    B = pyb.Pin('P5', pyb.Pin.OUT_PP)                           # init pin b on P5
    B.value(1)                                                  # set pin b value
    tim = pyb.Timer(2, freq=1000)                               # init timer
    motor = tim.channel(3, pyb.Timer.PWM, pin=pyb.Pin('P4'))    # init motor pwm on P6
    motor.pulse_width_percent(Motor_speed)                      # start motor
    ser = pyb.Servo(1)                                          # init servo on P7
    ser.angle(0)                                                # set servo startup position


# === code logic ===
'''
    if camera just saw box:
        cur_com = box_color
        past = False
        #  Wait some time
        past = True
        #  Wait some time
        cur_com = None
        past = False

    if camera just saw a turn:
        cur_com = turn direction
        past = False
        #  Wait some time
        cur_com = None

    if camera saw 12'th turn:
        flag = False
'''

# === functions ===

def main_loop():
    while flag:
        past = None             # already behind
        cur_com = None          # current command
        wall_status = None      # position relative to walls

        # get info from camera
        cur_com, past, wall_status, flag = cfunc.cam_get_state(flag)

        if cur_com == "green" and past == False:
            cur_ang = ang
        elif cur_com == "red" and past == False:
            cur_ang = -ang
        elif cur_com == "green" and past == True:
            cur_ang = -ang
        elif cur_com == "red" and past == True:
            cur_ang = ang
        elif cur_com == "right":
            cur_ang = turn
        elif cur_com == "left":
            cur_ang = -turn
        else:
            cur_ang = 0

        ser.angle(cur_ang)
        # ser.angle(cur_ang, speed_of_servo)


# === main code ===

def main():
    main_init()
    main_loop()
    ser.angle(0)                    # return servo to normal position
    motor.pulse_width_percent(0)    # speed down


# execute code
main()
