const express = require("express");
const path = require("path");
const slash = require("slash");
const trimEnd = require("lodash.trimEnd");

const app = express();
const port = 8000;

const staticAssetsRootDir = path.resolve(path.join(__dirname, "../../../../"));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "backgroundTester.html"));
});

//Switching in test doubles
app.get("/extension/devtools/src/backgroundClient.js", (req, res) => {
  const relPathToFake = path.relative(
    staticAssetsRootDir,
    path.join(__dirname, "interactiveDevtoolsClient.js")
  );

  const urlRelativeToRoot = "/" + slash(relPathToFake);

  res.redirect(urlRelativeToRoot);
});

app.get("/nativeApp/src/extensionClient.js", (req, res) => {
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

  next();
});

app.use(express.static(staticAssetsRootDir));

app.listen(port, () =>
  console.log(`Background script test server listening on port ${port}`)
);
