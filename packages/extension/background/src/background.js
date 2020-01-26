import { listenForConnectionAttempts } from "./backgroundListener.js";

console.log("This is from the background script");

(async function() {
  const devtoolsConnection = await listenForConnectionAttempts();

  devtoolsConnection.inputs$.next(
    "This is from the background script - being sent to the devtools scripts"
  );
})();
