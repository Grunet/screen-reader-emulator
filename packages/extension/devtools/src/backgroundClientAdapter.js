import { connectToBackgroundScripts } from "../../background/src/backgroundClient.js";

class BackgroundClientAdapter {
  constructor() {
    this.__backgroundClient = connectToBackgroundScripts();
  }

  get inputs$() {
    return this.__backgroundClient.inputs$;
  }

  get outputs$() {
    return this.__backgroundClient.outputs$;
  }
}

function createConnectionToBackgroundScripts() {
  return new BackgroundClientAdapter();
}

export { createConnectionToBackgroundScripts };
