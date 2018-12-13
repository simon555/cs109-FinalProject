# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from pandas.api.types import CategoricalDtype
from sklearn.model_selection import train_test_split
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_rows', 500)
plt.style.use('seaborn')
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader

from torch.nn.modules import Module
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from numpy import genfromtxt
from time import time
from copy import deepcopy

from tqdm import tqdm_notebook



device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print('device used : ', device)


X_train = genfromtxt('../../data/ready/X_train.csv', delimiter=',')
X_test = genfromtxt('../../data/ready/X_test.csv', delimiter=',')
X_val = genfromtxt('../../data/ready/X_val.csv', delimiter=',')
protected_train = pd.read_csv('../../data/ready/protected_train.csv')




y_train = genfromtxt('../../data/ready/y_train.csv', delimiter=',')
y_test = genfromtxt('../../data/ready/y_test.csv', delimiter=',')
y_val = genfromtxt('../../data/ready/y_val.csv', delimiter=',')
protected_val = pd.read_csv('../../data/ready/protected_val.csv', delimiter=',')



class Data(Dataset):
    def __init__(self, X_train, y_train, classes):
        self.x = Variable(torch.from_numpy(X_train)).float()
        self.y = Variable(torch.from_numpy(y_train)).float()
        self.classes = torch.Tensor(list(classes.values == 1))==True
        self.len = self.x.shape[0]
    def __getitem__(self,index):    
        return self.x[index], self.y[index], self.classes[index]
    def __len__(self):
        return self.len
    
    
    
    
class LinearRegressionPytorch(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.linear = nn.Linear(input_size, 1)
        self.cuda_ready = torch.cuda.is_available()
        
        if self.cuda_ready:
            self.cuda()
    
    def forward(self, x, device=device):
        out = self.linear(x)
        return out
    
    
    
class FairMSE(Module):
    def __init__(self, alpha_fairness, L1=False, L2=False, device=device):
        super().__init__()
        self.alpha_fairness = alpha_fairness
        self.mse = nn.MSELoss(reduction='elementwise_mean')
        self.L1=L1
        self.L2=L2
        self.device=device

        if torch.cuda.is_available():
            self.cuda()
    
    def compute_L1(self, named_params):
        l1_loss = Variable(torch.FloatTensor(1), requires_grad=True).to(self.device)
        for name, param in named_params:
           if 'bias' not in name:
               l1_loss =l1_loss +  torch.sum(torch.abs(param))
        return(l1_loss)
        
    
    def forward(self, outputs, labels, classes, named_params=[], device=device):
       
        regularizer = 0
        
        if 1 in classes:         
            protected_outputs = outputs[classes]
            protected_labels = labels[classes]
            total_mse = self.mse(outputs, labels)
            protected_mse = self.mse(protected_outputs, protected_labels)
            
            
            if self.L1:
                regularizer = regularizer + self.compute_L1(named_params)
            
            return total_mse + self.alpha_fairness*(protected_mse - total_mse)**2 + regularizer, total_mse, protected_mse
        else:
            total_mse = self.mse(outputs, labels)
            return total_mse + regularizer, total_mse, None
        
    
        
class MLP(nn.Module):
    def __init__(self, input_dim):
        super(MLP, self).__init__()
        self.hidden = nn.Linear(input_dim, 20)
        self.hidden1 = nn.Linear(20, 10)
        self.hidden2 = nn.Linear(10, 5)
        self.out   = nn.Linear(5, 1)
        
        self.cuda_ready=torch.cuda.is_available()
    
        if self.cuda_ready:
            self.cuda()

    def forward(self, x, device=device):
        x = F.relu(self.hidden(x))
        x = F.relu(self.hidden1(x))
        x = F.relu(self.hidden2(x))
        x = self.out(x)
        return x

def fit_model(X_train, y_train, protected_class, X_val, y_val, protected_class_val, model, 
              alpha = 0,
              batch_size = 32, 
              lr = 0.001, 
              epochs = 50,
             device=device,
             L1=False,
             L2=False):
    criterion = FairMSE(alpha,L1=L1, L2=L2)
    optimiser = torch.optim.Adam(model.parameters(), lr) #Stochastic Gradient Descent
    
    inputs_all = Variable(torch.from_numpy(X_train)).float().to(device)
    labels_all = Variable(torch.from_numpy(y_train)).float().view(y_train.shape[0],1).to(device)
    classes_all = torch.Tensor(list(protected_class.values == 1))==True
    classes_all = classes_all.view(classes_all.shape[0],1)
    
    inputs_all_val = Variable(torch.from_numpy(X_val)).float().to(device)
    labels_all_val = Variable(torch.from_numpy(y_val)).float().view(y_val.shape[0],1).to(device)
    classes_all_val = torch.Tensor(list(protected_class_val.values == 1))==True
    classes_all_val =  classes_all_val.view(classes_all_val.shape[0],1)
    
    dataset=Data(X_train, y_train, protected_class)
    trainloader=DataLoader(dataset = dataset, batch_size = batch_size)
    
    number_of_batch = X_train.shape[0]//batch_size
    
    loss_hist = []
    total_mse_hist = []
    fairness_hist = []
    
    val_loss_hist = []
    val_total_mse_hist = []
    val_fairness_hist = []
    
    
    tmp_best_model = None
    best_loss_val = 1000
    #print('start of the training')
    
    
    
    for epoch in range(epochs):
        t1=time()
        for x, y, classes in tqdm_notebook(trainloader):
            x=x.to(device)
            y=y.view(y.shape[0],1).to(device)
            optimiser.zero_grad()
            outputs = model.forward(x)
            loss, total_mse, protected_mse = criterion(outputs, y, classes, model.named_parameters())
            
            
            
            loss.backward()# back props
            optimiser.step()# update the parameters
        
        
        outputs_all = model.forward(inputs_all)        
        loss, total_mse, protected_mse = criterion(outputs_all, labels_all, classes_all)
        
        
        
        loss_hist.append(loss)
        total_mse_hist.append(total_mse)
        fairness_hist.append((total_mse-protected_mse)**2)

        #print('TRAINING')
        #print("epoch: {}, Total MSE: {}, Fairness: {}, loss: {}".format(epoch, total_mse, alpha*(protected_mse-total_mse)**2, loss))
        
        
        outputs_all_val = model.forward(inputs_all_val)
        loss_val, total_mse_val, protected_mse_val = criterion(outputs_all_val, labels_all_val, classes_all_val)
        
        val_loss_hist.append(loss_val)
        val_total_mse_hist.append(total_mse_val)
        val_fairness_hist.append((total_mse_val-protected_mse_val)**2)
       
        if loss_val < best_loss_val:
            #print('New best model!')           
            tmp_best_model = deepcopy(model)
            
            best_loss_val = loss_val

            best_train={'loss': loss, 'total_mse':total_mse, 'protected_mse': protected_mse}
            best_val={'loss':loss_val, 'total_mse':total_mse_val, 'protected_mse': protected_mse_val}        
        
    t2=time()
    print('full run ', t2-t1)
    return (tmp_best_model, 
        best_train, 
        best_val, 
        (loss_hist, total_mse_hist, fairness_hist), 
        (val_loss_hist, val_total_mse_hist, val_fairness_hist))
    
    
models = [LinearRegressionPytorch(X_train.shape[1]), MLP(X_train.shape[1])]
alphas = [0,5,10,15,20]




fit_linear_L2 = []
fairness_linear_L2 = []
fit_MLP_L2 = []
fairness_MLP_L2 = []

for model_type, model in enumerate(models):
    for alpha in alphas:
        print('')
        print('training of model ', model._get_name())
        
        print('alpha : ', alpha)
        tmp_best_model, best_train, best_val, train_hist, val_hist =  fit_model(X_train, y_train, protected_train['Hispanic'],
                                                                                X_val, y_val, protected_val['Hispanic'], 
                                                                                model = model,
                                                                                alpha = alpha,
                                                                                epochs = 50,
                                                                               L2=1)
        
        fairness = (best_val['total_mse']-best_val['protected_mse'])**2
        fairness = fairness.detach().numpy()
        
        if model_type == 0:
            fit_linear_L2.append(tmp_best_model)
            fairness_linear_L2.append(fairness)
        else:
            fit_MLP_L2.append(tmp_best_model)
            fairness_MLP_L2.append(fairness)
            

