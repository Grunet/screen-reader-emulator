from pathlib import Path
import json


def getVersionNumber():
    constantDict = __getSharedConstantsData()
    return constantDict["version"]


def getExtensionId():
    constantDict = __getSharedConstantsData()
    return constantDict["ids"]["extension"]


def getNativeAppId():
    constantDict = __getSharedConstantsData()
    return constantDict["ids"]["nativeApp"]


def __getSharedConstantsData():
    sharedConstPath = __getSharedConstantsPath()
    with open(sharedConstPath, "r") as f:
        constantDict = json.load(f)
        return constantDict


def __getSharedConstantsPath():
    rootPkgDir = __getRootPackagesDir()
    sharedConstantsPath = __findSharedConstantsJson(rootPkgDir)

    return sharedConstantsPath


def __findSharedConstantsJson(rootPkgDir):
    matchesGenerator = rootPkgDir.glob("**/sharedConstants.json")
    matchesList = list(matchesGenerator)

    if len(matchesList) == 0:
        raise FileNotFoundError("No shared constants file could be found.")
    elif len(matchesList) > 1:
        raise FileNotFoundError(
            (
                "Two or more copies of the share constants file were found."
                " There should only be 1"
            )
        )
    else:
        return matchesList[0]


def __getRootPackagesDir():
    pkgDirParts = __getPackageDir().parts
    index = pkgDirParts.index("packages")
    rootPkgDir = Path(*pkgDirParts[: index + 1])

    return rootPkgDir


def __getPackageDir():
    taskDir = Path(__file__).parent
    pkgDir = Path(
        *["packages" if part == "scripts" else part for part in taskDir.parts]
    )
    return pkgDir
