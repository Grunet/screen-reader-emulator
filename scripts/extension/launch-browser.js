const webExt = require("web-ext");
const { findMatchingOutDir } = require("./dirFinder.js");

const outDir = findMatchingOutDir(__dirname);

(async function () {
  //webExt.util.logger.consoleStream.makeVerbose();

  const extensionRunner = await webExt.cmd.run(
    {
      sourceDir: outDir.abs,
    },
    {
      shouldExitProgram: false,
    }
  );

  console.log(extensionRunner);
})();
