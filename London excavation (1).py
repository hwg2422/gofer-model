#!/usr/bin/env python
# coding: utf-8

# In[12]:


#import gofer_auth.py - handles authentication (token will remain for a limited time)
import gofer_auth


# In[5]:


# imports 
import requests
import time
import sys
from urllib.parse import urlencode
from gofer_auth import AcquireNewAccessTokenDeviceFLow as get_token
API_LOCATION = "https://api.gofer.oasys.software.com"

import matplotlib.pyplot as plt
import math


# In[3]:


#Get token, define high level GET function for later use
auth_token = get_token() # using function from gofer_auth

def get(route):
    url = f"{API_LOCATION}/{route}"
    headers = {'authorization': 'Bearer' + auth_token}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return res.text


# In[5]:


# Function to get a list of my models, use to find ID of target model
def get_model_IDs():
    try:
        model_list = get("v1/models/")
        assert len(model_list) > 0
    except AssertionError:
        return "NO models found"
    else:
        return model_list
        
the_model_list = get_model_IDs()
if the_model_list == "NO models found":
    print(the_model_list)
else:
    num_models = len(the_model_list)
    m = 1 # postion in list of model I want to show ID and name of below
    print('%s models found' %num_models)
    print('model ID: %s' %the_model_list[m]['id'])
    print('Model description: %s' %the_model_list[m]['description'])


# In[ ]:


# Copy the model ID from above
modelID = ""


# In[ ]:


# Function to count the number of stages not run in a model
def get_an_status(ID, check_run):
    an_status = get("v1/models/" + ID + "/analysis")
    num_stages = len(an_status)
    stages_not_run = 0
    for i in range(0, num_stages):
        if an_status[i]['analysisStatus'] == 0:
            stages_not_run += 1
    if check_run == 'true':
        return stages_not_run
    else:
        return an_status
check_stages_not_run = get_an_status(modelID,'true')
print('%s stages not run' %check_stages_not_run)


# In[ ]:


# Get results for last stage in target model, print model for one node (zero'th node in list)
my_analysis_status = get_an_status(modelID,'false')
num_stages = len(my_analysis_status)
last_stageID = my_analysis_status[num_stages =1]['id'] #get stage ID of last stage in model (first stage is 0)
last_results = get("v1/models/" + modelID + "/stages/" + last_stageID + "/results?type=default") ~Get results
print(last_results['nodes'][0]) #print for zero'th node


# In[ ]:


# Find nodes with structural results, append as list
my_structural_results = [] #bla list
for i in last_results['nodes']:
    if i['bendingmoment'] != None:
        my_structural_results.append(i)
        
print('Complete')

