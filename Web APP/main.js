displayIMG("#myFile1", "#displayImage1");
displayIMG("#myFile2", "#displayImage2");

var img;

function displayIMG(file, location) {
    const image_input = document.querySelector(file);

    image_input.addEventListener("change", function() {
        const reader = new FileReader();
        reader.addEventListener("load", () => {
            const uploaded_image = reader.result;
            document.querySelector(location).style.backgroundImage = `url(${uploaded_image})`;
            img = uploaded_image;
            console.log(img);
        });
        reader.readAsDataURL(this.files[0]);
        console.log(this.files[0]);
    });
}