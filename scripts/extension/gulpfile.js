const { src, dest, series } = require("gulp");
const mergeStream = require("merge-stream");
const webpack = require("webpack-stream");
const jeditor = require("gulp-json-editor");

const del = require("del");

const path = require("path");
const slash = require("slash");

const { getVersionNumber } = require("./versionExtractor.js");
const { findMatchingOutDir, findMatchingPkgDir } = require("./dirFinder.js");

function clean() {
  return del(slash(findMatchingOutDir(__dirname).rel) + "/**", { force: true });
}

async function build() {
  let extensionSourceDir = findMatchingPkgDir(__dirname);

  let versionNumber = await getVersionNumber();

  const contentBundleFilename = "content.js";
  const backgroundBundleFilename = "background.js";
  let outDir = findMatchingOutDir(__dirname);

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

exports.clean = clean;
exports.build = build;
exports.default = series(clean, build);
