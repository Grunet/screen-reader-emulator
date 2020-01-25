import { connectToBackgroundScripts } from "../../background/src/backgroundClient.js";

class BackgroundClientAdapter {
  constructor() {
    this.__backgroundClient = connectToBackgroundScripts();
  }

  get inputs$() {
    return this.__backgroundClient.outputs$;
  }

  get outputs$() {
    return this.__backgroundClient.inputs$;
  }
}

function createConnectionToBackgroundScripts() {
  return new BackgroundClientAdapter();
}

export { createConnectionToBackgroundScripts };
