import numpy as np
import math
import os
import cv2
from web import db, app
from config import basedir
from PIL import Image, ImageDraw


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
            height = int(width / picture_size)
        elif (width / height) < (picture_size):
            width = int(height * picture_size)
        left = - (width - self.width) // 2
        top = - (height - self.height) // 2
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
        width = (self.width / (lastx - firstx)) * 100
        left = - (firstx / self.width) * width
        top = - (firsty / self.height) * width
        return Screen(width, None, left, top)


def handle_parse(items, minX, minY, maxX, maxY, room):
    trimmed_screen = Screen(maxX - minX, maxY - minY)
    final_screen = trimmed_screen.get_formatted_screen(16 / 9)
    draw, room_map = create_map(final_screen.width, final_screen.height)
    for item in items:
        device, rect, color = item
        rect = ((rect[0][0] - minX, rect[0][1] - minY), rect[1], rect[2])
        device_screen = final_screen.get_device_screen(device, rect)
        device.save_screen_params(device_screen)
        draw_map(draw, rect, color)
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
    is_parsed = False
    img = cv2.imread(impath)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    items = list()
    maxX = maxY = -math.inf
    minY = minX = math.inf
    for device in devices:
        R = int(device.color[1:3], 16)
        G = int(device.color[3:5], 16)
        B = int(device.color[5:7], 16)
        color = (B, G, R)
        hsv_color = np.array(color, dtype=np.uint8, ndmin=3)
        hue = cv2.cvtColor(hsv_color, cv2.COLOR_BGR2HSV).flatten()[0]
        hue_min = np.array([max(hue - 10, 0), 100, 100], dtype=np.uint8)
        hue_max = np.array([min(hue + 10, 179), 255, 255], dtype=np.uint8)
        thresh = cv2.inRange(hsv_img, hue_min, hue_max)
        _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        try:
            rect = cv2.minAreaRect(sorted(contours, key=cv2.contourArea, reverse=True)[0])
            box = np.int0(cv2.boxPoints(rect))
            minX = min(minX, np.ndarray.min(box[..., 0]))
            maxX = max(maxX, np.ndarray.max(box[..., 0]))
            minY = min(minY, np.ndarray.min(box[..., 1]))
            maxY = max(maxY, np.ndarray.max(box[..., 1]))
            items.append([device, rect, (color[2], color[1], color[0])])
            is_parsed = True
        except IndexError:
            pass
    if is_parsed:
        handle_parse(items, minX, minY, maxX, maxY, room)
        return True
    else:
        return False
