"""USAGE: 
   Place .py file in the same folder as the images. Ensure that the only other files (apart from the images files) in the directory are .DS_Store and images.py
   run oython script from terminal: 'python images.py' 
   Result: first number - total number of images, second number - original images (.jpg), third number - generated images (.png) 
   If images have already been separated, an error message will me displayed 
"""


import os
import shutil  


pngCnt=0 
jpgCnt=0 #original images are .jpg and generated images are .png 

dir = os.getcwd()
path = dir + "/generated"

if (os.path.exists(path)): 
	print ("ERROR: Images have been separated into original and generated folders")
else: 
	originalPath = dir + "/original"
	os.mkdir(path) #makes directory for generated images
	os.mkdir(originalPath) #makes directory for original images
	list = os.listdir(dir)

	for i in list: 
		if(".png" in i):
			pngCnt += 1
			shutil.move(dir+"/"+i, path)
		elif (".jpg" in i): 
			jpgCnt += 1
			shutil.move(dir+"/"+i, originalPath)

	number_files = len(list) - 1 #subract stats.csv, .DS_Store and images.py file

	print (number_files)
	print('.jpg images:', jpgCnt)
	print('.png images:', pngCnt)
