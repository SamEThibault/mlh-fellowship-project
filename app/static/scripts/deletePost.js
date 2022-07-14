// listens for the timeline delete form to submit (DELETE)
const removeForm = document.querySelector('#rmForm')
removeForm.addEventListener('submit', event => {

    // prevent the default browser actions to occur on submit
    event.preventDefault()

    // specify data format
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/x-www-form-urlencoded");

    // add parameters: the id that is entered by the user
    var urlencoded = new URLSearchParams();
    urlencoded.append("id", document.getElementById('inputID').value);

    var requestOptions = {
        method: 'DELETE',
        headers: myHeaders,
        body: urlencoded,
        redirect: 'follow'
    };

    var err = false;
    fetch("/api/timeline_post", requestOptions)
        .then(response => response.status)
        .then(status => {
            
            // if err occured, show it
            if (status != 200) {
                err = true;
                document.querySelector("#del-msg").innerHTML = "Error: " + status
            }
        })
        .catch(error => console.log('error', error))
        .finally(function () {
            // if no error occured, reload the page to display the updated db.
            if (!err)
                window.location.reload()
        })
})