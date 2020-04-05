const path = require("path");

function findMatchingOutDir(scriptsSubPath) {
  const scriptsDirParts = scriptsSubPath.split(path.sep);
  const index = scriptsDirParts.indexOf("scripts");
  if (index < 0) {
    throw new Error("Unable to find source directory from scripts directory");
  }

  const outDirParts = scriptsDirParts.slice();
  outDirParts[index] = "out";

  const outDirAbsPath = path.join(...outDirParts);
  const outDirRelPath = path.relative(scriptsSubPath, outDirAbsPath);

  return {
    abs: outDirAbsPath,
    rel: outDirRelPath,
  };
}

function findMatchingPkgDir(scriptsSubPath) {
  const scriptsDirParts = scriptsSubPath.split(path.sep);
  const index = scriptsDirParts.indexOf("scripts");
  if (index < 0) {
    throw new Error("Unable to find source directory from scripts directory");
  }

  const pkgDirParts = scriptsDirParts.slice();
  pkgDirParts[index] = "packages";

  const pkgDirAbsPath = path.join(...pkgDirParts);
  const pkgDirRelPath = path.relative(scriptsSubPath, pkgDirAbsPath);

  return {
    abs: pkgDirAbsPath,
    rel: pkgDirRelPath,
  };
}

module.exports.findMatchingOutDir = findMatchingOutDir;
module.exports.findMatchingPkgDir = findMatchingPkgDir;
