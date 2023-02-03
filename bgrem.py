import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys
from  PIL  import Image

def removebg(imgstr):
    img = cv.imread(imgstr, cv.IMREAD_UNCHANGED)
    original = img.copy()

    l = int(max(5, 6))
    u = int(min(6, 6))

    ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imwrite("cvtcolour.png",ed)
    edges = cv.GaussianBlur(img, (21, 51), 3)
    edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(edges, l, u)

    _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)
    cv.imwrite('./processing/mask.png', mask)
    data = mask.tolist()
    sys.setrecursionlimit(10**4)
    for i in  range(len(data)):
        for j in  range(len(data[i])):
            if data[i][j] !=  255:
                data[i][j] =  -1
            else:
                break
        for j in  range(len(data[i])-1, -1, -1):
            if data[i][j] !=  255:
                data[i][j] =  -1
            else:
                break
    image = np.array(data)
    image[image !=  -1] =  255
    image[image ==  -1] =  0

    mask = np.array(image, np.uint8)
    cv.imwrite('./processing/bg1.png', mask)
    result = cv.bitwise_and(original, original, mask=mask)
    result[mask ==  0] =  255
    cv.imwrite('./processing/bg.png', result)

    img = Image.open('./processing/bg.png')
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
            newData.append((0,0,0, 0))
        elif item[0] ==  0  and item[1] ==  0 and item[2] ==  0:
            newData.append((0,0,0, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save("./processing/1.png", "PNG")

def rem(imgstr):
    img = cv.imread(imgstr)
    mask = np.zeros(img.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    width, height, c = img.shape
    rect = (0+3,0+3,height-3,width-15)
    print(width, height)
    #cv.rectangle(img,(0,0), (height, width), (255,0,0), 2)
    cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
    cv.imwrite("./processing/out.png", img)

def removeSkin(imgstr):
    min_YCrCb = np.array([0,133,77],np.uint8)
    max_YCrCb = np.array([235,173,127],np.uint8)

    # input_image = Image.open("bgtshirt.png")
    # pixel_map = input_image.load()
    # width, height = input_image.size
    # print(input_image.getpixel((0, 0)))
    # for i in range(width//2):
    #     for j in range(height):
    #         # getting the RGB pixel value.
    #         r, g, b = input_image.getpixel((i, j))
    #         if(0<r<235 and 133<g<173 and 77<b<127):
    #             pixel_map[i, j] = (255, 255, 255)
    # input_image.save("grayscale.png", format="png")


    # Get pointer to video frames from primary device
    image = cv.imread(imgstr)
    imageYCrCb = cv.cvtColor(image,cv.COLOR_BGR2YCR_CB)

    skinRegionYCrCb = cv.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    revSkinYCrCb = cv.bitwise_not(skinRegionYCrCb)
    cv.imwrite("./processing/revskinmask1.png", revSkinYCrCb)
    cv.imwrite("./processing/skinmask.png", skinRegionYCrCb)
    #revSkinRegionYCrCb = cv2.bitwise_not(skinRegionYCrCb)
    skinYCrCb = cv.bitwise_and(image, image, mask = revSkinYCrCb)
    cv.imwrite("./processing/skinmask1.png", skinYCrCb)
    mask1 = cv.imread('./processing/bg1.png')
    mask2 = cv.imread('./processing/skinmask1.png')
    new = cv.bitwise_and(mask2, mask1, mask = None)
    cv.imwrite('./processing/ggwp.png', new)

    cv.imwrite("./processing/ycrcb.png", skinYCrCb)
    removebg("./processing/ggwp.png")

def init(path):
    rem(path)
    removebg("./processing/out.png")
    removeSkin("./processing/1.png")


