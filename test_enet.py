#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing function

Created on Sun Dec  9 21:30:22 2018

@author: peter
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import ElasticNetCV
import pandas as pd
import pickle


def main():
    # prelims
    N_cycles = np.array([20,30,40,50,60,70,80,90,100])
    rmse = np.zeros(N_cycles.shape)
    use_log_cycle_life = True
    use_all_features = False
    which_features = [2,3,4,21,22,24,25,39,40,48,49,63,65]
    
    # load all models
    models = pickle.load(open("enet_trainedmodels.p", "rb" ))
    
    # loop through enets and make predictions
    for i in np.arange(len(N_cycles)):
        print('Starting N_cycles = ' + str(int(N_cycles[i])))
        
        file_name = "testing/cycles_2TO" + str(int(N_cycles[i])) + "_log.csv"
        features, cycle_lives, feature_names = load_dataset(file_name, False, use_all_features, which_features)
        
        # set enet model
        enet = models[i]
        
        # predictions
        if use_log_cycle_life:
            predicted_cycle_lives = 10**enet.predict(features)
        else:
            predicted_cycle_lives = enet.predict(features)
        
        plt.plot(cycle_lives,predicted_cycle_lives,'o')
        plt.plot([0,1400],[0,1400],'r-')
        plt.ylabel('Predicted cycle life')
        plt.xlabel('Observed cycle life')
        #plt.axis('equal')
        plt.axis([0, 1400, 0, 1400])
        plt.show()
        
        residuals = predicted_cycle_lives - cycle_lives
        rmse[i] = np.sqrt(((residuals) ** 2).mean())
        
        print('RMSE:')
        print(rmse[i])
        print('=======================================')
        
    
    # plot rmse vs cycle number
    plt.plot(N_cycles, rmse, '-o')
    plt.ylabel('testing RMSE error')
    plt.xlabel('cycle number')
    plt.show()

def load_dataset(csv_path, add_intercept=True, use_all_features=True, which_features=[2]):
    """Load dataset from a CSV file.

    Args:
         csv_path: Path to CSV file containing dataset.
         add_intercept: Add an intercept entry to x-values.

    Returns:
        xs: Numpy array of x-values (features).
        ys: Numpy array of y-values (labels).
        headers: list of headers
    """
    
    # Load headers
    with open(csv_path, 'r') as csv_fh:
        headers = csv_fh.readline().strip().split(',')

    # Load features and labels
    # x_cols = [i for i in range(len(headers)) if headers[i] == 'cycle_lives']
    # l_cols = [i for i in range(len(headers)) if headers[i] == label_col]
    if use_all_features:
        features = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=range(2, len(headers)))
    else:
        features = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=which_features)
    cycle_lives = np.loadtxt(csv_path, delimiter=',', skiprows=1, usecols=[1])
    feature_names = headers[2:len(headers)]

    m = features.shape[0]
    if add_intercept:
        features = np.concatenate((np.ones([m, 1]), features),axis=1)
        feature_names = ['intercept'] + feature_names

    return features, cycle_lives, feature_names


if __name__ == "__main__":
    main()