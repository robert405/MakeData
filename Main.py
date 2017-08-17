import numpy as np
from PIL import Image
import glob
#import os

def main():

    inputGoodPath = "./PreData/good/*/"
    inputBadPath = "./PreData/bad/*/"
    outputGoodPath = "../Data/good/"
    outputBadPath = "../Data/bad/"

    allTree = glob.glob(inputGoodPath)
    counterId = 0
    tooSmallCounterGood = 0

    print("Begining Good Data")
    for treePath in allTree:

        print("Cropping file in : " + treePath)
        tempTreePath = treePath + "*.jpg"
        allFile = glob.glob(tempTreePath)

        for file in allFile:
            img = load_image(file)
            tooSmall = getMultipleCrop(counterId, img, (224, 224), 120, outputGoodPath)
            tooSmallCounterGood += tooSmall
            counterId += 1

            #if (tooSmall == 1):
                #os.remove(file)

    print("Good done!")
    print("Nb good image too small : " + str(tooSmallCounterGood))

    allTree = glob.glob(inputBadPath)
    counterId = 0
    tooSmallCounterBad = 0

    print("Begining Bad Data")
    for treePath in allTree:

        print("Cropping file in : " + treePath)
        tempTreePath = treePath + "*.jpg"
        allFile = glob.glob(tempTreePath)

        for file in allFile:
            img = load_image(file)
            tooSmall = getMultipleCrop(counterId, img, (224, 224), 100, outputBadPath)
            tooSmallCounterBad += tooSmall
            counterId += 1

            #if (tooSmall == 1):
                #os.remove(file)

    print("Bad done!")
    print("Nb bad image too small : " + str(tooSmallCounterBad))


def load_image(infilename) :
    img = Image.open(infilename)
    img.load()
    wsize = (int)(float(img.size[0]) / 2)
    hsize = (int)(float(img.size[1]) / 2)
    img = img.resize((wsize, hsize), Image.ANTIALIAS)
    data = np.asarray(img, dtype="int32" )
    return data

def save_image(filename, data):
    data = data.astype('uint8')
    im = Image.fromarray(data)
    im.save(filename)

def getCropOfMatrix(img, left, top, shape):

    right = left + shape[0]
    bottom = top + shape[1]
    return img[left:right, top:bottom]

def getMultipleCrop(counterId, img, cropShape, step, savePath):

    tooSmallCounter = 0

    if (img.shape[0] > cropShape[0] and img.shape[1] > cropShape[1]):

        x = img.shape[0] - cropShape[0]
        y = img.shape[1] - cropShape[1]

        for i in range(0, x, step):
            for j in range(0, y, step):
                crop = getCropOfMatrix(img, i, j, cropShape)
                cropName = "crop"+ str(counterId) + "-" + str(int(i/step)) + "-" + str(int(j/step)) +".jpg"
                save_image((savePath + cropName), crop)

    else:
        tooSmallCounter = 1

    return tooSmallCounter

main()