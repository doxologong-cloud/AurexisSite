import re

# 1. Update style.css
with open('static/style.css', 'r', encoding='utf-8') as f:
    css_text = f.read()

# Replace hardcoded body cursor
old_body_cursor = r"cursor: url\('data:image/svg\+xml;utf8,<svg.*?'\) 12 6, auto !important;"
new_body_cursor = "cursor: var(--cursor-default, auto) !important;"
css_text = re.sub(old_body_cursor, new_body_cursor, css_text)

# Replace hardcoded pointer cursor
old_pointer_cursor = r"cursor: url\('data:image/svg\+xml;utf8,<svg.*?'\) 12 6, pointer !important;"
new_pointer_cursor = "cursor: var(--cursor-pointer, pointer) !important;"
css_text = re.sub(old_pointer_cursor, new_pointer_cursor, css_text)

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css_text)


# 2. Update script.js
with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# We need to inject the cursor logic into changeTheme.
# Let's find changeTheme
old_change_theme = """function changeTheme(themeName) {
    const root = document.documentElement;
    if (themeName === 'matrix') {
        root.style.setProperty('--neon-color', '#ffcc00');
        root.style.setProperty('--bg-color', '#0a0a0a');
        root.style.setProperty('--glow-color', 'rgba(255, 204, 0, 0.5)');
        root.style.setProperty('--neon-primary', '#e5b322');
    } else if (themeName === 'synthwave') {
        root.style.setProperty('--neon-color', '#ff00ff');
        root.style.setProperty('--bg-color', '#1a0b2e');
        root.style.setProperty('--glow-color', 'rgba(255, 0, 255, 0.5)');
        root.style.setProperty('--neon-primary', '#b026ff');
    } else if (themeName === 'cyberpunk') {
        root.style.setProperty('--neon-color', '#00ffcc');
        root.style.setProperty('--bg-color', '#0b1a1a');
        root.style.setProperty('--glow-color', 'rgba(0, 255, 204, 0.5)');
        root.style.setProperty('--neon-primary', '#00ff88');
    }
    localStorage.setItem('aurex_theme', themeName);"""

new_change_theme = """function changeTheme(themeName) {
    const root = document.documentElement;
    let color1, color2, ptrColor1, ptrColor2;
    
    if (themeName === 'matrix') {
        root.style.setProperty('--neon-color', '#ffcc00');
        root.style.setProperty('--bg-color', '#0a0a0a');
        root.style.setProperty('--glow-color', 'rgba(255, 204, 0, 0.5)');
        root.style.setProperty('--neon-primary', '#e5b322');
        color1 = 'FFE373'; color2 = 'D4AF37'; ptrColor1 = 'ffffff'; ptrColor2 = 'FFE373';
    } else if (themeName === 'synthwave') {
        root.style.setProperty('--neon-color', '#ff00ff');
        root.style.setProperty('--bg-color', '#1a0b2e');
        root.style.setProperty('--glow-color', 'rgba(255, 0, 255, 0.5)');
        root.style.setProperty('--neon-primary', '#b026ff');
        color1 = 'ff66ff'; color2 = 'ff00ff'; ptrColor1 = 'ffffff'; ptrColor2 = 'ff66ff';
    } else if (themeName === 'cyberpunk') {
        root.style.setProperty('--neon-color', '#00ffcc');
        root.style.setProperty('--bg-color', '#0b1a1a');
        root.style.setProperty('--glow-color', 'rgba(0, 255, 204, 0.5)');
        root.style.setProperty('--neon-primary', '#00ff88');
        color1 = '66ffeb'; color2 = '00ffcc'; ptrColor1 = 'ffffff'; ptrColor2 = '66ffeb';
    }
    
    const svgDefault = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${color1}"/><stop offset="100%25" stop-color="%23${color2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad)"/></g></svg>`;
    const svgPointer = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${ptrColor1}"/><stop offset="100%25" stop-color="%23${ptrColor2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad-ptr)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad-ptr)"/></g></svg>`;
    
    root.style.setProperty('--cursor-default', `url('${svgDefault}') 12 6, auto`);
    root.style.setProperty('--cursor-pointer', `url('${svgPointer}') 12 6, pointer`);
    
    localStorage.setItem('aurex_theme', themeName);"""

js_text = js_text.replace(old_change_theme, new_change_theme)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

# Let's also patch the FOUC inline script in index.html to apply the cursor on load so it doesn't flicker standard cursor
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

old_inline_theme = """        if (savedTheme === 'matrix') {
            root.style.setProperty('--neon-color', '#ffcc00');
            root.style.setProperty('--bg-color', '#0a0a0a');
            root.style.setProperty('--glow-color', 'rgba(255, 204, 0, 0.5)');
        } else if (savedTheme === 'synthwave') {
            root.style.setProperty('--neon-color', '#ff00ff');
            root.style.setProperty('--bg-color', '#1a0b2e');
            root.style.setProperty('--glow-color', 'rgba(255, 0, 255, 0.5)');
        } else if (savedTheme === 'cyberpunk') {
            root.style.setProperty('--neon-color', '#00ffcc');
            root.style.setProperty('--bg-color', '#0b1a1a');
            root.style.setProperty('--glow-color', 'rgba(0, 255, 204, 0.5)');
        }"""

new_inline_theme = """        let color1, color2, ptrColor1, ptrColor2;
        if (savedTheme === 'matrix') {
            root.style.setProperty('--neon-color', '#ffcc00');
            root.style.setProperty('--bg-color', '#0a0a0a');
            root.style.setProperty('--glow-color', 'rgba(255, 204, 0, 0.5)');
            root.style.setProperty('--neon-primary', '#e5b322');
            color1 = 'FFE373'; color2 = 'D4AF37'; ptrColor1 = 'ffffff'; ptrColor2 = 'FFE373';
        } else if (savedTheme === 'synthwave') {
            root.style.setProperty('--neon-color', '#ff00ff');
            root.style.setProperty('--bg-color', '#1a0b2e');
            root.style.setProperty('--glow-color', 'rgba(255, 0, 255, 0.5)');
            root.style.setProperty('--neon-primary', '#b026ff');
            color1 = 'ff66ff'; color2 = 'ff00ff'; ptrColor1 = 'ffffff'; ptrColor2 = 'ff66ff';
        } else if (savedTheme === 'cyberpunk') {
            root.style.setProperty('--neon-color', '#00ffcc');
            root.style.setProperty('--bg-color', '#0b1a1a');
            root.style.setProperty('--glow-color', 'rgba(0, 255, 204, 0.5)');
            root.style.setProperty('--neon-primary', '#00ff88');
            color1 = '66ffeb'; color2 = '00ffcc'; ptrColor1 = 'ffffff'; ptrColor2 = '66ffeb';
        } else {
            color1 = 'FFE373'; color2 = 'D4AF37'; ptrColor1 = 'ffffff'; ptrColor2 = 'FFE373'; // fallback matrix
        }
        
        const svgDefault = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${color1}"/><stop offset="100%25" stop-color="%23${color2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad)"/></g></svg>`;
        const svgPointer = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${ptrColor1}"/><stop offset="100%25" stop-color="%23${ptrColor2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad-ptr)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad-ptr)"/></g></svg>`;
        root.style.setProperty('--cursor-default', `url('${svgDefault}') 12 6, auto`);
        root.style.setProperty('--cursor-pointer', `url('${svgPointer}') 12 6, pointer`);
"""

html_text = html_text.replace(old_inline_theme, new_inline_theme)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_text)

print("Dynamic themed cursor successfully injected!")
