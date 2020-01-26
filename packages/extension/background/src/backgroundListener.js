import { createAdaptedDevtoolsStreams } from "./devtoolsStreamsAdapter.js";

async function listenForConnectionAttempts() {
  return new Promise(resolve => {
    browser.runtime.onConnect.addListener(__onConnected);

    function __onConnected(port) {
      resolve(new createAdaptedDevtoolsStreams(port));
    }
  });
}

export { listenForConnectionAttempts };
