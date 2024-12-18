function togglePasswordVisibility(inputId, toggleId) {
    const passwordInput = document.getElementById(inputId);
    const passwordToggle = document.getElementById(toggleId);

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordToggle.classList.remove('fa-eye-slash');
        passwordToggle.classList.add('fa-eye');
    } else {
        passwordInput.type = 'password';
        passwordToggle.classList.remove('fa-eye');
        passwordToggle.classList.add('fa-eye-slash');
      }
  }
  document.addEventListener('DOMContentLoaded', function () {
      const registrationForm = document.getElementById('registrationForm');                
      registrationForm.addEventListener('submit', function (e) {
          e.preventDefault();
          const formData = new FormData(registrationForm);
          const data = Object.fromEntries(formData.entries());

      
      // Validate password length and special character
      const password = data.password;
      const confirmPassword = data.confirmPassword;

      const passwordRegex = /^(?=.*[!@#$%^&*(),.?":{}|<>])[a-zA-Z\d!@#$%^&*(),.?":{}|<>]{6,}$/;

      if (!passwordRegex.test(password)) {
          alert('Password must be at least 6 characters long and include at least one special character!');
          return;
      }

      if (password !== confirmPassword) {
          alert('Passwords do not match!');
          return;
      }

      const submitButton = registrationForm.querySelector('button[type="submit"]');
      submitButton.disabled = true;
      submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

      fetch("/sign_up_user", {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      })
      .then(response => {
          return response.json().then(data => {
              if (!response.ok) {
                  throw new Error(data.message || 'Registration failed');
              }
              return data;
          });
      })
      .then(result => {
          alert('Registration successful! Redirecting to login...');
          window.location.href = result.redirect_url;
      })
      .catch(error => {
          alert(error.message);
      })
      .finally(() => {
          submitButton.disabled = false;
          submitButton.innerHTML = 'Register';
      });
  });
});