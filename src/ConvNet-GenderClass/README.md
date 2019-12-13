# Part 2 of Invisible Individuals: Auditing pretrained version of this ConvNet

## Directory Structure
```
.
+-- Viz.R
+-- classify_multiple.py
+-- data.py
+-- detect.py
+-- dlibdetect.py
+-- eval.py
+-- export.py
+-- filter_by_face.py
+-- guess.py
+-- model.py
+-- predictions_all.csv
+-- prob_generated_density_plot2.png
+-- train.py
+-- utils.py
+-- yolodetect.py
```

## Description of Directories and Files
- Python scripts taken from Daniel Pressel's tensorflow implementation of a ConvNet that classifies Age and Gender. His implementation is based off of the following paper: https://talhassner.github.io/home/publication/2015_CVPR. These scripts include: data.py, detect.py, dlibdetect.py, eval.py, export.py, filter_by_face.py, guess.py, model.py, train.py, utils.py, and yolodetect.py. For more details about Pressel's implementation visit: https://github.com/dpressel/rude-carnie.
- In auditing the performance of this kind of network in classifying gender (i.e. using our dataset, Invisible Individuals, as a test set), we used a pre-trained gender checkpoint that is not included in this repo. Find this pre-trained checkpoint here: https://drive.google.com/drive/folders/0B8N1oYmGLVGWemZQd3JMOEZvdGs
- classify_multiple.py is written completely by our team. It mostly just includes logic to select the images to predict on, to write those predictions to as csv, compare those predictions to the actual values, and to calculate positive predictive value for each gender/race group
- predictions_all.csv includes the following information: filenames, actual gender labels, actual race labels, whether the corresponding image has been generated, the predicted gender outputted by the classifier, and the probability (or confidence) the classifier outputted that label with
- Viz.R is an R script that was used to create a plot that depicts the distributions of the classifiers' confidence (or probability) values and compares the difference between this distribution for the generated and the original images.
- prob_generated_density_plot2.png is the plot that is generated with Viz.R


## Local Setup
This project has pretty much the same set of dependencies as those specified in the README within the dcgan directory. Just activate the virutal environment you created for that part of the project and you should be all set to classify some images. To create the visualization using the R Script provided, you will need to have R installed. 

### More information about running the classifier and using the pretrained checkpoint to guess the gender of subjects in images can be found: https://github.com/dpressel/rude-carnie.

