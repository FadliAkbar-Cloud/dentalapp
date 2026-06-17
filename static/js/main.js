/**
 * Main JavaScript untuk Dental X-Ray Analyzer
 */

// Drag & Drop functionality
document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    if (dropZone) {
        // Drag & Drop events
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });
        
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('drag-over');
        });
        
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                handleFileSelect(files[0]);
            }
        });
        
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });
    }
    
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });
    }
    
    function handleFileSelect(file) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                if (imagePreview) {
                    imagePreview.src = e.target.result;
                    previewContainer.style.display = 'block';
                }
                if (analyzeBtn) {
                    analyzeBtn.disabled = false;
                }
            };
            reader.readAsDataURL(file);
        } else {
            alert('File harus berupa gambar (JPG, PNG, JPEG)');
        }
    }
});

// Show loading indicator
function showLoading() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Memproses...';
    }
}

// Hide loading indicator (called after response)
function hideLoading() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = 'Analisis Gambar →';
    }
}

// Validate file before upload
function validateFile(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (!allowedTypes.includes(file.type)) {
        alert('Format file tidak didukung. Gunakan JPG, JPEG, atau PNG.');
        return false;
    }
    
    if (file.size > maxSize) {
        alert('Ukuran file terlalu besar. Maksimal 16MB.');
        return false;
    }
    
    return true;
}

// Smooth scroll untuk anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});