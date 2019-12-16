from invoke import task

from pathlib import Path
import shutil
import markdown
import configparser

import versionIdentifier


@task
def clean(c):
    outDir = __getOutDir()
    if outDir.is_dir():
        shutil.rmtree(outDir)


@task(pre=[clean])
def build(c):
    outDir = __getOutDir()
    outDir.mkdir(parents=True)

    pkgDir = __getPackageDir()

    __copySourceFiles(outDir, pkgDir / "src")

    readMeOutFilename = __convertReadMeToHtml(outDir, pkgDir / "readme.md")

    __updateManifestPlaceholders(
        outDir,
        pkgDir / "manifest.ini",
        readMeOutFilename,
        versionIdentifier.getVersionNumber(),
    )


@task(
    pre=[build],
    help={
        "nvdaConfigPath": "Absolute path to NVDA's configuration directory. Probably under AppData/Roaming"
    },
)
def copy(c, nvdaConfigPath):
    nvdaConfigPathAsStr = nvdaConfigPath
    nvdaConfigPath = Path(nvdaConfigPathAsStr)

    addOnsDir = nvdaConfigPath / "addons"
    if not addOnsDir.is_dir():
        return

    outDir = __getOutDir()

    manifestDict, _ = __readManifestDictFromFile(outDir / "manifest.ini")
    pluginName = manifestDict["name"]

    thisPluginsDir = addOnsDir / pluginName
    if thisPluginsDir.is_dir():
        shutil.rmtree(thisPluginsDir)

    shutil.copytree(outDir, thisPluginsDir)


def __getOutDir():
    taskDir = Path(__file__).parent
    outDir = Path(*["out" if part == "scripts" else part for part in taskDir.parts])
    return outDir


def __getPackageDir():
    taskDir = Path(__file__).parent
    pkgDir = Path(
        *["packages" if part == "scripts" else part for part in taskDir.parts]
    )
    return pkgDir


def __copySourceFiles(outDir, srcDir):
    pluginDir = outDir / "globalPlugins"
    shutil.copytree(srcDir, pluginDir)


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
    parser.optionxform = str  # Override default of converting keys to lowercase (per https://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case)

    # Workaround for manifest not having a section header (per https://stackoverflow.com/questions/2885190/using-configparser-to-read-a-file-without-section-name)
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

