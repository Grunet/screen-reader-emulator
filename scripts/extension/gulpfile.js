const { src, dest, series } = require('gulp');
const del = require('del');
const bump = require('gulp-bump');

const path = require('path')
const slash = require('slash');

const { getVersionNumber } = require('./versionExtractor.js');

function clean() {
    return del('../../out/extension/**', { force: true });
}

async function build() {
    let sourceDir = __findSourceDirectory();

    let versionNumber = await getVersionNumber(sourceDir.abs);

    let extensionSourceDir = path.join(sourceDir.rel, "extension");

    return src(slash(extensionSourceDir + "/**/manifest.json"))
        .pipe(bump({ version: versionNumber }))
        .pipe(dest('../../out/extension/'));
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

exports.clean = clean;
exports.build = build;
exports.default = series(clean, build);