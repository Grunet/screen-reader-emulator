import { createStreamsFromPort } from "../../lib/src/portToStreams.js";

class DevtoolsPortToStreamsAdapter {
  constructor(devtoolsPort) {
    this.__devtoolsStreams = createStreamsFromPort(devtoolsPort);
  }

  get inputs$() {
    return this.__devtoolsStreams.inputs$;
  }

  get outputs$() {
    return this.__devtoolsStreams.outputs$;
  }
}

function createAdaptedDevtoolsStreams(devtoolsPort) {
  return new DevtoolsPortToStreamsAdapter(devtoolsPort);
}

export { createAdaptedDevtoolsStreams };
