import numpy as np
import math
import os
import cv2
from web import db, app
from config import basedir
from PIL import Image, ImageDraw


<<<<<<< HEAD
class Screen():
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def calibrate_resolution(self, w, h):
        width = self.width
        height = self.height
        if (width / height) > (w / h):
            height = int(width * h / w)
        elif (width / height) < (w / h):
            width = int(height * w / h)
        deltax = (width - self.width) // 2
        deltay = (height - self.height) // 2
        self.width = width
        self.height = height
        return deltax, deltay
=======
def calibrate_resolution(resolution, w, h):
    width = resolution[0]
    height = resolution[1]
    if (width / height) > (w / h):
        height = int(width * h / w)
    elif (width / height) < (w / h):
        width = int(height * w / h)
    return width, height
>>>>>>> 042ce21620fac92a45faec120d4e374ab4ab320e


def handle_parse(items, minX, minY, maxX, maxY, room):
    screen = Screen(maxX - minX, maxY - minY)
    deltax, deltay = screen.calibrate_resolution(16, 9)
    draw, room_map = create_map(screen.width, screen.height)
    for item in items:
        user, rect, color = item
        rect = ((rect[0][0] - minX, rect[0][1] - minY), rect[1], rect[2])
        save_parse(user, rect, deltax, deltay, screen.width, screen.height)
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


def save_parse(user, rect, deltax, deltay, new_width, new_height):
    if -95 < rect[2] < -85:
        firsty = int(rect[0][1] - rect[1][0] / 2) + deltay
        firstx = int(rect[0][0] - rect[1][1] / 2) + deltax
        lastx = int(rect[0][0] + rect[1][1] / 2) + deltax
    else:
        firsty = int(rect[0][1] - rect[1][1] / 2) + deltay
        firstx = int(rect[0][0] - rect[1][0] / 2) + deltax
        lastx = int(rect[0][0] + rect[1][0] / 2) + deltax
    width = (new_width / (lastx - firstx)) * 100
    left = - (firstx / new_width) * width
    top = - (firsty / new_height) * width
    user.res_k = int(width)
    user.top = int(top)
    user.left = int(left)
    db.session.commit()


def parse(room, users, impath):
    img = cv2.imread(impath)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    items = list()
    maxX = maxY = -math.inf
    minY = minX = math.inf
    for user in users:
        R = int(user.color[1:3], 16)
        G = int(user.color[3:5], 16)
        B = int(user.color[5:7], 16)
        color = (B, G, R)
        hsv_color = np.array(color, dtype=np.uint8, ndmin=3)
        hue = cv2.cvtColor(hsv_color, cv2.COLOR_BGR2HSV).flatten()[0]
        h_min = np.array([max(hue - 10, 0), 100, 100], dtype=np.uint8)
        h_max = np.array([min(hue + 10, 179), 255, 255], dtype=np.uint8)
        thresh = cv2.inRange(hsv_img, h_min, h_max)
        _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rect = cv2.minAreaRect(sorted(contours, key=cv2.contourArea, reverse=True)[0])
        box = np.int0(cv2.boxPoints(rect))
        minX = min(minX, np.ndarray.min(box[..., 0]))
        maxX = max(maxX, np.ndarray.max(box[..., 0]))
        minY = min(minY, np.ndarray.min(box[..., 1]))
        maxY = max(maxY, np.ndarray.max(box[..., 1]))
        items.append([user, rect, (color[2], color[1], color[0])])
    handle_parse(items, minX, minY, maxX, maxY, room)
