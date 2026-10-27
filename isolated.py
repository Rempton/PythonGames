<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Mein Taktik-Game-Center</title>
    <style>
        body {
            background-color: #0d0d1a;
            color: white;
            font-family: 'Arial', sans-serif;
            text-align: center;
            margin: 0;
            padding: 20px;
        }
        h1 { color: #00ffff; font-size: 32px; margin-bottom: 10px; }
        .container { max-width: 900px; margin: 0 auto; }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 5px;
            width: 350px;
            margin: 20px auto;
            background-color: #222;
            padding: 10px;
            border-radius: 8px;
        }
        .cell {
            width: 60px;
            height: 60px;
            background-color: #333;
            border: 2px solid gray;
            border-radius: 4px;
            transition: all 0.2s;
        }
        .info { font-size: 18px; margin: 15px 0; font-weight: bold; }
        .rules { text-align: left; background: #1a1a30; padding: 15px; border-radius: 8px; margin-top: 30px; display: inline-block; }
        .balance-badge {
            background-color: #ffaa00;
            color: black;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>🎮 ALL OR NOTHING: GAME CENTER 🎮</h1>
    <div class="balance-badge">⚖️ BALANCE-UPDATE: AKTIV</div>
    <div id="turn-info" class="info">Am Zug: <span style="color: cyan;">BLAU (WASD)</span></div>
    
    <!-- Das Spielfeld für Isoliert -->
    <div class="grid-container" id="board"></div>

    <div class="rules">
        <h3>📜 REGELN FÜR ISOLIERT (BALANCED):</h3>
        <ul>
            <li><b>Spieler 1 (Blau):</b> Steuerung mit <b>W, A, S, D</b></li>
            <li><b>Spieler 2 (Rot):</b> Steuerung mit den <b>Pfeiltasten</b></li>
            <li>⚡ <b>Der Balance-Kniff:</b> Da Blau anfängt, wird bei seinem ersten Schritt ein <i>zufälliges zusätzliches Feld</i> auf der Map zerstört! Das bricht den unfairen Startvorteil.</li>
            <li>Jedes Feld, das du verlässt, wird sofort <b>tödlich rot zerstört</b>!</li>
            <li>Wer sich nicht mehr bewegen kann, verliert das Match.</li>
        </ul>
    </div>
</div>

<script>
    const size = 5;
    let grid = {};
    let p1 = {x: 0, y: 2, color: 'cyan', name: 'BLAU'};
    let p2 = {x: 4, y: 2, color: 'tomato', name: 'ROT'};
    let turn = 1; 
    let gameOver = false;
    let p1FirstMove = true; // Tracker für das Balance-Feature

    // Grid initialisieren
    for(let y=0; y<size; y++) {
        for(let x=0; x<size; x++) {
            grid[`${x},${y}`] = 'free';
        }
    }
    grid[`${p1.x},${p1.y}`] = 'p1';
    grid[`${p2.x},${p2.y}`] = 'p2';

    const board = document.getElementById('board');
    function drawBoard() {
        board.innerHTML = '';
        for(let y=0; y<size; y++) {
            for(let x=0; x<size; x++) {
                const cell = document.createElement('div');
                cell.className = 'cell';
                const status = grid[`${x},${y}`];
                
                if(status === 'p1') cell.style.backgroundColor = 'cyan';
                else if(status === 'p2') cell.style.backgroundColor = 'tomato';
                else if(status === 'destroyed') {
                    cell.style.backgroundColor = '#550000';
                    cell.style.borderColor = 'crimson';
                }
                board.appendChild(cell);
            }
        }
    }

    window.addEventListener('keydown', (e) => {
        if(gameOver) return;
        let key = e.key.toLowerCase();
        
        if(turn === 1) { 
            if(key === 'w') movePlayer(1, 0, -1);
            if(key === 's') movePlayer(1, 0, 1);
            if(key === 'a') movePlayer(1, -1, 0);
            if(key === 'd') movePlayer(1, 1, 0);
        } else if(turn === 2) { 
            if(e.key === 'ArrowUp') movePlayer(2, 0, -1);
            if(e.key === 'ArrowDown') movePlayer(2, 0, 1);
            if(e.key === 'ArrowLeft') movePlayer(2, -1, 0);
            if(e.key === 'ArrowRight') movePlayer(2, 1, 0);
        }
    });

    function movePlayer(spieler, dx, dy) {
        let p = (spieler === 1) ? p1 : p2;
        let nx = p.x + dx;
        let ny = p.y + dy;

        if(nx >= 0 && nx < size && ny >= 0 && ny < size) {
            let targetStatus = grid[`${nx},${ny}`];
            if(targetStatus === 'free') {
                grid[`${p.x},${p.y}`] = 'destroyed'; 
                p.x = nx;
                p.y = ny;
                grid[`${p.x},${p.y}`] = (spieler === 1) ? 'p1' : 'p2';
                
                // --- HIER TRITT DER BALANCE CHANGE IN KRAFT ---
                if (spieler === 1 && p1FirstMove) {
                    p1FirstMove = false;
                    destroyRandomCell();
                }
                
                turn = (turn === 1) ? 2 : 1;
                document.getElementById('turn-info').innerHTML = `Am Zug: <span style="color: ${(turn === 1) ? 'cyan' : 'tomato'};">${(turn === 1) ? 'BLAU (WASD)' : 'ROT (Pfeile)'}</span>`;
                
                drawBoard();
                checkWin();
            }
        }
    }

    // Funktion, die ein zufälliges freies Feld blockiert
    function destroyRandomCell() {
        let freieFelder = [];
        for(let y=0; y<size; y++) {
            for(let x=0; x<size; x++) {
                if (grid[`${x},${y}`] === 'free') {
                    freieFelder.push(`${x},${y}`);
                }
            }
        }
        if (freieFelder.length > 0) {
            let zufallsIndex = Math.floor(Math.random() * freieFelder.length);
            grid[freieFelder[zufallsIndex]] = 'destroyed';
        }
    }

    function checkWin() {
        let p = (turn === 1) ? p1 : p2;
        let currentWeg = false;
        let wege = [[0,1], [0,-1], [1,0], [-1,0]];
        
        wege.forEach(w => {
            let tx = p.x + w[0];
            let ty = p.y + w[1];
            if(tx >= 0 && tx < size && ty >= 0 && ty < size) {
                if(grid[`${tx},${ty}`] === 'free') currentWeg = true;
            }
        });

        if(!currentWeg) {
            gameOver = true;
            let gewinner = (turn === 1) ? 'ROT' : 'BLAU';
            document.getElementById('turn-info').innerHTML = `🏆 SPIEL VORBEI! ${gewinner} GEWINNT DAS DUELL! 🏆`;
            document.getElementById('turn-info').style.color = 'yellow';
        }
    }

    drawBoard();
</script>

</body>
</html>
