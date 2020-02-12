import { connectToNativeApp } from "../../../../nativeApp/src/clients/extensionClient.js";

class NativeAppClientAdapter {
  constructor(nativeAppClient) {
    this.__nativeAppClient = nativeAppClient;
  }

  get input$() {
    return this.__nativeAppClient.input$;
  }

  get output$() {
    return this.__nativeAppClient.output$;
  }
}

function createConnectionToNativeApp() {
  const nativeAppClient = connectToNativeApp();

  return new NativeAppClientAdapter(nativeAppClient);
}

export { createConnectionToNativeApp };
