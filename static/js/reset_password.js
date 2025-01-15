document.getElementById('reset-form').addEventListener('submit', function(event) {
    var newPassword = document.getElementById('new-password').value;
    var confirmPassword = document.getElementById('confirm-password').value;
  
    if (newPassword === '' || confirmPassword === '') {
      alert('Please fill in all fields.');
      event.preventDefault();
    } else if (newPassword !== confirmPassword) {
      alert('Passwords do not match. Please make sure both passwords are the same.');
      event.preventDefault();
    } else if (newPassword.length < 6) {
      alert('Password must be at least 6 characters long.');
      event.preventDefault();
    } else if (newPassword.length > 20) {
      alert('Password must be less than 20 characters long.');
      event.preventDefault();
    } else if (!/[A-Z]/.test(newPassword)) {
      alert('Password must contain at least one uppercase letter.');
      event.preventDefault();
    }
    else if (!/[a-z]/.test(newPassword)) {
      alert('Password must contain at least one lowercase letter.');
      event.preventDefault();
    }
    else if (!/[0-9]/.test(newPassword)) {
      alert('Password must contain at least one number.');
      event.preventDefault();
    }
    else if (!/[^a-zA-Z0-9]/.test(newPassword)) {
      alert('Password must contain at least one special character.');
      event.preventDefault();
    }  
});