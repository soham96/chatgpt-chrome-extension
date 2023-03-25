// Create a context menu item
chrome.contextMenus.create({
  id: "ask-writer",
  title: "Write for me",
  contexts: ["all"],
});

chrome.contextMenus.create({
  title: "Expand Text",
  id: "expand",
  parentId: "ask-writer",
  contexts:["selection"],
});

chrome.contextMenus.create({
  title: "Formalize",
  id: "formalize",
  parentId: "ask-writer",
  contexts:["selection"],
});

// Listen for when the user clicks on the context menu item
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "expand") {
    // Send a message to the content script
    chrome.tabs.sendMessage(tab.id, { type: "expand" });
  }
});

