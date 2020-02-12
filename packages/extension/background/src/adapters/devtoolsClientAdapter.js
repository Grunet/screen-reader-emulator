import { connectToDevtoolsScripts } from "../../../devtools/src/clients/backgroundClient.js";

class DevtoolsClientAdapter {
  constructor(devtoolsClient) {
    this.__devtoolsClient = devtoolsClient;
  }

  get input$() {
    return this.__devtoolsClient.input$;
  }

  get output$() {
    return this.__devtoolsClient.output$;
  }
}

async function createConnectionToDevtoolsScripts() {
  const devtoolsClient = await connectToDevtoolsScripts();

  return new DevtoolsClientAdapter(devtoolsClient);
}

export { createConnectionToDevtoolsScripts };
