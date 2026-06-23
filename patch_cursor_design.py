import re

try:
    with open('static/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Find the block we added previously
    old_block_regex = r"/\* === ANIMATED DOM CURSOR === \*/.*?#custom-cursor\.hover-effect \{.*?\}"
    
    new_block = """/* === ANIMATED DOM CURSOR === */
html.cursor-circle, html.cursor-circle * {
    cursor: none !important;
}

#custom-cursor {
    position: fixed;
    top: 0;
    left: 0;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999999;
    transform: translate(-50%, -50%);
    transition: width 0.15s ease, height 0.15s ease, background-color 0.15s ease, border 0.15s ease, opacity 0.15s ease;
    border: 2px solid var(--neon-primary, #ff0055);
    box-sizing: border-box;
    display: none;
    box-shadow: 0 0 10px var(--neon-primary, #ff0055), 0 0 10px var(--neon-primary, #ff0055) inset;
}

/* Inner dot */
#custom-cursor::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 6px;
    height: 6px;
    background-color: var(--neon-primary, #ff0055);
    border-radius: 50%;
    transition: opacity 0.15s ease, transform 0.15s ease;
}

/* Click effect: Ripple expansion */
#custom-cursor.click-effect {
    width: 45px;
    height: 45px;
    border-width: 1px;
    opacity: 0.5;
}
#custom-cursor.click-effect::after {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0);
}

/* Hover effect: Hollow larger ring */
#custom-cursor.hover-effect {
    width: 32px;
    height: 32px;
    background-color: rgba(255, 255, 255, 0.05);
    border-color: var(--neon-color, #ffcc00);
    box-shadow: 0 0 15px var(--neon-color, #ffcc00), 0 0 15px var(--neon-color, #ffcc00) inset;
}
#custom-cursor.hover-effect::after {
    opacity: 0;
}"""

    # We need to replace it using re.DOTALL
    if "/* === ANIMATED DOM CURSOR === */" in css:
        css = re.sub(old_block_regex, new_block, css, flags=re.DOTALL)
        with open('static/style.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("Patched style.css successfully with improved cursor.")
    else:
        print("Could not find the animated cursor block to replace.")

    # Bump cache
    for path in ['templates/index.html', 'templates/admin.html']:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            html = re.sub(r'\?v=\d+', '?v=107', html)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception:
            pass

except Exception as e:
    print(f"Error: {e}")
