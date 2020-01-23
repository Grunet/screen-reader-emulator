import { BackgroundClient } from "../../background/src/backgroundClient.js";

console.log("This is from the panel's javascript");

const backgroundClient = new BackgroundClient();

backgroundClient.__inputs$.next(
  "This is from the panel's javascript - through the RxJS Subject"
);
