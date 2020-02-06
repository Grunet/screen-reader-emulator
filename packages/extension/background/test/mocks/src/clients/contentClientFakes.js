import { createFakeStreams } from "../../../../../../lib/test/mocks/src/portToStreamsFakes.js";

function connectToInteractiveFake() {
  return createFakeStreams("BackgroundClient");
}

export { connectToInteractiveFake };
