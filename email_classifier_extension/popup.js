// popup.js
document.getElementById("classifyBtn").addEventListener("click", () => {
  let emailText = document.getElementById("emailContent").value;
  chrome.runtime.sendMessage({ action: "classifyEmail", emailContent: emailText }, response => {
    document.getElementById("result").innerText = response.classification ? `Classification: ${response.classification}` : "Error";
  });
});