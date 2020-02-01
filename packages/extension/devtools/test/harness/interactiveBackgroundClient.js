import { InteractiveFake } from "../../../background/test/mocks/src/backgroundClientFakes.js";

function connectToBackgroundScripts() {
  return new InteractiveFake();
}

export { connectToBackgroundScripts };
