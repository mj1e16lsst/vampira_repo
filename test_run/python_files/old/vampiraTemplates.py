#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import sys


def findSingle(inString, findx):
    return [i for i, ltr in enumerate(inString) if ltr == findx]


# In[4]:


def find(inString,findx):
    return [m.start() for m in re.finditer(findx, inString)]


# In[5]:


def separateLists(inList):
    inputList = []
    findC = ','
    sepLocs = find(inList,findC)
    sepLocs.insert(0,0)
    sepLocs.append(len(inList))
    
    inputList = [inList[x:y] for x,y in zip(sepLocs[0:-1],sepLocs[1:])]
    inputList = [x.replace(',','') for x in inputList]
    
    for x,inL in enumerate(inputList):
        if '=' in inL:
            loc1 = inL.find('=')
            inVal = inL[:loc1]
            inputList[x] = inVal
    
    return inputList


# In[6]:


def variableSeparation(inString):
    find1 = 'def '
    find2 = '('
    find3 = '):'
    find4 = 'return '
    find5 = '\n'
    
    functionDict = {}
    
    functionLocs = find(inString,find1)
    functionLocs.append(len(inString))
    
    for fNum in range(len(functionLocs)-1):
        
        searchString = inString[functionLocs[fNum]:functionLocs[fNum+1]]
        loc2 = searchString.index(find2)
        loc3 = searchString.index(find3)
	
	try:
            #loc4 = searchString.index(find4)
	    loc4s = find(searchString,find4)
	except:
	    continue
	loc5s = [searchString[x:].index(find5) + x for x in loc4s]
        #loc5 = searchString[loc4:].index(find5) + loc4
        
        functName = searchString[len(find1):loc2]
        
        inputList = searchString[loc2+len(find2):loc3]
        if ',' in inputList:
            #print(inputList)
            inputList = separateLists(inputList)
        else:
            inputList = [inputList]

	#for outLen in range(len(loc4s)):
        #outputList = searchString[loc4s[outLen]+len(find4):loc5s[outLen]]
        outputList = searchString[loc4s[-1]+len(find4):loc5s[-1]]
	if ',' in outputList:
            outputList = separateLists(outputList)
        else:
            outputList = [outputList]
        
        functionDict['funct_{0}'.format(fNum)] = [functName,inputList,outputList]
    return functionDict



bundleStart = """
document
prefix prov <http://www.w3.org/ns/prov#>
prefix tmpl <http://openprovenance.org/tmpl#>
prefix var <http://openprovenance.org/var#>
prefix exe <http://example.org/>
prefix u2p <http://uml2prov.org/>

bundle exe:bundle1"""


# In[9]:


bundleEnd = '''
endBundle
endDocument'''


# In[10]:


def createInputEntities(inputList):
    inputEntities = []
    for i,inVal in enumerate(inputList):
        entityString = """
        entity(var:input{0}, [prov:value = 'var:input{0}value'])
        used(var:message, var:input{0}, -, [prov:role='u2p:{1}'])""".format(i,inVal)
        
        inputEntities.append(entityString)
    
    inputEntityString = '\n'.join(inputEntities)
    return inputEntityString


# In[11]:


def createActivity(activity,agent):
    activityString = """
    activity(var:message, [prov:type = 'u2p:{0}', tmpl:startTime = 'var:messageStartTime', tmpl:endTime ='var:messageEndTime' ])
    agent(var:lifeline, [prov:type='u2p:{1}'])
    
    wasAssociatedWith(var:message, var:lifeline, - , [])
    """.format(activity,agent)
    
    return activityString


# In[12]:


def createOutputEntities(inputList,outputList):
    outputEntities = []
    for o,outVal in enumerate(outputList):
        outputString = """
        entity(var:output{0}, [prov:value = 'var:output{0}value'])
        wasGeneratedBy(var:output{0}, var:message, -, [prov:role='u2p:{1}'])""".format(o,outVal)
        for i,inVal in enumerate(inputList):
            derivedString = """
            wasDerivedFrom(var:output{}, var:input{})""".format(o,i)
            outputString += derivedString
        
        outputEntities.append(outputString)
    outputEntityString = '\n'.join(outputEntities)
    
    return outputEntityString


# In[13]:


def generateBundle(function,bundleStart,bundleEnd):
    
    inEntities = createInputEntities(function[1])
    activity = createActivity(function[0],'pythonCode')
    outEntities = createOutputEntities(function[1],function[2])
    
    bundleList = [bundleStart,inEntities,activity,outEntities,bundleEnd]
    bundle = '\n'.join(bundleList)
    
    return bundle





