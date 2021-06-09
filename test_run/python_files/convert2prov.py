#!/usr/bin/env python
# coding: utf-8

# In[33]:


import os
import subprocess
import time


def generateLists(templateDir):
    templatelistextra = os.listdir(templateDir)
    
    templatelist = []
    for x in range(len(templatelistextra)):
        a = templatelistextra[x].find('.')
        if a !=0:
            if '.provn' in templatelistextra[x]:
                templatelist.append(templatelistextra[x])
                
    namelist = []
    for x in range(len(templatelist)):
        loc = templatelist[x].find('_template.provn')
        if loc !=0:
            namelist.append(templatelist[x][0:loc])

    return templatelist, namelist


# In[22]:


def convertall(jsonDir, templateDir, templatelist, namelist, provDir):
    directorylist = os.listdir(jsonDir)
    for y in range(0, len(directorylist)):    
        for x in range(0, len(namelist)):
            a = (directorylist[y]).find(namelist[x])
            if a != -1:
                subprocess.call(['provconvert', '-infile', templateDir+templatelist[x], '-bindings', jsonDir+directorylist[y], '-bindformat', 'json', '-bindver', '3', '-outfile', provDir+namelist[x]+str(time.time())+'.provn'])




