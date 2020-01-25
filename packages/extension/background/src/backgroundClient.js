import { Observable, Subject } from "../../node_modules/rxjs/_esm2015/index.js"; //Workaround for https://github.com/ReactiveX/rxjs/issues/4416

class BackgroundClient {
  constructor() {
    let port = browser.runtime.connect();

    this.__inputs$ = new Subject();
    this.__inputs$.subscribe({
      next: msg => port.postMessage(msg)
    });

    this.__outputs$ = new Observable(subscriber => {
      port.onMessage.addListener(msg => subscriber.next(msg));
    });
  }

  get inputs$() {
    return this.__inputs$;
  }
  get outputs$() {
    return this.__outputs$;
  }
}

function connectToBackgroundScripts() {
  return new BackgroundClient();
}

export { connectToBackgroundScripts };
