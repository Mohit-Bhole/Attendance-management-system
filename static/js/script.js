// Main JavaScript file for Smart Attendance Management System

document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializeAttendanceToggles();
    handlePrintAction();
    setupFormValidation();
    setupPasswordToggle();
    fadeInElements();
    fixModalIssues();
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Fix modal flickering and positioning issues
function fixModalIssues() {
    // Get all modal triggers
    const modalTriggers = document.querySelectorAll('[data-bs-toggle="modal"]');
    if (modalTriggers.length === 0) return;

    // For each modal trigger
    modalTriggers.forEach(trigger => {
        // Get the target modal
        const targetModalId = trigger.getAttribute('data-bs-target');
        const targetModal = document.querySelector(targetModalId);
        
        if (targetModal) {
            // Properly initialize the modal
            const modal = new bootstrap.Modal(targetModal, {
                backdrop: 'static',
                keyboard: false
            });
            
            // Prevent multiple modals from opening at once
            trigger.addEventListener('click', function(e) {
                e.preventDefault();
                // Close any open modals first
                document.querySelectorAll('.modal.show').forEach(openModal => {
                    if (openModal !== targetModal) {
                        const bsModal = bootstrap.Modal.getInstance(openModal);
                        if (bsModal) bsModal.hide();
                    }
                });
                // Show this modal
                modal.show();
            });
            
            // Add z-index to ensure proper stacking
            targetModal.style.zIndex = 1055;
        }
    });
}

// Handle attendance toggle switches
function initializeAttendanceToggles() {
    const toggles = document.querySelectorAll('.form-check-input[type="checkbox"]');
    if (toggles.length === 0) return;

    toggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (label && label.classList.contains('status-label')) {
                if (this.checked) {
                    label.textContent = 'Present';
                    label.classList.remove('status-absent');
                    label.classList.add('status-present');
                } else {
                    label.textContent = 'Absent';
                    label.classList.remove('status-present');
                    label.classList.add('status-absent');
                }
            }
        });
    });
}

// Handle print action
function handlePrintAction() {
    const printButtons = document.querySelectorAll('.print-button');
    if (printButtons.length === 0) return;

    printButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            window.print();
        });
    });
}

// Setup form validation
function setupFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    if (forms.length === 0) return;

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

// Setup password visibility toggle
function setupPasswordToggle() {
    const toggles = document.querySelectorAll('.password-toggle');
    if (toggles.length === 0) return;

    toggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const passwordInput = document.querySelector(this.dataset.target);
            if (passwordInput) {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                
                // Toggle icon
                if (this.querySelector('i')) {
                    this.querySelector('i').classList.toggle('bi-eye');
                    this.querySelector('i').classList.toggle('bi-eye-slash');
                }
            }
        });
    });
}

// Add fade-in animation to elements
function fadeInElements() {
    const elements = document.querySelectorAll('.fade-in');
    if (elements.length === 0) return;

    elements.forEach(element => {
        element.style.opacity = 0;
        
        let delay = element.dataset.delay || 0;
        
        setTimeout(() => {
            element.style.opacity = 1;
        }, delay);
    });
}

// Export attendance data to CSV
function exportToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) {
        console.error('Table not found');
        return;
    }
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [], cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            // Get the text content, replace quotes with double quotes
            let data = cols[j].textContent.replace(/"/g, '""');
            // Add the data, enclosed in quotes
            row.push('"' + data + '"');
        }
        
        csv.push(row.join(','));
    }
    
    // Download CSV file
    downloadCSV(csv.join('\n'), filename);
}

// Download CSV file
function downloadCSV(csv, filename) {
    const csvFile = new Blob([csv], {type: 'text/csv'});
    const downloadLink = document.createElement('a');
    
    // File name
    downloadLink.download = filename || 'attendance_data.csv';
    
    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);
    
    // Hide download link
    downloadLink.style.display = 'none';
    
    // Add the link to DOM
    document.body.appendChild(downloadLink);
    
    // Click download link
    downloadLink.click();
    
    // Remove link from DOM
    document.body.removeChild(downloadLink);
}

// Mark all students present
function markAllPresent() {
    const checkboxes = document.querySelectorAll('.attendance-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = true;
        
        // Update label if it exists
        const label = checkbox.nextElementSibling;
        if (label && label.classList.contains('status-label')) {
            label.textContent = 'Present';
            label.classList.remove('status-absent');
            label.classList.add('status-present');
        }
    });
}

// Mark all students absent
function markAllAbsent() {
    const checkboxes = document.querySelectorAll('.attendance-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
        
        // Update label if it exists
        const label = checkbox.nextElementSibling;
        if (label && label.classList.contains('status-label')) {
            label.textContent = 'Absent';
            label.classList.remove('status-present');
            label.classList.add('status-absent');
        }
    });
} 