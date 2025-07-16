// content.js

let lastScannedText = "";
let warningModal = null;
let currentTargetElement = null;
let formElement = null;
let lastKeyWasEnter = false;

function scanText(text, targetElement) {
    if (text.trim() === "" || text === lastScannedText) {
        return;
    }
    lastScannedText = text;

    chrome.runtime.sendMessage({ action: "scanText", text: text }, (response) => {
        if (chrome.runtime.lastError) {
            console.error("Prompt Poison Shield Error:", chrome.runtime.lastError.message);
            return;
        }

        if (response && response.findings && response.findings.length > 0) {
            displayWarning(response.findings, targetElement);
        } else {
            hideWarning();
        }
    });
}

function displayWarning(findings, targetElement) {
    if (warningModal) {
        // Update existing modal if already visible
        const list = warningModal.querySelector('#pps-findings-list');
        list.innerHTML = ''; // Clear previous findings
    } else {
        // Create the modal if it doesn't exist
        warningModal = document.createElement('div');
        warningModal.id = 'pps-warning-modal';
        warningModal.className = 'pps-modal';
        
        const modalContent = `
            <div class="pps-modal-content">
                <div class="pps-modal-header">
                    🧠 Prompt Poison Shield
                </div>
                <p><strong>Warning:</strong> Potential sensitive data detected in your prompt:</p>
                <ul id="pps-findings-list"></ul>
                <p class="pps-footer">Submitting this data could expose secrets, proprietary information, or personal data. Are you sure you want to continue?</p>
                <div class="pps-button-container">
                    <button id="pps-cancel-btn" class="pps-btn pps-btn-cancel">Cancel & Clear</button>
                    <button id="pps-proceed-btn" class="pps-btn pps-btn-proceed">Proceed Anyway</button>
                </div>
            </div>
        `;
        warningModal.innerHTML = modalContent;
        document.body.appendChild(warningModal);

        // Add event listeners once
        document.getElementById('pps-proceed-btn').addEventListener('click', () => {
            hideWarning();
            // We need a way to bypass the check for this specific submission
            if(formElement) {
                lastKeyWasEnter = true; // Set a flag to allow the next submission
                formElement.requestSubmit(); // Try to resubmit the form
            }
        });

        document.getElementById('pps-cancel-btn').addEventListener('click', () => {
            if (currentTargetElement) {
                if(currentTargetElement.isContentEditable) {
                    currentTargetElement.textContent = '';
                } else {
                    currentTargetElement.value = '';
                }
            }
            hideWarning();
        });
    }

    // Populate the findings list
    const findingsList = warningModal.querySelector('#pps-findings-list');
    findings.forEach(finding => {
        const listItem = document.createElement('li');
        listItem.textContent = `${finding.name}: ${finding.description}`;
        findingsList.appendChild(listItem);
    });

    warningModal.style.display = 'block';
}

function hideWarning() {
    if (warningModal) {
        warningModal.style.display = 'none';
    }
}

function handleInputEvent(event) {
    currentTargetElement = event.target;
    const text = currentTargetElement.isContentEditable ? currentTargetElement.textContent : currentTargetElement.value;
    scanText(text, currentTargetElement);
}

function handleKeyDown(event) {
    // We specifically look for the Enter key press that signifies submission
    if (event.key === 'Enter' && !event.shiftKey) {
        if (warningModal && warningModal.style.display === 'block') {
             if (!lastKeyWasEnter) {
                event.preventDefault(); // Stop the form submission
                event.stopPropagation(); // Stop the event from bubbling up
                console.log("Prompt Poison Shield: Blocked submission due to active warning.");
             } else {
                lastKeyWasEnter = false; // Reset the flag
             }
        }
    }
}

function findForm(element) {
    if (!element) return null;
    let parent = element.parentElement;
    while (parent) {
        if (parent.tagName === 'FORM') {
            return parent;
        }
        parent = parent.parentElement;
    }
    return null;
}

// Attach listeners to the document to catch dynamically loaded elements
document.addEventListener('focusin', (event) => {
    if (event.target.tagName === 'TEXTAREA' || event.target.isContentEditable) {
        currentTargetElement = event.target;
        formElement = findForm(currentTargetElement);
        currentTargetElement.addEventListener('input', handleInputEvent);
        if (formElement) {
            formElement.addEventListener('keydown', handleKeyDown, true); // Use capture to get event first
        } else {
            currentTargetElement.addEventListener('keydown', handleKeyDown, true);

        }
    }
});

document.addEventListener('focusout', (event) => {
     if (event.target.tagName === 'TEXTAREA' || event.target.isContentEditable) {
         event.target.removeEventListener('input', handleInputEvent);
          if (formElement) {
            formElement.removeEventListener('keydown', handleKeyDown, true);
        } else {
             event.target.removeEventListener('keydown', handleKeyDown, true);
        }
     }
});

console.log("Prompt Poison Shield content script injected and is active.");
