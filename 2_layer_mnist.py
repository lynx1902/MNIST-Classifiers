# -*- coding: utf-8 -*-
"""2-Layer MNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sofyzi_3pLO_ZAmgesinEPVIeRUnZeds
"""

pip install idx2numpy

# Commented out IPython magic to ensure Python compatibility.
import gzip
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from scipy.special import softmax
import idx2numpy

# %matplotlib inline

train_x = gzip.open('/content/train-images-idx3-ubyte.gz','r')
train_y = gzip.open('/content/train-labels-idx1-ubyte.gz','r')
test_x = gzip.open('/content/t10k-images-idx3-ubyte.gz','r')
test_y = gzip.open('/content/t10k-labels-idx1-ubyte.gz','r')

trainset_x_orig = idx2numpy.convert_from_file(train_x)
trainset_y_orig = idx2numpy.convert_from_file(train_y)
testset_x_orig = idx2numpy.convert_from_file(test_x)
testset_y_orig = idx2numpy.convert_from_file(test_y)

trainset_x = trainset_x_orig.reshape(trainset_x_orig.shape[0],-1).T
trainset_y = trainset_y_orig.reshape(trainset_y_orig.shape[0],-1).T 
testset_x = testset_x_orig.reshape(testset_x_orig.shape[0],-1).T 
testset_y = testset_y_orig.reshape(testset_y_orig.shape[0],-1).T

trainset_x = trainset_x/255
testset_x = testset_x/255

layers_dims = [784,64,10]

ohe = OneHotEncoder(sparse=False)
trainset_y_ohe = ohe.fit_transform(trainset_y.T)
trainset_y_ohe = trainset_y_ohe.astype(np.uint8)
trainset_y_ohe = trainset_y_ohe.T

testset_y_ohe = ohe.fit_transform(testset_y.T)
testset_y_ohe = testset_y_ohe.astype(np.uint8)
testset_y_ohe = testset_y_ohe.T

def softmax_activation(Z):
    #A = np.exp(Z-np.max(Z))/np.sum(np.exp(Z-np.max(Z)))
    S = (Z-np.max(Z))
    X = np.exp(S)
    sum = np.sum(X)
    A = X/sum
    return A

def relu_activation(Z):
    A = np.maximum(0,Z)
    return A

def relu_backward(Z):
    return Z>0

def initialize_wb(layers_dims):
    W1 = np.random.rand(layers_dims[1],layers_dims[0])*0.001
    b1 = np.zeros((layers_dims[1],1))
    W2 = np.random.rand(layers_dims[2],layers_dims[1])*0.001
    b2 = np.zeros((layers_dims[2],1))
    
    params = {"W1":W1,
             "b1":b1,
             "W2":W2,
             "b2":b2}
    
    return params

def forward_prop(W1,b1,W2,b2,A0):
    
    Z1 = np.dot(W1,A0) + b1
    A1 = relu_activation(Z1)
    Z2 = np.dot(W2,A1) + b2
    A2 = softmax_activation(Z2)
    
    for_prop ={"Z1":Z1,
               "A1":A1,
               "Z2":Z2,
               "A2":A2}
    
    return for_prop

def cost_function(A,Y):
    eps = 1e-1
    m = Y.shape[1]
    # logprods = np.dot(Y, np.log(A+eps).T) 
    # cost = -1/m*np.sum(logprods)
    l=-1*(Y*(np.log(A+eps)))
    L=np.sum(l,axis=0)
    cost=np.sum(L)
    cost/=m

    
    cost = np.squeeze(cost)
    
    return cost

def backward_prop(W1,Z1,A1,W2,Z2,A2,A0,Y):
    m = Y.shape[1]
    dZ2 = A2 - Y
    dW2 = 1/m * np.dot(dZ2,A1.T)
    db2 = 1/m * np.sum(dZ2,axis=1,keepdims=True)
    dZ1 = np.dot(W2.T,dZ2) * relu_backward(Z1)
    dW1 = 1/m * np.dot(dZ1,A0.T)
    db1 = 1/m * np.sum(dZ1,axis=1,keepdims=True)
    
    grads = {"dW1":dW1,
             "db1":db1,
             "dW2":dW2,
             "db2":db2}
    return grads

def update_wb(dW1,db1,dW2,db2,W1,W2,b1,b2,learning_rate):
    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2
    
    params = {"W1":W1,
              "b1":b1,
              "W2":W2,
              "b2":b2}
    
    return params

def predict(A):
    return np.argmax(A,axis=0)

def accuracy(prediction,Y):
    
    return np.sum(prediction==Y)/Y.size

def gradient_descent(X,Y,layers_dims,iterations,learning_rate):
    costs=[]
    params = initialize_wb(layers_dims)
    for i in range(iterations):
        for_prop = forward_prop(params["W1"],params["b1"],params["W2"],params["b2"],trainset_x)
        cost = cost_function(for_prop["A2"],trainset_y_ohe)
        grads = backward_prop(params["W1"],for_prop["Z1"],for_prop["A1"],params["W2"],for_prop["Z2"],for_prop["A2"],trainset_x,trainset_y_ohe)
        params = update_wb(grads["dW1"],grads["db1"],grads["dW2"],grads["db2"],params["W1"],params["W2"],params["b1"],params["b2"],learning_rate)
        
        if (i%10==0):
            print("Cost after iteration {}: {}".format(i,cost))
            costs.append(cost)
            prediction = predict(for_prop["A2"])
            
            print("Accuracy: "+str(accuracy(prediction,trainset_y_ohe)))
    
    plt.plot(np.squeeze(costs))
    plt.ylabel('cost')
    plt.xlabel('iterations (per tens)')
    plt.title("Learning rate =" + str(learning_rate))
    plt.show()
    
    
    return params

params = gradient_descent(trainset_x,trainset_y_ohe,layers_dims,410,0.005)

for_prop = forward_prop(params["W1"],params["b1"],params["W2"],params["b2"],testset_x)
prediction = predict(for_prop["A2"])
print("Accuracy: "+str(accuracy(prediction,testset_y_ohe)))