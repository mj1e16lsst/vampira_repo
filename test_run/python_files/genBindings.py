#!/usr/bin/env python
# coding: utf-8

# In[9]:


import json
import time
import datetime
from collections import defaultdict, Counter, OrderedDict
import uuid
import os
ts = time.time()
import random

import inspect
import types
import functools
import sys
import templateDictionary
# In[2]:


#### initial setup

bindings = {
  "context": {
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "lsim": "http://example.org/",
    "urn_uuid": "urn:uuid:",
    "run": "http://example.org/"
  }
}

session_id = 'simple{}'.format(time.time())
prov_id_counter = Counter()
prov_id_cache = dict()



# In[3]:


def timestamp():
    ts = str(time.time())
    return ts



# In[4]:


def datetimestamp():
    dts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S')
    return dts

#### generate unique but linking identifier



# In[5]:


def gen_identifier(variable, naming_template="entity"):
    try:
        prov_id = prov_id_cache[id(variable)]
    except KeyError:
        prov_id_counter[naming_template] += 1
        prov_id = '{}_{}_{}'.format(naming_template, session_id, prov_id_counter[naming_template])
        prov_id_cache[id(variable)] = prov_id
    
    #print(prov_id)
    return prov_id




# In[8]:

def provcall(inlist, outlist, template, longname,jsonDir='./'):
    inlist = [str(x).replace('*','') for x in inlist]
    outlist = [str(x).replace('*','') for x in outlist]
    identifier = uuid.uuid4()
    bindings['var'] = {}
    bindings['var']['messageStartTime'] = [ {"@type": "xsd:dateTime", "@value": datetimestamp()} ] # change to date time
    bindings['var']['template'] = [template]
    bindings['var']['message'] = [ {"@id": "urn_uuid:"+str(longname)+str(identifier) } ] # is this right? rm str(longname) if you broke it
    print(longname,'longname')
    #print(templateDictionary.tempDict.keys())
    # janky way to always match template and binding in/out size
    if longname in templateDictionary.tempDict:
        if len(outlist) < len(templateDictionary.tempDict[longname][1]):
            print('mismatch lengths')
            lenDiff = len(templateDictionary.tempDict[longname][1]) - len(outlist)
            for extra in range(lenDiff):
                outlist.append('Not Computed')
        if len(inlist) < len(templateDictionary.tempDict[longname][0]):
            print('mismatch input')
            lenDiff = len(templateDictionary.tempDict[longname][0]) - len(inlist)
            for extra in range(lenDiff):
                inlist.append('Not Computed')

    for X in range(len(outlist)):
        outVal = str(outlist[X])
        if len(outVal) > 100:
            outVal = str(outlist[X])[0:100]
        bindings['var']['output'+str(X)] = [ {"@id": "run:"+gen_identifier(outlist[X])} ] # added value, remove if broken
        bindings['var']['output'+str(X)+'value'] = [ {"@value": outVal,"@type":"xsd:string"} ]  

    for X in range(len(inlist)):
        inVal = str(inlist[X])
        if len(inVal) > 100:
            inVal = str(inlist[X])[0:100]        
        bindings['var']['input'+str(X)] = [ {"@id": "run:"+gen_identifier(inlist[X])} ]
        bindings['var']['input'+str(X)+'value'] = [ {"@value":str(inVal),"@type":"xsd:string"} ] 
    bindings['var']['messageEndTime'] = [ {"@type": "xsd:dateTime", "@value": datetimestamp()} ] # change to datetime
    
    with open(jsonDir+longname+timestamp()+str(random.random())+".json", 'w') as f:
        json.dump(bindings, f, indent=2)
    return json.dumps(bindings)



# In[1]:




# def provcall(inlist, outlist, template, longname,jsonDir='./'):
#     identifier = uuid.uuid4()
#     bindings['var'] = {}
#     bindings['var']['messageStartTime'] = [ {"@type": "xsd:dateTime", "@value": datetimestamp()} ] # change to date time
#     bindings['var']['template'] = [template]
#     bindings['var']['message'] = [ {"@id": "urn_uuid:"+str(longname)+str(identifier) } ] # is this right? rm str(longname) if you broke it
#     for X in range(len(outlist)):
#         outVal = str(outlist[X])
#         bindings['var']['output'+str(X)] = [ {"@id": "run:"+gen_identifier(outlist[X])} ] # added value, remove if broken
#         bindings['var']['output'+str(X)+'value'] = [ {"@value": outVal,"@type":"xsd:string"} ]  
#     for X in range(len(inlist)):       
#         inVal = str(inlist[X])        
#         bindings['var']['input'+str(X)] = [ {"@id": "run:"+gen_identifier(inlist[X])} ]
#         bindings['var']['input'+str(X)+'value'] = [ {"@value":str(inVal),"@type":"xsd:string"} ] 
#     bindings['var']['messageEndTime'] = [ {"@type": "xsd:dateTime", "@value": datetimestamp()} ] # change to datetime
    
#     with open(jsonDir+longname+timestamp()+str(random.random())+".json", 'w') as f:
#         json.dump(bindings, f, indent=2)
#     return json.dumps(bindings)



# In[7]:


def printDict():
    print(prov_id_cache,"prov_id_cache")
    
#provcall([1],[2],"daoStarFinder_PythonCode2Images_SQ_tmpl.provn","daoStarFinder")


# In[99]:


def provWrap(func):
    '''Decorator to record provenance'''

    def wrap(*args,**kwargs):
        
        name = func.__name__
        longname = name
        template = name+'_template.provn'
        inlist = list(args)

	filePath = sys.path[0]
        jsonDir = filePath+'/json/'

        a = inspect.getargspec(func)
        try:
            defaultsKeys = a.args[-len(a.defaults):] 
            defaultsVals = list(a.defaults)

            kwargList = []

            for k,key in enumerate(defaultsKeys):
                if key in kwargs.keys():
                    kwargList.append(kwargs[key])
                else:
                    kwargList.append(defaultsVals[k])

            inlist.extend(kwargList)
        except TypeError:
            print('No kwargs')
            
        #potential bugs depending on their output format
        output = func(*args,**kwargs)
        outlist = [output]
        provcall(inlist,outlist,template,longname,jsonDir=jsonDir)
        
        return output
    return wrap


# In[2]:


def decorate_all_in_module(module, decorator):
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, types.FunctionType):
            setattr(module, name, decorator(obj))






