import { Subject } from "../../../node_modules/rxjs/_esm2015/index.js"; //Workaround for https://github.com/ReactiveX/rxjs/issues/4416

class InteractiveFake {
  constructor() {
    this.__inputs$ = new Subject();
    this.__inputs$.subscribe({
      next: msg => console.dir(msg) //Logging to the console instead of posting to the devtools script
    });

    this.__outputs$ = new Subject(); //Switched to a Subject to allow for manual updates to the stream
    this.__getRefOnGlobalFakes().outputs$ = this.__outputs$; //So it can be accessed from the console and updated with calls to "next(msg)"
  }

  __getRefOnGlobalFakes() {
    globalThis.Fakes = globalThis.Fakes || {};
    globalThis.Fakes.DevtoolsClient = {};

    return globalThis.Fakes.DevtoolsClient;
  }

  get inputs$() {
    return this.__inputs$;
  }
  get outputs$() {
    return this.__outputs$;
  }
}

async function connectToInteractiveFake() {
  return new Promise(resolve => {
    resolve(new InteractiveFake());
  });
}

export { connectToInteractiveFake };
