// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    // hide all textareas
    var x = document.querySelectorAll("#edit-view");
    x.forEach(element => element.style.display = "none");
    // Select the submit button and input to be used later
    const edit = document.querySelectorAll('button.edit');
    edit.forEach(element => element.addEventListener('click',function(){
        const id = element.id;
        var elems = document.querySelectorAll('#edit-view');
        // filter for specific post clicked on
        for (var i =0; i<elems.length; i+=1){
            if (elems[i].className == id){
                elems[i].style.display = 'block';
            }
        }
        postedit(id)
    }))
});// end DomContentLoaded

function postedit(id){
    // Hide post and place in textarea
    document.querySelector(`#post${id}`).style.display = 'none';
    // submit edited post 
    document.querySelector(`form#form${id}`).onsubmit = function() {
        var body = document.querySelector(`#text-post-body${id}`).value;
        save_post(id)
        return false;
};
}// end postedit()

function save_post(id){
    fetch(`/edit/${id}`,{
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector(`#text-post-body${id}`).value,
            id: id,
        })
    })
    clean_up()
.then(response => response.json())
.then(result => {
});
}// End save_post()

function clean_up(){
    document.querySelector('#edit-view').style.display = 'block';
}// End clean_up