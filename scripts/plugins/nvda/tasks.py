from invoke import task

import os
from pathlib import Path
import shutil
import markdown
import configparser
import subprocess

import constantsExtractor
from dirFinder import findMatchingOutDir, findMatchingPkgDir


@task
def clean(c):
    outDir = findMatchingOutDir(__file__)
    if outDir.is_dir():
        shutil.rmtree(outDir)


@task
def build(c):
    outDir = findMatchingOutDir(__file__)
    outDir.mkdir(parents=True)

    pkgDir = findMatchingPkgDir(__file__)

    __copySourceFiles(outDir, pkgDir / "src")

    __updatePythonImportsForNVDA(outDir)

    __copyDependencyAdapter(outDir, Path(__file__).parent / "dependencyAdapter.py")

    readMeOutFilename = __convertReadMeToHtml(outDir, pkgDir / "readme.md")

    __updateManifestPlaceholders(
        outDir,
        pkgDir / "manifest.ini",
        readMeOutFilename,
        constantsExtractor.getVersionNumber(),
    )


@task
def copy(c):
    nvdaConfigPathAsStr = os.environ["NVDA_CONFIG_PATH"]
    nvdaConfigPath = Path(nvdaConfigPathAsStr)

    addOnsDir = nvdaConfigPath / "addons"
    if not addOnsDir.is_dir():
        return

    outDir = findMatchingOutDir(__file__)

    manifestDict, _ = __readManifestDictFromFile(outDir / "manifest.ini")
    pluginName = manifestDict["name"]

    thisPluginsDir = addOnsDir / pluginName
    if thisPluginsDir.is_dir():
        shutil.rmtree(thisPluginsDir)

    shutil.copytree(outDir, thisPluginsDir)


@task
def start(c):
    nvdaExePathAsStr = os.environ["NVDA_EXE_PATH"]
    nvdaExePath = Path(nvdaExePathAsStr)

    # Making sure it's running something with at least the right name
    # See the warning from https://docs.python.org/2/library/subprocess.html#frequently-used-arguments # noqa
    if nvdaExePath.name != "nvda.exe":
        raise Exception("The path to NVDA should end with the exe's filename")

    subprocess.Popen(
        [nvdaExePathAsStr, "--replace"],
        shell=True,  # Bypasses the "requested operation requires elevation" error
    )


def __copySourceFiles(outDir, srcDir):
    pluginDir = outDir / "globalPlugins"
    shutil.copytree(srcDir, pluginDir, ignore=__excludeClientsFolder)


def __updatePythonImportsForNVDA(outDir):
    for path in outDir.glob("**/*.py"):
        fileText = path.read_text()

        updatedText = fileText.replace("from plugins.nvda.src.", "from .")

        path.write_text(updatedText)


def __copyDependencyAdapter(outDir, pathToDependencyAdapter):
    origEntryPointPath = __findPathToOriginalEntryPoint(outDir)

    hiddenEntryPointPath = __hideOriginalEntryPointFromNVDA(origEntryPointPath)

    exposedEntryPointPath = (
        outDir / "globalPlugins" / "entryPoint.py"
    )  # TODO - The "globalPlugins" string is duplicated below
    shutil.copyfile(
        pathToDependencyAdapter, exposedEntryPointPath,
    )

    __updateDependencyAdapterPlaceholders(
        exposedEntryPointPath, hiddenEntryPointPath.stem
    )


def __findPathToOriginalEntryPoint(outDir):
    paths = list()
    for path in outDir.glob("**/*.py"):
        fileText = path.read_text()

        if "class GlobalPlugin" in fileText:
            paths.append(path)

    if len(paths) <= 0:
        raise Exception("No file declaring a GlobalPlugin class was found")
    elif len(paths) >= 2:
        raise Exception("More than 1 file declaring a GlobalPlugin class was found")

    return paths[0]


def __hideOriginalEntryPointFromNVDA(origEntryPointPath):
    # Trying to avoid any unexpected direct imports by NVDA (see https://github.com/nvaccess/nvda/blob/23ad41e62dd24bad60c1fe61cf70e59b43e6d39c/source/globalPluginHandler.py for where this check is made) # noqa
    hiddenEntryPointName = "_" + origEntryPointPath.name
    hiddenEntryPointPath = origEntryPointPath.with_name(hiddenEntryPointName)

    origEntryPointPath.rename(hiddenEntryPointPath)

    return hiddenEntryPointPath


def __updateDependencyAdapterPlaceholders(dependencyAdapterPath, wrappedModuleName):
    placeholderCode = dependencyAdapterPath.read_text()

    populatedCode = placeholderCode.replace("filenameOfEntryPoint", wrappedModuleName)

    dependencyAdapterPath.write_text(populatedCode)


def __excludeClientsFolder(path, names):
    pathObj = Path(path)
    return set(name for name in names if pathObj.stem == "src" and "clients" in name)


def __convertReadMeToHtml(outDir, readMeSrcPath):
    outFilename = readMeSrcPath.with_suffix(".html").name

    readMeOutPath = outDir / "doc" / "en" / outFilename
    readMeOutPath.parent.mkdir(parents=True)
    readMeOutPath.touch()

    markdown.markdownFromFile(input=str(readMeSrcPath), output=str(readMeOutPath))

    return outFilename


def __updateManifestPlaceholders(
    outDir, manifestSrcPath, readMeOutFilename, versionNumber
):
    manifestDict, parser = __readManifestDictFromFile(manifestSrcPath)

    manifestDict["version"] = versionNumber
    manifestDict["docFileName"] = readMeOutFilename

    __writeManifestDictToFile(outDir / "manifest.ini", parser)


def __readManifestDictFromFile(manifestPath):
    parser = configparser.ConfigParser()
    # Override default of converting keys to lowercase
    # per https://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case # noqa
    parser.optionxform = str

    # Workaround for manifest not having a section header (
    # per https://stackoverflow.com/questions/2885190/using-configparser-to-read-a-file-without-section-name) # noqa
    with open(manifestPath) as stream:
        parser.read_string("[DUMMY]\n" + stream.read())
    manifestDict = parser["DUMMY"]

    return manifestDict, parser


def __writeManifestDictToFile(destPath, parser):
    with open(destPath, "w") as f:
        parser.write(f)

    # Getting rid of the dummy section header
    with open(destPath, "r") as f:
        fileContents = f.readlines()
    with open(destPath, "w") as f:
        f.writelines(fileContents[1:])
