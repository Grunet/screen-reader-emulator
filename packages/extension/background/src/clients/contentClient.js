import { createStreamsFromPort } from "../../../../lib/src/portToStreams.js";

function connectToBackgroundScripts() {
  let port = browser.runtime.connect();

  return createStreamsFromPort(port);
}

export { connectToBackgroundScripts };
