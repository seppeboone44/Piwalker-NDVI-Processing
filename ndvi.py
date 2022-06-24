#importing all functions
import cv2
import numpy as np
from fastiecm import fastiecm

#defining function 'display' to display the image on the screen, we do not end up using this function in the final programm, but we used it during testing.
def display(image, image_name):
    image = np.array(image, dtype=float)/float(255)#convert the image to an array
    
    #resizing
    shape = image.shape 
    height = int(shape[0]/2.8)
    width = int(shape[1]/2.8)
    image = cv2.resize(image, (width, height))

    cv2.namedWindow(image_name)#creating a window
    cv2.imshow(image_name, image)#displaying the image
    cv2.waitKey(0)#waiting until any key is pressed
    cv2.destroyAllWindows()#the window is closed again

#defining a function to stretch the contrast of the image, this enures we get the maximum amount of data out of the picture.    
def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)
    
    out_min = 0.0
    out_max = 255.0

    out = im-in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

#This function calculates the NDVI values for the image.
def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.001
    ndvi = (b.astype(float) - r) / bottom
    return ndvi

#We set some variables for the loop to use.
tot = 320
x = 1

#The loop automaticaly calculates the NDVI of all images (total of 320) and stores the processed images in the same folder the program is stored in.
for i in range (0, (tot)):
    
    imageread = str('C:/Users/user/Desktop/Astro-Pi_data/piwalker/photo_%03d.jpg' % (x,) ) #This is where the program can find the image.
    image = cv2.imread(imageread) #defining the scource image
    original = np.array(image, dtype=float)/float(255)#convert the image to an array
    contrasted = contrast_stretch(original) #Using the contrast_stretch function to stretch the contrast.
    ndvi = calc_ndvi(contrasted) #Using the calc_ndvi function to calculate the NDVI value of all pixels in the image.
    ndvi_contrasted = contrast_stretch(ndvi) #The ndvi image turns out really dark, so the contrast is streched again to produce a clear image.
    colour_mapped_prep = ndvi_contrasted.astype(np.uint8) #the image is prepared for colourmapping.
    colour_mapped_image = cv2.applyColorMap(colour_mapped_prep, fastiecm) #And finally a colourmapped version of the NDVI image is produced.

    #The following code was usefull during testing, but for the processing of all pictures it isn't used anymore.
    
    #display (original, 'Original')
    #display(contrasted, 'Contrasted original')
    #display(ndvi_contrasted, 'NDVI')
    #display(colour_mapped_image, 'Color Mapped')

    #cv2.imwrite('Contrasted.jpg', contrasted)
    #cv2.imwrite('NDVI.jpg', ndvi)
    #cv2.imwrite('NDVI_contrasted.jpg', ndvi_contrasted)
    imagewrite = ('Colour_Mapped_image_%03d.jpg' % (x,)) #The name of the new image is defined.
    cv2.imwrite(imagewrite, colour_mapped_image) #And finally the new image is saved.
   
    x += 1 #We add 1 to x to run the loop for the next image.
