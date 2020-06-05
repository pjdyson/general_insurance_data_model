# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import datetime as dt


days_in_year = 365.25


def generate_policies(start_date, 
                      insured_limit,
                      insured_excess,
                      policy_premium,
                      n_policies=1000):
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
                              'Policy_premium': policy_premium,
                              'Policy_risk_factor_1':policy_risk_factors_1,
                              'Policy_risk_factor_2':policy_risk_factors_2,
                              'Policy_risk_factor_3':policy_risk_factors_3,
                              'Insured_limit':insured_limit,
                              'Insured_excess':insured_excess})
    db_policies.set_index('Policy_ID', inplace=True)
    
    return db_policies 

def generate_claims(db_policies, 
                    frequency, 
                    severity_mean_gu, 
                    severity_sd_gu,
                    delay_reportdays_mean,
                    delay_reportdays_sd,
                    delay_paymentdays_mean,
                    delay_paymentdays_sd):
    
    db_policy_claims = db_policies.copy()
    n_policies=len(db_policy_claims)
    
    #Ultimate Claim Flag
    db_policy_claims['Claim_flag_rnd'] = np.random.uniform(0,1,n_policies)
    db_policy_claims['Claim_flag'] =0
    db_policy_claims['Claim_flag'] = db_policy_claims['Claim_flag'].where(db_policy_claims['Claim_flag_rnd']>frequency,1)
    
    #Set claim value (ground up)
    db_policy_claims['Claim_value_gu'] = np.nan
    db_policy_claims['Claim_incident_days'] = np.nan
    db_policy_claims['Claim_report_days'] = np.nan
    db_policy_claims['Claim_payment_days'] = np.nan
    mu_cvalue = np.log((severity_mean_gu**2.0)/np.sqrt(severity_mean_gu**2.+severity_sd_gu**2.))
    sigma_cvalue = np.sqrt(np.log((severity_sd_gu**2.)/(severity_mean_gu**2.)+1))

    db_policy_claims['Claim_value_gu'] = np.where(db_policy_claims['Claim_flag']==1, 
                    np.random.lognormal(mean=mu_cvalue, sigma=sigma_cvalue, size=len(db_policy_claims)),np.nan)
    
    #set incident date
    db_policy_claims['Claim_incident_days'] = np.where(db_policy_claims['Claim_flag']==1, 
                    np.random.uniform(0,days_in_year),np.nan)
    
    
    #Set Reported Date
    mu_reportdays = np.log((delay_reportdays_mean**2.0)/np.sqrt(delay_reportdays_mean**2.+delay_reportdays_sd**2.))
    sigma_reportdays = np.sqrt(np.log((delay_reportdays_sd**2.)/(delay_reportdays_sd**2.)+1))

    db_policy_claims['Claim_report_days'] = np.where(db_policy_claims['Claim_flag']==1, 
                    np.random.lognormal(mean=mu_reportdays, sigma=sigma_reportdays, size=len(db_policy_claims)),np.nan)
    

    #Set Paid Date
    mu_paymentdays = np.log((delay_paymentdays_mean**2.0)/np.sqrt(delay_paymentdays_mean**2.+delay_paymentdays_sd**2.))
    sigma_paymentdays = np.sqrt(np.log((delay_paymentdays_sd**2.)/(delay_paymentdays_mean**2.)+1))
    
    db_policy_claims['Claim_payment_days'] = np.where(db_policy_claims['Claim_flag']==1, 
                    np.random.lognormal(mean=mu_paymentdays, sigma=sigma_paymentdays, size=len(db_policy_claims)),np.nan)


    cols_to_drop = ['Claim_flag_rnd']
    db_policy_claims.drop(cols_to_drop, axis='columns', inplace=True)
    
    
    return db_policy_claims
    

# run code to test

start_date = dt.datetime.strptime('01/01/2019', '%d/%m/%Y')

db_policies = generate_policies(insured_limit=1000,
                                insured_excess=250,
                                policy_premium=150,
                              n_policies=1000,
                              start_date=start_date)
db_policies_claims = generate_claims(db_policies=db_policies,
                                     frequency=0.1, 
                                     severity_mean_gu=300,
                                     severity_sd_gu=500,
                                     delay_reportdays_mean=10,
                                     delay_reportdays_sd=10,
                                     delay_paymentdays_mean=40,
                                     delay_paymentdays_sd=10,
                                     )
db_policies_claims.head()
