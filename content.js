// Listen for messages from the background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

  if (message.action === "getSelectedText") {
    sendResponse( {selectedText: window.getSelection().toString() });
    } else {
      sendResponse( { selectedText: ''});
    }
    return true;
});
    
