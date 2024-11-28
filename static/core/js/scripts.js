document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const showLogin = document.getElementById('show-login');
    const showSignup = document.getElementById('show-signup');

    // Initially show the signup form and hide the login form
    signupForm.classList.add('active');
    signupForm.classList.remove('inactive');
    loginForm.classList.add('inactive');
    loginForm.classList.remove('active');

    if (showLogin) {
        showLogin.addEventListener('click', function(event) {
            event.preventDefault();
            // Switch to login form
            signupForm.classList.add('inactive');
            signupForm.classList.remove('active');
            loginForm.classList.add('active');
            loginForm.classList.remove('inactive');
        });
    }

    if (showSignup) {
        showSignup.addEventListener('click', function(event) {
            event.preventDefault();
            // Switch to signup form
            loginForm.classList.add('inactive');
            loginForm.classList.remove('active');
            signupForm.classList.add('active');
            signupForm.classList.remove('inactive');
        });
    }

    // Handle login form submission
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
            } else {
                const errorData = await response.json();
                document.getElementById('login-error-message').innerText = errorData.message;
            }
        } catch (error) {
            document.getElementById('login-error-message').innerText = 'An error occurred. Please try again later.';
        }
    });

    // Handle signup form submission
    document.getElementById('signupForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const username = document.getElementById('signup-username').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('signup-password').value;
        
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
                signupForm.classList.add('inactive');  // Hide signup form
                signupForm.classList.remove('active');
                loginForm.classList.add('active');    // Show login form
                loginForm.classList.remove('inactive');
            } else {
                const errorData = await response.json();
                document.getElementById('signup-error-message').innerText = errorData.message;
            }
        } catch (error) {
            document.getElementById('signup-error-message').innerText = 'An error occurred. Please try again later.';
        }
    });
});
