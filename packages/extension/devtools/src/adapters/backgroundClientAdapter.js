import { connectToBackgroundScripts } from "../../../background/src/clients/contentClient.js";

class BackgroundClientAdapter {
  constructor(backgroundClient) {
    this.__backgroundClient = backgroundClient;
  }

  get input$() {
    return this.__backgroundClient.input$;
  }

  get output$() {
    return this.__backgroundClient.output$;
  }
}

function createConnectionToBackgroundScripts() {
  const backgroundClient = connectToBackgroundScripts();

  return new BackgroundClientAdapter(backgroundClient);
}

export { createConnectionToBackgroundScripts };
