document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const username = document.getElementById('username');
            const password = document.getElementById('password');

            const formData = new FormData(loginForm);
            const data = Object.fromEntries(formData.entries());
            
            const submitButton = loginForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

            fetch("/login", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                return response.json().then(data => {
                    if (!response.ok) {
                        throw new Error(data.message || 'Login failed');
                    }
                    return data;
                });
            })
            .then(result => {
                console.log(result.status)
                if (result.status === 'success') {
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