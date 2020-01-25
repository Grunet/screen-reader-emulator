import { InteractiveFake } from "../mocks/backgroundClientFakes.js";

function connectToBackgroundScripts() {
  return new InteractiveFake();
}

export { connectToBackgroundScripts };
