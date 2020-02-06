import { createFakeStreams } from "../../../../../lib/test/mocks/src/portToStreamsFakes.js";

function connectToInteractiveFake() {
  return createFakeStreams("NativeAppClient");
}

export { connectToInteractiveFake };
