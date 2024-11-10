document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('http://localhost:8000/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.message);
            // Redirect to dashboard or perform other actions
        } else {
            const errorData = await response.json();
            document.getElementById('error-message').innerText = errorData.message;
        }
    } catch (error) {
        document.getElementById('error-message').innerText = 'An error occurred. Please try again later.';
    }
});
