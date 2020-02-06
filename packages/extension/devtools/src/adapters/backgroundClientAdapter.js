import { connectToBackgroundScripts } from "../../../background/src/contentClient.js";

class BackgroundClientAdapter {
  constructor(backgroundClient) {
    this.__backgroundClient = backgroundClient;
  }

  get inputs$() {
    return this.__backgroundClient.inputs$;
  }

  get outputs$() {
    return this.__backgroundClient.outputs$;
  }
}

function createConnectionToBackgroundScripts() {
  const backgroundClient = connectToBackgroundScripts();

  return new BackgroundClientAdapter(backgroundClient);
}

export { createConnectionToBackgroundScripts };
