# Part 1 of Invisible Individuals
## Using Deep Convolutional Generative Adversarial Networks, implented with TensorFlow, to generate a diverse set of human faces.


This repository contains source code that is based off of the article ["Deep Convolutional Generative Adversarial Networks with TensorFlow"](https://www.oreilly.com/ideas/deep-convolutional-generative-adversarial-networks-with-tensorflow).

## Local setup using Miniconda


1. Install miniconda using (https://conda.io/miniconda.html). Use Python3.6.

2. After the installation, create a new virtual environment, using this command.
	```
	$ conda create -n dcgan
	$ source activate venv
	```
   
3. Once in the virtual environment, [install TensorFlow by following the instructions](https://www.tensorflow.org/install/).

4. To install the rest of the dependenies, navigate into your repository and run 

	```
	$ pip install matplotlib
	$ pip install requests
	$ pip install Pillow
	$ pip install tqdm
	```
   
5. Now you can run 

	```
	jupyter notebook
	```
	
	to finally start up the notebook. A browser should open automatically.
	
6. Choose `DCGANs with Tensorflow.ipynb` to open the Notebook.
7. Further instructions are included within the notebook. Note that the main modifications (from the original version) are that we read the entire Fairface dataset in and split the set into race/gender subgroups within the 1st code snippet. From here, we specify the directory of a specific race/gender subgroup to train the GAN on in the 2nd snippet. Towards the end of the notebook, we wrote a few functions to save sample images during the last epoch to that same race/gender directory. The last snippet contains the hyperparameters we used to train the GAN before creating our final set of images.

