document.getElementById('login-form').addEventListener('submit', function(event) {
    var Password = document.getElementById('password').value;
    var email = document.getElementById('email').value;
  
    if (Password === '' || email === '') {
      alert('Please fill in all fields.');
      event.preventDefault();
    } 
});