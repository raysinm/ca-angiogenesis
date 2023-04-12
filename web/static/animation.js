// Define the list of matrices to display
// Get the matrix list from Flask using Jinja2 syntax
// var matrix_list = {{ matrix_list|safe }};

// Print the matrix list to the console for testing
console.log(matrix_list);

// Set up the canvas context
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

// Define the animation function
function animate() {
    // Clear the canvas
    // ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the current matrix
    const matrix = matrixList[frame];
    for (let row = 0; row < matrix.length; row++) {
        for (let col = 0; col < matrix[0].length; col++) {
            const color = matrix[row][col];
            if (color == 0) {
                ctx.fillStyle = "black";
            } else if (color == 1) {
                ctx.fillStyle = "red";
            } else if (color == 2) {
                ctx.fillStyle = "yellow";
            } else if (color == 3) {
                ctx.fillStyle = "blue";
            }
            ctx.fillRect(col * 10, row * 10, 10, 10);
        }
    }

    // Update the frame counter
    frame = (frame + 1) % matrixList.length;
}

// Set up the animation loop
let frame = 0;
const fps = 30;
const interval = 1000 / fps;
setInterval(animate, interval);