// Mark Lesson as Completed
document.getElementById('mark-complete-btn')?.addEventListener('click', function () {
    const lessonId = this.getAttribute('data-lesson-id');
    console.log('Mark Complete button clicked! Lesson ID:', lessonId); // Debugging

    fetch(`/lesson/${lessonId}/complete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(data.message);

                // Enable certificate button if applicable
                const certificateButton = document.getElementById('certificate-btn');
                if (certificateButton) {
                    certificateButton.disabled = false;
                    certificateButton.classList.add('enabled');
                }

                location.reload(); // Optional: reload to reflect changes
            } else {
                alert("Failed: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred. Please try again.");
        });
});

// Function to get CSRF Token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Event Listener for Certificate Button
document.getElementById('certificate-btn')?.addEventListener('click', function () {
    alert('Congratulations! Your certificate is ready to download.');
    // Add logic for downloading the certificate if needed
});

// Add Visual Feedback on Form Submission
const assignmentForm = document.getElementById('assignment-form');
assignmentForm?.addEventListener('submit', function (event) {
    event.preventDefault();
    const urlInput = document.getElementById('assignment-url');
    const url = urlInput.value;

    if (url) {
        alert('Assignment submitted successfully!');
        urlInput.value = ''; // Clear the input after submission
    } else {
        alert('Please enter a valid URL before submitting.');
    }
});
