import { Observable, Subject } from "../../node_modules/rxjs/dist/esm/index.js"; //Workaround for https://github.com/ReactiveX/rxjs/issues/4416

class PortToStreamsAdapter {
  constructor(port) {
    this.__input$ = new Subject();
    this.__input$.subscribe({
      next: (msg) => port.postMessage(msg),
    });

    this.__output$ = new Observable((subscriber) => {
      port.onMessage.addListener((msg) => subscriber.next(msg));
    });
  }

  get input$() {
    return this.__input$;
  }
  get output$() {
    return this.__output$;
  }
}

function createStreamsFromPort(port) {
  return new PortToStreamsAdapter(port);
}

export { createStreamsFromPort };
