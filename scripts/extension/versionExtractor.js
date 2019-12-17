const path = require('path');
const glob = require('glob');
const jsonfile = require('jsonfile');

async function getVersionNumber() {
    let sourceDir = __findSourceDirectory().abs;
    let constantsFilePath = await __findSharedConstantsJson(sourceDir);
    let versionNumber = await __getVersionFromFile(constantsFilePath);

    return versionNumber;
}

function __findSourceDirectory() {
    let scriptsDirParts = __dirname.split(path.sep);
    let index = scriptsDirParts.indexOf("scripts");
    if (index < 0) {
        throw new Error("Unable to find source directory from scripts directory");
    }

    let sourceDirParts = scriptsDirParts.slice(0, index + 1);
    sourceDirParts[index] = "packages";

    let sourceDirAbsPath = path.join(...sourceDirParts);
    let sourceDirRelPath = path.relative(__dirname, sourceDirAbsPath);

    return {
        abs: sourceDirAbsPath,
        rel: sourceDirRelPath
    }
}

async function __findSharedConstantsJson(sourceDir) {
    return new Promise(
        function (resolve, reject) {
            const opts = {
                cwd: sourceDir,
                nodir: true,
                realpath: true
            }

            glob("**/sharedConstants.json", opts, function (err, files) {
                if (err) {
                    reject(err);
                } else {
                    if (!files || files.length <= 0) {
                        reject("No shared constants file could be found.")
                    } else if (files.length > 1) {
                        reject("Two or more copies of the share constants file were found. There should only be 1");
                    } else {
                        resolve(files[0]);
                    }
                }
            });
        }
    );
}

async function __getVersionFromFile(filepath) {
    let constantsDict = await jsonfile.readFile(filepath);

    return constantsDict["version"];
}

module.exports.getVersionNumber = getVersionNumber;