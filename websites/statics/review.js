var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});
function MyFilter() {
    var input = document.getElementById('search').value.trim(); // Trim whitespace from input
    var word = input.toUpperCase();
    var notes = document.getElementsByClassName('diary-title');

    for (var i = 0; i < notes.length; i++) {
        var title = notes[i].textContent.toUpperCase();
        var listItem = notes[i].closest('fieldset');
        if (title.indexOf(word) > -1) {
            listItem.style.display = '';
        } else {
            listItem.style.display = 'none';
        }
    }
}
function deletenote(note_id){
    fetch('/delete_note', {
        method: 'POST',
        body: JSON.stringify({note_id: note_id}),
    }).then((_res) => {
        window.location.href = '/review_notes'
    }) 

}
