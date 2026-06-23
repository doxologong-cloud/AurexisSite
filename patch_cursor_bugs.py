import re

try:
    with open('static/script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # We need to modify changeTheme to prevent injecting cursor: url() when shape === 'circle'
    old_rasterize_logic = r"rasterizeSVGToPNG\(themeName === 'hacked' \? hackerCursorStr : svgDefaultStr, hotspotDefX, hotspotDefY, function\(pngUrlDefault\) \{.*?\}\);\s*\}\);"
    
    new_rasterize_logic = """if (shape === 'circle') {
            let cursorStyleEl = document.getElementById('dynamic-cursor-style');
            if (!cursorStyleEl) {
                cursorStyleEl = document.createElement('style');
                cursorStyleEl.id = 'dynamic-cursor-style';
                document.head.appendChild(cursorStyleEl);
            }
            cursorStyleEl.innerHTML = `* { cursor: none !important; }`;
        } else {
            rasterizeSVGToPNG(themeName === 'hacked' ? hackerCursorStr : svgDefaultStr, hotspotDefX, hotspotDefY, function(pngUrlDefault) {
                rasterizeSVGToPNG(themeName === 'hacked' ? hackerCursorStr : svgPointerStr, hotspotPtrX, hotspotPtrY, function(pngUrlPointer) {
                    let cursorStyleEl = document.getElementById('dynamic-cursor-style');
                    if (!cursorStyleEl) {
                        cursorStyleEl = document.createElement('style');
                        cursorStyleEl.id = 'dynamic-cursor-style';
                        document.head.appendChild(cursorStyleEl);
                    }
                    cursorStyleEl.innerHTML = `
                        html, body, div, p, span, h1, h2, h3, h4, h5, h6, section, article, nav, header, footer, main, ul, li, label,
                        .view, .view * {
                            cursor: ${pngUrlDefault}, auto !important;
                        }
                        a, a:hover, a:active, a:focus,
                        button, button:hover, button:active, button:focus,
                        input, select, textarea, .theme-card, .msgr-tab, .dropdown-item,
                        [onclick], [onclick] * {
                            cursor: ${pngUrlPointer}, pointer !important;
                        }
                    `;
                });
            });
        }"""
    
    # We replace the rasterize logic using re.DOTALL
    js = re.sub(old_rasterize_logic, new_rasterize_logic, js, flags=re.DOTALL)

    # Now add mouseleave/mouseenter logic to DOM cursor
    old_dom_logic = r"document.addEventListener\('mouseup', \(\) => \{\s*if \(cursor\) \{\s*cursor.classList.remove\('click-effect'\);\s*\}\s*\}\);"
    new_dom_logic = """document.addEventListener('mouseup', () => {
        if (cursor) cursor.classList.remove('click-effect');
    });

    document.addEventListener('mouseleave', () => {
        if (cursor) cursor.style.opacity = '0';
    });

    document.addEventListener('mouseenter', () => {
        if (cursor && document.documentElement.classList.contains('cursor-circle')) cursor.style.opacity = '1';
    });"""

    js = re.sub(old_dom_logic, new_dom_logic, js)

    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched script.js successfully to fix overlapping cursors and mouseleave bugs.")

    # Bump cache
    for path in ['templates/index.html', 'templates/admin.html']:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                html = f.read()
            html = re.sub(r'\?v=\d+', '?v=110', html)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception:
            pass

except Exception as e:
    print(f"Error: {e}")
