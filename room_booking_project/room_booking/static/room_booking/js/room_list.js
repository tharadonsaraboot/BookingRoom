document.getElementById('scrollButton').addEventListener('click', function(event){
    event.preventDefault();
    const targetSection = document.getElementById('target-section');
    targetSection.scrollIntoView({ behavior: 'smooth' });
});