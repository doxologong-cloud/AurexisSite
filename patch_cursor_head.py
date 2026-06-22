import re

def fix_html_head(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Clean up any bad cursor strings
        html = html.replace(r"url(\'data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}\') 16 16, crosshair", r'url("data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}") 2 2, crosshair')
        html = html.replace(r"url(\'data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}\') 2 2, crosshair", r'url("data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}") 2 2, crosshair')
        
        # Inject the style element generation at the end of the inline script in head
        # Find the end of the inline script: `    })();\n</script>`
        
        style_injection = """
        let cursorStyleEl = document.getElementById('dynamic-cursor-style');
        if (!cursorStyleEl) {
            cursorStyleEl = document.createElement('style');
            cursorStyleEl.id = 'dynamic-cursor-style';
            document.head.appendChild(cursorStyleEl);
        }
        cursorStyleEl.innerHTML = `
            html, body, div, p, span, h1, h2, h3, h4, h5, h6, section, article, nav, header, footer, main, ul, li, label,
            #cursor-lock, .view, .view * {
                cursor: ${finalCursorDefault} !important;
            }
            a, a:hover, a:active, a:focus,
            button, button:hover, button:active, button:focus,
            input, select, textarea, .theme-card, .msgr-tab, .dropdown-item,
            [onclick], [onclick] * {
                cursor: ${finalCursorPointer} !important;
            }
            #cursor-lock {
                cursor: ${finalCursorDefault} !important;
            }
        `;
"""
        
        # We want to replace the end of the IIFE
        if 'cursorStyleEl.innerHTML' not in html:
            html = html.replace("    })();\n</script>", style_injection + "    })();\n</script>")

        # Bump cache
        html = re.sub(r'\?v=\d+', '?v=96', html)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Fixed {filepath}")
    except FileNotFoundError:
        pass

fix_html_head('templates/index.html')
fix_html_head('templates/admin.html')

def fix_js(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            js = f.read()

        # Clean up bad cursor strings in script.js too
        js = js.replace(r"url(\'data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}\') 16 16, crosshair", r'url("data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}") 2 2, crosshair')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(js)
        print(f"Fixed {filepath}")
    except FileNotFoundError:
        pass

fix_js('static/script.js')
