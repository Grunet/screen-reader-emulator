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

const {
  getVersionNumber,
  getExtensionId,
  getNativeAppId,
} = require("./constantsExtractor.js");
const { findMatchingOutDir, findMatchingPkgDir } = require("./dirFinder.js");

function clean() {
  return del(slash(findMatchingOutDir(__dirname).rel) + "/**", { force: true });
}

async function build() {
  const extensionSourceDir = findMatchingPkgDir(__dirname);
  const outDir = findMatchingOutDir(__dirname);

  const versionNumber = await getVersionNumber();
  const extensionId = await getExtensionId();
  const nativeAppId = await getNativeAppId();

  const devtoolsBundleFilename = "devtools.js";
  const panelBundleFilename = "devtools-panel.js";
  const backgroundBundleFilename = "background.js";

  const devtoolsHtmlFilename = "devtools-page.html";
  const panelHtmlFilename = "panel.html";

  const iconFilename = "NotImplementedYet.png"; // TODO - The icon hasn't been decided on yet, so stubbing it for now

  return mergeStream(
    __getJsBundlingStream(
      extensionSourceDir,
      {
        devtools: devtoolsBundleFilename,
        panel: panelBundleFilename,
        background: backgroundBundleFilename,
      },
      {
        NATIVE_APP_ID: nativeAppId,
        ASSETS_PATH_TO_ICON: iconFilename,
        DEVTOOLS_PATH_TO_PANEL_HTML: panelHtmlFilename,
      }
    ),
    __getHtmlCreationStream(
      __dirname + "/jsShell.html",
      devtoolsHtmlFilename,
      devtoolsBundleFilename
    ),
    __getHtmlCreationStream(
      __dirname + "/jsShell.html",
      panelHtmlFilename,
      panelBundleFilename
    ),
    __getManifestHydrationStream(extensionSourceDir.rel + "/**/manifest.json", {
      devtoolsHtmlFilename: devtoolsHtmlFilename,
      backgroundBundleFilename: backgroundBundleFilename,
      versionNumber: versionNumber,
      extensionId: extensionId,
    })
  ).pipe(dest(slash(outDir.rel)));
}

function __getJsBundlingStream(
  extensionSourceDir,
  bundleFilenames,
  globalConstants
) {
  const globalConstantsAsJSON = Object.fromEntries(
    Object.entries(globalConstants).map(([k, v]) => [k, JSON.stringify(v)])
  );

  return src(slash(extensionSourceDir.rel)) //this might not matter to the webpack call
    .pipe(
      webpackStream({
        plugins: [new webpack.DefinePlugin(globalConstantsAsJSON)],
        entry: {
          [bundleFilenames.devtools]: path.join(
            extensionSourceDir.abs,
            "devtools",
            "src",
            "index.js"
          ),
          [bundleFilenames.panel]: path.join(
            extensionSourceDir.abs,
            "devtools",
            "src",
            "panel.js"
          ),
          [bundleFilenames.background]: path.join(
            extensionSourceDir.abs,
            "background",
            "src",
            "background.js"
          ),
        },
        output: {
          filename: "[name]",
        },
      })
    );
}

function __getHtmlCreationStream(
  pathToHtmlTemplate,
  filenameForNewHtml,
  pathToJsFromManifest
) {
  return src(slash(pathToHtmlTemplate))
    .pipe(template({ pathToJsFromManifest: pathToJsFromManifest }))
    .pipe(rename(filenameForNewHtml));
}

function __getManifestHydrationStream(globForManifest, inputs) {
  const {
    devtoolsHtmlFilename,
    backgroundBundleFilename,
    versionNumber,
    extensionId,
  } = inputs;

  return src(slash(globForManifest)).pipe(
    jeditor({
      browser_specific_settings: {
        gecko: {
          id: extensionId,
        },
      },
      devtools_page: devtoolsHtmlFilename,
      background: {
        scripts: [backgroundBundleFilename],
      },
      version: versionNumber,
    })
  );
}

exports.clean = clean;
exports.build = build;
exports.default = series(clean, build);
