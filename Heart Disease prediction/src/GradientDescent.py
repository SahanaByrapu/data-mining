# -*- coding: utf-8 -*-
"""HW2_GD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_qDTyn1GkwNevmAiNibDhUK3zifrT8ra
"""

import numpy as np
import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score
from statistics import mean
from fractions import Fraction as fr
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

Traindata_df = pd.read_csv('/content/1644871518_6273746_cleveland-train.csv')
Testdata_df = pd.read_csv('/content/1644871518_6284828_cleveland-test.csv')
Testdata_df

X= Traindata_df.iloc[0:152,0:13]
    Y= Traindata_df['heartdisease::category|-1|1']
    X_test_file=Testdata_df[0:145]
    
    X=X.to_numpy()
    Y=Y.to_numpy()
    X_test_file=X_test_file.to_numpy()

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4, random_state=15)
print("X_train",X_train)
print("Y_train",Y_train)
print(Y_train.shape)

def generateXvector(X):
    """ Taking the original independent variables matrix and add a row of 1 which corresponds to x_0
        Parameters: X:  independent variables matrix
        Return value: the matrix that contains all the values in the dataset, not include the outcomes variables. """  
    vectorX = np.c_[np.ones((len(X), 1)), X]
    return vectorX

def theta_init(X):
    """ Generate an initial value of vector θ from the original independent variables matrix
         Parameters: X:  independent variables matrix
        Return value: a vector of theta filled with initial guess
    """
    theta = np.random.randn(len(X[0])+1, 1)
    #theta = np.zeros((len(X[0])+1,1))
    
    return theta

def sigmoid(z):
    """ Calculate the sigmoid value of the inputs
        Parameters: z:  values
        Return value: the sigmoid value
    """
    z = 1 / (1+math.e**-z)
    return z

def logloss(y_new,X,theta,m):
    """ Calculate the logloss value of the inputs
        Parameters: y_new: training data labels  X: independent variables matrix
                    theta: weight vector         m:total number of training samples
        Return value: the cross entropy error 
    """
    z=sigmoid(y_new*np.dot(X,theta))
    cost= (1/m)* np.sum((np.log(1/z)))
    return cost

def gradient(y_new,vectorX,theta,m):
    """ Calculate the gradient value of the inputs
        Parameters: y_new: training data labels  vectorX: independent variables matrix
                    theta: weight vector         m:total number of training samples
        Return value: the gradient value 
    """
    yixi = y_new*vectorX
    z= -y_new*np.dot(vectorX,theta)
    z=sigmoid(z)
    vector_gr = yixi * z
    vector_gr=np.array(vector_gr)
    vector_gr=vector_gr.sum(axis=0)
    gradient= (-1/m)*(vector_gr)
    return gradient

def Logistics_Regression(X,y,learningrate, iterations):
    """ Find the Logistics regression model for the data set
         Parameters: X: independent variables matrix y: dependent variables matrix
                     learningrate: learningrate of Gradient Descent
                    iterations: the number of iterations
        Return value: the final theta vector,cross_entropy error and the plot of cost function
    """
   
    y_new = np.reshape(y, (len(y), 1))  
    cost_lst = []
    vectorX = generateXvector(X)
    theta = theta_init(X)
    m = len(X)
    cross_entropy=0
    iteration=0
    index=[]
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    for i in range(iterations):
        gradients = gradient(y_new,vectorX,theta,m)
        index.append(i)
        if(gradients.all()<=0.001):
            print("converged") 
            return theta,cross_entropy
        gradients=np.reshape(gradients,(14,1))
        theta = theta - learningrate * gradients
        y_pred = sigmoid(vectorX.dot(theta))
        cost_value = logloss(y_new,vectorX,theta,m)
        cost_lst.append(cost_value)
        cross_entropy= cost_lst[-1]
    plt.plot(index,cost_lst)
    plt.show()
    
    return theta,cross_entropy

def column(matrix, i):
    """ Returning all the values in a specific columns
         Parameters:X: the input matrix i: the column
         Return value: an array with desired column
    """
    return [row[i] for row in matrix]

def accuracy_LR(X,y,learningrate, iteration,X_test, y_test):
    """ Returning the accuracy score for a training model"""
    ideal,cost_value= Logistics_Regression(X,y,learningrate, iteration)
    hypo_line = ideal[0]
    acc=0
    for i in range(1,len(ideal)):
        hypo_line = hypo_line + ideal[i]*column(X_test,i-1)
    logistic_function = sigmoid(hypo_line)
    for i in range(len(logistic_function)):
        if logistic_function[i] >= 0.5:
            logistic_function[i] = 1
        else:
            logistic_function[i] = -1
    if len(y_test)>0:
      last1 = np.concatenate((logistic_function.reshape(len(logistic_function),1), y_test.reshape(len(y_test),1)),1)
      count = 0
      for i in range(len(y_test)):
        if last1[i][0] == last1[i][1]:
            count = count+1
      acc = count/(len(y_test))
      plt.show()
    return ideal,cost_value,logistic_function,1-acc

""" learning Logistic Regression model using Gradient algorithm 
    parameters : X_train - Independent variables matrix
                 Y_train -  dependent variables matrix
                 X_test - testing data variable matrix
                 Y-test - testing data 
                 learning rate =0.00001
    for 10000 iterations 
"""

w1,cross_entropy1,predict1,classificatn_err1=accuracy_LR(X_train,Y_train, 0.00001, 10000, X_test, Y_test)

""" cross entropy error for each iteration """

"""for 100000 iterations"""
w2,cross_entropy2,predict2,classificatn_err2=accuracy_LR(X_train,Y_train, 0.00001, 100000,X_test, Y_test)

"""for 1000000 iterations"""
w3,cross_entropy3,predict3,classificatn_err3=accuracy_LR(X_train,Y_train, 0.00001, 1000000,X_test, Y_test)

"""displaying returned weight vector, cross entropy error, prediction array , classification error on the training data"""

print("weight vector1",w1,"cross_entropy1",cross_entropy1,"predict1",predict1,"classificatn_err1",classificatn_err1)

print("weight vector2",w2,"cross_entropy2",cross_entropy2,"predict2",predict2,"classificatn_err2",classificatn_err2)

print("weight vector3",w3,"cross_entropy3",cross_entropy3,"predict3",predict3,"classificatn_err3",classificatn_err3)

""" predicting class labels  for the given test file 1644871518_6284828_cleveland-test.csv """
""" for 10000, 100000, 1000000 iterations""""
y=[]
y=np.array(y)
w_test1,cross_entropy_test1,predict_test1,err=accuracy_LR(X_train,Y_train, 0.00001, 10000,X_test_file, y)
#w_test2,cross_entropy_test2,predict_test2,err=accuracy_LR(X_train,Y_train, 0.00001, 100000,X_test_file, y)
#w_test3,cross_entropy_test3,predict_test3,err=accuracy_LR(X_train,Y_train, 0.00001, 1000000,X_test_file, y)

""" writing predicted class labels for each iteration bound """

with open("test2_2.dat", "w") as a_file:
    for i in range(len(predict_test2)):
        a_file.write(str(int(float(predict_test2[i])))) 
        a_file.write('\n')

with open("test1_8.dat", "w") as a_file:
    for i in range(len(predict_test1)):
        a_file.write(str(int(float(predict_test1[i]))))
        a_file.write('\n')

with open("test3_2.dat", "w") as a_file:
    for i in range(len(predict_test3)):
        a_file.write(str(int(float(predict_test3[i]))))
        a_file.write('\n')

""" skLearn implmentation of Logistic Regression model """ 

""" splitting the input training data into train data and test data """

X_train1, X_test1, Y_train1, Y_test1 = train_test_split(X_train , Y_train, test_size = 0.4, random_state = 0)

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train1, Y_train1)

""" displays intercept and the coefficients"""
classifier.intercept_, classifier.coef_

"""predicts and prints the accuracy score for the test data of the input training data """
y_pred = classifier.predict(X_test1)
print(accuracy_score(y_pred,Y_test1))

"""predicts the class labels for the test data of the input testing data """
y_test_pred = classifier.predict(X_test_file)

"""displays the classification error of the training data """
print("classification error",1-0.8378)

""" computes the cross entropy error for the skLearn Logistic regression model """
import array
X_1og=generateXvector(X_train1)
Y_log=Y_train1.reshape(54,1)
theta_log=[]
theta_log_2=[]
theta_log_2=classifier.coef_[0][0:14]
theta_log = np.insert(theta_log_2, 0, classifier.intercept_[0])
theta_log=theta_log.reshape(14,1)
print(Y_log.shape,X_1og.shape,theta_log.shape,theta_log)
print("loss", logloss(Y_log,X_1og,theta_log,m))

"""writing the predicted data of skLearn Logistic regression model into output file """
with open("testlog.dat", "w") as a_file:
    for i in range(len(y_test_pred)):
        a_file.write(str(int(float(y_test_pred[i]))))
        a_file.write('\n')

def column(matrix, i):
    """ Returning all the values in a specific columns
         Parameters:X: the input matrix i: the column
         Return value: an array with desired column
    """
    return [row[i] for row in matrix]

"""feature scaling implementation """
""" computes the difference between traing data and mean ,divided by standard deviation """ 
def normalize(X):
    X1= (X - np.mean(X))/np.std(X)
    return X1

"""Logistic regression model using gradient descent for the scaled features  """
""" terminates the algorithm whenever each term in gradient reaches the given tolerance level - here 10^-6"""
def Logistics_Regression_scale(X,y,learningrate):
    
    y_new = np.reshape(y, (len(y), 1))  
    cost_lst = []
    vectorX = generateXvector(X)
    theta = theta_init(X)
    m = len(X)
    cross_entropy=0
    iterations=0
      
    while True:
        iterations+=1
        gradients = gradient(y_new,vectorX, theta,m)
        print(gradients,iterations)
        theta = theta - learningrate * gradients
        if(gradients.all()<=0.5):
           break;
        y_pred = sigmoid(vectorX.dot(theta))
        cost_value = logloss(y_new,vectorX,theta,m)
        cost_lst.append(cost_value)
        #print(cost_lst,iteration)
        cross_entropy= cost_lst[-1]
    

    return theta,cross_entropy,iterations

X_scale_train=normalize(X_train)
theta,cross_entropy,iterations=Logistics_Regression_scale(X_scale_train,Y_train,0.08)

theta,cross_entropy,iterations=Logistics_Regression_scale(X_scale_train,Y_train,0.0001)

theta,cross_entropy,iterations=Logistics_Regression_scale(X_scale_train,Y_train,0.05)