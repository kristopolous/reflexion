document.addEventListener('DOMContentLoaded', () => {
  const uploadArea = document.getElementById('uploadArea');
  const imageInput = document.getElementById('imageInput');
  const imagePreview = document.getElementById('imagePreview');
  const previewImg = document.getElementById('previewImg');
  const removeImage = document.getElementById('removeImage');
  const generateBtn = document.getElementById('generateBtn');
  const resultsSection = document.getElementById('resultsSection');
  const creativeGrid = document.getElementById('creativeGrid');
  const loadingOverlay = document.getElementById('loadingOverlay');
  const loadingText = document.getElementById('loadingText');

  uploadArea.addEventListener('click', () => imageInput.click());

  imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        previewImg.src = e.target.result;
        imagePreview.style.display = 'block';
        uploadArea.style.display = 'none';
      }
      reader.readAsDataURL(file);
    }
  });

  removeImage.addEventListener('click', () => {
    imagePreview.style.display = 'none';
    uploadArea.style.display = 'flex';
    previewImg.src = '';
  });

  generateBtn.addEventListener('click', async () => {
    loadingOverlay.style.display = 'flex';
    loadingText.textContent = 'Generating creatives...';

    const imageFile = imageInput.files[0];
    const prompt = document.getElementById('brandUrl').value;

    if (!imageFile) {
      alert('Please upload an image.');
      loadingOverlay.style.display = 'none';
      return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('prompt', prompt); // Use URL for brand context

    try {
      const response = await fetch('http://localhost:5000/generate', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(data);

      creativeGrid.innerHTML = '';
      if (data.media_kit) {
        Object.values(data.media_kit).forEach(item => {
          const img = document.createElement('img');
          img.src = item.url;
          img.alt = item.description;
          creativeGrid.appendChild(img);
        });
      } else {
        creativeGrid.textContent = "Failed to generate creatives.";
      }

      resultsSection.style.display = 'block';
      loadingOverlay.style.display = 'none';

    } catch (error) {
      console.error('Error:', error);
      loadingText.textContent = 'Error generating creatives.';
    }
  });
});