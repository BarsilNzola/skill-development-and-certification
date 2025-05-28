document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.querySelector('input[type="file"]');
    const previewBox = document.getElementById('image-preview');
    const form = document.querySelector('form');

    // Initialize preview box
    if (previewBox) {
        previewBox.classList.add('empty');
    }

    // Enhanced file input handling
    if (imageInput && previewBox) {
        // Click to upload
        imageInput.addEventListener('change', handleFileSelect);
        
        // Drag and drop functionality
        previewBox.addEventListener('dragover', (e) => {
            e.preventDefault();
            previewBox.classList.add('drag-over');
        });

        previewBox.addEventListener('dragleave', () => {
            previewBox.classList.remove('drag-over');
        });

        previewBox.addEventListener('drop', (e) => {
            e.preventDefault();
            previewBox.classList.remove('drag-over');
            
            if (e.dataTransfer.files.length) {
                imageInput.files = e.dataTransfer.files;
                handleFileSelect({ target: imageInput });
            }
        });

        // Click on preview to trigger file input
        previewBox.addEventListener('click', () => {
            imageInput.click();
        });
    }

    function handleFileSelect(event) {
        const file = event.target.files[0];
        const validImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];

        if (file) {
            if (!validImageTypes.includes(file.type)) {
                showAlert('Please select a valid image file (JPEG, PNG, GIF, or WEBP)', 'error');
                return;
            }

            if (file.size > 5 * 1024 * 1024) { // 5MB limit
                showAlert('Image size should be less than 5MB', 'error');
                return;
            }

            const reader = new FileReader();

            reader.onloadstart = () => {
                previewBox.innerHTML = '<p>Loading image...</p>';
            };

            reader.onload = (e) => {
                previewBox.classList.remove('empty');
                previewBox.innerHTML = `<img src="${e.target.result}" alt="Profile Preview">`;
            };

            reader.onerror = () => {
                previewBox.classList.add('empty');
                previewBox.innerHTML = '<p>Error loading image</p>';
            };

            reader.readAsDataURL(file);
        } else {
            previewBox.classList.add('empty');
            previewBox.innerHTML = '<p>No image selected</p>';
        }
    }

    // Form submission handling
    if (form) {
        form.addEventListener('submit', (e) => {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Uploading...';
            }
        });
    }

    // Alert message handling
    function showAlert(message, type = 'success') {
        // Remove existing alerts
        const existingAlert = document.querySelector('.alert');
        if (existingAlert) {
            existingAlert.remove();
        }

        const alertDiv = document.createElement('div');
        alertDiv.className = `alert ${type}`;
        alertDiv.textContent = message;

        // Insert after the h2 or at the top of the form
        const h2 = document.querySelector('.profile-edit h2');
        if (h2) {
            h2.insertAdjacentElement('afterend', alertDiv);
        } else {
            form.prepend(alertDiv);
        }

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.style.opacity = '0';
            setTimeout(() => alertDiv.remove(), 300);
        }, 5000);
    }

    // Accessibility improvements
    const interactiveElements = document.querySelectorAll('button, input, [tabindex]');
    interactiveElements.forEach(el => {
        el.addEventListener('focus', function() {
            this.style.outline = '2px solid #004466';
            this.style.outlineOffset = '3px';
        });
        
        el.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
});