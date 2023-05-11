function ShowAnimation(gifData){
    const response = JSON.parse(giData); 
    // create an image element
    const img = document.createElement('img');
    
    // set the src attribute of the image element to the base64-encoded string
    img.src = "data:image/gif;base64," + response;
    
    // add the image element to the container
    document.getElementById('animation-container').appendChild(img);
};

document.addEventListener('DOMContentLoaded', () => {
    console.log("dom")
    const form = document.getElementById("run-simulation-form")
    form.addEventListener("submit", function(event){
        event.preventDefault();
        const formData = new FormData(form);
    
        // First fetch to submit form data
        fetch('/run_simulation', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Returns a json gif
            return response.json()
        })
        .then(data => {
            console.log(data);
            ShowAnimation(data) //Danger: Whats being passed
        })
        .catch(error => console.error(error));
    });
});
 