const { src, dest, series } = require('gulp');
const mergeStream = require('merge-stream');
const webpack = require('webpack-stream');
const jeditor = require("gulp-json-editor");

const del = require('del');

const path = require('path');
const slash = require('slash');

const { getVersionNumber } = require('./versionExtractor.js');

function clean() {
    return del(slash(__findOutDirectory().rel) + '/**', { force: true });
}

async function build() {
    let extensionSourceDir = __findPkgDirectory().rel;
    let outDir = __findOutDirectory().rel;

    let versionNumber = await getVersionNumber();

    return mergeStream(
        src(slash(extensionSourceDir)) //this might not matter to the webpack call
            .pipe(webpack({
                entry: {
                    'content.js': path.join(__dirname, '../../packages/extension/content/src/content.js'),
                    'background.js': path.join(__dirname, '../../packages/extension/background/src/background.js')
                },
                output: {
                    filename: '[name]',
                }
            })),
        src(slash(extensionSourceDir + "/**/manifest.json"))
            .pipe(jeditor({
                'background': {
                    'scripts': ['background.js']
                },
                'content_scripts': [
                    {
                        'js': ['content.js'],
                        'matches': ['<all_urls>']
                    }
                ],
                'version': versionNumber
            }))
    )
        .pipe(dest(slash(outDir)));
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
    }
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
    }
}

exports.clean = clean;
exports.build = build;
exports.default = series(clean, build);