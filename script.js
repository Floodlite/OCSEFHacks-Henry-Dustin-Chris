const canvas = document.getElementById('simulationCanvas');
const ctx = canvas.getContext('2d');
function image() {
    
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); //loop

    // UIs
    ctx.fillStyle = "#04260b"; // #034710 #04260b good colors
    ctx.fillRect(0,0,200,450);
    ctx.fillStyle = "#04300c";
    ctx.fillRect(200,250,500,200);
    
    //UI texts
    ctx.font = "40px arial";
    ctx.fillStyle = "#ffffff";
    ctx.textAlign = "center";
    ctx.fillText("Stats", 100, 50);
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 2;
    ctx.strokeText("Stats", 100, 50);

    

    requestAnimationFrame(draw); //loop
}
draw();