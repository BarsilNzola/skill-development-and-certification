function openFeedbackModal(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            document.getElementById('feedbackContent').innerHTML = html;
            document.getElementById('feedbackModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error loading feedback:', error);
            document.getElementById('feedbackContent').innerHTML = `
                <div class="error-message">
                    <p>Error loading feedback. Please try again later.</p>
                </div>
            `;
            document.getElementById('feedbackModal').style.display = 'block';
        });
}

function closeFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('feedbackModal');
    if (event.target == modal) {
        closeFeedbackModal();
    }
}