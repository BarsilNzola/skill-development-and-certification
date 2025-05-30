// Global functions for password toggling
function toggleLoginPassword() {
    const passwordField = document.querySelector('#loginForm input[name="password"]');
    if (passwordField) {
        passwordField.type = passwordField.type === 'password' ? 'text' : 'password';
    }
}

function toggleSignupPasswords() {
    const password1 = document.querySelector('#signupForm input[name="password1"]');
    const password2 = document.querySelector('#signupForm input[name="password2"]');
    const checkbox = document.querySelector('#signupForm .show-password-checkbox');
    
    if (!checkbox || !password1 || !password2) return;
    
    const showPassword = checkbox.checked;
    password1.type = showPassword ? 'text' : 'password';
    password2.type = showPassword ? 'text' : 'password';
}

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const showLogin = document.getElementById('show-login');
    const showSignup = document.getElementById('show-signup');

    // Dynamic base URL
    const baseUrl = window.location.hostname === 'localhost' 
                    ? 'http://localhost:8000' 
                    : 'https://skill-development-and-certification.onrender.com';

    // Initialize forms based on errors
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
    function toggleForms() {
        loginForm.classList.toggle('active');
        signupForm.classList.toggle('active');
        window.scrollTo({
            top: document.querySelector('.login-signup-container').offsetTop - 20,
            behavior: 'smooth'
        });
    }

    if (showLogin) showLogin.addEventListener('click', (e) => { e.preventDefault(); toggleForms(); });
    if (showSignup) showSignup.addEventListener('click', (e) => { e.preventDefault(); toggleForms(); });

    // Password toggle event listeners
    const loginCheckbox = document.querySelector('#loginForm .show-password-checkbox');
    if (loginCheckbox) {
        loginCheckbox.addEventListener('change', toggleLoginPassword);
    }
    
    const signupCheckbox = document.querySelector('#signupForm .show-password-checkbox');
    if (signupCheckbox) {
        signupCheckbox.addEventListener('change', toggleSignupPasswords);
    }

    // Password validation
    const password1 = document.querySelector('#signupForm input[name="password1"]');
    const password2 = document.querySelector('#signupForm input[name="password2"]');
    
    if (password1 && password2) {
        [password1, password2].forEach(field => {
            field.addEventListener('input', validatePasswords);
        });
    }

    function validatePasswords() {
        const errorElement = document.getElementById('signup-error-message');
        if (!errorElement || !password1 || !password2) return;
        
        if (password1.value && password2.value && password1.value !== password2.value) {
            errorElement.textContent = "Passwords do not match";
        } else {
            errorElement.textContent = "";
        }
    }

    // Username validation
    const usernameField = document.querySelector('#signupForm input[name="username"]');
    if (usernameField) {
        usernameField.addEventListener('input', function() {
            const errorElement = this.closest('.form-field')?.querySelector('.error-message');
            const hasSpaces = /\s/.test(this.value);
            
            this.setCustomValidity(hasSpaces ? "Username cannot contain spaces" : "");
            if (errorElement) {
                errorElement.textContent = hasSpaces ? "Username cannot contain spaces" : "";
            }
        });
    }

    // Login form submission
    document.getElementById('login-form')?.addEventListener('submit', async (event) => {
        event.preventDefault();

        const username = document.getElementById('login_username').value;
        const password = document.getElementById('login_password').value;
        const errorElement = document.getElementById('login-error-message');

        if (!username || !password) {
            if (errorElement) errorElement.textContent = 'Please fill in all fields';
            return;
        }

        try {
            const response = await fetch(`${baseUrl}/api/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            
            if (response.ok) {
                window.location.href = `${baseUrl}/dashboard/`;
            } else if (errorElement) {
                errorElement.textContent = data.message || 'Login failed';
            }
        } catch (error) {
            console.error('Login error:', error);
            if (errorElement) errorElement.textContent = 'An error occurred. Please try again.';
        }
    });

    // Signup Form Handler
    document.getElementById('signup-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const errorElement = document.getElementById('signup-error-message');
        errorElement.textContent = '';

        const formData = {
            username: document.getElementById('id_username').value.trim(),
            email: document.querySelector('[name="email"]').value.trim(),
            password1: document.querySelector('[name="password1"]').value.trim(),
            password2: document.querySelector('[name="password2"]').value.trim(),
            first_name: document.querySelector('[name="first_name"]').value.trim(),
            last_name: document.querySelector('[name="last_name"]').value.trim(),
        };

        try {
            const response = await fetch('/api/login_signup/', {  // Match your urls.py
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (data.success) {
                // Success: Redirect or show message
                if (data.redirect_url) {
                    window.location.href = window.location.origin + '/' + data.redirect_url;
                }
            } else {
                // Display errors
                if (data.errors) {
                    const firstError = Object.values(data.errors)[0];
                    errorElement.textContent = firstError;
                } else if (data.error) {
                    errorElement.textContent = data.error;
                }
            }
        } catch (error) {
            errorElement.textContent = 'Network error. Please try again.';
        }
    });
    


    // Accessibility focus styles
    const focusableElements = document.querySelectorAll('input, button, a, [tabindex]');
    focusableElements.forEach(el => {
        el.addEventListener('focus', () => el.style.outline = '2px solid #004466');
        el.addEventListener('blur', () => el.style.outline = 'none');
    });
});