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

  
  const analyzeBtn = document.getElementById('analyzeBtn');
  analyzeBtn.addEventListener('click', async () => {
    const brandUrlInput = document.getElementById('brandUrl');
    const url = brandUrlInput.value;

    try {
      const response = await fetch(`/scrape_and_refine?url=${url}`);
      if (response.ok) {
        const data = await response.json();
        brandUrlInput.value = data.prompt;
      } else {
        console.error('Error:', response.status);
        alert('Failed to analyze URL.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to analyze URL.');
    }
  });

  generateBtn.addEventListener('click', async () => {
    loadingOverlay.style.display = 'flex';
    loadingText.textContent = 'Generating creatives...';

    const imageFile = imageInput.files[0];
    let prompt = document.getElementById('brandUrl').value;
    const freeformText = document.getElementById('freeformText').value;
    const interests = Array.from(document.querySelectorAll('.interest-tag.active'))
        .map(el => el.dataset.interest)
        .join(', ');

    if (!imageFile) {
      alert('Please upload an image.');
      loadingOverlay.style.display = 'none';
      return;
    }

    let refinedPrompt = prompt + " " + freeformText + " Interests: " + interests;
    
    try {
      const refinedPromptResponse = await fetch(`/scrape_and_refine?url=${prompt}`);
      if (refinedPromptResponse.ok) {
        const refinedPromptData = await refinedPromptResponse.json();
        refinedPrompt = refinedPromptData.prompt;
        document.getElementById('brandUrl').value = refinedPrompt;
      } else {
        console.warn("Failed to get refined prompt, using original URL");
      }
    } catch (error) {
      console.error("Error getting refined prompt:", error);
    }

    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('prompt', refinedPrompt);

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
        Object.entries(data.media_kit).forEach(([platform, item]) => {
          const container = document.createElement('div');
          container.classList.add('creative-container');

          const label = document.createElement('h4');
          label.textContent = platform;
          container.appendChild(label);

          const img = document.createElement('img');
          img.src = item.url;
          img.alt = item.description;
          img.style.maxWidth = '100%';
          img.style.height = 'auto';

          container.appendChild(img);

          // Set aspect ratio based on platform
          if (item.format === 'story' || item.format === 'reel') {
            container.style.maxWidth = '200px'; // Adjust as needed
          } else {
            container.style.maxWidth = '200px'; // Adjust as needed
          }

          creativeGrid.appendChild(container);
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

  document.getElementById('modifyBtn').addEventListener('click', async () => {
    const modifyPrompt = document.getElementById('modifyPrompt').value;
    const imageFile = imageInput.files[0];

    if (!imageFile) {
      alert('Please upload an image first.');
      return;
    }

    loadingOverlay.style.display = 'flex';
    loadingText.textContent = 'Modifying image...';

    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('prompt', modifyPrompt);

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
        Object.entries(data.media_kit).forEach(([platform, item]) => {
          const container = document.createElement('div');
          container.classList.add('creative-container');

          const label = document.createElement('h4');
          label.textContent = platform;
          container.appendChild(label);

          const img = document.createElement('img');
          img.src = item.url;
          img.alt = item.description;
          img.style.maxWidth = '100%';
          img.style.height = 'auto';

          container.appendChild(img);

          // Set aspect ratio based on platform
          if (item.format === 'story' || item.format === 'reel') {
            container.style.maxWidth = '200px'; // Adjust as needed
          } else {
            container.style.maxWidth = '200px'; // Adjust as needed
          }

          creativeGrid.appendChild(container);
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
