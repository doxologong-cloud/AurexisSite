import re

try:
    with open('static/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    old_block_regex = r"/\* === ANIMATED DOM CURSOR === \*/.*?#custom-cursor\.hover-effect \{.*?\}"
    
    new_block = """/* === ANIMATED DOM CURSOR === */
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
}"""

    if "/* === ANIMATED DOM CURSOR === */" in css:
        css = re.sub(old_block_regex, new_block, css, flags=re.DOTALL|re.MULTILINE)
        with open('static/style.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("Patched style.css successfully, restoring solid filled circle.")
    else:
        print("Could not find the animated cursor block to replace.")

    # Bump cache
    for path in ['templates/index.html', 'templates/admin.html']:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            html = re.sub(r'\?v=\d+', '?v=109', html)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception:
            pass

except Exception as e:
    print(f"Error: {e}")
