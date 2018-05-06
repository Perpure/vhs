# -*- encoding: utf-8 -*-

import cv2
import numpy as np

cv2.namedWindow( "result" , cv2.WINDOW_NORMAL)

img = cv2.imread("testroom.jpg") # Читаем изображение
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Меняем цветовую схему с BGR на HSV
colors = [[0, 0, 255], [255, 0, 0]] # Интересующие нас цвета в BGR

for color in colors:
    hsv_color = np.array(color, dtype=np.uint8, ndmin=3) # Меняем схему цвета на HSV
    hue = cv2.cvtColor(hsv_color, cv2.COLOR_BGR2HSV).flatten()[0] # Достаём из него только Hue

    h_min = np.array([max(hue - 10, 0), 100, 100], dtype=np.uint8) # Создаём минимальный предел
    h_max = np.array([min(hue + 10, 179), 255, 255], dtype=np.uint8) # И максимальный

    thresh = cv2.inRange(hsv_img, h_min, h_max) # Накладываем цветовой фильтр

    _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Ищем контуры

    cnt = sorted(contours, key = cv2.contourArea, reverse = True)[0] # Выбираем из них наибольший по площади
    rect = cv2.minAreaRect(cnt) # Описываем четырёхугольник вокруг него
    box = np.int0(cv2.boxPoints(rect)) # Переводим в вершины, округляя координаты
    cv2.drawContours(img, [box], 0, [255, 255, 255], 10) # Рисуем

cv2.imshow('result', img) # Показываем

cv2.waitKey()

cv2.destroyAllWindows()
