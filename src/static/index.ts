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

const fileInput = document.querySelector(".form") as HTMLFormElement;
const resultsDiv = document.querySelector(".images") as HTMLDivElement;

fileInput.addEventListener("submit", (event) => {
    event.preventDefault();

    const formData = new FormData(fileInput);

    fetch("/uploadfile", {
        method: "POST",
        body: formData,
    }).then((response) => {
        if (!response.ok) {
            const error = response.text();
            alert(`Error: ${error}`);
            return;
        }

        response.json().then((data) => {
            // Loop through each classification
            for (const classification in data["images"]) {
                const images = data["images"][classification];

                // Create a new div for the classification
                const classificationDiv = document.createElement("div");
                classificationDiv.classList.add("classification");
                classificationDiv.innerHTML = `<h2>${classification}</h2>`;
                resultsDiv.appendChild(classificationDiv);

                // Loop through each image in the classification
                for (const image of images) {
                    // Create a new image element
                    const img = document.createElement("img");
                    img.src = `data:image/png;base64,${image}`;
                    classificationDiv.appendChild(img);
                }
            }
        });
    });
});
