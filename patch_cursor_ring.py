import re

try:
    with open('static/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    old_block_regex = r"/\* === ANIMATED DOM CURSOR === \*/.*?#custom-cursor\.hover-effect::after \{.*?^\}"
    
    new_block = """/* === ANIMATED DOM CURSOR === */
html.cursor-circle, html.cursor-circle * {
    cursor: none !important;
}

#custom-cursor {
    position: fixed;
    top: 0;
    left: 0;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: transparent !important;
    pointer-events: none;
    z-index: 9999999;
    transform: translate(-50%, -50%);
    transition: width 0.15s ease, height 0.15s ease, border-color 0.15s ease, opacity 0.15s ease, box-shadow 0.15s ease;
    border: 2px solid var(--neon-primary, #ff0055);
    box-sizing: border-box;
    display: none;
    box-shadow: 0 0 10px var(--neon-primary, #ff0055), 0 0 10px var(--neon-primary, #ff0055) inset;
}

/* Click effect: Ripple expansion */
#custom-cursor.click-effect {
    width: 40px;
    height: 40px;
    border-width: 1px;
    opacity: 0.5;
}

/* Hover effect: Slightly larger ring for buttons/links */
#custom-cursor.hover-effect {
    width: 28px;
    height: 28px;
    border-color: var(--neon-color, #ffcc00);
    box-shadow: 0 0 15px var(--neon-color, #ffcc00), 0 0 15px var(--neon-color, #ffcc00) inset;
}"""

    if "/* === ANIMATED DOM CURSOR === */" in css:
        css = re.sub(old_block_regex, new_block, css, flags=re.DOTALL|re.MULTILINE)
        with open('static/style.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("Patched style.css successfully with hollow ring cursor.")
    else:
        print("Could not find the animated cursor block to replace.")

    # Bump cache
    for path in ['templates/index.html', 'templates/admin.html']:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            html = re.sub(r'\?v=\d+', '?v=108', html)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception:
            pass

except Exception as e:
    print(f"Error: {e}")
