import path from "path";
import { fileURLToPath } from "url";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

import express from "express";
import slash from "slash";
import trimEnd from "lodash.trimEnd";

const app = express();
const port = 8000;
const staticAssetsRootDir = path.resolve(path.join(__dirname, "../../../../"));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "backgroundTester.html"));
});

//Switching in test doubles
app.get("/extension/devtools/src/clients/backgroundClient.js", (req, res) => {
  const relPathToFake = path.relative(
    staticAssetsRootDir,
    path.join(__dirname, "interactiveDevtoolsClient.js")
  );

  const urlRelativeToRoot = "/" + slash(relPathToFake);

  res.redirect(urlRelativeToRoot);
});

app.get("/nativeApp/src/clients/extensionClient.js", (req, res) => {
  const relPathToFake = path.relative(
    staticAssetsRootDir,
    path.join(__dirname, "interactiveNativeAppClient.js")
  );

  const urlRelativeToRoot = "/" + slash(relPathToFake);

  res.redirect(urlRelativeToRoot);
});

//Workaround for https://github.com/ReactiveX/rxjs/issues/4416
app.use("/node_modules/rxjs/", (req, res, next) => {
  if (!req.url.includes(".js")) {
    req.url = trimEnd(req.url, "/") + ".js";
  }

  const absPathToRxJsFile = path.resolve(
    path.join(staticAssetsRootDir, "node_modules/rxjs", req.url)
  );

  fs.readFile(absPathToRxJsFile, (err, data) => {
    if (err) {
      next(err);
      return;
    }

    const absPathToTsLibFile = slash(
      path.join(
        path.relative(absPathToRxJsFile, staticAssetsRootDir),
        "node_modules/tslib/tslib.es6.js"
      )
    );

    const modifiedRxJsFileText = data
      .toString()
      .replace(/from "tslib"/g, `from "${absPathToTsLibFile}"`);
    //console.log(modifiedRxJsFileText.split("\n")[0]);

    res.setHeader("content-type", "text/javascript");
    res.send(Buffer.from(modifiedRxJsFileText));
  });
});

app.use(express.static(staticAssetsRootDir));

app.listen(port, () =>
  console.log(`Background script test server listening on port ${port}`)
);
