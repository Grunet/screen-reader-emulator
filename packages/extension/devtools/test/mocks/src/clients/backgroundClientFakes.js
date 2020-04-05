import { createFakeStreams } from "../../../../../../lib/test/mocks/src/portToStreamsFakes.js";

async function connectToInteractiveFake() {
  return new Promise((resolve) => {
    resolve(createFakeStreams("DevtoolsClient"));
  });
}

export { connectToInteractiveFake };
