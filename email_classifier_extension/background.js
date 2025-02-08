chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "classifyEmail") {
    fetch("https://mail-classsifier-extension-8.onrender.com/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: request.emailContent })
    })
    .then(response => response.json())
    .then(data => sendResponse({ classification: data.classification }))
    .catch(error => sendResponse({ error: error.message }));
    return true;
  }
});