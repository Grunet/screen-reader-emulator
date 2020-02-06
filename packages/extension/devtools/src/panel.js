import { createConnectionToBackgroundScripts } from "./adapters/backgroundClientAdapter.js";

console.log("This is from the panel's javascript");

const backgroundConnection = createConnectionToBackgroundScripts();
backgroundConnection.inputs$.next(
  "This is from the panel's javascript - to the background connection"
);
