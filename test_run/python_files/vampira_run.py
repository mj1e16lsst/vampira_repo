
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
#import genBindings
import vampiraTemplates
import moduleList

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
#outputLengths = [len(x[2]) for x in example_sep.values()]
tot_sep_dict = {x[0]:[x[1],x[2]] for x in example_sep.values()}
# In[7]:

for key in example_sep.keys():
    noSpecial = [''.join(e for e in string if e.isalnum() or e is '_') for string in example_sep[key]]
    bundle = vampiraTemplates.generateBundle(noSpecial,vampiraTemplates.bundleStart,vampiraTemplates.bundleEnd)
    with open(currentDir+'/templates/{}_template.provn'.format(noSpecial[0]),'w') as f:
        f.write(bundle)

modLocs = moduleList.moduleLocations

for mod in modLocs:
    with open(mod,'r') as f:
        exDat = f.read()
    example_sep = vampiraTemplates.variableSeparation(exDat)
    tot_sep_dict.update({x[0]:[x[1],x[2]] for x in example_sep.values()}) # functions with the same name may try to overwrite, possible future bug
    for key in example_sep.keys():
        noSpecial = [''.join(e for e in string if e.isalnum() or e is '_') for string in example_sep[key]]
        bundle = vampiraTemplates.generateBundle(noSpecial,vampiraTemplates.bundleStart,vampiraTemplates.bundleEnd)
        with open(currentDir+'/templates/{}_template.provn'.format(noSpecial[0]),'w') as f:
            f.write(bundle)
# In[8]:
with open(currentDir+'/templateDictionary.py','w') as f:
    f.write('tempDict = {}'.format(tot_sep_dict))

newName = decorate.decorateFile(exampleScript,modules=moduleList.modules)


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



