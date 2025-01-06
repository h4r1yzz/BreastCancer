# Overview
This project focuses on building a machine learning model to predict whether a breast tumor is malignant (cancerous) or benign (non-cancerous) based on features extracted from digitized images of fine needle aspirates (FNA) of breast masses. The dataset used in this project is the Breast Cancer Wisconsin (Diagnostic) Dataset, which is publicly available from the UCI Machine Learning Repository.

The goal of this project is to:

1. Preprocess and explore the dataset.

2. Train and evaluate various machine learning models.

3. Deploy the best-performing model for predictions.

This repository contains the code, datasets, and documentation necessary to replicate the project.


## Table of Contents
1. [Dataset](#Dataset).

2. [Installation](#Installation).

3. [Model Training and Evaluation](#Model-Training-and-Evaluation).

4. [Results](#Results).

5. [Link Text](#sample-section).


## Dataset
The dataset used in this project is the Breast Cancer Wisconsin (Diagnostic) Dataset. It contains 569 instances with 30 features each, computed from digitized images of breast mass FNA. The features describe characteristics of the cell nuclei, such as radius, texture, perimeter, area, smoothness, compactness, concavity, symmetry, and fractal dimension.

Target Variable: diagnosis (M = Malignant, B = Benign)

Features: 30 numeric attributes derived from the images.

The dataset is included in the data/ directory as breast_cancer.csv.



# Installation
To set up the project, follow these steps:

Clone the repository:
``` 
git clone https://github.com/your-username/breast-cancer-ml-project.git
cd breast-cancer-ml-project
```
Create a virtual environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install the required dependencies:
```
pip install -r requirements.txt
```

## Model Training and Evaluation
Models Tested
The following machine learning models were trained and evaluated:

1. Logistic Regression

2. Support Vector Machine (SVM)

3. Random Forest Classifier

4. Gradient Boosting Classifier

5. K-Nearest Neighbors (KNN)

# Evaluation Metrics
The models were evaluated using the following metrics:

1. Accuracy

2. Precision

3. Recall

4. F1-Score

5. ROC-AUC Score

## Results
The evaluation results are stored in the results/ directory, including:

1. Confusion matrices

2. ROC curves

3. Feature importance plots



# Example headings

## Sample Section

## This'll be a _Helpful_ Section About the Greek Letter Θ!
A heading containing characters not allowed in fragments, UTF-8 characters, two consecutive spaces between the first and second words, and formatting.

## This heading is not unique in the file

TEXT 1

## This heading is not unique in the file

TEXT 2

# Links to the example headings above

Link to the helpful section: [Link Text](#thisll--be-a-helpful-section-about-the-greek-letter-Θ).

Link to the first non-unique section: [Link Text](#this-heading-is-not-unique-in-the-file).

Link to the second non-unique section: [Link Text](#this-heading-is-not-unique-in-the-file-1).


