// this script generates the animation for the experience scroller arrows

// each arrow smooth-scrolls to its designated section div
profBtn = document.getElementById('prof-button');
profBtn.addEventListener('click', () => {
    document.getElementById('experience').scrollIntoView({
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