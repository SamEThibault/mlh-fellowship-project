samButton = document.getElementById('sam-button');
samButton.addEventListener('click', () => {
    document.getElementById('sam').scrollIntoView({
        'behavior': 'smooth',
        'block': 'center',
        'inline': 'center'
    });
})