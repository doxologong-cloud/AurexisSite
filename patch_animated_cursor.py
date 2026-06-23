import re

def patch_css():
    try:
        with open('static/style.css', 'r', encoding='utf-8') as f:
            css = f.read()

        custom_cursor_css = """
/* === ANIMATED DOM CURSOR === */
html.cursor-circle, html.cursor-circle * {
    cursor: none !important;
}

#custom-cursor {
    position: fixed;
    top: 0;
    left: 0;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background-color: var(--neon-primary, #ff0055);
    pointer-events: none;
    z-index: 9999999;
    transform: translate(-50%, -50%);
    transition: width 0.15s cubic-bezier(0.175, 0.885, 0.32, 1.275), 
                height 0.15s cubic-bezier(0.175, 0.885, 0.32, 1.275), 
                background-color 0.15s ease, 
                border 0.15s ease,
                box-shadow 0.15s ease;
    border: 2px solid transparent;
    box-sizing: border-box;
    display: none;
    box-shadow: 0 0 10px var(--neon-primary, #ff0055);
}

#custom-cursor.click-effect {
    width: 35px;
    height: 35px;
    background-color: transparent !important;
    border: 3px solid var(--neon-primary, #ff0055);
    box-shadow: 0 0 15px var(--neon-primary, #ff0055) inset, 0 0 15px var(--neon-primary, #ff0055);
}

#custom-cursor.hover-effect {
    width: 24px;
    height: 24px;
    background-color: transparent;
    border: 2px solid var(--neon-color, #ffcc00);
    box-shadow: 0 0 10px var(--neon-color, #ffcc00) inset, 0 0 10px var(--neon-color, #ffcc00);
}
"""
        if '#custom-cursor' not in css:
            css += '\n' + custom_cursor_css
            with open('static/style.css', 'w', encoding='utf-8') as f:
                f.write(css)
            print("Patched style.css")
    except Exception as e:
        print("CSS error:", e)

def patch_html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Add html.cursor-circle logic in <head>
        if "document.documentElement.classList.add('cursor-circle')" not in html:
            old_head_script = "const shape = localStorage.getItem('aurex_cursor_shape') || 'triangle';"
            new_head_script = "const shape = localStorage.getItem('aurex_cursor_shape') || 'triangle';\n        if (shape === 'circle') document.documentElement.classList.add('cursor-circle');"
            html = html.replace(old_head_script, new_head_script)

        # Add the <div id="custom-cursor"> immediately after <body>
        if 'id="custom-cursor"' not in html:
            html = html.replace('<body>', '<body>\n    <!-- Animated Custom Cursor -->\n    <div id="custom-cursor"></div>')

        html = re.sub(r'\?v=\d+', '?v=106', html)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")
    except Exception as e:
        print(f"HTML error ({filepath}):", e)

def patch_js():
    try:
        with open('static/script.js', 'r', encoding='utf-8') as f:
            js = f.read()

        # Update changeCursorShape
        old_change = "window.changeCursorShape = function(shape) {\n    localStorage.setItem('aurex_cursor_shape', shape);"
        new_change = """window.changeCursorShape = function(shape) {
    localStorage.setItem('aurex_cursor_shape', shape);
    
    const cursorDOM = document.getElementById('custom-cursor');
    if (shape === 'circle') {
        document.documentElement.classList.add('cursor-circle');
        if (cursorDOM) cursorDOM.style.display = 'block';
    } else {
        document.documentElement.classList.remove('cursor-circle');
        if (cursorDOM) cursorDOM.style.display = 'none';
    }"""
        if "document.documentElement.classList.add('cursor-circle');" not in js:
            js = js.replace(old_change, new_change)

        # Append DOM cursor event listeners at the end of the file
        dom_cursor_js = """
// === ANIMATED DOM CURSOR LOGIC ===
document.addEventListener('DOMContentLoaded', () => {
    const cursor = document.getElementById('custom-cursor');
    const shape = localStorage.getItem('aurex_cursor_shape') || 'triangle';
    if (shape === 'circle' && cursor) {
        cursor.style.display = 'block';
    }

    document.addEventListener('mousemove', (e) => {
        if (!cursor || !document.documentElement.classList.contains('cursor-circle')) return;
        
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        
        // Hover detection
        const isClickable = e.target.closest('a, button, input, select, textarea, .theme-card, .dropdown-item, .cursor-btn, .clickable, i');
        if (isClickable) {
            cursor.classList.add('hover-effect');
        } else {
            cursor.classList.remove('hover-effect');
        }
    });

    document.addEventListener('mousedown', () => {
        if (cursor && document.documentElement.classList.contains('cursor-circle')) {
            cursor.classList.add('click-effect');
        }
    });

    document.addEventListener('mouseup', () => {
        if (cursor) {
            cursor.classList.remove('click-effect');
        }
    });
});
"""
        if "ANIMATED DOM CURSOR LOGIC" not in js:
            js += "\n" + dom_cursor_js

        with open('static/script.js', 'w', encoding='utf-8') as f:
            f.write(js)
        print("Patched script.js")
    except Exception as e:
        print("JS error:", e)

patch_css()
patch_html('templates/index.html')
patch_html('templates/admin.html')
patch_js()
