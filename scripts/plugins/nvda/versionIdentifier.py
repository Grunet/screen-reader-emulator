from pathlib import Path
import json

def getVersionNumber():
    sharedConstPath = getSharedConstantsPath()
    with open(sharedConstPath, 'r') as f:
        constantDict = json.load(f)
        return constantDict['version']
    
def getSharedConstantsPath():
    rootPkgDir = getRootPackagesDir()
    sharedConstantsPath = findSharedConstantsJson(rootPkgDir)
    
    return sharedConstantsPath
    
def findSharedConstantsJson(rootPkgDir):
    matchesGenerator = rootPkgDir.glob('**/sharedConstants.json')
    matchesList = list(matchesGenerator)
    
    if (len(matchesList)==0):
        raise FileNotFoundError("No shared constants file could be found.")
    elif (len(matchesList)>1):
        raise FileNotFoundError("Two or more copies of the share constants file were found. There should only be 1")
    else:
        return matchesList[0]
    
def getRootPackagesDir():
    pkgDirParts = __getPackageDirectory().parts
    index = pkgDirParts.index("packages")
    rootPkgDir = Path(*pkgDirParts[:index+1])
    
    return rootPkgDir

def __getPackageDirectory():
    taskDir = Path(__file__).parent
    pkgDir = Path(*["packages" if part=="scripts" else part for part in taskDir.parts])
    return pkgDir