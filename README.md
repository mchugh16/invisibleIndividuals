# Invisible Individuals
In an attempt to identify limitations and improve facial recognition of marginalized identities, our research consisted of two parts:
1. Creating a diverse and unconstrained (in relation to pose, illumination and expression) dataset comprised of both synthesized and photographed images

2. Identifying limitations of existing tools in classifying gender by auditing a lightweight, open source gender classification algorithm. We worked on answering the following questions:
- Are these facial recognition algorithms really as accurate as the researchers who developed them say they are?
- Can these algorithms consistently maintain its performance and accurately classify the genders of individuals across racial groups?

## Directory Structure
```
.
+-- data-flat
+-- data-separated
|   +-- female
|       +-- female_black
|           +-- cropped
|           +-- original
|       +-- female_east_asian
|           +-- cropped
|           +-- original
|       +-- female_indian
|           +-- cropped
|           +-- original
|       +-- female_latino_hispanic
|           +-- cropped
|           +-- original
|       +-- female_middle_eastern
|           +-- cropped
|           +-- original
|       +-- female_southeast_asian
|           +-- cropped
|           +-- original
|       +-- female_white
|           +-- cropped
|           +-- original
|   +-- male
|       +-- male_black
|           +-- cropped
|           +-- original
|       +-- male_east_asian
|           +-- cropped
|           +-- original
|       +-- male_indian
|           +-- cropped
|           +-- original
|       +-- male_latino_hispanic
|           +-- cropped
|           +-- original
|       +-- male_middle_eastern
|           +-- cropped
|           +-- original
|       +-- male_southeast_asian
|           +-- cropped
|           +-- original
|       +-- male_white
|           +-- cropped
|           +-- original
+-- src
|   +-- ConvNet-GenderClass
|       +-- README.md
|       +-- Viz.R
|       +-- annotations.csv
|       +-- classify_multiple.py
|       +-- data.py
|       +-- detect.py
|       +-- dlibdetect.py
|       +-- eval.py
|       +-- export.py
|       +-- filter_by_face.py
|       +-- guess.py
|       +-- model.py
|       +-- predictions_all.csv
|       +-- prob_generated_density_plot2.png
|       +-- train.py
|       +-- utils.py
|       +-- yolodetect.py
|   +-- dcgan
|       +-- DCGANs with Tensorflow.ipynb
|       +-- README.md
|       +-- helper.py
|   +--process_data
|       +-- crop.py
|       +-- separate_generated_original.py
+-- ProjectPoster.pptx
+-- README.md
```

## Description of Directories and Files
- data-flat: final version of our dataset (Invisible Individuals!). Directory has generated images, original images (from Fairface), and a csv with annotations for the dataset.
- data-separated: directory with generated and original (Fairface) images. This directory is divided by genders, then races, then cropped (generated) vs. original images. This is a pre-flattened version of the 'data-flat' version. 
- ProjectPoster.pptx: poster used to present this research after CS701
- src contains 3 directories: ConvNet-GenderClass, dcgan, and process_data
- ConvNet-GenderClass is a combination of (1) an implementation of an Age and Gender Deep Learning Network implemented in Tensorflow, and (2) scripts we used to run the pretained version of the netrok on our images, the resulting predictions file, and an R script to creates a plot of the distributions of the probabilities of the classifications of the generated versus original images. This directory contains everything used for Part 2 of our research. See the README in this file for more details, examples, and set up instructions.
- dcgan contains an ipython notebook with an implementation of a deep convolutional gan (which we used to separate the original fairface dataset and synthesize images for each gender/race subset) as well as a helper python script. This directory contains everything we used to for Part 1 of our research. See the README in this file for more details, examples, and set up instructions.
- process_data contains python scripts to crop our generated images as well as separated the generated images from the original images. These scripts were used in between Part 1 and Part 2 of our research. After generating the images and before running both the generated and original images through the classifier, it was necessary to separate out the generated images, and crop out the whitespace. To do this, we used the data-separated directory. We ran the separate_generated_original script within each race/gender subset directory. The images were, as a result, split into generated and original directories. After this we ran the crop.py script on each "generated" dir. The result of running these scripts is what resides withing the data-separated dir. 
