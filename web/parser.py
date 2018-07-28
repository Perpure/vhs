import math
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
from config import basedir


class ImageObject:
    is_display = False
    is_number = False

    def __init__(self, contour, id):
        self.id = id
        self.contour = contour
        self.rect = cv2.minAreaRect(contour)
        self.box = np.int0(cv2.boxPoints(self.rect))
        self.min_x = np.ndarray.min(self.box[..., 0])
        self.max_x = np.ndarray.max(self.box[..., 0])
        self.min_y = np.ndarray.min(self.box[..., 1])
        self.max_y = np.ndarray.max(self.box[..., 1])

    def find_relation(self, image_objects):
        for image_object in image_objects:
            if (self.min_x < image_object.min_x < self.max_x) and (self.min_y < image_object.min_y < self.max_y):
                self.is_display = True
                self.relation = image_object.id
                image_object.is_number = True
                image_object.relation = self.id

    @staticmethod
    def identify(display, mask, img):
        pass
        # matrix = ""
        # min_x = display.min_x
        # max_x = display.max_x
        # min_y = display.min_y
        # max_y = display.max_y
        # width = max_x - min_x
        # height = max_y - min_y
        # for y in range(1, 4):
        #     h = min_y + (height * (1 + y * 2)) // 10
        #     for x in range(1, 4):
        #         print(y, min_y, height)
        #         w = min_x + (width * (1 + x * 2)) // 10
        #         cv2.circle(img, (w, h), 3, 255, -1)
        #         if mask[h][w] == 0:
        #             matrix += '1'
        #         else:
        #             matrix += '0'
        # return matrix


class Screen:
    def __init__(self, width, height, left=0, top=0):
        self.width = width
        self.height = height
        self.left = left
        self.top = top

    def get_formatted_screen(self, picture_size):
        width = self.width
        height = self.height
        if (width / height) > picture_size:
            height = int(1 / picture_size * width)
        elif (width / height) < picture_size:
            width = int(picture_size * height)
        left = (self.width - width) // 2
        top = (self.height - height) // 2
        return Screen(width, height, left, top)

    def get_device_screen(self, rect):
        if -95 < rect[2] < -85:
            firsty = int(rect[0][1] - rect[1][0] / 2) - self.top
            firstx = int(rect[0][0] - rect[1][1] / 2) - self.left
            lastx = int(rect[0][0] + rect[1][1] / 2) - self.left
        else:
            firsty = int(rect[0][1] - rect[1][1] / 2) - self.top
            firstx = int(rect[0][0] - rect[1][0] / 2) - self.left
            lastx = int(rect[0][0] + rect[1][0] / 2) - self.left
        scale = (self.width / (lastx - firstx)) * 100
        left = - (firstx / self.width) * scale
        top = - (firsty / self.height) * scale
        device_screen = Screen(lastx - firstx, None, left, top)
        device_screen.scale = scale
        return device_screen


class Parser:
    def __init__(self, room, devices, impath):
        self.room = room
        self.devices = devices
        self.impath = impath

    def parse(self):
        device_amount, image_objects, items = self.__variables_initialise(self.devices)

        img = self.__image_converting(self.impath)
        mask = self.create_mask(img)
        contours = self.find_contours(device_amount, mask)

        maxX, maxY, minX, minY = self.__contour_calculation(contours, image_objects)

        for image_object in image_objects:
            image_object.find_relation(image_objects)

            print(image_object.rect)

        displays = sorted(image_objects, key=lambda x: x.is_display)[-device_amount:]

        print('displays: ', displays)

        self.__matrix_identify(self.devices, displays, img, items, mask)

        print('items: ', items)

        self.__handle_parse(items, minX, minY, maxX, maxY)

        is_parsed = True

        return is_parsed

    def __handle_parse(self, items, minX, minY, maxX, maxY):
        trimmed_screen = Screen(maxX - minX, maxY - minY)
        final_screen = trimmed_screen.get_formatted_screen(16 / 9)
        draw, room_map = self.__create_map(final_screen)
        for item in items:
            device, display = item
            display.rect = ((display.rect[0][0] - minX, display.rect[0][1] - minY), display.rect[1], display.rect[2])
            device_screen = final_screen.get_device_screen(display.rect)
            device.save_screen_params(device_screen)
            self.__draw_map(draw, display.rect, (255, 0, 0))

        self.__save_map(draw, self.room, room_map)

    @staticmethod
    def find_contours(device_amount, mask):
        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=lambda x: len(x))[-device_amount * 2:]
        print('contours: ', contours)
        return contours

    @staticmethod
    def create_mask(img):
        lower_red = np.array((0, 150, 150), np.uint8)
        print('lower_red: ', lower_red)
        upper_red = np.array((20, 255, 255), np.uint8)
        print('upper_red: ', upper_red)
        mask = cv2.inRange(img, lower_red, upper_red)
        cv2.imwrite('images/calibrate/' + 'mask' + '.png', mask)
        return mask

    @classmethod
    def __draw_map(cls, draw, rect, color):
        draw.polygon(np.int0(cv2.boxPoints(rect)).flatten().tolist(), fill=color)

    @classmethod
    def __create_map(cls, final_screen):
        room_map = Image.new('RGB', [final_screen.width, final_screen.height], (255, 255, 255))
        return ImageDraw.Draw(room_map), room_map

    @classmethod
    def __save_map(cls, draw, room, room_map):
        del draw
        filename = basedir + '/images/' + str(room.id) + '_map.jpg'
        if os.path.exists(filename):
            os.remove(filename)
        room_map.save(filename)

    @classmethod
    def __variables_initialise(cls, devices):
        device_amount = len(devices)  # TODO take device amount on calibrate pic
        print('device amount: ', device_amount)
        image_objects = []
        items = list()
        return device_amount, image_objects, items

    @classmethod
    def __image_converting(cls, impath):
        img = cv2.imread(impath)
        cv2.imwrite('images/calibrate/' + 'img_non_hsv' + '.png', img)
        img = cv2.medianBlur(img, 5)
        cv2.imwrite('images/calibrate/' + 'img_medianBlur' + '.png', img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        cv2.imwrite('images/calibrate/' + 'img_hsv' + '.png', img)
        return img

    @classmethod
    def __matrix_identify(cls, devices, displays, img, items, mask):
        for display in displays:
            # matrix = display.identify(display, mask, img)

            # print('matrix: ', matrix)
            print('rect: ', display.rect)

            for device in devices:
                items.append([device, display])
                break

    @classmethod
    def __contour_calculation(cls, contours, image_objects):
        i = 0
        maxX = maxY = -math.inf
        minY = minX = math.inf
        for contour in contours:
            image_object = ImageObject(contour, i)
            image_objects.append(image_object)
            minX = min(minX, image_object.min_x)
            maxX = max(maxX, image_object.max_x)
            minY = min(minY, image_object.min_y)
            maxY = max(maxY, image_object.max_y)
            i += 1
        print('i = ', i)
        return maxX, maxY, minX, minY
