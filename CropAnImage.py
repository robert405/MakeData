import numpy as np
from PIL import Image
import glob


def main():

    inputPath = "./notCropedImages/*.jpg"
    outputPath = "./cropedImages/"

    allfile = glob.glob(inputPath)
    counterId = 0

    for file in allfile:

        img = load_image(file)
        getMultipleCrop(counterId, img, (224, 224), 150, outputPath)
        counterId += 1

    print("Done!")



def load_image(infilename) :
    img = Image.open(infilename)
    img.load()
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

    if (img.shape[0] > cropShape[0] and img.shape[1] > cropShape[1]):

        x = img.shape[0] - cropShape[0]
        y = img.shape[1] - cropShape[1]

        for i in range(0, x, step):
            for j in range(0, y, step):
                crop = getCropOfMatrix(img, i, j, cropShape)
                cropName = "crop"+ str(counterId) + "-" + str(int(i/step)) + "-" + str(int(j/step)) +".jpg"
                save_image((savePath + cropName), crop)

main()