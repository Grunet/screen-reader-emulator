from invoke import task

from pathlib import Path
import shutil
import markdown
import configparser

import json

@task
def clean(c):
    outDir = getOutDir()
    if outDir.is_dir():
        shutil.rmtree(outDir)

@task(pre=[clean])
def build(c):
    outDir = getOutDir()
    outDir.mkdir(parents=True)
        
    pkgDir = getPackageDir()
    
    srcDir = pkgDir/"src"
    pluginDir = outDir/"globalPlugins"
    shutil.copytree(srcDir, pluginDir)
    
    readMeSrcPath = pkgDir/"readme.md"
    
    readMeOutFilename = "readme.html"
    readMeOutPath = outDir/"doc"/"en"/readMeOutFilename
    readMeOutPath.parent.mkdir(parents=True)
    readMeOutPath.touch()
    
    markdown.markdownFromFile(input=str(readMeSrcPath), output=str(readMeOutPath))
    
    manifestSrcPath = pkgDir/"manifest.ini"
    
    parser = configparser.ConfigParser()
    #Workaround for manifest not having a section header (per https://stackoverflow.com/questions/2885190/using-configparser-to-read-a-file-without-section-name) 
    with open(manifestSrcPath) as stream:
        parser.read_string("[DUMMY]\n" + stream.read())
    manifestDict = parser['DUMMY']
    manifestDict['version'] = getVersionNumber()
    manifestDict['docFileName']=readMeOutFilename
    
    manifestOutPath = outDir/"manifest.ini"
    with open(manifestOutPath, 'w') as f:
        parser.write(f)
    #Getting rid of the dummy section header
    with open(manifestOutPath, 'r') as f:
        fileContents = f.readlines()
    with open(manifestOutPath, 'w') as f:
        f.writelines(fileContents[1:])
    
    
    
    
def getOutDir():
    taskDir = Path(__file__).parent
    outDir = Path(*["out" if part=="scripts" else part for part in taskDir.parts])
    return outDir

def getPackageDir():
    taskDir = Path(__file__).parent
    pkgDir = Path(*["packages" if part=="scripts" else part for part in taskDir.parts])
    return pkgDir




# Move this into it's own utility module? 
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
    pkgDirParts = getPackageDir().parts
    index = pkgDirParts.index("packages")
    rootPkgDir = Path(*pkgDirParts[:index+1])
    
    return rootPkgDir

    
    