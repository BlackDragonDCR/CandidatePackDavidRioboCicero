const API_BASE = '/api';
//only for testing with live server
//const API_BASE = 'http://localhost:8000/api';

console.log('JavaScript loaded');

async function loadImages() {
    console.log('Loading images...');
    try {
        const response = await fetch(`${API_BASE}/list_images`);
        const data = await response.json();
        console.log('Images:', data);
        
        const listContainer = document.getElementById('imageList');
        
        if (!data.items || data.items.length === 0) {
            listContainer.innerHTML = '<p>No images uploaded yet</p>';
            return;
        }
        
        listContainer.innerHTML = '';
        data.items.forEach(item => {
            const div = document.createElement('div');
            div.className = 'image-item';
            div.innerHTML = `
                <img src="${item.url}" alt="${item.image_id}">
                <p>${item.image_id.slice(0, 20)}...</p>
                <button onclick="shareImage('${item.image_id}')">Share</button>
                <button onclick="viewImage('${item.image_id}')">View</button>
            `;
            listContainer.appendChild(div);
        });

        // Update analyse select
        const analyseSelect = document.getElementById('analyseSelect');
        if (analyseSelect) {
            analyseSelect.innerHTML = '<option value="">Select an image...</option>';
            data.items.forEach(item => {
                const option = document.createElement('option');
                option.value = item.image_id;
                option.textContent = item.image_id.slice(0, 35) + '...';
                analyseSelect.appendChild(option);
            });
        }
        
    } catch (error) {
        console.error('Error:', error);
         const listContainer = document.getElementById('imageList');
        if (listContainer) {
            listContainer.innerHTML = '<p>Error loading images. Is backend running?</p>';
        }
    }
}

//view images
window.viewImage = (imageId) => {
    console.log('Viewing image:', imageId);
    const imageUrl = `${API_BASE.replace('/api', '')}/uploads/${imageId}`;
    window.open(imageUrl, '_blank');
};

//share images
window.shareImage = async (imageId) => {
    console.log('Sharing image:', imageId);
    
    try {
        const response = await fetch(`${API_BASE}/share_image`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image_id: imageId })
        });
        
        const data = await response.json();
        console.log('Share response:', data);
        
        if (response.ok) {
            const fullUrl = `http://localhost:8000${data.url}`;
            alert(`Share link (valid for 10 minutes):\n${fullUrl}`);
            await navigator.clipboard.writeText(fullUrl);
            alert('Link copied to clipboard!');
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Network error');
    }
};


//upload images
const uploadForm = document.getElementById('uploadForm');
if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Upload form submitted');
        
        const fileInput = document.getElementById('imageFile');
        const file = fileInput.files[0];
        
        if (!file) {
            alert('Please select a file');
            return;
        }
        
        console.log('File:', file.name);
        
        const formData = new FormData();
        formData.append('image', file);
        
        try {
            const response = await fetch(`${API_BASE}/upload_image`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            console.log('Upload response:', data);
            
            if (response.ok) {
                alert(`Uploaded! ID: ${data.image_id}`);
                fileInput.value = '';
                loadImages();
            } else {
                alert(`Error: ${data.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Network error');
        }
    });
} else {
    console.error('uploadForm not found in HTML');
}

//analyse image
// ========== ANALYSE IMAGE ==========
const analyseBtn = document.getElementById('analyseBtn');
if (analyseBtn) {
    analyseBtn.addEventListener('click', async () => {
        const select = document.getElementById('analyseSelect');
        const imageId = select.value;
        
        if (!imageId) {
            alert('Please select an image');
            return;
        }
        
        console.log('Analysing:', imageId);
        
        // Mostrar loading
        const previewContainer = document.getElementById('analysisPreview');
        const contentContainer = document.getElementById('analysisContent');
        previewContainer.style.display = 'block';
        contentContainer.innerHTML = '<p>Loading analysis...</p>';
        
        try {
            // Fetch image analysis
            const response = await fetch(`${API_BASE}/analyse_image`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image_id: imageId })
            });
            
            const data = await response.json();
            console.log('Analyse response:', data);
            
            if (response.ok) {
                const a = data.analysis;
                const imageUrl = `${API_BASE.replace('/api', '')}/uploads/${imageId}`;
                
                // Build the HTML content
                contentContainer.innerHTML = `
                    <div style="text-align: center;">
                        <img src="${imageUrl}" alt="${imageId}">
                        <p><strong>Image ID:</strong> ${imageId}</p>
                    </div>
                    <div class="analysis-detail">
                        <div class="analysis-card">
                            <strong>${a.width} x ${a.height}</strong>
                            <span>Dimensions (px)</span>
                        </div>
                        <div class="analysis-card">
                            <strong>${a.format}</strong>
                            <span>Format</span>
                        </div>
                        <div class="analysis-card">
                            <strong>${a.size_kb.toFixed(2)} KB</strong>
                            <span>File size</span>
                        </div>
                        <div class="analysis-card">
                            <strong>${a.mode || 'N/A'}</strong>
                            <span>Color mode</span>
                        </div>
                    </div>
                `;
                
                // Also show simple message in the result div
                const resultDiv = document.getElementById('analysisResult');
                if (resultDiv) {
                    resultDiv.innerHTML = `Analysis complete for ${imageId.slice(0, 20)}...`;
                    resultDiv.className = 'success';
                    setTimeout(() => {
                        resultDiv.innerHTML = '';
                        resultDiv.className = '';
                    }, 3000);
                }
            } else {
                contentContainer.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            }
        } catch (error) {
            console.error('Error:', error);
            contentContainer.innerHTML = '<p style="color: red;">Network error. Is backend running?</p>';
        }
    });
}

// Load images when page loads
loadImages();