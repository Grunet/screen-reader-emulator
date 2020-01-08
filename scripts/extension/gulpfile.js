const { src, dest, series } = require("gulp");
const mergeStream = require("merge-stream");
const webpack = require("webpack");
const webpackStream = require("webpack-stream");
const jeditor = require("gulp-json-editor");
const template = require("gulp-template");
const rename = require("gulp-rename");

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

  const devtoolsBundleFilename = "devtools.js";
  const panelBundleFilename = "devtools-panel.js";
  const backgroundBundleFilename = "background.js";

  const devtoolsHtmlFilename = "devtools-page.html";
  const panelHtmlFilename = "panel.html";

  const iconFilename = "NotImplementedYet.png"; // TODO - The icon hasn't been decided on yet, so stubbing it for now

  let outDir = findMatchingOutDir(__dirname);

  return mergeStream(
    src(slash(extensionSourceDir.rel)) //this might not matter to the webpack call
      .pipe(
        webpackStream({
          plugins: [
            new webpack.DefinePlugin({
              ASSETS_PATH_TO_ICON: JSON.stringify(iconFilename),
              DEVTOOLS_PATH_TO_PANEL_HTML: JSON.stringify(panelHtmlFilename)
            })
          ],
          entry: {
            [devtoolsBundleFilename]: path.join(
              extensionSourceDir.abs,
              "devtools",
              "src",
              "index.js"
            ),
            [panelBundleFilename]: path.join(
              extensionSourceDir.abs,
              "devtools",
              "src",
              "panel.js"
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
    src(slash(__dirname + "/jsShell.html"))
      .pipe(template({ pathToJsFromManifest: devtoolsBundleFilename }))
      .pipe(rename(devtoolsHtmlFilename)),
    src(slash(__dirname + "/jsShell.html"))
      .pipe(template({ pathToJsFromManifest: panelBundleFilename }))
      .pipe(rename(panelHtmlFilename)),
    src(slash(extensionSourceDir.rel + "/**/manifest.json")).pipe(
      jeditor({
        devtools_page: devtoolsHtmlFilename,
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
