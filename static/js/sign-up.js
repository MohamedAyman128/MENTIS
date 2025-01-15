document.getElementById('sign-up-form').addEventListener('submit', function(event) {
    var Password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm-password').value;
  
    if (Password === '' || confirmPassword === '') {
      alert('Please fill in all fields.');
      event.preventDefault();
    } else if (Password !== confirmPassword) {
      alert('Passwords do not match. Please make sure both passwords are the same.');
      event.preventDefault();
    } else if (Password.length < 6) {
      alert('Password must be at least 6 characters long.');
      event.preventDefault();
    } else if (Password.length > 20) {
      alert('Password must be less than 20 characters long.');
      event.preventDefault();
    } else if (!/[A-Z]/.test(Password)) {
      alert('Password must contain at least one uppercase letter.');
      event.preventDefault();
    }
    else if (!/[a-z]/.test(Password)) {
      alert('Password must contain at least one lowercase letter.');
      event.preventDefault();
    }
    else if (!/[0-9]/.test(Password)) {
      alert('Password must contain at least one number.');
      event.preventDefault();
    }
    else if (!/[^a-zA-Z0-9]/.test(Password)) {
      alert('Password must contain at least one special character.');
      event.preventDefault();
    }  
});