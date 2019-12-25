const {
  exec
  // spawn - wasn't able to get this working because of issues similar to the ones here:
  // https://github.com/nodejs/node/issues/3675
  // https://stackoverflow.com/questions/17516772/using-nodejss-spawn-causes-unknown-option-and-error-spawn-enoent-err/17537559#17537559
} = require("child_process");
const { findMatchingOutDir } = require("./dirFinder.js");

exec("web-ext run", {
  cwd: findMatchingOutDir(__dirname).abs
});
//webExtProcess.on("message", msg => console.log(msg)); //Only writes anything after termintation. Need to use "spawn" to get the realtime output
