document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const showLogin = document.getElementById('show-login');
    const showSignup = document.getElementById('show-signup');

    // Dynamically set the base URL depending on the environment
    const baseUrl = window.location.hostname === 'localhost' 
                    ? 'http://localhost:8000' 
                    : 'https://skill-development-and-certification.onrender.com';

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
    document.getElementById('login-form').addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.getElementById('login_username').value;
        const password = document.getElementById('login_password').value;

        try {
            const response = await fetch(`${baseUrl}/api/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                const data = await response.json();
                alert(data.message);

                // Redirect to the dashboard
                window.location.href = `${baseUrl}/dashboard/`;
            } else {
                const errorData = await response.json();
                document.getElementById('login-error-message').innerText = errorData.message;
            }
        } catch (error) {
            document.getElementById('login-error-message').innerText = 'An error occurred. Please try again later.';
        }
    });

    // Handle signup form submission
    document.getElementById('signup-form').addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.querySelector('#id_username')?.value.trim() || '';
        const email = document.querySelector('[name="email"]').value.trim();
        const password = document.querySelector('#id_password')?.value.trim() || '';
        const confirm_password = document.querySelector('[name="confirm_password"]').value.trim();

        console.log(`Username: ${username}, Email: ${email}, Password: ${password}, Confirm Password: ${confirm_password}`);

        // Handle missing data
        if (!username || !password) {
            console.error('One or more fields are missing.');
            document.getElementById('login-error-message').innerText = 'Please fill in all fields.';
            return;
        }

        if (password !== confirm_password) {
            document.getElementById('signup-error-message').innerText = "Passwords do not match.";
            return;
        }

        try {
            const response = await fetch(`${baseUrl}/api/signup/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({ username, email, password, confirm_password }),
            });

            if (response.ok) {
                const data = await response.json();
                alert('Registration successful! Redirecting to login...');

                // Redirect to login form
                signupForm.classList.add('inactive');
                signupForm.classList.remove('active');
                loginForm.classList.add('active');
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
