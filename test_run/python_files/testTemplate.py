import moduleList
import vampiraTemplates
import os

currentDir = os.getcwd()

modLocs = moduleList.moduleLocations
#print(len(modLocs))
for i,mod in enumerate(modLocs):
    with open(mod,'r') as f:
        exDat = f.read()
    example_sep = vampiraTemplates.variableSeparation(exDat)
    #print(example_sep)
    for key in example_sep.keys():
        bundle = vampiraTemplates.generateBundle(example_sep[key],vampiraTemplates.bundleStart,vampiraTemplates.bundleEnd)
	#print(bundle)
        with open(currentDir+'/templates/{}_template.provn'.format(example_sep[key][0]),'w') as f:
            f.write(bundle)

