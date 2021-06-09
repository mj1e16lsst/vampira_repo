
# coding: utf-8

# In[1]:

import os
import subprocess
import sys


# In[2]:

#os.chdir('/home/mj1e16/vampira_repo/test_run/python_files/')


# In[3]:

import convert2prov
import decorate
import genBindings
import vampiraTemplates


# In[4]:

currentDir = os.getcwd()
newDirectories = ['prov','json','templates']
for name in newDirectories:
    try:
        subprocess.call(['mkdir',name])
    except:
        print('Directory {} already exists'.format(name))


# In[5]:

#exampleScript = '/home/mj1e16/vampira_repo/test_run/python_files/exampleScript.py'
exampleScript = sys.argv[1]


# In[6]:

with open(exampleScript,'r') as f:
    script = f.read()

example_sep = vampiraTemplates.variableSeparation(script)


# In[7]:

for key in example_sep.keys():
    bundle = vampiraTemplates.generateBundle(example_sep[key],vampiraTemplates.bundleStart,vampiraTemplates.bundleEnd)
    with open(currentDir+'/templates/{}_template.provn'.format(example_sep[key][0]),'w') as f:
        f.write(bundle)


# In[8]:

newName = decorate.decorateFile(exampleScript)


# In[9]:

subprocess.call(['python',newName])


# In[10]:

templatelist, namelist = convert2prov.generateLists(currentDir+'/templates/')


# In[12]:

convert2prov.convertall(currentDir+'/json/',currentDir+'/templates/',templatelist, namelist,currentDir+'/prov/')


# In[13]:

subprocess.call(['make','merge'])


# In[14]:

subprocess.call(['make','flatten'])


# In[ ]:



