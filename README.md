<div style="text-align:center"><img src="https://github.com/cemreefe/are-you-wearing-your-mask/blob/master/media/collage/collage4.jpg?raw=true" alt="people detected using opencv"/></div>

***People on İstiklal St. detected by OpenCV***

# Are you wearing your mask?

> The spread of Covid-19 virus has changed mask-wearing habits of many countries around the globe. We will try and track the ratio of mask-wearers in the population of Istanbul with a sample from _İstiklal St._.

<div style="text-align:center"><img src="https://github.com/cemreefe/are-you-wearing-your-mask/blob/master/media/predictions/predictions.png?raw=true" alt="masked or not masked predictions"/></div>

## The aim of this project

  - To **track public awareness** and how different events affect mask usage
  - To **demonstrate the pandemic's effect** on everyday life and how it changes over time
  - To learn the basics of **Computer Vision**, and experiment with **CNNs**
  - To have something to do during the three-week quarantine period
  
> There have also been claims that globalization could be jeopardized by a prolonged global health crisis, as supply chains have been disrupted and reliance on the Chinese economy questioned. 
[_Wikipedia, Socio-economic impact of the 2019–20 coronavirus pandemic_](https://en.wikipedia.org/wiki/Socio-economic_impact_of_the_2019%E2%80%9320_coronavirus_pandemic)

- To track if the **disruption of supply chains** cause a drop in mask usage or not
<br>



## Table of Contents

- [Project Description](#project)
- [Dependencies](#dependencies)
- [Dataset Preparation](#dataset-preparation)
- [Training and Evaluation](#training-and-evaluation)
- [Challenges](#challenges)
- [Future Work](#future-work)


<br>

## Project Description


In order to track the ratio of people who wear masks in public, we first need a dataset of images of people in public, every day in great quantities. To achieve this we opted to use the live touristic cameras provided by the _Istanbul Metropolitan Municipality_ (İBB). 

Feeding the live feed into OpenCV's human detection tool, we were able to extract images of people in real time. `people-detector.py` detects people in real time from the camera feed and saves them as seperate image files with appropriate time stamps.

The image data can then be processed by running `mask-classifier.py` which uses the model trained by using `mask-classifier-training.ipynb`. The training of the model requires labeled software which can be labeled using `gui-annotation-tool.py`. 

The mask classifier script predicts labels for all existing image data and plots the ratio of people wearing masks day by day.

<br>

## Dependencies

- OpenCV
- Tensorflow
- Keras
- NumPy
- Pillow
- Streamlink
- Matplotlib
- Tkinter (for the gui annotation tool)

<br>

## Dataset Preparation


> Run `people-detector.py` to collect images and then run `gui-annotation-tool.py` to label the data. 

<br>

## Training and Evaluation

1. Open up `mask-classifier-training.ipynb` and load your labels file
2. Train as the notebook upsamples the number of masked people (TODO: the ratio should be calculated)
3. Plot training history and pick promising checkpoints.
4. Inspect their confusion matrices on your test set.
    * For reference, the model I used had 89% accuracy with a balanced confusion matrix
5. Move your model of choice into `models/` and name it `mask-detector.h5`
6. Run `mask.classifier.py` to plot the percentage of masked people in the population.

<br>

## Challenges

Of course there has been a lot of challenges in this projects, but I wanted to list two remarkable problems I needed to solve during this project.

### Duplicates

Since the algorithm takes input frame by frame and does not do any sort of object tracking, a way to identify previously people previously seen by the model and not take them into account was needed. To achieve this we keep recently seen people in memory. If an image similar to one that is recently seen is encountered, the image in memory is updated and its age is reset. This way in the next iteration this image will again be similar to its newer version.

<div style="text-align:center"><img src="https://github.com/cemreefe/are-you-wearing-your-mask/blob/master/media/similarity/similarity.png?raw=true" alt="different and similar images by MSE and Imagehash difference"/></div>

To check the similarity, MSE is calculated between the images. We also take the difference between their hashes. We use these two difference measures to split the pairs into three groups: _similar_, _ambigous_ & _different_.

- Similar images are updated and refreshed.
- Ambigious images are added to recently seen images but not written to a file as a new encounter.
- Different images are added to recently seen and written to a file as a new encounter.

### Yellow taxis as people

A lot of taxis were being recognized as people, and when head detection was used in earlier versions to filter out unwanted images from the dataset they passed with high confidence.

So a taxi filter was put into place that checks how much taxi color is apparent in an image. If the taxi color abundancy is above the threshold, the taxi filter deletes said image.

<div style="text-align:center"><img src="https://github.com/cemreefe/are-you-wearing-your-mask/blob/master/media/taxiscore.png?raw=true" alt="taxi color filter"/></div>

<br>

## Future Work

> Most importantly, data should be collected everyday for several weeks to give  meaningful insight

Other future work:

* Better models could be used both for detection and classification
* Scripts should be modified to be manipulated from the terminal
* Some parts of the code should be automated

