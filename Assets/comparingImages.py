import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import sys
from sklearn import svm, preprocessing
from skimage.feature import hog
from skimage import data, exposure
from skimage.transform import resize
from collections import Counter



#This fucntion was taken from Programming Assignment 1 in CS482
def load_image(filepath):
    """Loads an image into a numpy array.
    Note: image will have 3 color channels [r, g, b]."""
    img = Image.open(filepath)
    return (np.asarray(img).astype(float)/255)[:, :, :3]

    
def convertImage(image):
    #Converts the provided image to a hog_image, and appednds the features to the frame for processing later.

    #Parameters:
    #    image (np.array):The image to be converted.

    #Returns:
    #    test_frame(np.array):A collection of all features within the image
    testing_data = []
    testing_features = []
    # Construct HOG descriptor
    image = resize(image, (128*4, 64*4))
    features, hog_image = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True, channel_axis=-1)
    # Add HOG image and hog_features to dataset. 
    testing_data.append(hog_image)
    testing_features.append(features)
    hog_testing_features = np.array(testing_features)
    test_frame = np.hstack((hog_testing_features,[[]]))
    return test_frame

        
def display(imagePath, num):
    #Converts the provided image to a hog_image, and appednds the features to the frame for processing later.

    #Parameters:
    #    imagePath (str):The source for all the images
    #    num (int): Used to tell the program which image it needs to draw for the testing.

    #Returns:
    #    occurence_count.most_common(1)[0][0] (str): The most common occurance in the test predition, i.e. the prediction with the highest degree of accuracy. 
    
    #Start by assessing the HOG Features, and creating our training data set and features. 
    training_data = []
    training_features = []
    trainLabels = ["dead_end", "dead_end", "trap", "trap", "trap", "exit", "left", "straight", "left_or_straight", "left_or_right", "left_or_right", "left", "left", "left", "right", "right", "left_or_right", "right", "right", "straight_or_left" , "straight_or_left", "straight_or_right", "straight_then_left", "straight_then_right", "straight_then_right", "wall"]
    for files in os.listdir(imagePath + "potentialCorners\"):
        if files.endswith(".JPG"):
            image = load_image(imagePath + files)
            # Construct HOG descriptor
            image = resize(image, (128*4, 64*4))
            features, hog_image = hog(image, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True, channel_axis=-1)
            # Add HOG image to dataset. 
            training_data.append(hog_image)
            training_features.append(features)
        else:
            continue
            
    #Train the SVM classifier on the data
    clf = svm.SVC()
    hog_features = np.array(training_features)
    labelEncoder = preprocessing.LabelEncoder()
    trainLabels = labelEncoder.fit_transform(trainLabels)
    trainLabels = np.array(trainLabels, dtype=np.int32)
    trainLabels = trainLabels.reshape(len(trainLabels),1)
    data_frame = np.hstack((hog_features,trainLabels))
    np.random.shuffle(data_frame)
    percentage = 100
    partition = int(len(hog_features)*percentage/100)
    x_train, x_test = data_frame[:partition,:-1],  data_frame[partition:,:-1]
    y_train, y_test = data_frame[:partition,-1:].ravel() , data_frame[partition:,-1:].ravel()
    clf.fit(x_train,y_train)

    #Load the test image, and get a preditiction based on the trained images. 
    test_image = load_image(imagePath + "decisionScreenshot/cameracapture" + num + ".png")
    testResponse = clf.predict(convertImage(test_image)).ravel().tolist()
    occurence_count = Counter(labelEncoder.inverse_transform([int(a) for a in testResponse]))
    return(occurence_count.most_common(1)[0][0])
                    
#Print the prediction
print(display(sys.argv[1]))
