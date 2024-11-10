document.getElementById('signupForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('http://localhost:8000/api/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            alert(data.message);
            // Redirect to login or perform other actions
        } else {
            const errorData = await response.json();
            document.getElementById('signup-error-message').innerText = errorData.message;
        }
    } catch (error) {
        document.getElementById('signup-error-message').innerText = 'An error occurred. Please try again later.';
    }
});
