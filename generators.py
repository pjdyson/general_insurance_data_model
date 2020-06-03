# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import datetime as dt


def generate_policy(n_policies=1000, start_date):
    '''
    generates a set number of policies representing a single origin year
    '''
    db_policy = pd.DataFrame({'Policy_ID':range(n_policies)})
    db_policy.set_index('Policy_ID', inplace=True)
    
    #Set policy start date (uniform dist of days from start date)
        # no seasonality
        
    #Create risk factors (stored as standard normals)
    
    #Insured value (Average?)
    
    return db_policy 

def generate_claim(db_policy):
    #nothing
    
    #Ultimate Claim Flag
    
    #Set value (% of insured value, normal dist?)
    
    #Set Reported Date
    
    #Set Paid Date
    
    x=None
    


db_policy = generate_policy(1000)
db_policy
