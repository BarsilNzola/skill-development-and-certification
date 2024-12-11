document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.querySelector('input[type="file"]');
    const previewBox = document.getElementById('image-preview');

    if (imageInput) {
        imageInput.addEventListener('change', (event) => {
            const file = event.target.files[0];

            if (file) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    previewBox.innerHTML = `<img src="${e.target.result}" alt="Profile Preview">`;
                };

                reader.readAsDataURL(file);
            } else {
                previewBox.innerHTML = '<p>No image selected</p>';
            }
        });
    }
});
