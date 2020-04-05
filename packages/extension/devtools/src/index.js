/* global ASSETS_PATH_TO_ICON, DEVTOOLS_PATH_TO_PANEL_HTML*/

function handleShown() {}

function handleHidden() {}

browser.devtools.panels
  .create("Screen Reader", ASSETS_PATH_TO_ICON, DEVTOOLS_PATH_TO_PANEL_HTML)
  .then((newPanel) => {
    newPanel.onShown.addListener(handleShown);
    newPanel.onHidden.addListener(handleHidden);
  });
