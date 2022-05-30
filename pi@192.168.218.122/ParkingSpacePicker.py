import cv2, pickle, os


parkin_img="parkin1.jpg"
parkin_vid="parkinv.mp4"
reset_key=ord("r")
quit_key=ord("q")
# width, height = 107, 48
width, height = 107, 150

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    img = cv2.imread(parkin_img)
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
        
    key =cv2.waitKey(1)
    if key == quit_key:
        break
    elif key == reset_key:
        os.remove("CarParkPos")
        break
        