import { createConnectionToDevtoolsScripts } from "./devtoolsClientAdapter.js";

console.log("This is from the background script");

(async function() {
  const devtoolsConnection = await createConnectionToDevtoolsScripts();

  devtoolsConnection.inputs$.next(
    "This is from the background script - being sent to the devtools scripts"
  );
})();
