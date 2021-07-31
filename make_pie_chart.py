import os
import sys
import pandas as pd
import numpy as np
import cv2
import numpy

image_resolution=1024
image_names = []
images = []
white_color = 255
black_pixel = [0,0,0]
transparant_pixel = [0,0,0,0]
donut_chart = False


common_img_extn=["tif","tiff","png","jpg","jpeg","bmp","gif","eps"]
image_dir = "./"
file_names = os.listdir(r"./")

for file_name in file_names:
    if file_name.split(".")[-1] in common_img_extn:
        image_names.append(file_name)

for image in image_names:
    img=cv2.imread(image,cv2.IMREAD_UNCHANGED)
    img=cv2.resize(img,(image_resolution,image_resolution))
    images.append(img)

arr = []
if len(sys.argv[1:]) > len(image_names):
    raise NameError("Can only have {} values or less in arguments.".len(image_names))
else:
    num_data=len(sys.argv[1:])
for arg in sys.argv[1:]:
    try:
        arr.append(int(arg))
    except:
        raise NameError("Argument {} is not int.".format(arg))

arr = pd.Series(arr)
sum_arr = sum(arr)
arr = (arr/sum_arr)*100

start_angle = []
end_angle = []

s_angle = 0
for s in arr:
    start_angle.append(s_angle)
    s_angle=round(s_angle+((s*360)/100))
    end_angle.append(s_angle)


for i in range(num_data):
    mask = np.zeros((image_resolution,image_resolution))
    radius= int(image_resolution/2)-1
    angle = 0
    startAngle=start_angle[i]
    endAngle=end_angle[i]
    center=(radius,radius)
    color=white_color
    
    if donut_chart == True:
        half_radius = int(radius/2)
    else:
        half_radius = 0
        
    for r in range(half_radius,int(radius)):
        axes = (r+1,r+1)
        axes2 = (r+1,r)
        axes3 = (r,r+1)
        cv2.ellipse(mask,center,axes,angle,startAngle,endAngle,color)
        cv2.ellipse(mask,center,axes2,angle,startAngle,endAngle,color)
        cv2.ellipse(mask,center,axes3,angle,startAngle,endAngle,color)
    img=images[i]
    
    for x in range(image_resolution):
        for y in range(image_resolution):
            if(mask[x,y]==0):
                if(len(img[x,y])==3):
                    img[x,y]=black_pixel
                else:
                    img[x,y]=transparant_pixel

    if i==0:
        final_img=img
    else:
        final_img=cv2.addWeighted(final_img,1.0,img,1.0,0)
try:    
    os.mkdir("output")
except:
    pass
cv2.imwrite('output/final_img.png',final_img)
