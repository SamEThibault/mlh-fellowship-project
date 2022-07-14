// listens for the timeline form to submit (POST)
const addForm = document.querySelector('#addForm')
addForm.addEventListener('submit', event => {
    event.preventDefault() // ensure no browser-specific action on form submit

    // specify data format
    var myHeadersP = new Headers();
    myHeadersP.append("Content-Type", "application/x-www-form-urlencoded");

    // add search parameters based on form's inputs
    var urlencodedP = new URLSearchParams();
    urlencodedP.append("email", document.getElementById("inputEmail").value);
    urlencodedP.append("content", document.getElementById("inputContent").value);

    // populate the request details
    var requestOptionsP = {
        method: 'POST',
        headers: myHeadersP,
        body: urlencodedP,
        redirect: 'follow',
        mode: 'no-cors'
    };

    var err = false;
    // send the http request, and handle errors if status != 200
    fetch("/api/timeline_post", requestOptionsP)
        .then(response => response.status)
        .then(status => {

            if (status != 200) {
                // if it's not, show error msg (if error msg is in HTML format, remove the element tags for plain text)
                document.querySelector('#err-msg').innerHTML = "Error: " + status
                err = true;
            }

        })
        .catch(error => console.log('error', error))
        .finally(function () {
            // if the response is OK
            if (!err)
                window.location.reload()
        })
})