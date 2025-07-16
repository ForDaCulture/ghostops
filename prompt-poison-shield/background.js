// background.js

// Import the rules from rules.js
importScripts('rules.js');

const rules = getDetectionRules();

// Listener for messages from the content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scanText") {
        const textToScan = request.text;
        if (!textToScan) {
            sendResponse({ findings: [] });
            return true; // Indicates we will send a response asynchronously
        }

        const findings = [];
        rules.forEach(rule => {
            if (rule.pattern.test(textToScan)) {
                findings.push({
                    name: rule.name,
                    description: rule.description
                });
            }
        });

        // Send the findings back to the content script
        sendResponse({ findings: findings });
    }
    return true; // Keep the message channel open for the asynchronous response
});

console.log("Prompt Poison Shield background script loaded.");
