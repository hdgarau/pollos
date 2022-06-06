import cv2
import pickle
from classes.config import Config

refPt = []

final_boundaries = []
image = None
pathConfig = "resources\\data\\config.data"
try:
    with open(pathConfig,"rb") as f:
        config = pickle.load(f)
        print(config)
except:
    config = Config()

clickHold = False

def click_and_crop(event, x, y, flags, param):
    global refPt, image, clickHold, config, pathConfig
    if event == cv2.EVENT_LBUTTONDOWN:
        clickHold = True
        refPt = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        final_boundaries.append((refPt[0],refPt[1]))
        config.zonaElegidaOrigen, config.zonaElegidaFin = refPt
        with open(pathConfig, "wb") as f:
            pickle.dump(config, f)
        clickHold = False
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        clone = image.copy()
        cv2.rectangle(clone, refPt[0], (x, y), (255, 0, 0), 2)
        cv2.imshow("image", clone)


def main(video_path):
    global image, clickHold, config
    cap = cv2.VideoCapture(video_path)
    while True:
        success, image = cap.read()
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        #image = cv2.imread(frame) #convert to image boundary
        if config.zonaElegidaOrigen != None and config.zonaElegidaFin != None:
            cv2.rectangle(image, config.zonaElegidaOrigen, config.zonaElegidaFin, (0, 255, 0), 2)
        #cv2.namedWindow("image")
        if not clickHold:
            #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imshow("image", image)
        cv2.setMouseCallback("image", click_and_crop)
        cv2.waitKey(80)
    cv2.destroyAllWindows()
    return (final_boundaries)

main("resources\\ejemplo1.mp4")
