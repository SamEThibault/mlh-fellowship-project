// if the user wants to signin instead, redirect to proper page
const signinBtn = document.querySelector('#signin-btn')
signinBtn.addEventListener('click', event => {
    document.location.href = "/signin"})

// when submitting sign up form, post a request and display error or redirect on success
const signupForm = document.querySelector('#signup-form')
signupForm.addEventListener('submit', event => {

    // prevent the default browser actions to occur on submit
    event.preventDefault()

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/x-www-form-urlencoded");
    
    var urlencoded = new URLSearchParams();
    urlencoded.append("name", document.getElementById("inputName").value);
    urlencoded.append("password", document.getElementById("inputPassword").value);
    
    var requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: urlencoded,
      redirect: 'follow'
    };
    
    err = false
    fetch("/api/signup", requestOptions)
      .then(response => response.text())
            .then(text => {
                // check if the response is in JSON format
                try {
                    JSON.parse(text);
                } catch (e) {
                    // if it's not, show error msg
                    document.querySelector('#err-msg').innerHTML = text
                    err = true;
                }
            })
            .catch(error => console.log('error', error))
            .finally(function () {
                // if the response was JSON, redirect to signin page
                if (!err)
                    document.location.href = "/signin"
            })
})