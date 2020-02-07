import { createStreamsFromPort } from "../../../lib/src/portToStreams.js";

/* global NATIVE_APP_ID */

function connectToNativeApp() {
  const port = browser.runtime.connectNative(NATIVE_APP_ID);

  return createStreamsFromPort(port);
}

export { connectToNativeApp };
