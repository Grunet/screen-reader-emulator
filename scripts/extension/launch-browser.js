const path = require("path");
const {
  exec,
  // spawn - wasn't able to get this working because of issues similar to the ones here:
  // https://github.com/nodejs/node/issues/3675
  // https://stackoverflow.com/questions/17516772/using-nodejss-spawn-causes-unknown-option-and-error-spawn-enoent-err/17537559#17537559
} = require("child_process");

const params = __getParametersForLaunch();

exec(params.cmd, { cwd: params.cwd });
//webExtProcess.on("message", msg => console.log(msg)); //Only writes anything after termintation. Need to use "spawn" to get the realtime output

function __getParametersForLaunch() {
  const { findMatchingOutDir } = require("./dirFinder.js");

  const outDir = findMatchingOutDir(__dirname);
  const absPathToWebExtBinary = path.resolve(
    __dirname,
    path.normalize("./node_modules/.bin/web-ext")
  );

  const relPathToWebExtBinary = path.relative(
    outDir.abs,
    absPathToWebExtBinary
  ); //This can't have any spaces in it (at least on Windows)

  const launchBrowserWithExtCmd = __getCmdToExecute(
    relPathToWebExtBinary,
    "run"
  );

  return {
    cmd: launchBrowserWithExtCmd,
    cwd: outDir.abs,
  };
}

function __getCmdToExecute(pathToWebExtBinary, subCommand) {
  return `${pathToWebExtBinary} ${subCommand}`;
}
