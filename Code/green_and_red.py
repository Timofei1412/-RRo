
# add some libraries
import sensor, image, time, pyb

# required camera internals inits
def init_camera():
    sensor.reset()                        # reset previous camera settings
    sensor.set_pixformat(sensor.RGB565)   # set colored output
    sensor.set_framesize(sensor.QQVGA)    # set camera size
    sensor.skip_frames(time = 2000)       # skip some frames for camera initalization
    clock = time.clock()

# options for camera movement
debug = True
near_dist_area = 4000
saw_interval = 1000
wall_diff_normal = 500

# Thresholds
greenTh  = (31, 64, -50, -28, 18, 53)
redTh    = (19, 60, 29, 80, 6, 54)
blueTh   = (19, 68, -10, 18, -48, -12)
orangeTh = (22, 64, -8, 23, -48, -16)
blackTh  = (0, 18, -15, 9, -12, 13)
whiteTh  = (59, 100, -10, 4, -12, 3)

# set options
def set_debug(flag = True):
    debug = flag
def set_near_dist_area(value = 4000):
    near_dist_area = value
def set_saw_interval(value = 1000):
    saw_interval = value
def set_wall_diff_normal(value = 500):
    wall_diff_normal = value

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
    '''
        find nearest blob in array by its area
    '''
    nrs = None
    for blb in blobs:
        if nrs == None or blb.area() > nrs.area():
            nrs = blb
    return nrs

# variable for blocks bypass
last_saw = pyb.millis()

def cam_get_state(flag: bool):
    '''
        get positional information from camera
    '''
    # enable camera global control
    global img, clock, sensor, last_saw

    # internal camera functions
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8, 1.0)

    # find blocks
    blobs_green = img.find_blobs([greenTh], merge=True)
    blobs_red = img.find_blobs([redTh], merge=True)

    # find nearest red and green block
    # (need to find its color)
    nearest_blob_red = find_nearest_blob(blobs_red)
    nearest_blob_green = find_nearest_blob(blobs_green)
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

    # set variable for movement
    if nearest_blob != None and nearest_blob.area() > near_dist_area:
        last_saw = pyb.millis()

    # find left and right walls sizes
    left_wall_pix = sum([x.area() for x in img.find_blobs([blackTh], False, (0, 0, int(img.width() / 2), img.height()))])
    right_wall_pix = sum([x.area() for x in img.find_blobs([blackTh], False, (int(img.width() / 2), 0, int(img.width() / 2), img.height()))])
    # find difference between walls sizes
    diff = left_wall_pix - rigth_wall_pix

    # find robot position relative to walls
    if abs(diff) < wall_diff_normal:
        diff_res = "normal"
    elif diff > 0:
        diff_res = "too_left"
    elif diff < 0:
        diff_res = "too_right"
    else:
        diff_res = "normal"

    # print (and draw) some technical info
    if debug:
        # print walls info
        print("diff: ", diff)
        print(diff_res)

        # add binary image of walls
        view_img = img.copy() # copy image for editing
        view_img.binary([blackTh]) # binary the image
        # add debug info
        debug_blobs(view_img, blobs_green, (0, 255, 0))
        debug_blobs(view_img, blobs_red, (255, 0, 0))
        debug_blobs(view_img, [nearest_blob], (0, 0, 255))
        # dublicate image
        img.draw_image(img, int(img.width() / 2), 0, 0.5, 0.5)
        # add the debug image to the main image
        img.draw_image(view_img, 0, 0, 0.5, 0.5)

    # return required information
    return nearest_col, (pyb.millis() - last_saw) > saw_interval, diff_res, flag

camera_init()
while(True):
    if debug:
        print(cam_get_state())
    else:
        cam_get_state()
