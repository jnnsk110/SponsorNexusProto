// Sponsor Nexus Prototype Script
console.log('Sponsor Nexus Prototype Loaded');

// Original switchView logic is removed as we moved to multi-page structure.
// This script now handles simulated interactions.

// Example: Chart rendering simulation (if we had charts)
// Example: Form validation (if we had complex forms)

// Currently, navigation is handled by standard HTML links.
// Some pages might have inline scripts for simple toggles (like toggleRoleMenu).

// Modal Logic
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Close modal when clicking outside
window.onclick = function (event) {
    if (event.target.classList.contains('popup-overlay')) {
        event.target.classList.remove('active');
        document.body.style.overflow = '';
    }
};

window.onload = function () {
    console.log('Current Mode: ' + document.body.className);
};
