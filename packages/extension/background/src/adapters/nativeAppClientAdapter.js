import { connectToNativeApp } from "../../../../nativeApp/src/extensionClient.js";

class NativeAppClientAdapter {
  constructor(nativeAppClient) {
    this.__nativeAppClient = nativeAppClient;
  }

  get inputs$() {
    return this.__nativeAppClient.inputs$;
  }

  get outputs$() {
    return this.__nativeAppClient.outputs$;
  }
}

function createConnectionToNativeApp() {
  const nativeAppClient = connectToNativeApp();

  return new NativeAppClientAdapter(nativeAppClient);
}

export { createConnectionToNativeApp };
