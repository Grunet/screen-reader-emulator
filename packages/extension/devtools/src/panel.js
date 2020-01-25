import { createConnectionToBackgroundScripts } from "./backgroundClientAdapter.js";

console.log("This is from the panel's javascript");

const backgroundConnection = createConnectionToBackgroundScripts();
backgroundConnection.outputs$.next(
  "This is from the panel's javascript - through the background connection"
);
