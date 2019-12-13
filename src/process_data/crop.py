"""" USAGE: 
     Place .py files in the folder with images to be cropped. 
     Results: Cropped images will be saved in a folder, one level up, called "cropped". Use the following commands to make sure cropped and generated have the same number of files:
            $ ls -1q cropped | wc -l
            $ ls -1q generated | wc -l
            
        
"""

import shutil 
from PIL import Image 
import os 

def get_image_files(data_dir):
	files = os.listdir(data_dir)
	return files

def crop_save(path, save_name): 
	im = Image.open(path)
	left = 113
	top = 35
	right = 330
	bottom = 250
	im1 = im.crop((left, top, right, bottom))
	im1.save(save_name)
	im1.close()

dir = os.getcwd()
croppedPath = "../cropped"
os.mkdir(croppedPath) #makes directory for cropped images
fn_list = get_image_files(dir)

for i in fn_list:
	if ((i != ".DS_Store") and (i != "crop.py")):  
		file_path = dir + "/" + i
		crop_save(file_path, "cropped_"+i)
		shutil.move(dir+"/cropped_"+i, croppedPath)	
