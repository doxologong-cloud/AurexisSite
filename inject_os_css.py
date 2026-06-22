import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    css_text = f.read()

window_css = """
/* WEB-OS WINDOW STYLES */
.window {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(10, 10, 10, 0.9);
    border: 1px solid #ffcc00;
    border-radius: 8px;
    box-shadow: 0 0 20px rgba(255, 204, 0, 0.2);
    display: none;
    flex-direction: column;
    min-width: 300px;
    min-height: 200px;
    max-width: 90vw;
    max-height: 85vh;
    overflow: hidden;
    z-index: 100;
    backdrop-filter: blur(10px);
}

.window.active {
    display: flex !important;
}

.window-header {
    height: 40px;
    background: rgba(255, 204, 0, 0.1);
    border-bottom: 1px solid rgba(255, 204, 0, 0.3);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 15px;
    cursor: grab;
    user-select: none;
}

.window-header:active {
    cursor: grabbing;
}

.window-title {
    font-weight: 700;
    font-size: 14px;
    color: #ffcc00;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.window-controls {
    display: flex;
    gap: 10px;
}

.window-btn {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    cursor: pointer;
    border: none;
}

.btn-close { background: #ff4757; }
.btn-min { background: #ffa502; }
.btn-max { background: #2ed573; }

.window-content {
    flex: 1;
    overflow-y: auto;
    position: relative;
    padding: 0;
}

/* OVERRIDE EXISTING VIEW STYLES FOR WINDOW MODE */
.view {
    display: none; /* override existing display styles */
    animation: none;
}
"""

if 'WEB-OS WINDOW STYLES' not in css_text:
    css_text += "\n" + window_css
    with open('static/style.css', 'w', encoding='utf-8') as f:
        f.write(css_text)
    print("Injected Window CSS.")
else:
    print("Window CSS already exists.")
