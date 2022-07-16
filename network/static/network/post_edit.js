// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    // hide all textareas
    var x = document.querySelectorAll("#edit-view");
    x.forEach(element => element.style.display = "none");

    // Select the submit button and input to be used later
    const edit = document.querySelectorAll('button.edit');
    edit.forEach(element => element.addEventListener('click',function(){
        const id = element.id
        postedit(id)
    }))
});// end DomContentLoaded

function postedit(id){
    // Hide post and place in textarea
    document.querySelector('#edit-view').style.display = 'block';
// TODO: Need to open the correct textarea not just the first one
    // Send mail once form is submitted
    document.querySelector('form#form').onsubmit = function() {
    save_post(id)
    return false;
};
}// end postedit()

function save_post(id){
    // alert('made it to save_post')
    fetch(`/edit/${id}`,{
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#post-body').value,
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