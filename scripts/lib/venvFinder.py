from pathlib import Path
import subprocess


def getPathToPkgDependencies(pkgDir):
    absPathToPkgVirtualEnv = __getPathToPkgVirtualEnv(pkgDir)

    absPathToDependencies = absPathToPkgVirtualEnv / "Lib" / "site-packages"

    return absPathToDependencies


def __getPathToPkgVirtualEnv(pkgDir):
    alreadyTriedToInstallMissingVirtualEnv = False

    while True:
        doesVirtualEnvExist, objPathToPkgVirtualEnv = __checkForPkgVirtualEnv(pkgDir)

        if doesVirtualEnvExist is True:
            return objPathToPkgVirtualEnv

        if not alreadyTriedToInstallMissingVirtualEnv:
            subprocess.call(["pipenv", "install"], cwd=pkgDir)

            alreadyTriedToInstallMissingVirtualEnv = True
        else:
            raise FileNotFoundError(
                "Attempted to install the virtualenv from the Pipfile,"
                / " but still couldn't find it"
            )


def __checkForPkgVirtualEnv(pkgDir):
    strPathToPkgVirtualEnv = (
        subprocess.run(["pipenv", "--venv"], cwd=pkgDir, stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip()
    )

    objPathToPkgVirtualEnv = Path(strPathToPkgVirtualEnv)

    # The former check is needed since the latter returns true for Path("")
    doesPathExist = (
        len(strPathToPkgVirtualEnv) != 0
    ) and objPathToPkgVirtualEnv.exists()

    return doesPathExist, objPathToPkgVirtualEnv
