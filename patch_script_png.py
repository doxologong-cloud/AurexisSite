import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# We need to find the section in script.js where `finalCursorDefault` and `finalCursorPointer` are defined and cursorStyleEl is populated.
# We will replace it with the rasterizeSVGToPNG logic.

old_block = r"""        let finalCursorDefault = `url\("data:image/svg\+xml,\$\{encodeURIComponent\(svgDefaultStr\)\}"\) 12 6, auto`;
        let finalCursorPointer = `url\("data:image/svg\+xml,\$\{encodeURIComponent\(svgPointerStr\)\}"\) 12 6, pointer`;

        if \(themeName === 'hacked'\) \{
            const hackerCursorStr = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M 2 2 L 10 22 L 13 13 L 22 10 Z" fill="#ff0000" stroke="#ff0000" stroke-width="2" stroke-linejoin="round" stroke-opacity="0.4"/></svg>`;
            finalCursorDefault = `url\("data:image/svg\+xml,\$\{encodeURIComponent\(hackerCursorStr\)\}"\) 2 2, crosshair`;
            finalCursorPointer = `url\("data:image/svg\+xml,\$\{encodeURIComponent\(hackerCursorStr\)\}"\) 2 2, crosshair`;
        \}

        let cursorStyleEl = document\.getElementById\('dynamic-cursor-style'\);
        if \(!cursorStyleEl\) \{
            cursorStyleEl = document\.createElement\('style'\);
            cursorStyleEl\.id = 'dynamic-cursor-style';
            document\.head\.appendChild\(cursorStyleEl\);
        \}
        cursorStyleEl\.innerHTML = `
            html, body, div, p, span, h1, h2, h3, h4, h5, h6, section, article, nav, header, footer, main, ul, li, label,
            #cursor-lock, \.view, \.view \* \{
                cursor: \$\{finalCursorDefault\} !important;
            \}
            a, a:hover, a:active, a:focus,
            button, button:hover, button:active, button:focus,
            input, select, textarea, \.theme-card, \.msgr-tab, \.dropdown-item,
            \[onclick\], \[onclick\] \* \{
                cursor: \$\{finalCursorPointer\} !important;
            \}
            #cursor-lock \{
                cursor: \$\{finalCursorDefault\} !important;
            \}
        `;"""

new_block = """        // Helper function for PNG rasterization
        function rasterizeSVGToPNG(svgStr, hotspotX, hotspotY, callback) {
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                canvas.width = img.width || 32;
                canvas.height = img.height || 32;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                const pngDataUrl = canvas.toDataURL('image/png');
                callback(`url("${pngDataUrl}") ${hotspotX} ${hotspotY}`);
            };
            img.src = 'data:image/svg+xml,' + encodeURIComponent(svgStr);
        }

        const hackerCursorStr = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M 2 2 L 10 22 L 13 13 L 22 10 Z" fill="#ff0000" stroke="#ff0000" stroke-width="2" stroke-linejoin="round" stroke-opacity="0.4"/></svg>`;

        rasterizeSVGToPNG(themeName === 'hacked' ? hackerCursorStr : svgDefaultStr, themeName === 'hacked' ? 2 : 12, themeName === 'hacked' ? 2 : 6, function(pngUrlDefault) {
            rasterizeSVGToPNG(themeName === 'hacked' ? hackerCursorStr : svgPointerStr, themeName === 'hacked' ? 2 : 12, themeName === 'hacked' ? 2 : 6, function(pngUrlPointer) {
                let cursorStyleEl = document.getElementById('dynamic-cursor-style');
                if (!cursorStyleEl) {
                    cursorStyleEl = document.createElement('style');
                    cursorStyleEl.id = 'dynamic-cursor-style';
                    document.head.appendChild(cursorStyleEl);
                }
                cursorStyleEl.innerHTML = `
                    html, body, div, p, span, h1, h2, h3, h4, h5, h6, section, article, nav, header, footer, main, ul, li, label,
                    #cursor-lock, .view, .view * {
                        cursor: ${pngUrlDefault}, auto !important;
                    }
                    a, a:hover, a:active, a:focus,
                    button, button:hover, button:active, button:focus,
                    input, select, textarea, .theme-card, .msgr-tab, .dropdown-item,
                    [onclick], [onclick] * {
                        cursor: ${pngUrlPointer}, pointer !important;
                    }
                    #cursor-lock {
                        cursor: ${pngUrlDefault}, auto !important;
                    }
                `;
            });
        });"""

if re.search(old_block, js):
    js = re.sub(old_block, new_block, js)
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched script.js")
else:
    print("Could not find the old block in script.js")

# also increment cache buster
for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'\?v=\d+', '?v=100', html)
        # Update version in footer
        html = re.sub(r'Последнее обновление: v[\d\.]+', 'Последнее обновление: v1.10', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Bumped version in {path}")
    except FileNotFoundError:
        pass
