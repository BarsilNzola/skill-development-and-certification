document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const showLogin = document.getElementById('show-login');
    const showSignup = document.getElementById('show-signup');

    // Dynamic base URL depending on environment
    const baseUrl = window.location.hostname === 'localhost' 
                    ? 'http://localhost:8000' 
                    : 'https://skill-development-and-certification.onrender.com';

    // Initialize forms based on server-side errors
    if (loginForm && signupForm) {
        const hasLoginErrors = document.querySelector('#login-form .error-message li');
        const hasSignupErrors = document.querySelector('#signup-form .error-message li');
        
        if (hasSignupErrors) {
            signupForm.classList.add('active');
            loginForm.classList.remove('active');
        } else {
            loginForm.classList.add('active');
            signupForm.classList.remove('active');
        }
    }

    // Toggle between forms
    if (showLogin) {
        showLogin.addEventListener('click', function(event) {
            event.preventDefault();
            toggleForms();
        });
    }

    if (showSignup) {
        showSignup.addEventListener('click', function(event) {
            event.preventDefault();
            toggleForms();
        });
    }

    function toggleForms() {
        loginForm.classList.toggle('active');
        signupForm.classList.toggle('active');
        window.scrollTo({
            top: document.querySelector('.login-signup-container').offsetTop - 20,
            behavior: 'smooth'
        });
    }

    // Initialize password fields
    const loginCheckbox = document.querySelector('#loginForm .show-password-checkbox');
    if (loginCheckbox) {
        loginCheckbox.addEventListener('change', toggleLoginPassword);
    }
    
    const signupCheckbox = document.querySelector('#signupForm .show-password-checkbox');
    if (signupCheckbox) {
        signupCheckbox.addEventListener('change', toggleSignupPasswords);
    }

    // Add real-time password validation
    const passwordField = document.querySelector('#id_password');
    const confirmPasswordField = document.querySelector('[name="confirm_password"]');
    
    if (passwordField && confirmPasswordField) {
        [passwordField, confirmPasswordField].forEach(field => {
            field.addEventListener('input', function() {
                validatePasswords();
            });
        });
    }

    function validatePasswords() {
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;
        const errorElement = document.getElementById('signup-error-message');
        
        if (password && confirmPassword && password !== confirmPassword) {
            errorElement.textContent = "Passwords do not match";
        } else {
            errorElement.textContent = "";
        }
    }

    // Password visibility toggles
    function toggleLoginPassword() {
        const passwordField = document.querySelector('#loginForm input[type="password"]');
        if (passwordField) {
            passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
        }
    }

    function toggleSignupPasswords() {
        const passwordFields = document.querySelectorAll('#signupForm input[type="password"]');
        const showPassword = document.querySelector('#signupForm .show-password-checkbox').checked;
        
        passwordFields.forEach(field => {
            field.type = showPassword ? 'text' : 'password';
        });
    }

    // Real-time username validation
    document.getElementById('id_username')?.addEventListener('input', function() {
        const errorElement = this.nextElementSibling?.nextElementSibling; // Skip help text
        if (/\s/.test(this.value)) {
            if (errorElement) errorElement.textContent = "Username cannot contain spaces";
            this.setCustomValidity("Username cannot contain spaces");
        } else {
            if (errorElement) errorElement.textContent = "";
            this.setCustomValidity("");
        }
    });

    // login form submission handler
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
                window.location.href = `${baseUrl}/dashboard/`;
            } else {
                const errorData = await response.json();
                document.getElementById('login-error-message').innerText = errorData.message;
            }
        } catch (error) {
            document.getElementById('login-error-message').innerText = 'An error occurred. Please try again later.';
        }
    });

    // signup form submission handler
    document.getElementById('signup-form').addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.querySelector('#id_username')?.value.trim() || '';
        const email = document.querySelector('[name="email"]').value.trim();
        const password = document.querySelector('#id_password')?.value.trim() || '';
        const confirm_password = document.querySelector('[name="confirm_password"]').value.trim();

        if (!username || !password) {
            document.getElementById('signup-error-message').innerText = 'Please fill in all fields.';
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
                toggleForms(); // Switch to login form
            } else {
                const errorData = await response.json();
                document.getElementById('signup-error-message').innerText = errorData.message;
            }
        } catch (error) {
            document.getElementById('signup-error-message').innerText = 'An error occurred. Please try again later.';
        }
    });

    // Add focus styles for better accessibility
    const inputs = document.querySelectorAll('input, button, a');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.outline = '2px solid #004466';
            this.style.outlineOffset = '2px';
        });
        
        input.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
});