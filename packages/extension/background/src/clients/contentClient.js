import { createStreamsFromPort } from "../../../../lib/src/portToStreams.js";

function connectToBackgroundScripts() {
  const port = browser.runtime.connect();

  return createStreamsFromPort(port);
}

export { connectToBackgroundScripts };
