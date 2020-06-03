# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np


def generate_policy(n_policies=1000):
    '''
    generates a set number of policies representing a single origin year
    '''
    db_policy = pd.DataFrame({'Policy_ID':range(n_policies)})
    db_policy.set_index('Policy_ID', inplace=True)
    return db_policy 

def generate_claim(db_policy):
    #nothing
    
    #Ultimate Claim Flag
    
    #Set value
    
    #Set Reported Date
    
    #Set Paid Date
    
    x=None
    


db_policy = generate_policy(1000)
db_policy
