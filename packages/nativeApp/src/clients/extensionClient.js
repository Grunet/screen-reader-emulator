import { createStreamsFromPort } from "../../../lib/src/portToStreams.js";

/* global NATIVE_APP_ID */

function connectToNativeApp() {
  const port = browser.runtime.connectNative(NATIVE_APP_ID); //FYI this seems to still create a port even if it can't connect to the native app

  return createStreamsFromPort(port);
}

export { connectToNativeApp };
