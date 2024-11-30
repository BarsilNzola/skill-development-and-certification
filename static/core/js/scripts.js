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
    document.getElementById('login-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const username = document.getElementById('id_username').value;
        const password = document.getElementById('id_password').value;
        
        try {
            const response = await fetch('http://localhost:8000/api/login/', {
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
                window.location.href = 'http://localhost:8000/dashboard/';
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
        
        const username = document.getElementById('id_username').value;
        const email = document.getElementById('id_email').value;
        const password = document.getElementById('id_password').value;
        const confirm_password = document.getElementById('id_confirm_password').value;
    
        console.log(`Username: ${username}, Email: ${email}, Password: ${password}, Confirm Password: ${confirm_password}`);
    
        if (password !== confirm_password) {
            document.getElementById('signup-error-message').innerText = "Passwords do not match.";
            return;
        }
    
        try {
            const response = await fetch('http://localhost:8000/api/signup/', {
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
