import numpy as np
import math
import os
import cv2
from web import db, app
from config import basedir
from PIL import Image, ImageDraw


class ImageObject():
    is_display = False
    is_number = False

    def __init__(self, contour, id):
        self.id = id
        self.contour = contour
        rect = cv2.minAreaRect(contour)
        box = np.int0(cv2.boxPoints(rect))
        self.min_x = np.ndarray.min(box[..., 0])
        self.max_x = np.ndarray.max(box[..., 0])
        self.min_y = np.ndarray.min(box[..., 1])
        self.max_y = np.ndarray.max(box[..., 1])

    def find_relation(self, image_objects):
        for image_object in image_objects:
            if (self.min_x < image_object.min_x < self.max_x) and (self.min_y < image_object.min_y < self.max_y):
                self.is_display = True
                self.relation = image_object.id
                image_object.is_number = True
                image_object.relation = self.id

    def indentify(self):
        matrix = ""
        min_x = display.min_x
        max_x = display.max_x
        min_y = display.min_y
        max_y = display.max_y
        width = max_x - min_x
        height = max_y - min_y
        for y in range(1,4):
            h = min_y + (height * (1 + y*2)) // 10
            for x in range(1,4):
                print(y, min_y, height)
                w = min_x + (width * (1 + x*2)) // 10
                cv2.circle(img,(w,h),3,255,-1)
                if mask[h][w] == 0:
                    matrix += '1'
                else:
                    matrix += '0'
        return matrix

class Screen():
    def __init__(self, width, height, left=0, top=0):
        self.width = width
        self.height = height
        self.left = left
        self.top = top

    def get_formatted_screen(self, picture_size):
        width = self.width
        height = self.height
        if (width / height) > (picture_size):
            height = int(1 / picture_size * width)
        elif (width / height) < (picture_size):
            width = int(picture_size * height)
        left = (self.width - width) // 2
        top = (self.height - height) // 2
        return Screen(width, height, left, top)

    def get_device_screen(self, device, rect):
        if -95 < rect[2] < -85:
            firsty = int(rect[0][1] - rect[1][0] / 2) - self.top
            firstx = int(rect[0][0] - rect[1][1] / 2) - self.left
            lastx = int(rect[0][0] + rect[1][1] / 2) - self.left
        else:
            firsty = int(rect[0][1] - rect[1][1] / 2) - self.top
            firstx = int(rect[0][0] - rect[1][0] / 2) - self.left
            lastx = int(rect[0][0] + rect[1][0] / 2) - self.left
        scale = (self.width / (lastx - firstx)) * 100
        left = - (firstx / self.width) * width
        top = - (firsty / self.height) * width
        device_screen = Screen(lastx - firstx, None, left, top)
        device_screen.scale = scale
        return device_screen


def handle_parse(items, minX, minY, maxX, maxY, room):
    trimmed_screen = Screen(maxX - minX, maxY - minY)
    final_screen = trimmed_screen.get_formatted_screen(16 / 9)
    draw, room_map = create_map(final_screen.width, final_screen.height)
    for item in items:
        device, rect, display = item
        rect = ((rect[0][0] - minX, rect[0][1] - minY), rect[1], rect[2])
        device_screen = final_screen.get_device_screen(device, rect)
        device.save_screen_params(device_screen)
        draw_map(draw, rect, (255, 0, 0))
    save_map(draw, room, room_map)


def draw_map(draw, rect, color):
    draw.polygon(np.int0(cv2.boxPoints(rect)).flatten().tolist(), fill=color)


def create_map(width, height):
    room_map = Image.new('RGB', [width, height], (255, 255, 255))
    return ImageDraw.Draw(room_map), room_map


def save_map(draw, room, room_map):
    del draw
    filename = basedir + '/images/' + str(room.id) + '_map.jpg'
    if os.path.exists(filename):
        os.remove(filename)
    room_map.save(filename)


def parse(room, devices, impath):
    device_amount = len(devices) #TODO take device amount on calibrate pic
    is_parsed = False
    maxX = maxY = -math.inf
    minY = minX = math.inf
    image_objects = []
    img = cv2.imread(impath)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    items = list()
    lower_red = np.array((0, 150, 150), np.uint8)
    upper_red = np.array((20, 255, 255), np.uint8)
    mask = cv2.inRange(img, lower_red, upper_red)
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,
                                              cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=lambda x: len(x))[-device_amount*2:]
    i = 0
    for contour in contours:
        image_object = ImageObject(contour, i)
        image_objects.append(image_object)
        minX = min(minX, image_object.min_x)
        maxX = max(maxX, image_object.max_x)
        minY = min(minY, image_object.min_y)
        maxY = max(maxY, image_object.max_y)
        i+=1
    for image_object in image_objects:
        image_object.find_relation(image_objects)
    displays = sorted(image_objects, key=lambda x: x.is_display)[-device_amount:]
    for display in displays:
        matrix = display.identify()
        for device in devices:
            if matrix == device.matrix:
                items.append([device, rect, display])
                break
    handle_parse(items, minX, minY, maxX, maxY, room)
    is_parsed = True
    return is_parsed
