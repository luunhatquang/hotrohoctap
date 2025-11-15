// Quick filter function
function quickFilter(min, max) {
    document.getElementById('minTuition').value = min;
    document.getElementById('maxTuition').value = max;
    
    // Highlight active button
    document.querySelectorAll('.quick-tuition-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    applyFilter();
}

// Apply filter function
function applyFilter() {
    const minTuition = document.getElementById('minTuition').value || 0;
    const maxTuition = document.getElementById('maxTuition').value || 100;
    
    // Redirect với query parameters để backend xử lý
    window.location.href = `?min_tuition=${minTuition}&max_tuition=${maxTuition}`;
}

// Toggle favorite
document.querySelectorAll('.uni-favorite').forEach(item => {
    item.addEventListener('click', function() {
        const icon = this.querySelector('i');
        if (icon.classList.contains('far')) {
            icon.classList.remove('far');
            icon.classList.add('fas');
            this.classList.add('active');
        } else {
            icon.classList.remove('fas');
            icon.classList.add('far');
            this.classList.remove('active');
        }
    });
});

