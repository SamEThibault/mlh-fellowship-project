// since getAll() must execute on load to populate the table:
window.onload = function() {
    getAll()
}

async function submitForm() {

    // POST
    // specify data format
    var myHeadersP = new Headers();
    myHeadersP.append("Content-Type", "application/x-www-form-urlencoded");
    myHeadersP.append("Access-Control-Allow-Origin", "*")
    myHeadersP.append("Access-Control-Allow-Methods", "POST, PUT, PATCH, GET, DELETE, OPTIONS")
    myHeadersP.append("Access-Control-Allow-Headers", "Origin, X-Api-Key, X-Requested-With, Content-Type, Accept, Authorization")

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
        redirect: 'follow'
    };

    // then request, log the results or error msg, and call the getAll request
    fetch("http://localhost:5000/api/timeline_post", requestOptionsP)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error))
        .finally(getAll())
}

// get all documents and populate frontend table
async function getAll() {

    var myHeadersG = new Headers();
    myHeadersG.append("Access-Control-Allow-Origin", "*")
    myHeadersG.append("Access-Control-Allow-Methods", "POST, PUT, PATCH, GET, DELETE, OPTIONS")
    myHeadersG.append("Access-Control-Allow-Headers", "Origin, X-Api-Key, X-Requested-With, Content-Type, Accept, Authorization")

    var requestOptionsG = {
        method: 'GET',
        headers: myHeadersG,
        redirect: 'follow'
    };

    // fetch all documents from db
    fetch("http://localhost:5000/api/timeline_post", requestOptionsG)
        .then(response => response.text())
        .then(results => {

            // at this point, response is now a JSON object
            var text = JSON.parse(results).timeline_posts
            console.log(text)

            // to populate frontend table, count columns
            var col = []
            for (var i = 0; i < text.length; i++) {
                for (var key in text[i]) {
                    if (col.indexOf(key) === -1) {
                        col.push(key)
                    }
                }
            }

            // find table to fill
            var table = document.getElementById("table")

            var tr = table.insertRow(-1)
      
            // insert a cell for each document field
            for (var i = 0; i < text.length; i++) {

                tr = table.insertRow(-1);

                for (var j = col.length - 1; j >= 0; j--) {
                    var tabCell = tr.insertCell(-1);
                    tabCell.innerHTML = text[i][col[j]];
                }
            }

            
        })
        .catch(error => console.log('error', error))
}
