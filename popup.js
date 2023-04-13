
async function summarizeClick(event) {
  const activeTab = await chrome.tabs.query({
	lastFocusedWindow: true,
        active: true
    });
  chrome.tabs.sendMessage(activeTab[0].id, {type: "summarize" });
  text=document.getSelection().toString().trim() ;
  if (!text) {
      alert(
        "No text found. Select this option after right clicking on a textarea that contains text or on a selected portion of text."
      );
      return;
    }

  console.log(text)
  fetch("http://localhost:8000/summarize", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Credentials" : true
    },
    body: JSON.stringify({ text }),
    //mode: "no-cors"
  })
    .then((response) => response.json())
    .then(async (data) => {
      // Use original text element and fallback to current active text element

  document.getElementById('editor').value ="hello this ais ohia";
  //document.getElementById('editor').value =`${data.reply}`;
  
}
);
}

// Constants for character limit
const CHARACTER_LIMIT = 1000;

async function getSelectedText() {
    const queryOptions = { active: true, currentWindow: true };
    const [tab] = await chrome.tabs.query(queryOptions);

    // Inject the content script
    await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
    });

    return new Promise(async (resolve) => {
        // Function to handle the response
        const handleResponse = (response) => {
            if (chrome.runtime.lastError) {
                console.error(chrome.runtime.lastError.message);
                resolve('');
            } else {
                if (response && response.selectedText) {
                    resolve(response.selectedText);
                } else {
                    resolve('');
                }
            }
        };

        // Send message to the main frame
        chrome.tabs.sendMessage(tab.id, { action: "getSelectedText" }, handleResponse);

        // If the main frame does not return any selected text, send message to all frames
        const allFrames = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: () => {
                return Array.from(document.querySelectorAll("iframe")).map((iframe, index) => index);
            },
        });

        for (const index of allFrames[0].result) {
            chrome.tabs.sendMessage(tab.id, { action: "getSelectedText", frameId: index }, handleResponse);
        }
    });
}

async function sendRequest(action, text) {
    // Replace with your server's API endpoint and API key
    const apiUrl = 'http://localhost:8000/router';

    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
	    'Access-Control-Allow-Origin': '*',
	    'Access-Control-Allow-Credentials' : true
        },
        body: JSON.stringify({ action, text })
    });

    const result = await response.json();
    return result.output;
}

async function replaceSelectedText(newText) {
    const queryOptions = { active: true, currentWindow: true };
    const [tab] = await chrome.tabs.query(queryOptions);

    chrome.tabs.executeScript(tab.id, {
        code: `document.execCommand('insertText', false, '${newText}')`
    });
}

// Function to update the output area
function updateOutput(newText) {
    document.getElementById("outputText").value = newText;
}

// Add event listeners to the buttons
document.addEventListener("DOMContentLoaded", async () => {
    const selectedText = await getSelectedText();
    document.getElementById("selectedText").value = selectedText.slice(0, CHARACTER_LIMIT);

    const buttons = document.querySelectorAll("button");
    buttons.forEach((btn) => {
        btn.disabled = selectedText.length === 0 || selectedText.length > CHARACTER_LIMIT;
        btn.addEventListener("click", async () => {
            const action = btn.id.replace("Btn", "").toLowerCase();
            const result = await sendRequest(action, selectedText);
            updateOutput(result);
            replaceSelectedText(result);
        });
    });
});
