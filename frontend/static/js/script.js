// 画像が選ばれたときにプレビューを表示
document.getElementById("image").addEventListener("change", function(e) {
    const file = e.target.files[0];

    if (file) {
        const previewContainer = document.getElementById("result_img_container");
        previewContainer.innerHTML = ''; 

        const upload_header = document.createElement('h2')
        upload_header.textContent = "Uploaded Image"
        previewContainer.appendChild(upload_header)

        const imgPreview = new Image();
        imgPreview.src = URL.createObjectURL(file); 
        imgPreview.width = 500;  
        imgPreview.height = 300; 
        
        previewContainer.appendChild(imgPreview); 
    }
});

//説明文を取得して表示する
document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const fileInput = document.getElementById("image");
    formData.append("image", fileInput.files[0]);

    // CSRFトークンを取得
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
        const response = await fetch("/get_res/", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        });
        console.log(response)
        if (!response.ok) {
            throw new Error('Failed to generate review. Status: ' + response.status);
        }
        const data = await response.json();

        // レビューの表示
        document.getElementById("review").textContent = data.review;

    } catch (error) {
        console.error('Error:', error);
        document.getElementById("review").textContent = "Error generating review. Please try again.";
    }
});
