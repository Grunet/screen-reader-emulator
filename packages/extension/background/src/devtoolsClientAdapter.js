import { connectToDevtoolsScripts } from "../../devtools/src/devtoolsClient.js";

class DevtoolsClientAdapter {
  constructor(devtoolsClient) {
    this.__devtoolsClient = devtoolsClient;
  }

  get inputs$() {
    return this.__devtoolsClient.inputs$;
  }

  get outputs$() {
    return this.__devtoolsClient.outputs$;
  }
}

async function createConnectionToDevtoolsScripts() {
  const devtoolsClient = await connectToDevtoolsScripts();

  return new DevtoolsClientAdapter(devtoolsClient);
}

export { createConnectionToDevtoolsScripts };
