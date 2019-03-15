"""
This file will use SKLearn Linear SVMs to create a model so we can
start guessing how jobs will behave

Gee, I hope this works reasonably well.

based on first output, linear seems to be giving a 75% precision

"""
import numpy as np
import pandas as pd


features = pd.read_csv("data-generation/jobs_features.csv")
labels = pd.read_csv("data-generation/job_labels.csv")

all_data = features.merge(labels, left_on="name", right_on="file")
all_data['name'] = pd.factorize(all_data['name'])[0]
all_data['class'] = pd.factorize(all_data['class'])[0]
all_data['file'] = pd.factorize(all_data['file'])[0]

X = all_data.drop('class', axis=1)  
y = all_data['class']

from sklearn.model_selection import train_test_split  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)  

from sklearn.svm import SVC  
svclassifier = SVC(kernel='linear')  
svclassifier.fit(X_train, y_train)  

y_pred = svclassifier.predict(X_test)  


from sklearn.metrics import classification_report, confusion_matrix  
print(confusion_matrix(y_test,y_pred))  
print(classification_report(y_test,y_pred))