# -*- coding: utf-8 -*-
"""PyTorchMNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Gr6bpx-j3P0t4P23LpyBHOCxcx_DvGCw
"""

import torch
import torchvision
from torchvision import transforms,datasets

train = datasets.MNIST('',train=True,download=True,transform=transforms.Compose([transforms.ToTensor()]))
test = datasets.MNIST('',train=False,download=True,transform=transforms.Compose([transforms.ToTensor()]))

trainset = torch.utils.data.DataLoader(train,batch_size=128,shuffle=True)
testset = torch.utils.data.DataLoader(test,batch_size=128,shuffle=False)

import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
  def __init__(self):
    super().__init__()
    self.fc1 = nn.Linear(28*28,64)
    self.fc2 = nn.Linear(64,64)
    self.fc3 = nn.Linear(64,64)
    self.fc4 = nn.Linear(64,10)

  def forward(self,x):
      x = F.relu(self.fc1(x))
      x = F.relu(self.fc2(x))
      x = F.relu(self.fc3(x))
      x = self.fc4(x)
      return F.log_softmax(x,dim=1)

net = Net()
print(net)

import torch.optim as optim
loss_function = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(),lr=0.001)

loss_plot = []
for epoch in range(8):
  for data in trainset:
    X,y = data
    output = net(X.view(-1,784))
    loss = loss_function(output,y)
    loss_plot.append(loss.item())

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
  print(loss)

with torch.no_grad():
    n_correct = 0
    n_samples = 0
    for X, y in trainset:
      X = X.reshape(-1, 28*28)
      outputs = net(X)

      _,predictions = torch.max(outputs, 1) #torch.max function will return the value and the index and we are interested in the actual index
      n_samples += y.shape[0]
      n_correct += (predictions == y).sum().item()
  
    acc = 100* n_correct / n_samples
    print(f'Training accuracy = {acc:.4f}')

from matplotlib import pyplot as plt
plt.plot(loss_plot)

correct = 0
total = 0

with torch.no_grad():
  for data in testset:
    X,y = data 
    output = net(X.view(-1,784))
    for idx, i in enumerate(output):
      if torch.argmax(i) == y[idx]:
        correct += 1
      total += 1
print("Accuracy: ", round(correct/total,4))
