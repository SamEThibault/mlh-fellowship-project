function submitForm() {

    // POST
    // specify data format
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/x-www-form-urlencoded");

    // add search parameters based on form's inputs
    var urlencoded = new URLSearchParams();
    urlencoded.append("name", document.getElementById("inputName").value);
    urlencoded.append("email", document.getElementById("inputEmail").value);
    urlencoded.append("content", document.getElementById("inputContent").value);

    // populate the request details
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: urlencoded,
        redirect: 'follow'
    };

    // then request, log the results or error msg
    fetch("http://localhost:5000/api/timeline_post", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error))
        .finally(getAll())
}


function getAll() {

    console.log("we made it")

    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };


    fetch("http://localhost:5000/api/timeline_post", requestOptions)
        .then(response => response.text())
        .then(text => document.getElementById("timeline").innerText = text)
        .catch(error => console.log('error', error))

}