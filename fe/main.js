document.addEventListener('DOMContentLoaded', () => {
  const uploadArea = document.getElementById('uploadArea');
  const analyzeText = document.getElementById('analyzeText');
  const imageInput = document.getElementById('imageInput');
  const imagePreview = document.getElementById('imagePreview');
  const previewImg = document.getElementById('previewImg');
  const removeImage = document.getElementById('removeImage');
  const generateBtn = document.getElementById('generateBtn');
  const resultsSection = document.getElementById('resultsSection');
  const creativeGrid = document.getElementById('creativeGrid');
  const loadingOverlay = document.getElementById('loadingOverlay');
  const loadingText = document.getElementById('loadingText');
  let imgurl = '';

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
      const response = await fetch(`scrape_and_refine?url=${url}`);
      if (response.ok) {
        const data = await response.json();
        analyzeText.value = data.prompt;
      } else {
        console.error('Error:', response.status);
        alert('Failed to analyze URL.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to analyze URL.');
    }
  });

  function getFormData() {
    const formData = new FormData();
    formData.append("context", analyzeText.value);
    
    // Add target demographics
    formData.append('ageRange', document.getElementById('ageRange').value);
    formData.append('gender', document.getElementById('gender').value);
    formData.append('location', document.getElementById('location').value);

    // Get selected interests
    const selectedInterests = Array.from(document.querySelectorAll('input[name="interest"]:checked'))
        .map(el => el.value)
        .join(', ');
    formData.append('interests', selectedInterests);
    formData.append('freeformText', document.getElementById('freeformText').value);

    // Add target platforms
    const platforms = Array.from(document.querySelectorAll('input[name="platform"]:checked'))
      .map(el => el.value);
    formData.append('platforms', JSON.stringify(platforms));

    // Add creative formats
    const formats = Array.from(document.querySelectorAll('input[name="format"]:checked'))
      .map(el => el.value);
    formData.append('formats', JSON.stringify(formats));

    // Add campaign objective
    formData.append('objective', document.querySelector('input[name="objective"]:checked').value);

    return formData;
  }
  
  generateBtn.addEventListener('click', async () => {
    loadingOverlay.style.display = 'flex';
    loadingText.textContent = 'Generating creatives...';

    const formData = getFormData();
    const imageFile = imageInput.files[0];
    formData.append('image', imageFile);

    try {
      const response = await fetch('generate', {
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
          console.log(platform, item);
          const container = document.createElement('div');
          container.classList.add('creative-container');

          const label = document.createElement('h4');
          label.textContent = platform;
          container.appendChild(label);

          const img = document.createElement('img');
          img.src = item.url.slice(1);
          img.alt = item.description;
          img.style.maxWidth = '100%';
          img.style.height = 'auto';
          imgurl = img.src;

          container.appendChild(img);
          
          creativeGrid.appendChild(container);
        });
      } else {
        creativeGrid.textContent = "Failed to generate creatives.";
      }


    } catch (error) {
      console.error('Error:', error);
      loadingText.textContent = 'Error generating creatives.';
    }
    resultsSection.style.display = 'block';
    loadingOverlay.style.display = 'none';

  });

  document.getElementById('modifyBtn').addEventListener('click', async () => {
    const modifyPrompt = document.getElementById('modifyPrompt').value;

    loadingOverlay.style.display = 'flex';
    loadingText.textContent = 'Modifying image...';

    let formData = getFormData();
    formData.append('prompt', modifyPrompt);
    formData.append('image_url',imgurl);

    try {
      const response = await fetch('generate', {
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
          img.src = item.url.slice(1);
          img.alt = item.description;
          img.style.maxWidth = '100%';
          img.style.height = 'auto';

          container.appendChild(img);

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
