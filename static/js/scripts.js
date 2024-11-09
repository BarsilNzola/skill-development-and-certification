// js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const content = document.getElementById('content');

    // Function to load content
    function loadContent(url) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                content.innerHTML = JSON.stringify(data, null, 2);
            })
            .catch(error => console.error('Error:', error));
    }

    // Example function to fetch courses
    function fetchCourses() {
        loadContent('http://localhost:8000/api/courses/');
    }

    // Fetch courses on page load
    fetchCourses();
});
