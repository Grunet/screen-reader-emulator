import { createStreamsFromPort } from "../../lib/src/portToStreams.js";

class BackgroundClient {
  constructor() {
    let port = browser.runtime.connect();

    this.__streams = createStreamsFromPort(port);
  }

  get inputs$() {
    return this.__streams.inputs$;
  }
  get outputs$() {
    return this.__streams.outputs$;
  }
}

function connectToBackgroundScripts() {
  return new BackgroundClient();
}

export { connectToBackgroundScripts };
