function  getImagePreview(event) {
    console.log(event.target.files[0]);
    var image = URL.createObjectURL(event.target.files[0]);
    console.log(image);
    var imagediv = document.getElementById('preview');
    var newImage = document.createElement('img')
    imagediv.innerHTML ="  "
    newImage.src = image
    newImage.className = "img-fluid img-thumbnail mx-auto d-block mb-2"
    newImage.style.height = '20vw'
    imagediv.appendChild(newImage);
}