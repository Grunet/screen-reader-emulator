import { Subject } from "../../../../node_modules/rxjs/_esm2015/index.js"; //Workaround for https://github.com/ReactiveX/rxjs/issues/4416

class InteractiveFake {
  constructor(globalPropName) {
    this.__input$ = new Subject();
    this.__input$.subscribe({
      next: (msg) => console.dir(msg), //Logging to the console instead of posting to the port
    });

    this.__output$ = new Subject(); //Switched to a Subject to allow for manual updates to the stream
    this.__getRefOnGlobalFakes(globalPropName).output$ = this.__output$; //So it can be accessed from the console and updated with calls to "next(msg)"
  }

  __getRefOnGlobalFakes(propName) {
    globalThis.Fakes = globalThis.Fakes || {};
    globalThis.Fakes[propName] = {};

    return globalThis.Fakes[propName];
  }

  get input$() {
    return this.__input$;
  }
  get output$() {
    return this.__output$;
  }
}

function createFakeStreams(propNameForGlobalAccess) {
  return new InteractiveFake(propNameForGlobalAccess);
}

export { createFakeStreams };
