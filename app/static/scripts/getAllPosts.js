// since getAll() must execute on load to populate the table:
window.onload = function () {
    getAll()
}

// get all documents and populate frontend table for timeline page
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

