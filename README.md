# general_insurance_data_model
Module to generate artificial data to test reserving engines

## Overview
The intention of this module is to allow the generation of a simple set of data which represents a set of insurance policies. The data generated can then be used to share demonstrations of new actuarial processes, models and software.
While there is really no substitute for real data, this is often commercially sensitive, so this may be the next best thing to help share ideas and solutions within the community.

## Policy generation
- Policies are assumed to be 12 months
- Start date of policies are uniformly distributed within 12 month period (no seasonality)
- End date of policies are 365.25 days from start date
- Three generic risk factors for the policy are generated (standard normals) [to be used to influence claim parameters]
- Option to set a policy excess and limit
- Option to set policy premium

## Claim generation
- Claims are assumed to arise from a single peril
- Only a single claim is generated per policy (or represeting total of policy claims). The policy is not terminated
- Frequency is set as ground-up frequency, if excess frequeny is used adjust policy excess to zero and limit as the policy exposed value
- Claim value generated from a lognormal with mean and SD
- Timeings are calibrated using distibutions, offset as follows
-- Incident date is set from a uniform distribution within policy year (no seasonality)
-- Reported date is the delay in days from the incident
-- Payment date is the delay in days from the reporting of the claim

## Historic years
- You can specify the number of historic years you would like in your data set
- Years are offset by 365.25 days which is not quite correct (due to leap year) but used as an approximation here
- You can specify a growth rate for the number of policies but all other parameters are assumed to be the same for prior years
