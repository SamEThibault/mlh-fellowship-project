// since getAll() must execute on load to populate the table:
window.onload = function () {
    getAll()
}

// listens for the form to submit (DELETE)
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
        .then(response => response.text())
        .then(result => {
            console.log(result);
            display = result
            if (result == "error, invalid ID. Try again") {
                err = true;
                document.querySelector("#del-msg").innerHTML = result
            }
        })
        .catch(error => console.log('error', error))
        .finally(function () {
            // if no error occured, reload the page to display the updated db.
            if (!err)
                window.location.reload()
        })
})

// listens for the form to submit (POST)
const addForm = document.querySelector('#addForm')
addForm.addEventListener('submit', event => {
    event.preventDefault() // ensure no browser-specific action on form submit

    // specify data format
    var myHeadersP = new Headers();
    myHeadersP.append("Content-Type", "application/x-www-form-urlencoded");

    // add search parameters based on form's inputs
    var urlencodedP = new URLSearchParams();
    urlencodedP.append("name", document.getElementById("inputName").value);
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
    // then request, log the results or error msg, and call the getAll request
    fetch("/api/timeline_post", requestOptionsP)
        .then(response => response.text())
        .then(text => {

            // check if the response is in JSON format
            try {
                console.log(text)
                JSON.parse(text);
            } catch (e) {
                // if it's not, show error msg (if error msg is in HTML format, remove the element tags for plain text)
                document.querySelector('#err-msg').innerHTML = text.replace(/<[^>]+>/g, '')
                err = true;
            }
        })
        .catch(error => console.log('error', error))
        .finally(function () {
            // if the response was JSON, reload to display new post
            if (!err)
                window.location.reload()
        })
})


// get all documents and populate frontend table
function getAll() {

    var requestOptionsG = {
        method: 'GET',
        redirect: 'follow',
        mode: 'no-cors'
    };

    // fetch all documents from db
    fetch("/api/timeline_post", requestOptionsG)
        .then(response => response.text())
        .then(async results => {

            // at this point, response is now a JSON object
            var text = JSON.parse(results).timeline_posts
            console.log(text)


            // generate bootstrap cards for each of the elements in the array
            let content = '';
            for (var obj of text) {

                content += `
                
                    <div class="card mb-3 mx-auto w-50" >
                        <div class="row g-0">
                        <div class="col-md-11">
                        <div class="card-body">
                            <h4 class="card-title">${obj.name}</h4> 
                            <h5 class="card-text"> Date: ${obj.created_at}</h5>
                            <h5 class="card-text"> Email: ${obj.email}</h5>
                            <p class="card-text">${obj.content}</p>
                            <p class="card-text"><small class="text-muted">${obj.id}</small></p>
                        </div>
                        </div>
                            <div class="col-md-1"> 
                                <img class="img-fluid avatar" src="${obj.avatar}" alt="avatar">
                            </div>
        
                        </div>
                    </div>
                `
            }

            document.querySelector('#generate-items').innerHTML = content;
        })
        .catch(error => console.log('error', error))
}

