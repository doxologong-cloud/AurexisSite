import re

def fix_script(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            js = f.read()

        # Remove the setProperty lines
        js = re.sub(r"root\.style\.setProperty\('--cursor-default', finalCursorDefault\);", "", js)
        js = re.sub(r"root\.style\.setProperty\('--cursor-pointer', finalCursorPointer\);", "", js)

        # Inject the dynamic style tag logic right where setProperty was
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
        
        # We need to insert style_injection after the hackerCursorStr block
        # We find `finalCursorPointer = ... crosshair";\n        }`
        pattern = r"(finalCursorPointer = `url\(\"data:image/svg\+xml,\$\{encodeURIComponent\(hackerCursorStr\)\}\"\) 2 2, crosshair`;\s*\})"
        
        # Replace
        js = re.sub(pattern, r"\1" + "\n" + style_injection, js)
        
        # Increment cache
        if path.endswith('.html'):
            js = re.sub(r'\?v=\d+', '?v=94', js)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(js)
        print(f"Patched {path}")
    except Exception as e:
        print(e)

fix_script('static/script.js')
fix_script('templates/index.html')
fix_script('templates/admin.html')

def fix_css(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            css = f.read()
            
        # We must remove ALL cursor rules from style.css so they don't conflict
        css = re.sub(r"html, body, div, p, span, h1, h2, h3, h4, h5, h6, section, article, nav, header, footer, main, ul, li, label \{\s*cursor: var\(--cursor-default, auto\) !important;\s*\}", "", css)
        css = re.sub(r"a, a:hover, a:active, a:focus,.*?\[onclick\] \{\s*cursor: var\(--cursor-pointer, pointer\) !important;\s*\}", "", css, flags=re.DOTALL)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(css)
        print(f"Cleaned {path}")
    except Exception as e:
        print(e)

fix_css('static/style.css')
