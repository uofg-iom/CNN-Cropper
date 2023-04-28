// const form = document.querySelector(".form") as HTMLFormElement;
// const imagesContainer = document.querySelector(".images") as HTMLDivElement;
// form.addEventListener("submit", async (event) => {
//   event.preventDefault();
//   const formData = new FormData(form);
//   try {
//     const response = await fetch("http://localhost:8000/uploadfile/", {
//       method: "POST",
//       body: formData,
//     });
//     const data = await response.json();
//     imagesContainer.innerHTML = data.images.map((image) => `<img src="data:image/jpeg;base64,${image}"/>`).join("");
//   } catch (error) {
//     console.error(error);
//   }
// });
var fileInput = document.querySelector(".form");
var resultsDiv = document.querySelector(".images");
fileInput.addEventListener("submit", function (event) {
    event.preventDefault();
    var formData = new FormData(fileInput);
    fetch("/uploadfile", {
        method: "POST",
        body: formData,
    }).then(function (response) {
        if (!response.ok) {
            var error = response.text();
            alert("Error: ".concat(error));
            return;
        }
        response.json().then(function (data) {
            // Loop through each classification
            for (var classification in data["images"]) {
                var images = data["images"][classification];
                // Create a new div for the classification
                var classificationDiv = document.createElement("div");
                classificationDiv.classList.add("classification");
                classificationDiv.innerHTML = "<h2>".concat(classification, "</h2>");
                resultsDiv.appendChild(classificationDiv);
                // Loop through each image in the classification
                for (var _i = 0, images_1 = images; _i < images_1.length; _i++) {
                    var image = images_1[_i];
                    // Create a new image element
                    var img = document.createElement("img");
                    img.src = "data:image/png;base64,".concat(image);
                    classificationDiv.appendChild(img);
                }
            }
        });
    });
});
