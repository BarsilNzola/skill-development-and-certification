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
