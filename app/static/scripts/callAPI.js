async function submitForm() {

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

    // then request, log the results or error msg, and call the getAll request
    fetch("http://localhost:5000/api/timeline_post", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error))
        .finally(getAll())
}

// get all documents
async function getAll() {

    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };


    fetch("http://localhost:5000/api/timeline_post", requestOptions)
        .then(response => response.text())
        .then(results => {

            // at this point, response is now a JSON object
            var text = JSON.parse(results).timeline_posts
            console.log(text)

            var col = []
            for (var i = 0; i < text.length; i++) {
                for (var key in text[i]) {
                    if (col.indexOf(key) === -1) {
                        col.push(key)
                    }
                }
            }

            var table = document.getElementById("table")

            var tr = table.insertRow(-1)
      
            for (var i = 0; i < text.length; i++) {

                tr = table.insertRow(-1);

                for (var j = col.length - 1; j >= 0; j--) {
                    var tabCell = tr.insertCell(-1);
                    tabCell.innerHTML = text[i][col[j]];
                }
            }



            // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
            var divContainer = document.getElementById("showData");
            divContainer.innerHTML = "";
            divContainer.appendChild(table);

        })
        .catch(error => console.log('error', error))

}