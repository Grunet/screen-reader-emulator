import { createStreamsFromPort } from "../../../../lib/src/portToStreams.js";

async function connectToDevtoolsScripts() {
  return new Promise((resolve) => {
    browser.runtime.onConnect.addListener(__onConnected);

    function __onConnected(port) {
      if (__isDevtoolsPort(port)) {
        const portAsStreams = createStreamsFromPort(port);

        resolve(portAsStreams);
      }
    }

    function __isDevtoolsPort() {
      return true; //Stub for now since there're no other connections to the background scripts
    }
  });
}

export { connectToDevtoolsScripts };
