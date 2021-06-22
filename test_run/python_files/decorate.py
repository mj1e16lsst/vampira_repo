#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import subprocess
import re

def findAll(inString,findx):
    return [m.start() for m in re.finditer(findx, inString)]


def decorateFile(exampleScript,modules=[]):
    
    find1 = '.py'
    loc1 = exampleScript.index(find1)
    scriptShort = exampleScript[0:loc1]

    scriptNew = scriptShort+'_decorated.py'

    with open(exampleScript,'r') as f:
        ogData = f.read()

    importRequired = 'import genBindings \n'

    imports = findAll(ogData,'import ')
    firstImport = imports[0]
    importLines = [ogData[x:x+ogData[x:].index('\n')] for x in imports]
    #print(importLines)
    asString = ' as '
    for mod in modules:
        modSearch = ' '+mod
        matchingMod = [y for y in importLines if modSearch in y] 
	if len(matchingMod) > 1:
            print('two imports matching the same naming convention')
        elif len(matchingMod) == 0:
            continue
        if asString in matchingMod[0]:
            functName = matchingMod[0][matchingMod[0].index(asString)+len(asString):]
            print(functName)
        else:
            functName = mod
        ogData = ogData.replace(matchingMod[0],matchingMod[0]+'\ngenBindings.decorate_all_in_module({},genBindings.provWrap)'.format(functName))
    ogData = ogData[:firstImport] + importRequired + ogData[firstImport:]

    functFinder = 'def '

    updatedData = ogData.replace('def ','@genBindings.provWrap\ndef ')
    
    with open(scriptNew,'w') as f:
        f.write(updatedData)
    
    return scriptNew


# In[ ]:




