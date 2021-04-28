#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import subprocess


def decorateFile(exampleScript):
    
    find1 = '.py'
    loc1 = exampleScript.index(find1)
    scriptShort = exampleScript[0:loc1]

    scriptNew = scriptShort+'_decorated.py'

    with open(exampleScript,'r') as f:
        ogData = f.read()

    importRequired = 'import genBindings \n'

    firstImport = ogData.index('import ')

    ogData = ogData[:firstImport] + importRequired + ogData[firstImport:]

    functFinder = 'def '

    updatedData = ogData.replace('def ','@genBindings.provWrap\ndef ')
    
    with open(scriptNew,'w') as f:
        f.write(updatedData)
    
    return scriptNew


# In[ ]:




