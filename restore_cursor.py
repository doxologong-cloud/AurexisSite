import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

custom_cursor_css = """
/* CUSTOM CURSOR */
body.custom-cursor-enabled, body.custom-cursor-enabled * {
    cursor: none !important;
}

#custom-cursor {
    position: fixed;
    top: 0;
    left: 0;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 999999999999;
    transform: translate(-50%, -50%);
    background: var(--neon-primary);
    box-shadow: 0 0 15px var(--neon-primary), 0 0 30px var(--neon-primary);
    transition: transform 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275), width 0.2s, height 0.2s;
    mix-blend-mode: screen;
}

#custom-cursor.clicking {
    transform: translate(-50%, -50%) scale(0.5);
    background: #fff;
    box-shadow: 0 0 20px #fff;
}

#custom-cursor.hovering {
    width: 40px;
    height: 40px;
    background: transparent;
    border: 2px solid var(--neon-primary);
    box-shadow: inset 0 0 10px var(--neon-primary), 0 0 10px var(--neon-primary);
}
"""

text += custom_cursor_css

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(text)

# Also update index.html to have the class and the div
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

html_text = html_text.replace('<body>', '<body class="custom-cursor-enabled">\n<div id="custom-cursor"></div>')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_text)

# And script.js
with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

js_to_add = """
// ==========================================
// Custom Cursor Logic
// ==========================================
const cursor = document.getElementById('custom-cursor');
if (cursor) {
    document.addEventListener('mousemove', e => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    document.addEventListener('mousedown', () => cursor.classList.add('clicking'));
    document.addEventListener('mouseup', () => cursor.classList.remove('clicking'));

    // Hover effect on interactive elements
    const interactiveElements = document.querySelectorAll('a, button, input, textarea, select, .theme-card, .msgr-tab, .dropdown-item');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hovering'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hovering'));
    });
}
"""

js_text += js_to_add

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Custom cursor fully restored with isolated scoping!")
