document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('div.#edit-view').style.display = 'none';

    document.querySelector('button.edit').onclick = postedit;
    document.querySelector('#compose').addEventListener('click', compose_email);
});
function postedit(){
    // Load the text area with the current post paragraph
    const division = document.createElement('div')
    division.innerHTML = post;
    // Add a save button 

    // Send submission to views and save onto server

    // close text area and load page with new paragraph
    alert('Hello, world!')
}