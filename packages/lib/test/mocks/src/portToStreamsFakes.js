import { Subject } from "../../../../node_modules/rxjs/_esm2015/index.js"; //Workaround for https://github.com/ReactiveX/rxjs/issues/4416

class InteractiveFake {
  constructor(globalPropName) {
    this.__inputs$ = new Subject();
    this.__inputs$.subscribe({
      next: msg => console.dir(msg) //Logging to the console instead of posting to the port
    });

    this.__outputs$ = new Subject(); //Switched to a Subject to allow for manual updates to the stream
    this.__getRefOnGlobalFakes(globalPropName).outputs$ = this.__outputs$; //So it can be accessed from the console and updated with calls to "next(msg)"
  }

  __getRefOnGlobalFakes(propName) {
    globalThis.Fakes = globalThis.Fakes || {};
    globalThis.Fakes[propName] = {};

    return globalThis.Fakes[propName];
  }

  get inputs$() {
    return this.__inputs$;
  }
  get outputs$() {
    return this.__outputs$;
  }
}

function createFakeStreams(propNameForGlobalAccess) {
  return new InteractiveFake(propNameForGlobalAccess);
}

export { createFakeStreams };
