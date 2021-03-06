
import skimage.transform as ski
from cv2 import cv2
from PIL import Image
import random
import os
import seaborn as sns;
from matplotlib import pyplot as plt


sns.set()
import numpy as np
def square_matrix(imagestring):
    imagestring=str(imagestring)
    imagearray = [0, ]
    for i in imagestring:
        imagearray.append(i)
    squarematrix = np.array(imagearray).reshape(11, 11)
    return squarematrix
def returnheatmaps(number):
# Part 1 this is the part that I used to get the classification of each of the access of an image so i have been able to load the image and convert each image to nd array

    def generateimageurl(c):
        arrayofimgurls = []
        images = os.listdir(os.path.join(os.getcwd(), 'MNIST_DS/' + c))
        for img in images:
            arrayofimgurls.append(os.path.join(os.getcwd(), 'MNIST_DS/' + c, img))
        return arrayofimgurls

    folderidentificationarray = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    new_arr = []
    for iden in folderidentificationarray:
        new_arr.append(generateimageurl(iden))
    images_in_folder0 = new_arr[0]
    images_in_folder1 = new_arr[1]
    images_in_folder2 = new_arr[2]
    images_in_folder3 = new_arr[3]
    images_in_folder4 = new_arr[4]
    images_in_folder5 = new_arr[5]
    images_in_folder6 = new_arr[6]
    images_in_folder7 = new_arr[7]
    images_in_folder8 = new_arr[8]
    images_in_folder9 = new_arr[9]

    def open_image_and_covert_to_array(num):
        empty_array = []
        for imgurl in num:
            image = Image.open(imgurl)
            empty_array.append(np.asarray(image))
        return empty_array

    converted0 = open_image_and_covert_to_array(images_in_folder0)
    converted1 = open_image_and_covert_to_array(images_in_folder1)
    converted2 = open_image_and_covert_to_array(images_in_folder2)
    converted3 = open_image_and_covert_to_array(images_in_folder3)
    converted4 = open_image_and_covert_to_array(images_in_folder4)
    converted5 = open_image_and_covert_to_array(images_in_folder5)
    converted6 = open_image_and_covert_to_array(images_in_folder6)
    converted7 = open_image_and_covert_to_array(images_in_folder7)
    converted8 = open_image_and_covert_to_array(images_in_folder8)
    converted9 = open_image_and_covert_to_array(images_in_folder9)
    r3= random.randint(0,9)

    if (number/10==0):
        g= converted0[r3]
    elif (number/10==1):
        g= converted1[r3]

    elif (number/10==2):
        g= converted2[r3]
    elif (number/10==3):
        g= converted3[r3]
    elif (number/10==4):
        g = converted4[r3]
    elif (number/10==5):
        g= converted5[r3]

    elif (number/10==6):
        g= converted6[r3]

    elif (number/10==7):
        g= converted7[r3]
    elif (number/10==8):
        g = converted8[r3]
    elif (number/10==9):
        g= converted9[r3]
    else :
        g = converted0[1]


    ax = sns.heatmap(g, annot=True, fmt="d")
    plt.show()
#Function in order to open images and crop them
def Openimgs():

    Croppedimgs = np.empty((0,20,20))

    for i in range(0,10,1):
        for FILENAME in os.listdir('MNIST_DS\\{}'.format(i)):
            img = cv2.imread(os.path.join('MNIST_DS\\{}'.format(i),FILENAME),0)
            if img is not None:
                Oimg = np.array(img)
                crimg = Oimg[6:26,6:26]
                Croppedimgs = np.append(Croppedimgs,[crimg], axis=0)
    return Croppedimgs
#Get image function
def get_image(index):
    filename = os.listdir('MNIST_DS\\{}'.format(int(index/10)))
    img = cv2.imread(os.path.join('MNIST_DS\\{}'.format(int(index/10)),filename[int((str(index))[-1])]),0)
    if img is not None:
        return img
#Barcodegenerator function with projections
def Barcodegenerator(image):
    bcde = np.array([])
    for i in range(0,180,30):
        VectorProjection = ski.radon(image, [i], circle=True, preserve_range=True)
        Thresholdvalues = np.mean(VectorProjection)
        for i in range(0, VectorProjection.size, 1):
            if (VectorProjection[i]>=Thresholdvalues):
                VectorProjection[i] = 1
            else:
                VectorProjection[i] = 0

        bcde = np.append(bcde, VectorProjection)


    stringcode = ''
    for i in range(0, bcde.size, 1):
        stringcode += str(int(bcde[i]))

    return stringcode


def Barcodesetgen():
    try:
#Opens barcodes.txt
        f = open("barcodes.txt", "x")
    except:
        f = open("barcodes.txt", "w")
#Accessing each image in the dataset in order to convert and crop.
    images = Openimgs()
    num_images = images.shape[0]

#Iterates within the dataset images converting each to a binary string and writing to file Barcodes.txt each on a new line
    for i in range(0,num_images,1):
        code_string = Barcodegenerator(np.asarray(images[i]))
        f.write(code_string +'\n')
#Closing of barcodes.txt file
    f.close()

Barcodesetgen()
