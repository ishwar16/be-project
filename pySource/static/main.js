//var nameString = "";
//
//let isConfigUpdate = false;
//let reader = new FileReader();
//displayIMG("#topV", "#displayImage1");
//displayIMG("#sideV", "#displayImage2");
//
//var img;
//
//function generateName() {
//    const D = new Date();
//    var s = D.toString().replace(/ /g, "").replace('GMT+0530(IndiaStandardTime)', "");
//    nameString = s;
//}
//
//// function that shows selected image in box
//function displayIMG(file, location) {
//    const image_input = document.querySelector(file);
//
//    image_input.addEventListener("change", function() {
//        const reader = new FileReader();
//        reader.addEventListener("load", () => {
//            const uploaded_image = reader.result;
//            document.querySelector(location).style.backgroundImage = `url(${uploaded_image})`;
//            img = uploaded_image;
//        });
//        reader.readAsDataURL(this.files[0]);
//        console.log(this.files[0]);
//    });
//}