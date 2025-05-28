document.addEventListener('DOMContentLoaded', function() {
    // Mark Lesson as Completed
    const completeBtn = document.getElementById('mark-complete-btn');
    if (completeBtn) {
        completeBtn.addEventListener('click', function() {
            const lessonId = this.dataset.lessonId;
            const btn = this;
            
            btn.disabled = true;
            btn.textContent = 'Processing...';
            
            fetch(`/lesson/${lessonId}/complete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    // Create a temporary success message
                    const successMsg = document.createElement('div');
                    successMsg.className = 'alert success';
                    successMsg.textContent = data.message;
                    document.querySelector('.completion-section').prepend(successMsg);
                    
                    // Update UI
                    btn.remove();
                    const completionText = document.createElement('p');
                    completionText.textContent = 'This lesson is completed ✅';
                    document.querySelector('.completion-section').appendChild(completionText);
                    
                    // Remove success message after 5 seconds
                    setTimeout(() => successMsg.remove(), 5000);
                    
                    // Enable certificate button if applicable
                    const certificateButton = document.getElementById('certificate-btn');
                    if (certificateButton) {
                        certificateButton.disabled = false;
                        certificateButton.classList.add('enabled');
                    }
                } else {
                    throw new Error(data.message || 'Unknown error occurred');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                btn.disabled = false;
                btn.textContent = 'Mark as Completed';
                alert(`Error: ${error.message}`);
            });
        });
    }

    // Certificate Button Event Listener 
    document.getElementById('certificate-btn')?.addEventListener('click', function() {
        alert('Congratulations! Your certificate is ready to download.');
        // Add logic for downloading the certificate if needed
    });

    // Form submission handling
    const assignmentForm = document.querySelector('.assignment-section form');
    if (assignmentForm) {
        assignmentForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Submitting...';
            }
            
            // Optional: Add fetch request for form submission here
            // if you're handling it via JavaScript
        });
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Accessibility enhancements
    const focusableElements = document.querySelectorAll(
        'a, button, input, select, textarea, [tabindex]'
    );
    
    focusableElements.forEach(el => {
        el.addEventListener('focus', function() {
            this.style.outline = '2px solid #004466';
            this.style.outlineOffset = '3px';
        });
        
        el.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
});