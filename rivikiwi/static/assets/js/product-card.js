function changeImage(element) {
    var mainImage = document.getElementById("main-image");
    
    mainImage.src = element.src;

    var thumbnails = document.querySelectorAll(".thumbnail");
    thumbnails.forEach(function(thumb) {
        thumb.classList.remove("active");
    });
    element.classList.add("active");
}
