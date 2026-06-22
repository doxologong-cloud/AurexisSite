import re

def fix_html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # We will inject a Rasterization function right after finalCursorPointer
        raster_logic = """
        // SVG to PNG Rasterization to fix Chromium hardware cursor SVG cache eviction
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

        // Apply PNG cursors asynchronously to prevent render blocking
        rasterizeSVGToPNG(theme === 'hacked' ? hackerCursorStr : svgDefaultStr, theme === 'hacked' ? 2 : 12, theme === 'hacked' ? 2 : 6, function(pngUrlDefault) {
            rasterizeSVGToPNG(theme === 'hacked' ? hackerCursorStr : svgPointerStr, theme === 'hacked' ? 2 : 12, theme === 'hacked' ? 2 : 6, function(pngUrlPointer) {
                let cursorStyleEl = document.getElementById('dynamic-cursor-style');
                if (cursorStyleEl) {
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
                }
            });
        });
        """
        
        # Insert before the end of the IIFE
        if 'rasterizeSVGToPNG' not in html:
            html = html.replace("    })();\n</script>", raster_logic + "\n    })();\n</script>")
            
        # Bump cache
        html = re.sub(r'\?v=\d+', '?v=99', html)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Fixed {filepath}")
    except FileNotFoundError:
        pass

fix_html('templates/index.html')
fix_html('templates/admin.html')

