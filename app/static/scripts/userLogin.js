// if the user wants to signup instead, redirect them
const signupBtn = document.querySelector('#signup-btn')
signupBtn.addEventListener('click', event => {
    document.location.href = "/signup"})

// when submitting login form, post a request and display error or redirect on success
const signinForm = document.querySelector('#signin-form')
signinForm.addEventListener('submit', event => {

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
    fetch("/api/signin", requestOptions)
      .then(response => response.text())
            .then(text => {
                
                // check if the response is in JSON format
                try {
                    JSON.parse(text);
                } catch (e) {
                    // if it's not, show error msg (if error msg is in HTML format, remove the element tags for plain text)
                    document.querySelector('#err-msg').innerHTML = text
                    err = true;
                }
            })
            .catch(error => console.log('error', error))
            .finally(function () {
                // if the response was JSON, reload to display new post
                if (!err)
                    document.location.href = "/timeline"
            })
})