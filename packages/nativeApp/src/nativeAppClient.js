import { createStreamsFromPort } from "../../lib/src/portToStreams.js";

function connectToNativeApp() {
  let port = browser.runtime.connectNative(
    "TO DO - replace this by something that can be switched out for the native app id during the webpack build"
  );

  return createStreamsFromPort(port);
}

export { connectToNativeApp };
