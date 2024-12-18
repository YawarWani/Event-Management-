document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const passwordInput = document.getElementById('password');
    const passwordToggle = document.getElementById('passwordToggle');
    
    // Password toggle functionality
    passwordToggle.addEventListener('click', function() {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            passwordToggle.classList.remove('fa-eye-slash');
            passwordToggle.classList.add('fa-eye');
        } else {
            passwordInput.type = 'password';
            passwordToggle.classList.remove('fa-eye');
            passwordToggle.classList.add('fa-eye-slash');
        }
    });
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.getElementById('email');
            console.log(email)
            const password = document.getElementById('password');

            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());
            
            const submitButton = loginForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

            fetch("/userLogin", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) {
                        console.log("First")
                        throw new Error(data.message || 'Login failed');
                    }
                    return data;
                });
            })
            .then(result => {
                console.log("hello")
                console.log(result.success)
                if (result.success === 'True') {
                    console.log("gusssa")
                    window.location.href = result.redirect_url;
                } else {
                    throw new Error(result.message || 'Login failed');
                }
            })
            .catch(error => {
                alert(error.message || 'Login failed. Please check your credentials.');
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.innerHTML = 'Login';
            });
        });
    }
});