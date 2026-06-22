import os

css_code = """
/* --- APOCALYPSE MODE (DOX EASTER EGG) --- */
body.apocalypse-mode {
    background-color: #050000 !important;
    color: #ff0033 !important;
    animation: screen-shake 0.3s infinite;
}

body.apocalypse-mode * {
    transition: all 0.5s ease;
}

body.apocalypse-mode #particles-js canvas {
    filter: hue-rotate(150deg) brightness(0.6) saturate(3) !important;
}

body.apocalypse-mode .view {
    transform: rotate(calc(var(--rand-rot, -3) * 1deg)) scale(0.95);
    border: 2px dashed #ff0033 !important;
    background: rgba(20, 0, 0, 0.9) !important;
    box-shadow: inset 0 0 50px rgba(255, 0, 0, 0.2) !important;
}

body.apocalypse-mode h1, body.apocalypse-mode h2, body.apocalypse-mode h3 {
    text-shadow: 3px 3px #ff0000, -3px -3px #0000ff;
    animation: text-glitch 0.1s infinite;
    color: #fff;
}

body.apocalypse-mode nav {
    transform: translateY(30px) rotate(2deg);
    background: rgba(50, 0, 0, 0.5) !important;
    border-bottom: 2px solid red;
}

body.apocalypse-mode .btn {
    transform: skew(15deg);
    background: #400 !important;
    color: red !important;
    border: 1px solid red !important;
}

.apocalypse-code-chunk {
    position: fixed;
    color: #ff0033;
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    opacity: 0.8;
    pointer-events: none;
    z-index: 99999;
    background: rgba(10,0,0,0.9);
    padding: 8px;
    border-left: 3px solid #ff0000;
    box-shadow: 0 0 10px #ff0000;
    animation: fall-down 4s linear forwards;
}

@keyframes screen-shake {
    0% { transform: translate(1px, 1px) }
    20% { transform: translate(-2px, -1px) }
    40% { transform: translate(-1px, 2px) }
    60% { transform: translate(2px, -2px) }
    80% { transform: translate(-2px, 1px) }
    100% { transform: translate(1px, -1px) }
}

@keyframes text-glitch {
    0% { transform: translate(0) }
    20% { transform: translate(-3px, 3px) }
    40% { transform: translate(-3px, -3px) }
    60% { transform: translate(3px, 3px) }
    80% { transform: translate(3px, -3px) }
    100% { transform: translate(0) }
}

@keyframes fall-down {
    0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
    100% { transform: translateY(110vh) rotate(20deg); opacity: 0; }
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(css_code)
print("Apocalypse CSS appended.")
