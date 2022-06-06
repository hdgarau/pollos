import cv2
import pickle
import numpy as np
from classes.config import Config

total = 0
image = None
pathConfig = "resources\\data\\config.data"

with open(pathConfig,"rb") as f:
    config = pickle.load(f)
    print(config)

clickHold = False

def main(video_path):
    global image, clickHold, config
    cap = cv2.VideoCapture(video_path)
    contado = False
    cont = 0
    fgbw = cv2.createBackgroundSubtractorMOG2()
    kernel = cv2.getStructuringElement(cv2.MARKER_CROSS,(3,3))
    while True:
        success, image = cap.read()
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)

        imagecrop = image[config.zonaElegidaOrigen[1]:config.zonaElegidaFin[1], config.zonaElegidaOrigen[0]:config.zonaElegidaFin[0]]
        imagecrop = cv2.resize(imagecrop, (500,500))
        fgmask = fgbw.apply(imagecrop)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        fgmask = cv2.dilate(fgmask,None, iterations=10)
        cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        for cnt in cnts:
            if cv2.contourArea(cnt) >15000 and cv2.contourArea(cnt) < 400 * 400:
                if cnt[0][0][0] < 100 and not contado:
                    contado = True
                    cont = cont + 1
                    print(cnt[0])
                    print(cont)
                    print (cv2.contourArea(cnt))

                    continue
                else:
                    contado = False
                    continue
        #cv2.imshow("image2", imagecrop)
        cv2.imshow("image3", fgmask)
        cv2.rectangle(image, config.zonaElegidaOrigen, config.zonaElegidaFin, (0, 255, 0), 2)
        cv2.putText(image, 'pollos: ' + str(cont), (80,50), cv2.FONT_ITALIC, 1, (0,0,0), 1, cv2.LINE_AA)

        cv2.imshow("image", image)
        cv2.waitKey(100)

main("resources\\ejemplo1.mp4")
