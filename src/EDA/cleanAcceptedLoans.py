# -*- coding: utf-8 -*-


# =============================================================================
# Basic imports
# =============================================================================

import pandas as pd
from collections import Counter
from pandas.api.types import CategoricalDtype


# =============================================================================
# GENERAL VARIABLES
# =============================================================================
INPUTFILE='../../data/smallData/rawData/AcceptedLoans.csv'
OUTPUTFILE = '../../data/tmp/Simon/AcceptedLoans.csv'


def clean(filename):
    
# =============================================================================
#     load data
# =============================================================================
    data=pd.read_csv(filename)
    
    
    #clean id
    data=data.drop('id', axis=1)
    
    #clean term
        
    t = CategoricalDtype(categories=[" 36 months", " 60 months"], ordered=True)
    te=  data.term.astype(t)
    data['term']=te.cat.codes    


    #clean rate
    def convertIntRate(s):
        """
        input : string of int_rate
        output : float between 0 and 100 corresponding to the interest rate
        """
        without_percent = s[:-1]
        number =float(without_percent)
        return(number)


    data['int_rate']= data['int_rate'].apply(convertIntRate)
        
        
    #clean grade    
    dummies = pd.get_dummies(data['grade'], prefix='grade')
    data=pd.concat([data, dummies], axis=1)
    data=data.drop('grade', axis=1)
    
    #clean sub_grade    
    def embed_subGrade(df):
        col, val = df['sub_grade'][0], int(df['sub_grade'][1])
        df['grade_'+col]=val
        return(df)
        
    data = data.apply(embed_subGrade, axis=1)
    data=data.drop('sub_grade', axis=1)
    
    #cleaning title
    data=data.drop('emp_title', axis=1)

    #clean emp_lenght        
    length_to_int = dict()
    length_to_int['< 1 year']=0
    length_to_int['1 year']=1
    length_to_int['2 years']=2
    length_to_int['3 years']=3
    length_to_int['4 years']=4
    length_to_int['5 years']=5
    length_to_int['6 years']=6
    length_to_int['7 years']=7
    length_to_int['8 years']=8
    length_to_int['9 years']=9
    length_to_int['10+ years']=10
    
    emp_length_missing = data['emp_length'].isnull()

    def embed_emp_length(s):
        """
        convert the string emp_length into an integer
        does not change the NaN input
        """
        try:
            return(length_to_int[s])
        except:
            pass
    
    data['emp_length']= data['emp_length'].apply(embed_emp_length)


    #clean home ownership    
    dum = pd.get_dummies(data['home_ownership'], prefix='HOME')
    data=pd.concat([data, dum], axis=1)
    
    data = data.drop('home_ownership', axis=1)
    
    # remove the HOME_NONE attribute
    data = data[data['HOME_NONE']==0]
    
    data=data.drop('HOME_NONE', axis=1) #only 3 points
    data=data.drop('HOME_RENT', axis=1) #to avoid colinearity


    #clean verification_status
    dum = pd.get_dummies(data['verification_status'], prefix='Income')    
    data=pd.concat([data, dum], axis=1)    
    data=data.drop('Income_Not Verified', axis=1) #to avoid colinearity
    data=data.drop('verification_status', axis=1) 
    
                
    #clean issue_d
    data = data.drop('issue_d', axis=1)

    
    #clean loan_status    
    categories_loan_status = list(Counter(data['loan_status']).keys())   
    t = CategoricalDtype(categories=categories_loan_status, ordered=True)
    te=  data['loan_status'].astype(t)
    data['loan_status']=te.cat.codes
    
    
    #clean payment_plann
    data = data.drop('pymnt_plan', axis=1)


    #clean desc
    data = data.drop('desc', axis=1)

    
    #clean purpose
    dum = pd.get_dummies(data['purpose'] , prefix= 'purpose')
    dum = dum.drop('purpose_debt_consolidation', axis=1) #to avoid colinearity
    data=pd.concat([data, dum], axis=1)
    categories_purpose = list(Counter(dum).keys())
    data=data.drop('purpose', axis=1)



    #clean title
    data = data.drop('title', axis=1)

    
    #clean zip_code    
    categories_zip_code =  list(Counter(data['zip_code']).keys())
    t = CategoricalDtype(categories=categories_zip_code, ordered=True)
    te=  data['zip_code'].astype(t)
    data['zip_code']=te.cat.codes


    #clean addr_state
    categories_addr_state=list(Counter(data['addr_state']).keys())
    t = CategoricalDtype(categories=categories_addr_state, ordered=True)
    te=  data['addr_state'].astype(t)
    data['addr_state']=te.cat.codes
    
    
    #clean earliest_cr_line
    data = data.drop('earliest_cr_line', axis=1)


    #clean revol_util
    def convert_Revol2Float(s):
        try:
            return(float(s[:-1]))
        except:
            return(s)

    data['revol_util']=data['revol_util'].apply(convert_Revol2Float)
    revol_util_missing = data['revol_util'].isna()
    


    #clean initial_list_status
    def convert_initial_list_status(s):
        if s=='f':
            return(0)
        elif s=='w':
            return(1)
        else:
            return(s)
    
    data['initial_list_status'] = data['initial_list_status'].apply(convert_initial_list_status)


    #clean last_pyment_date
    data = data.drop('last_pymnt_d', axis=1)
    
    #clean last_credit_pull_d
    data = data.drop('last_credit_pull_d', axis=1)
    
    
    #clean application_type
    def convert_application_type(s):
        if s=='Individual':
            return(0)
        elif s=='Joint App':
            return(1)
        else:
            return(s)
        
    data['application_type'] = data['application_type'].apply(convert_application_type)
    


    #clean verification_status_joint    
    dum = pd.get_dummies(data['verification_status_joint'], prefix='jointIncome')    
    dum = dum.drop('jointIncome_Not Verified', axis=1)   
    data=pd.concat([data, dum], axis=1)
    

    #clean sec_app_earliest_cr_line
    data=data.drop('sec_app_earliest_cr_line', axis=1)
    
    
    #clean hardship_flag
    data= data.drop('hardship_flag', axis=1)
    
    #clean hardship_type
    data= data.drop('hardship_type', axis=1)


    #clean hardship_reason
    data= data.drop('hardship_reason', axis=1)


    #clean hardship_status
    data= data.drop('hardship_status', axis=1)

    #clean hardship_start_date
    data= data.drop('hardship_start_date', axis=1)


    #clean hardship_end_date
    data= data.drop('hardship_end_date', axis=1)
    
    #clean payment_plan_start_date 
    data= data.drop('payment_plan_start_date', axis=1)
    
    #clean hardship_loan_status
    data= data.drop('hardship_loan_status', axis=1)


    #clean disbursement_method
    def convert_disbursement_method(s):
        if s == 'Cash':
            return(0)
        elif s=='DirectPay':
            return(1)
        else:
            return(s)
            
    data['disbursement_method'] = data['disbursement_method'].apply(convert_disbursement_method)


    #convert debt_settlement_flag    
    def convert_debt_settlement_flag(s):
        if s == 'N':
            return(0)
        elif s=='Y':
            return(1)
        else:
            return(s)
    

    data['debt_settlement_flag']=data['debt_settlement_flag'].apply(convert_debt_settlement_flag)


    #clean debt_settlement_flag_date
    data=data.drop('debt_settlement_flag_date',axis=1)
    
    #clean settlement_status
    dum = pd.get_dummies(data['settlement_status'], prefix='settlement_status')       
    dum=dum.drop('settlement_status_COMPLETE', axis=1)   
    data=pd.concat([data, dum], axis=1)
    
    #clean settlement_date
    data=data.drop('settlement_date', axis=1)
    
    
    #clean next_pymnt_d
    data=data.drop('next_pymnt_d', axis=1)
    
    #clean verification_status_joint
    data=data.drop('verification_status_joint', axis=1)
    
    #clean settlement_status
    data=data.drop('settlement_status', axis=1)
    
    
    
    return(data)




