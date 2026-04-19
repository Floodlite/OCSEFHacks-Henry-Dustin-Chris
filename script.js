const canvas = document.getElementById('simulationCanvas');
const ctx = canvas.getContext('2d');
const statsGrid = document.getElementById('statsGrid');
const animalGrid = document.getElementById('animalGrid');
const messageBox = document.getElementById('messageBox');
const eventList = document.getElementById('eventList');
const buildingChoices = document.getElementById('buildingChoices');
const builtCounts = document.getElementById('builtCounts');
const resetButton = document.getElementById('resetButton');

let gameState = null;

//background image
const background2 = new Image();
background2.src = "images/background2.jpg";

const statConfig = [
    ["Points", "score"],
    ["Round", "round"],
    ["Status", "status"],
    ["Pollution", "pollution"],
    ["Water", "water_level"],
    ["Temperature", "temperature"],
    ["Light", "light_level"],
    ["Organic Matter", "organic_matter"],
    ["Water Net", "city_water_net"],
    ["Pollution Rate", "city_pollution_production"],
    ["Passive Score", "city_point_generation"],
    ["Multiplier", "score_multiplier"],
];

function formatLabel(name) {
    return name
        .replaceAll("_", " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
}

function statValue(label, value) {
    if (label === "Temperature") {
        return `${value}\u00B0F`;
    }
    return value;
}


function renderStats() {
    statsGrid.innerHTML = statConfig.map(([label, key]) => `
        <div class="stat-card">
            <span class="stat-label">${label}</span>
            <strong class="stat-value">${statValue(label, gameState[key])}</strong>
        </div>
    `).join("");

    animalGrid.innerHTML = Object.entries(gameState.animals).map(([name, value]) => `
        <div class="animal-card">
            <span class="stat-label">${formatLabel(name)}</span>
            <strong class="stat-value">${value}</strong>
        </div>
    `).join("");
}


function renderEvents() {
    if (!gameState.active_events.length && !gameState.recent_events.length) {
        eventList.innerHTML = `<p class="empty-state">No unusual events this round.</p>`;
        return;
    }

    const recent = gameState.recent_events.map((event) => `
        <div class="event-card recent">
            <strong>${formatLabel(event.name)}</strong>
            <p>${event.description}</p>
            <span>Triggered for ${event.duration} turns</span>
        </div>
    `).join("");

    const active = gameState.active_events.map((event) => `
        <div class="event-card">
            <strong>${formatLabel(event.name)}</strong>
            <p>${event.description}</p>
            <span>${event.remaining_duration} turns remaining</span>
        </div>
    `).join("");

    eventList.innerHTML = recent + active;
}


function renderChoices() {
    if (gameState.gameover) {
        buildingChoices.innerHTML = `<p class="empty-state">Thank you for playing. Ecological damage is a real phenomenon occurring around the world as a side effect of urban development. It isn't inevitable. We can make a difference. To learn more, visit https://sdgs.un.org/topics/sustainable-cities-and-human-settlements Start a new game to play again.</p>`;
        return;
    }

    buildingChoices.innerHTML = gameState.available_buildings.map((building) => `
        <button class="building-card" type="button" data-building="${building.name}">
            <span class="building-name">${formatLabel(building.name)}</span>
            <span>Score: ${building.score}</span>
            <span>Pollution: ${building.pollution}</span>
            <span>Water: ${building.water}</span>
            <p>${building.ability}</p>
        </button>
    `).join("");

    document.querySelectorAll('[data-building]').forEach((button) => {
        button.addEventListener('click', () => chooseBuilding(button.dataset.building));
    });
}


function renderBuiltCounts() {
    const built = Object.entries(gameState.built_counts)
        .filter(([, count]) => count > 0)
        .map(([name, count]) => `<span class="pill">${formatLabel(name)} x${count}</span>`)
        .join("");

    builtCounts.innerHTML = built || `<p class="empty-state">Nothing constructed yet.</p>`;
}

function renderMessage(message = "") {
    if (gameState.gameover) {
        messageBox.textContent = `${gameState.lose_reason} Final score: ${gameState.score}.`;
        return;
    }

    if (message) {
        messageBox.textContent = message;
        return;
    }

    const fallback = gameState.last_building
        ? `${formatLabel(gameState.last_building)} shaped the ecosystem. Choose the next build for round ${gameState.round}.`
        : `Round ${gameState.round} is ready. Choose one of the available buildings to begin.`;

    messageBox.textContent = fallback;
}
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

function renderScene() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, '#8fd6ff');
    gradient.addColorStop(1, '#133b23');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (background2.complete) {
        ctx.globalAlpha = 0.35;
        ctx.drawImage(background2, 150, 30, 420, 260);
        ctx.globalAlpha = 1;
    }

    const pollutionHeight = Math.min(140, gameState.pollution * 1.2);
    ctx.fillStyle = 'rgba(61, 47, 47, 0.45)';
    ctx.fillRect(0, 0, canvas.width, pollutionHeight);

    const waterY = canvas.height - Math.min(150, Math.max(40, gameState.water_level / 12000));
    ctx.fillStyle = '#0b6fa4';
    ctx.fillRect(0, waterY, canvas.width, canvas.height - waterY);

    // bar graphs for animals
    const plantHeight = Math.min(170, gameState.animals.plants / 1.5);
    ctx.fillStyle = '#2f8f3d'
    ctx.fillRect(60, canvas.height - 40 - plantHeight, 110, plantHeight);

    const herbHeight = Math.min(170, gameState.animals.herbivores / 0.15);
    ctx.fillStyle = '#f4d35e';
    ctx.fillRect(220, canvas.height - 40 - herbHeight, 110, herbHeight);

    const carnHeight = Math.min(170, gameState.animals.carnivores / 2);
    ctx.fillStyle = '#ee964b';
    ctx.fillRect(380, canvas.height - 40 - carnHeight, 110, carnHeight);

    const apexHeight = Math.min(170, gameState.animals.apex_predators * 4);
    ctx.fillStyle = '#f95738';
    ctx.fillRect(540, canvas.height - 40 - apexHeight, 110, apexHeight);


    ctx.fillStyle = '#f7fff7';
    ctx.font = '700 18px Trebuchet MS';
    ctx.fillText('Plants', 83, canvas.height - 15);
    ctx.fillText('Herbivores', 226, canvas.height - 15);
    ctx.fillText('Carnivores', 387, canvas.height - 15);
    ctx.fillText('Apex', 579, canvas.height - 15);
}

function render(message = "") {
    if (!gameState) {
        return;
    }
    renderStats();
    renderEvents();
    renderChoices();
    renderBuiltCounts();
    renderMessage(message);
    renderScene();
}

async function loadGame(message = "") {
    const response = await fetch('/api/game');
    gameState = await response.json();
    render(message);
}

async function chooseBuilding(building) {
    const response = await fetch('/api/game/choose', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ building }),
    });
    const payload = await response.json();
    gameState = payload.state;
    render(payload.message);
}

async function resetGame() {
    const response = await fetch('/api/game/reset', {
        method: 'POST',
    });
    const payload = await response.json();
    gameState = payload.state;
    render(payload.message);
}

resetButton.addEventListener('click', resetGame);
background2.addEventListener('load', () => render());
loadGame();
