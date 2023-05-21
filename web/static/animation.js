function ShowAnimation(gifData){

    const response = JSON.parse(gifData);
    const animation_gif = response['animation'];

    // Create a new image element
    const img = document.createElement('img');
    
    // Set the src attribute of the image element to the base64-encoded string
    img.src = 'data:image/gif;base64,' + animation_gif;
    
    // Remove previous animation and add the new one to the container
    const container = document.getElementById('animation-container');
    container.innerHTML = '';
    container.appendChild(img);

    // Hide the loading bar
    loadingContainer = document.getElementById('loading-container');
    loadingContainer.style.display = '';
};

document.addEventListener('DOMContentLoaded', () => {
    console.log("dom");
    const form = document.getElementById("run-simulation-form");
    const submitButton = form.querySelector('input[type="submit"]');
    const loadingContainer = document.getElementById('loading-container');
    form.addEventListener("submit", function(event){
        event.preventDefault();
        const formData = new FormData(form);
    

        // Show the loading container
        loadingContainer.style.display = 'block';
        
        // Disable the submit button
        submitButton.disabled = true;

        // First fetch to submit form data
        fetch('/run_simulation', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // // Enable the submit button
            // submitButton.disabled = false;
            // Returns a json gif
            return response.json()
        })
        .then(data => {
            console.log(data);
            ShowAnimation(data) //Danger: Whats being passed
            // Enable the submit button
            submitButton.disabled = false;
        })
        .catch(error => {
            console.error(error);
            // Enable the submit button
            submitButton.disabled = false;
        });
    });
});
 