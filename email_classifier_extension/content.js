document.addEventListener("DOMContentLoaded", () => {
    let emailBody = document.querySelector(".a3s");
    if (emailBody) {
      chrome.runtime.sendMessage({ action: "classifyEmail", emailContent: emailBody.innerText }, response => {
        if (response.classification) {
          emailBody.style.border = response.classification === "spam" ? "3px solid red" : "3px solid green";
        }
      });
    }
  });
  