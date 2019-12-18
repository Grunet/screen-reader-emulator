const { src, dest, series } = require("gulp");
const mergeStream = require("merge-stream");
const webpack = require("webpack-stream");
const jeditor = require("gulp-json-editor");

const del = require("del");

const path = require("path");
const slash = require("slash");

const { getVersionNumber } = require("./versionExtractor.js");

function clean() {
  return del(slash(__findOutDirectory().rel) + "/**", { force: true });
}

async function build() {
  let extensionSourceDir = __findPkgDirectory();

  let versionNumber = await getVersionNumber();

  const contentBundleFilename = "content.js";
  const backgroundBundleFilename = "background.js";
  let outDir = __findOutDirectory();

  return mergeStream(
    src(slash(extensionSourceDir.rel)) //this might not matter to the webpack call
      .pipe(
        webpack({
          entry: {
            [contentBundleFilename]: path.join(
              extensionSourceDir.abs,
              "content",
              "src",
              "content.js"
            ),
            [backgroundBundleFilename]: path.join(
              extensionSourceDir.abs,
              "background",
              "src",
              "background.js"
            )
          },
          output: {
            filename: "[name]"
          }
        })
      ),
    src(slash(extensionSourceDir.rel + "/**/manifest.json")).pipe(
      jeditor({
        content_scripts: [
          {
            js: [contentBundleFilename],
            matches: ["<all_urls>"]
          }
        ],
        background: {
          scripts: [backgroundBundleFilename]
        },
        version: versionNumber
      })
    )
  ).pipe(dest(slash(outDir.rel)));
}

function __findOutDirectory() {
  let scriptsDirParts = __dirname.split(path.sep);
  let index = scriptsDirParts.indexOf("scripts");
  if (index < 0) {
    throw new Error("Unable to find source directory from scripts directory");
  }

  let outDirParts = scriptsDirParts.slice();
  outDirParts[index] = "out";

  let outDirAbsPath = path.join(...outDirParts);
  let outDirRelPath = path.relative(__dirname, outDirAbsPath);

  return {
    abs: outDirAbsPath,
    rel: outDirRelPath
  };
}

function __findPkgDirectory() {
  let scriptsDirParts = __dirname.split(path.sep);
  let index = scriptsDirParts.indexOf("scripts");
  if (index < 0) {
    throw new Error("Unable to find source directory from scripts directory");
  }

  let pkgDirParts = scriptsDirParts.slice();
  pkgDirParts[index] = "packages";

  let pkgDirAbsPath = path.join(...pkgDirParts);
  let pkgDirRelPath = path.relative(__dirname, pkgDirAbsPath);

  return {
    abs: pkgDirAbsPath,
    rel: pkgDirRelPath
  };
}

exports.clean = clean;
exports.build = build;
exports.default = series(clean, build);
