# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import datetime as dt


def generate_policies(start_date, insured_amount, n_policies=1000):
    '''
    generates a set number of policies representing a single origin year
    '''
    
    #generate policy start/end dates (uniformly distributed)
    days_in_year = 365.25
    start_date_offset = list(np.random.uniform(0,days_in_year, n_policies))
    start_date_offset.sort()
    start_date = [start_date + dt.timedelta(days=x) for x in start_date_offset]
    end_date = [x + dt.timedelta(days=days_in_year) for x in start_date]
    
    #Create risk factors (stored as standard normals)
    policy_risk_factors_1 = np.random.normal(size=n_policies)
    policy_risk_factors_2= np.random.normal(size=n_policies)
    policy_risk_factors_3= np.random.normal(size=n_policies)
    
    # build the dataframe
    db_policies = pd.DataFrame({'Policy_ID':range(n_policies), 
                              'Start_date':start_date,
                              'End_date':end_date,
                              'Policy_risk_factor_1':policy_risk_factors_1,
                              'Policy_risk_factor_2':policy_risk_factors_2,
                              'Policy_risk_factor_3':policy_risk_factors_3,
                              'Insured_amount':insured_amount})
    db_policies.set_index('Policy_ID', inplace=True)
    
    return db_policies 

def generate_claims(db_policy):
    
    db_policy_claims = db_policy.copy()
    
    #Ultimate Claim Flag
    
    #Set value (% of insured value, normal dist?)
    
    #Set Reported Date
    
    #Set Paid Date
    
    return db_policy_claims
    

start_date = dt.datetime.strptime('01/01/2019', '%d/%m/%Y')

db_policies = generate_policies(insured_amount=1000,
                              n_policies=1000,
                              start_date=start_date)
db_policies_claims = generate_claims(db_policies)
db_policies_claims.head()
