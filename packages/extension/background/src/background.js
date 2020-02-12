import { createConnectionToDevtoolsScripts } from "./adapters/devtoolsClientAdapter.js";
import { createConnectionToNativeApp } from "./adapters/nativeAppClientAdapter.js";

console.log("This is from the background script");

(async function() {
  const devtoolsConnection = await createConnectionToDevtoolsScripts();

  devtoolsConnection.input$.next(
    "This is from the background script - being sent to the devtools scripts"
  );
})();

const nativeAppConnection = createConnectionToNativeApp();
nativeAppConnection.input$.next(
  "This is from the background script - being sent to the native app"
);
