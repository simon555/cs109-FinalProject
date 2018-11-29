# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 21:56:22 2018

@author: simon
"""

from src.EDA.clean_object import cleanObject
from src.EDA.clean_numeric import cleanNumeric
import pandas as pd


def cleanForDemo(filename):
    """
    input : location of the file
    output : fully cleaned dataset
    
    
    
    the for demo means that for now we will only have 2 labels in loan_status, payed or not payed (yet)
    """
    
    data = pd.read_csv(filename)
    data=cleanObject(data)
    data=cleanNumeric(data)
    data=data.dropna()

    
    
    not_payed_indexes = [1,2,3,5]
    payed = [0]
    
    
    def adapt_loan_status(label):
        if label in not_payed_indexes:
            return(0)
        elif label in payed:
            return(1)
        else:
            return(label)
    
    data['loan_status'] = data['loan_status'].apply(adapt_loan_status)#    
    data = data[data['loan_status']!=4]
    
    return(data)
    


if __name__=='__main__':
    INPUTFILE='../../data/smallData/rawData/AcceptedLoans.csv'
    OUTPUTFILE = '../../data/tmp/demoClean.csv'
    data=cleanForDemo(INPUTFILE)