// Toggle favorite
document.querySelector('.btn-favorite-large').addEventListener('click', function() {
    const icon = this.querySelector('i');
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        this.style.background = '#ffd700';
        this.querySelector('span').textContent = 'Đã yêu thích';
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        this.style.background = 'white';
        this.querySelector('span').textContent = 'Yêu thích';
    }
});

