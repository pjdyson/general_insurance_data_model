# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import datetime as dt


days_in_year = 365.25


def generate_policies(uw_start_date, 
                      insured_limit,
                      insured_excess,
                      policy_premium,
                      n_policies,
                      class_name):
    '''
    generates a set number of policies representing a single origin year
    '''
    
    #generate policy start/end dates (uniformly distributed)
    days_in_year = 365.25
    start_date_offset = list(np.random.uniform(0,days_in_year, n_policies))
    start_date_offset.sort()
    uw_start_date = [uw_start_date + dt.timedelta(days=x) for x in start_date_offset]
    uw_end_date = [x + dt.timedelta(days=days_in_year) for x in uw_start_date]
    
    #Create risk factors (stored as standard normals)
    policy_risk_factors_1 = np.random.normal(size=n_policies)
    policy_risk_factors_2 = np.random.normal(size=n_policies)
    policy_risk_factors_3 = np.random.normal(size=n_policies)
    
    # build the dataframe
    db_policies = pd.DataFrame({'Class_name': class_name,
                                'Policy_ID':range(n_policies), 
                              'Start_date':uw_start_date,
                              'End_date':uw_end_date,
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
    
    #apply limit and excess to claim value
    db_policy_claims['Claim_value'] = db_policy_claims['Claim_value_gu'] - db_policy_claims['Insured_excess']
    db_policy_claims['Claim_value'] = db_policy_claims[['Claim_value','Insured_limit']].min(axis='columns')
    db_policy_claims['Claim_value'] = np.where(db_policy_claims['Claim_value']<0,0,db_policy_claims['Claim_value'])
    db_policy_claims['Claim_value'] = np.where(db_policy_claims['Claim_flag']==0,np.nan,db_policy_claims['Claim_value'])
    
    #set incident days
    db_policy_claims['Claim_incident_days'] = np.where(db_policy_claims['Claim_flag']==1, 
                    np.random.uniform(0,days_in_year),np.nan)
    
    
    #Set Reported days
    mu_reportdays = np.log((delay_reportdays_mean**2.0)/np.sqrt(delay_reportdays_mean**2.+delay_reportdays_sd**2.))
    sigma_reportdays = np.sqrt(np.log((delay_reportdays_sd**2.)/(delay_reportdays_sd**2.)+1))

    db_policy_claims['Claim_report_days'] = np.where(db_policy_claims['Claim_flag']==1, 
                    np.random.lognormal(mean=mu_reportdays, sigma=sigma_reportdays, size=len(db_policy_claims)),np.nan)
    

    #Set Paid days
    mu_paymentdays = np.log((delay_paymentdays_mean**2.0)/np.sqrt(delay_paymentdays_mean**2.+delay_paymentdays_sd**2.))
    sigma_paymentdays = np.sqrt(np.log((delay_paymentdays_sd**2.)/(delay_paymentdays_mean**2.)+1))
    
    db_policy_claims['Claim_payment_days'] = np.where(db_policy_claims['Claim_flag']==1, 
                    np.random.lognormal(mean=mu_paymentdays, sigma=sigma_paymentdays, size=len(db_policy_claims)),np.nan)

    #convert days to dates
    db_policy_claims['Claim_incident_days'] = pd.to_timedelta(db_policy_claims['Claim_incident_days'], unit='days')
    db_policy_claims['Claim_report_days'] = pd.to_timedelta(db_policy_claims['Claim_report_days'], unit='days')
    db_policy_claims['Claim_payment_days'] = pd.to_timedelta(db_policy_claims['Claim_payment_days'], unit='days')

    db_policy_claims['Claim_incident_date'] = db_policy_claims['Start_date'] +     db_policy_claims['Claim_incident_days']
    db_policy_claims['Claim_report_date'] = db_policy_claims['Claim_incident_date'] +     db_policy_claims['Claim_report_days']
    db_policy_claims['Claim_payment_date'] = db_policy_claims['Claim_report_date'] +     db_policy_claims['Claim_payment_days']

    db_policy_claims['End_date'] = np.where(db_policy_claims['Claim_flag']==1, 
                    db_policy_claims['Claim_incident_date'],db_policy_claims['End_date'])
    
    #tidy up the dataframe
    cols_to_drop = ['Claim_flag_rnd',
                    'Claim_flag',
                    'Claim_incident_days',
                    'Claim_report_days',
                    'Claim_payment_days']
    db_policy_claims.drop(cols_to_drop, axis='columns', inplace=True)
    
    return db_policy_claims

def summary_stats(db):
    db['UW_year'] = db['Start_date'].dt.year
    stats = db.groupby('UW_year').agg({
            'Start_date':'count',
            'Policy_premium':np.sum,
            'Claim_value':np.sum
                      })
    stats['Loss_ratio'] = stats['Claim_value']/stats['Policy_premium']
    stats.rename({'Start_date':'Policies_written'}, axis='columns', inplace=True)
    return stats
    
def generate_ultimate_portfolio(
        class_name='Class A',
        insured_limit=3000,
        insured_excess=250,
        policy_premium=150,
        n_policies=1000,
        uw_start_date=dt.datetime.strptime('01/01/2019', '%d/%m/%Y'),
        historic_years=10,
        historic_policy_growth=0.03,
        frequency=0.15, 
        severity_mean_gu=1000,
        severity_sd_gu=500,
        delay_reportdays_mean=10,
        delay_reportdays_sd=10,
        delay_paymentdays_mean=40,
        delay_paymentdays_sd=10):

    db_policy = []
    
    for year_offset in range(0,historic_years):
        uw_start_date = uw_start_date - dt.timedelta(days=days_in_year)
            # offsets start date back 365.25 days. This is not quite correct (due to leap years)
        temp_policy = generate_policies(class_name=class_name,
                                        insured_limit=insured_limit,
                                        insured_excess=insured_excess,
                                        policy_premium=policy_premium,
                                        n_policies=n_policies,
                                        uw_start_date=uw_start_date)
        
        temp_policy = generate_claims(db_policies=temp_policy,
                                             frequency=frequency, 
                                             severity_mean_gu=severity_mean_gu,
                                             severity_sd_gu=severity_sd_gu,
                                             delay_reportdays_mean=delay_reportdays_mean,
                                             delay_reportdays_sd=delay_reportdays_sd,
                                             delay_paymentdays_mean=delay_paymentdays_mean,
                                             delay_paymentdays_sd=delay_paymentdays_sd,
                                             )
        
        db_policy.append(temp_policy)

        # scale down policy number with growth rate
        n_policies = int(n_policies * (1-historic_policy_growth))

    db_policy = pd.concat(db_policy)
    
    stats = summary_stats(db_policy)
    
    return db_policy, stats

# run code to test
if __name__ == '__main__':
    uw_start_date = dt.datetime.strptime('01/01/2019', '%d/%m/%Y')
    data, stats = generate_ultimate_portfolio()

