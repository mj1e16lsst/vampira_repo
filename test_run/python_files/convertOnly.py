import os 
import sys
import subprocess

import convert2prov

currentDir = os.getcwd()

templatelist, namelist = convert2prov.generateLists(currentDir+'/templates/')

print(templatelist)
print(namelist)
# In[12]:

convert2prov.convertall(currentDir+'/json/',currentDir+'/templates/',templatelist, namelist,currentDir+'/prov/')


# In[13]:

subprocess.call(['make','merge'])


# In[14]:

subprocess.call(['make','flatten'])
