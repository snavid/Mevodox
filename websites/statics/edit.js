

function myfunc(note_id) {
  const editableContent1 = document.getElementById('editable-content1');
  const editableContent2 = document.getElementById('editable-content2');
  let content1 = editableContent1.innerHTML;
  let content2 = editableContent2.innerHTML;
  // Remove newline characters from content1 and content2
  content1 = content1.replace(/\r?\n|\r/g, "");
  content2 = content2.replace(/\r?\n|\r/g, "");
  // You can perform further actions with the submitted content
  console.log(content1, content2);
  // Send the data to the server using an AJAX request
  const xhr = new XMLHttpRequest();
  const url = '/mevodox_editor/' + note_id;
  const params = 'content1=' + encodeURIComponent(content1) + '&content2=' + encodeURIComponent(content2);
  xhr.open('POST', url, true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      console.log('Data successfully sent to the server.');
      // Redirect to the desired URL after successful submission
      window.location.href = '/review_notes';
    }
  };
  xhr.send(params);
}; 