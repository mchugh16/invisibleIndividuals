# Invisible Individuals
In an attempt to identify limitations and improve facial recognition of marginalized identities, our research consisted of two parts:
1. Creating a diverse and unconstrained (in relation to pose, illumination and expression) dataset comprised of both synthesized and photographed images

2. Identifying limitations of existing tools in classifying gender by auditing a lightweight, open source gender classification algorithm. We worked on answering the following questions:
- Are these facial recognition algorithms really as accurate as the researchers who developed them say they are?
- Can these algorithms consistently maintain its performance and accurately classify the genders of individuals across racial groups?

## Directory Structure
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
