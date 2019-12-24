const path = require("path");

function findMatchingOutDir(scriptsSubPath) {
  let scriptsDirParts = scriptsSubPath.split(path.sep);
  let index = scriptsDirParts.indexOf("scripts");
  if (index < 0) {
    throw new Error("Unable to find source directory from scripts directory");
  }

  let outDirParts = scriptsDirParts.slice();
  outDirParts[index] = "out";

  let outDirAbsPath = path.join(...outDirParts);
  let outDirRelPath = path.relative(scriptsSubPath, outDirAbsPath);

  return {
    abs: outDirAbsPath,
    rel: outDirRelPath
  };
}

function findMatchingPkgDir(scriptsSubPath) {
  let scriptsDirParts = scriptsSubPath.split(path.sep);
  let index = scriptsDirParts.indexOf("scripts");
  if (index < 0) {
    throw new Error("Unable to find source directory from scripts directory");
  }

  let pkgDirParts = scriptsDirParts.slice();
  pkgDirParts[index] = "packages";

  let pkgDirAbsPath = path.join(...pkgDirParts);
  let pkgDirRelPath = path.relative(scriptsSubPath, pkgDirAbsPath);

  return {
    abs: pkgDirAbsPath,
    rel: pkgDirRelPath
  };
}

module.exports.findMatchingOutDir = findMatchingOutDir;
module.exports.findMatchingPkgDir = findMatchingPkgDir;
