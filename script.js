const canvas = document.getElementById('simulationCanvas');
const ctx = canvas.getContext('2d');

let points = 0;
let round = 1;
let status = "Playing";
let pollution = 0;
let water_level = 100;
let temperature = 68 + Math.floor(Math.random()*10);
let organic_waste = 0;

const background2 = new Image();
background2.src = "background2.jpg"; // Set source


function example_stats(){
    points = 30;
    round = 3;
    status = "Playing"
    pollution = 21;
    water_level = 87;
    organic_waste = 15;
    temperature = 64;
};

example_stats(); //remove this later 


function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height); //loop


    // UIs
    ctx.fillStyle = "#04260b"; // #034710 #04260b good colors
    ctx.fillRect(0,0,200,450);
    ctx.fillStyle = "#04300c";
    ctx.fillRect(200,300,500,200);
    
    // UI texts
    ctx.font = "40px arial";
    ctx.fillStyle = "#ffffff";
    ctx.textAlign = "center";
    ctx.fillText("Stats", 100, 50);
    // line
    ctx.beginPath();
    ctx.strokeStyle = "#ffffff";
    ctx.moveTo(180, 60);
    ctx.lineTo(20, 60);
    ctx.lineWidth = 5;
    ctx.stroke();
    // stat values
    ctx.font = "20px arial";
    ctx.fillText("Points: " + String(points), 100, 95);
    ctx.fillText("Round: " + String(round), 100, 120);
    ctx.fillText("Status: " + status, 100, 145);
    ctx.fillText("Pollution: " + String(pollution) + "%", 100, 170);
    ctx.fillText("Water Level: " + String(water_level), 100, 195);
    ctx.fillText("Temperature: " + String(temperature) + "°F", 100, 220);
    ctx.fillText("Organic Waste: " + String(organic_waste), 100, 245);

    





    ctx.drawImage(background2, 200, -50, 500, 350);
    




    requestAnimationFrame(draw); //loop
};
draw();