import numpy as np
import math
import cv2
from PIL import Image, ImageDraw, ImageEnhance
def parse(colors, impath):
    img = cv2.imread(impath) # Читаем изображение
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Меняем цветовую схему с BGR на HSV

    rects = list()

    maxX = maxY = -math.inf
    minY = minX = math.inf
    
    for color in colors:
        # Меняем схему цвета на HSV
        hsv_color = np.array(color, dtype=np.uint8, ndmin=3) 
        # Достаём из него только Hue
        hue = cv2.cvtColor(hsv_color, cv2.COLOR_BGR2HSV).flatten()[0] 

        # Создаём минимальный предел
        h_min = np.array([max(hue - 10, 0), 100, 100], dtype=np.uint8) 
        # И максимальный
        h_max = np.array([min(hue + 10, 179), 255, 255], dtype=np.uint8) 

        # Накладываем цветовой фильтр
        thresh = cv2.inRange(hsv_img, h_min, h_max) 
        # Ищем контуры
        _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

        # Создаём прямоугольник из контура с наибольшей площадью
        rect = cv2.minAreaRect( sorted(contours, key = cv2.contourArea, reverse = True)[0] ) 
        rects.append( [color, rect] )

        # Переводим в вершины, округляя координаты
        box = np.int0(cv2.boxPoints(rect)) 
        minX = min(minX, np.ndarray.min( box[...,0] ))
        maxX = max(maxX, np.ndarray.max( box[...,0] ))
        minY = min(minY, np.ndarray.min( box[...,1] ))
        maxY = max(maxY, np.ndarray.max( box[...,1] ))
        
    # Формируем возвращаемый лист
    res = [ [rect[0], [int(rect[1][0][0] - minX), int(rect[1][0][1] - minY)], [int(x) for x in rect[1][1] ], int(rect[1][2])] for rect in rects] 
    # Находим разрешение
    resolution = [maxX - minX, maxY - minY]
    room_map = Image.new('RGB', (resolution[0],resolution[1]), (255, 255, 255))
    room_map.save('2.jpg')
    for i in res:
        firstx = int(i[1][0]-i[2][0]/2)
        lastx = int(i[1][0]+i[2][0]/2)
        firsty = int(i[1][1]-i[2][1]/2)
        lasty = int(i[1][1]+i[2][1]/2)
        room_map = Image.open('2.jpg')
        draw = ImageDraw.Draw(room_map)
        for x in range(firstx,lastx):
            for y in range(firsty,lasty):
                draw.point((x, y), (i[0][2],i[0][1],i[0][0]))
        room_map.save('2.jpg')
        res_k = resolution[0]/(lastx - firstx)
        print(firstx, lastx, firsty, lasty, res_k)
    return res, resolution
