// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    // Hide the 
    document.querySelector('#edit-view').style.display = 'none';
    alert('in here 5')
    // document.querySelector('button.edit').onclick = postedit;
    document.querySelector('button.edit').onclick = postedit;
    alert('line8')
});
function postedit(){
    // Hide post and place in textarea
    document.querySelector('#edit-view').style.display = 'block';
    // document.querySelector('p.post').style.display = 'none';
    post_id = document.getElementById()

    // Send mail once form is submitted
    document.querySelector('form#form').onsubmit = function() {
    save_post()
    return false;
};
}// end postedit()

function save_post(id){
    alert('made it to save_post')
    fetch(`/edit/${post_id}`,{
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#post-body').value,
        })
    })
.then(response => response.json())
.then(result => {
    alert("It worked")
});
}// end save_post()