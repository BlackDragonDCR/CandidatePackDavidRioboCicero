//const API_BASE = '/api';
//only for testing with live servr
const API_BASE = 'http://localhost:8000/api';

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
            `;
            listContainer.appendChild(div);
        });
        
    } catch (error) {
        console.error('Error:', error);
        listContainer.innerHTML = '<p>Error loading images. Is backend running?</p>';
    }
}

// Load images when page loads
loadImages();