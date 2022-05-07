import sensor, image, time, pyb

# === variables ===
# declarations
past = False                        # is box already behind
flag = 12                           # main loop flag
button = None                       # button pin
tim = None                          # timer
motor = None                        # pwm for motor
ser = None                          # serial
cur_com = "None"                    # current command
line_mutex = "free"                 # manager for line turn
cur_ang = 0                         # servo angle
# led
red_led = None
green_led = None
blue_led = None
# options
base_ang = -10                      # base angle without mods
ang = 25                            # servo angle on detour
aligment = 25                       # servo angle on detour
turn = 15                           # servo angle on rotation
debug = False                       # enable debug information
speed_of_servo = 500                # servo rotation speed ( more is lower )
Motor_speed = 40                    # motor speed
near_dist_area = 50                 # distance to box for trigger
wall_diff_normal = 10               # normal difference between walls sizes
line_min_size = 500                 # minimum size for line to turn
sensor_color_format = sensor.RGB565 # sensor colors type
sensor_res = sensor.QQVGA           # sensor resolution
# Thresholds
greenTh  = (32, 51, -45, -10, 10, 50)
redTh    = (10, 50, 24, 46, -3, 41)
blueTh   = (19, 68, -10, 18, -48, -12)
orangeTh = (35, 62, 4, 57, -9, 81)
blackTh  = (0, 18, -15, 9, -12, 13)
whiteTh  = (59, 100, -10, 4, -12, 3)  # unused
# regions of interests
boxes_roi = (10, 78, 134, 35)
wall_left_roi = (0, 0, 1, 120)
wall_right_roi = (159, 0, 1, 120)
lines_roi = (0, 64, 160, 34)

# === functions ===

def main_init():
    # set global variables
    global button, tim, motor, ser, sensor, clock, last_saw, red_led, green_led, blue_led
    # motors part
    button = pyb.Pin('P0', pyb.Pin.IN, pyb.Pin.PULL_UP)         # init button's pin
    tim = pyb.Timer(2, freq=1000)                               # init timer
    motor = tim.channel(3, pyb.Timer.PWM, pin=pyb.Pin('P4'))    # init motor pwm on P6
    ser = pyb.Servo(1)                                          # init servo on P7
    ser.angle(base_ang)                                         # set servo startup position
    # enable led colors
    red_led = pyb.LED(1)
    green_led = pyb.LED(2)
    blue_led = pyb.LED(3)
    # sensor part
    sensor.reset()                                              # reset previous camera settings
    sensor.set_pixformat(sensor_color_format)                   # set colored output
    sensor.set_framesize(sensor_res)                            # set camera size
    sensor.set_vflip(True)                                      # flip camera view
    sensor.set_hmirror(True)                                    # mirror camera view
    sensor.skip_frames(time = 2000)                             # skip some frames for camera initalization
    clock = time.clock()                                        # start internal timer

def debug_roi(img: Image, roi: tuple, color: tuple):
    if roi == None:
        return
    img.draw_rectangle(roi, color=color)

def binary_roi(img: Image, th: list, roi: tuple):
    img.crop(roi=roi).binary(th)

def debug_blobs(img: Image, blobs: list, color: tuple):
    '''
        draw some info about blobl on image
    '''
    for blb in blobs:
        if blb == None:
            continue
        img.draw_rectangle(blb.rect(), color=color) # draw rect around the blob
        img.draw_cross(blb.cx(), blb.cy(), color=color) # draw cross in the center of the blob
        # print blob's size in the left-top corner
        img.draw_string(blb.x(), blb.y(), str(blb.area()), color=(0, 255, 255))


def find_nearest_blob(blobs: list):
    ''' find nearest blob in array by its area '''
    return max(blobs, key=lambda x: x.area(), default=None)


def get_nearest_from_two(nearest_blob_red: blob, nearest_blob_green: blob):

    if nearest_blob_red == None and nearest_blob_green == None:
        nearest_blob = None
        nearest_col = None
    elif nearest_blob_red == None:
        nearest_blob = nearest_blob_green
        nearest_col = "green"
    elif nearest_blob_green == None:
        nearest_blob = nearest_blob_red
        nearest_col = "red"
    else:
        if nearest_blob_green.area() > nearest_blob_red.area():
            nearest_blob = nearest_blob_green
            nearest_col = "green"
        else:
            nearest_blob = nearest_blob_red
            nearest_col = "red"
    return nearest_blob, nearest_col


def find_diffs_params(left_wall_pix: int, right_wall_pix: int):
    # find difference between walls sizes
    diff = left_wall_pix - right_wall_pix

    # find robot position relative to walls
    if abs(diff) < wall_diff_normal:
        diff_res = "normal"
    elif diff > 0:
        diff_res = "too_left"
    elif diff < 0:
        diff_res = "too_right"
    else:
        diff_res = "normal"
    return diff, diff_res


def cam_get_state():
    ''' get positional information from camera '''
    # enable camera global control
    global img, clock, sensor, line_mutex, flag, red_led, green_led, blue_led
    cur_com = None

    # internal camera functions
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8, 1.0)

    # find blocks
    blobs_green = img.find_blobs([greenTh], merge=True, roi=boxes_roi)
    blobs_red = img.find_blobs([redTh], merge=True, roi=boxes_roi)

    # find nearest red and green block
    # (need to find its color)
    nearest_blob_red = find_nearest_blob(blobs_red)
    nearest_blob_green = find_nearest_blob(blobs_green)
    nearest_blob, cur_com = get_nearest_from_two(nearest_blob_red, nearest_blob_green)

    # find left and right walls sizes
    left_wall_pix = sum([x.area() for x in img.find_blobs([blackTh], roi=wall_left_roi)])
    right_wall_pix = sum([x.area() for x in img.find_blobs([blackTh], roi=wall_right_roi)])
    if debug:
        print(left_wall_pix, right_wall_pix)
    diff, diff_res = find_diffs_params(left_wall_pix, right_wall_pix)

    orange_lines = img.find_blobs([orangeTh], roi=lines_roi)
    blue_lines = img.find_blobs([blueTh], roi=lines_roi)
    orange_line = sum([x.area() for x in orange_lines])
    blue_line = sum([x.area() for x in blue_lines])

    if debug:
        debug_blobs(img, orange_lines, (255, 120, 0))
        debug_blobs(img, blue_lines, (0, 80, 128))
        print(orange_line)
        print(blue_line)

    if orange_line >= line_min_size:
        if line_mutex == "free" or line_mutex == "after_blue" or line_mutex == "orange_line":
            red_led.on()
            line_mutex = "orange_line"
            cur_com = "right"
        else:
            red_led.off()
        if line_mutex == "blue_line":
            line_mutex = "after_orange"
            flag -= 1
    elif blue_line >= line_min_size:
        if line_mutex == "free" or line_mutex == "after_orange" or line_mutex == "blue_line":
            blue_led.on()
            line_mutex = "blue_line"
            cur_com = "left"
        else:
            blue_led.off()
        if line_mutex == "orange_line":
            line_mutex = "after_blue"
            flag -= 1

    # print (and draw) some technical info
    if debug:
        print(line_mutex)
        if False:
            binary_roi(img, [blackTh], lines_roi)
        else:
            debug_blobs(img, blobs_green, (0, 255, 0))
            debug_blobs(img, blobs_red, (255, 0, 0))
            debug_blobs(img, [nearest_blob], (0, 0, 255))
            debug_roi(img, boxes_roi, (255, 0, 255))
            debug_roi(img, wall_left_roi, (255, 255, 0))
            debug_roi(img, wall_right_roi, (0, 0, 255))
            debug_roi(img, lines_roi, (255, 0, 0))

    # return required information
    return cur_com, diff_res


def main_loop():
    global ser, button, base_ang, red_led, green_led, blue_led
    # wait for button press
    if not debug:
        green_led.on()
        while button.value() == 1:
            pass
        green_led.off()
        # wait for second
        pyb.delay(1000)

    motor.pulse_width_percent(Motor_speed) # start motor

    while flag > 0:
        cur_com = None          # current command
        wall_status = None      # position relative to walls

        # get info from camera
        cur_com, wall_status = cam_get_state()

        cur_ang = base_ang

        if debug:
            print(cur_com)

        if wall_status == "normal":
            green_led.on()
        else:
            green_led.off()

        cur_ang = base_ang

        if cur_com == "green":
            cur_ang -= ang
        elif cur_com == "red":
            cur_ang += ang
        elif wall_status == "too_left":
            cur_ang += aligment
        elif wall_status == "too_right":
            cur_ang -= aligment

        if cur_com == "right":
            cur_ang += turn
        elif cur_com == "left":
            cur_ang -= turn

        if debug:
            print(cur_ang)

        ser.angle(cur_ang)
        #ser.angle(cur_ang, speed_of_servo)


# === main code ===

def main():
    main_init()
    main_loop()
    ser.angle(base_ang)             # return servo to normal position
    motor.pulse_width_percent(0)    # speed down

# execute code
main()
