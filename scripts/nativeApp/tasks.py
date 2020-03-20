from invoke import task

import constantsExtractor
from dirFinder import findMatchingOutDir, findMatchingPkgDir

from pathlib import Path
import json
import shutil
import subprocess

PATH_TO_ENTRY_POINT_FROM_PACKAGE_ROOT = Path("nativeApp", "src", "app.py")


@task
def clean(c):
    outDir = findMatchingOutDir(__file__)
    if outDir.is_dir():
        shutil.rmtree(outDir)

    # On Windows, manually cleanup any registry settings created by the build


@task
def build(c):
    outDir = findMatchingOutDir(__file__)  # out/nativeApp
    nativeAppPkgDir = findMatchingPkgDir(__file__)  # packages/nativeApp
    pkgDir = nativeAppPkgDir.parents[0]

    __copySrcToOut(outDir, pkgDir)

    pathToExe = __createExeFromCopiedSrc(
        outDir, pkgDir, PATH_TO_ENTRY_POINT_FROM_PACKAGE_ROOT
    )

    nameForManifest, pathToHydratedManifest = __hydrateManifest(
        outDir, nativeAppPkgDir, pathToExe
    )

    __createRefToManifest(nameForManifest, pathToHydratedManifest)


@task
def start(c):
    outDir = findMatchingOutDir(__file__)

    pathToExe = __getPathToExe(outDir, PATH_TO_ENTRY_POINT_FROM_PACKAGE_ROOT)

    subprocess.call(str(pathToExe.resolve()))


def __copySrcToOut(outDir, pkgDir):
    shutil.copytree(pkgDir, outDir, ignore=__excludeNonNativeAppRelatedSrcFiles)


def __excludeNonNativeAppRelatedSrcFiles(path, names):
    pathObj = Path(path)
    return set(
        name for name in names if not (pathObj / name).is_dir() and ".py" not in name
    )


def __createExeFromCopiedSrc(rootDir, pkgDir, relPathToEntryPoint):

    absPathToPkgVirtualEnv = __getPathToPkgVirtualEnv(pkgDir)

    absPathToDependencies = absPathToPkgVirtualEnv / "Lib" / "site-packages"

    subprocess.call(
        [
            "pyinstaller",
            "--paths",
            str(absPathToDependencies),
            str(relPathToEntryPoint),
        ],
        cwd=rootDir,
    )

    return __getPathToExe(rootDir, relPathToEntryPoint)


def __getPathToPkgVirtualEnv(pkgDir):
    return Path(
        subprocess.run(["pipenv", "--venv"], cwd=pkgDir, stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip()
    )  # This assumes the virtualenv has been created


def __getPathToExe(rootDir, relPathToEntryPoint):
    pathToExe = (
        rootDir / "dist" / relPathToEntryPoint.stem / relPathToEntryPoint.stem
    ).with_suffix(".exe")

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
        raise NotImplementedError("The build step currently only works on Windows")

