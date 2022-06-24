profBtn = document.getElementById('prof-button');
profBtn.addEventListener('click', () => {
    document.getElementById('professional').scrollIntoView({
        'behavior': 'smooth',
        'block': 'center',
        'inline': 'center'
    });
})

projectsBtn = document.getElementById('project-button');
projectsBtn.addEventListener('click', () => {
    document.getElementById('projects').scrollIntoView({
        'behavior': 'smooth',
        'block': 'center',
        'inline': 'center'
    });
})