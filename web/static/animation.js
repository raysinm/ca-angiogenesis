
function animate(matrix_list) {
    // Put your code here
    // var matrix_list = document.getElementById("matrix_list")
    // var matrix_list = {{ matrix_list|tojson }};
    // Print the matrix list to the console for testing
    console.log(matrix_list);

    // Set up the canvas context
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // Define the animation function
    function draw() {
        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // Draw the current matrix
        let matrix = matrix_list[frame];
        console.table(matrix)

        // matrix.forEach((row) => {
        //     row.forEach((element) =>{
        //         if (element == 0) {
        //             ctx.fillStyle = "black";
        //         } else if (element == 1) {
        //             ctx.fillStyle = "red";
        //         } else if (element == 2) {
        //             ctx.fillStyle = "yellow";
        //         } else if (element == 3) {
        //             ctx.fillStyle = "blue";
        //         }
        //         ctx.fillRect(col * 10, row * 10, 10, 10);
        //     })
        // });
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
        frame = (frame + 1) % matrix_list.length;
    }

    // Set up the animation loop
    let frame = 0;
    const fps = 20;
    const interval = 1000/fps;
    setInterval(draw, interval);
}
