// Quick filter function
function quickFilter(min, max) {
    document.getElementById('minScore').value = min;
    document.getElementById('maxScore').value = max;
    
    // Highlight active button
    document.querySelectorAll('.quick-score-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    applyFilter();
}

// Apply filter function
function applyFilter() {
    const minScore = document.getElementById('minScore').value || 0;
    const maxScore = document.getElementById('maxScore').value || 30;
    
    // Redirect với query parameters để backend xử lý
    window.location.href = `?min=${minScore}&max=${maxScore}`;
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

// Update result count on page load
window.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.uni-item').length;
    const resultCountElement = document.getElementById('resultCount');
    if (resultCountElement) {
        resultCountElement.textContent = items;
    }
});

