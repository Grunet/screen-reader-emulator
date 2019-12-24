from invoke import task

import constantsExtractor
from dirFinder import findMatchingOutDir, findMatchingPkgDir

from pathlib import Path
import json
import shutil


@task
def clean(c):
    outDir = findMatchingOutDir(__file__)
    if outDir.is_dir():
        shutil.rmtree(outDir)


@task(pre=[clean])
def build(c):
    outDir = findMatchingOutDir(__file__)
    pkgDir = findMatchingPkgDir(__file__)

    entryPoint = __copySrcToOut(outDir, pkgDir)
    pathToExe = __createExeFromCopiedSrc(outDir, entryPoint)

    nameForManifest, pathToHydratedManifest = __hydrateManifest(
        outDir, pkgDir, pathToExe
    )

    __createRefToManifest(nameForManifest, pathToHydratedManifest)


def __copySrcToOut(outDir, nativeAppPkgDir):
    shutil.copytree(nativeAppPkgDir / "src", outDir)
    entryPoint = "app.py"

    return entryPoint


def __createExeFromCopiedSrc(outDir, entryPoint):
    import subprocess

    subprocess.call(["pyinstaller", entryPoint], cwd=outDir)
    entryPointFilename = Path(entryPoint).stem  # Removes the ".py" extension
    pathToExe = (outDir / "dist" / entryPointFilename / entryPointFilename).with_suffix(
        ".exe"
    )

    return pathToExe


def __hydrateManifest(outDir, nativeAppPkgDir, pathToExe):
    nameForManifest = constantsExtractor.getNativeAppId()

    manifestSrc = nativeAppPkgDir / "manifest.json"

    with open(manifestSrc, "r") as f:
        manifestDict = json.load(f)

        manifestDict["name"] = nameForManifest
        manifestDict["allowed_extensions"] = [constantsExtractor.getExtensionId()]
        manifestDict["path"] = str(pathToExe.resolve())

    manifestOut = (outDir / nameForManifest).with_suffix(".json")

    with open(manifestOut, "w") as f:
        json.dump(manifestDict, f, sort_keys=True, indent=4)

    return nameForManifest, manifestOut


def __createRefToManifest(manifestName, pathToManifest):
    import platform
    import winreg

    if platform.system() == "Windows":
        key = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            str(Path("SOFTWARE", "Mozilla", "NativeMessagingHosts", manifestName)),
        )
        winreg.SetValueEx(key, None, 0, winreg.REG_SZ, str(pathToManifest.resolve()))
        key.Close()

    else:
        raise NotImplementedError("The build currently only works on Windows")
