const path = require("path");
const glob = require("glob");
const jsonfile = require("jsonfile");

async function getVersionNumber() {
  let constantsFilePath = await __findPathToConstantsFile();

  let versionNumber = await __getVersionFromFile(constantsFilePath);

  return versionNumber;
}

async function getNativeAppId() {
  let constantsFilePath = await __findPathToConstantsFile();

  let nativeAppId = await __getNativeAppIdFromFile(constantsFilePath);

  return nativeAppId;
}

async function __findPathToConstantsFile() {
  let sourceDir = __findRootPackageDirectory().abs;

  return __findSharedConstantsJson(sourceDir);
}

function __findRootPackageDirectory() {
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
  };
}

async function __findSharedConstantsJson(sourceDir) {
  return new Promise(function(resolve, reject) {
    const opts = {
      cwd: sourceDir,
      nodir: true,
      realpath: true
    };

    glob("**/sharedConstants.json", opts, function(err, files) {
      if (err) {
        reject(err);
      } else {
        if (!files || files.length <= 0) {
          reject("No shared constants file could be found.");
        } else if (files.length > 1) {
          reject(
            "Two or more copies of the share constants file were found. There should only be 1"
          );
        } else {
          resolve(files[0]);
        }
      }
    });
  });
}

async function __getVersionFromFile(filepath) {
  let constantsDict = await __getConstantsDict(filepath);

  return constantsDict["version"];
}

async function __getNativeAppIdFromFile(filepath) {
  let constantsDict = await __getConstantsDict(filepath);

  return constantsDict["ids"]["nativeApp"];
}

async function __getConstantsDict(filepath) {
  return jsonfile.readFile(filepath);
}

module.exports.getVersionNumber = getVersionNumber;
module.exports.getNativeAppId = getNativeAppId;
