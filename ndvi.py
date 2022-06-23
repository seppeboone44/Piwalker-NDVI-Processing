#importing all functions
import cv2
import numpy as np
from fastiecm import fastiecm

#defining function 'display' to display the image on the screen
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

def contrast_stretch(im):
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)
    
    out_min = 0.0
    out_max = 255.0

    out = im-in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def calc_ndvi(image):
    b, g, r = cv2.split(image)
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.001
    ndvi = (b.astype(float) - r) / bottom
    return ndvi


tot = 320
x = 1

for i in range (0, (tot)):
    
    imageread = str('C:/Users/seppe/Desktop/Astro-Pi_data/piwalker/photo_%03d.jpg' % (x,) )
    image = cv2.imread(imageread) #defining the scource image
    original = np.array(image, dtype=float)/float(255)#convert the image to an array
    contrasted = contrast_stretch(original)
    ndvi = calc_ndvi(contrasted)
    ndvi_contrasted = contrast_stretch(ndvi)
    colour_mapped_prep = ndvi_contrasted.astype(np.uint8)
    colour_mapped_image = cv2.applyColorMap(colour_mapped_prep, fastiecm)

    #display (original, 'Original')
    #display(contrasted, 'Contrasted original')
    #display(ndvi_contrasted, 'NDVI')
    #display(colour_mapped_image, 'Color Mapped')

    #cv2.imwrite('Contrasted.jpg', contrasted)
    #cv2.imwrite('NDVI.jpg', ndvi)
    #cv2.imwrite('NDVI_contrasted.jpg', ndvi_contrasted)
    imagewrite = ('Colour_Mapped_image_%03d.jpg' % (x,))
    cv2.imwrite(imagewrite, colour_mapped_image)

    x += 1
