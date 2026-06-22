import re

# 1. Update script.js handleRoute()
with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_route = """    function handleRoute() {
        const hash = window.location.hash || '#home';
        
        document.querySelectorAll('.view').forEach(v => {"""

new_route = """    function handleRoute() {
        // === CURSOR LOCK OVERLAY ===
        // Prevents browser cursor flashing during DOM reflows and CSS animations
        let cursorLock = document.getElementById('cursor-lock');
        if (!cursorLock) {
            cursorLock = document.createElement('div');
            cursorLock.id = 'cursor-lock';
            cursorLock.style.position = 'fixed';
            cursorLock.style.top = '0';
            cursorLock.style.left = '0';
            cursorLock.style.width = '100vw';
            cursorLock.style.height = '100vh';
            cursorLock.style.zIndex = '9999999';
            document.body.appendChild(cursorLock);
        }
        cursorLock.style.display = 'block';
        cursorLock.style.setProperty('cursor', 'var(--cursor-default, auto)', 'important');

        setTimeout(() => {
            cursorLock.style.display = 'none';
        }, 400); // 0.3s transition + 100ms buffer
        // ============================

        const hash = window.location.hash || '#home';
        
        document.querySelectorAll('.view').forEach(v => {"""

js = js.replace(old_route, new_route)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 2. Update style.css specific tag list
with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_css = r"html, body \{\s*cursor: var\(--cursor-default, auto\) !important;\s*\}"
new_css = """html, body, div, p, span, h1, h2, h3, h4, h5, h6, section, article, nav, header, footer, main, ul, li, label {
    cursor: var(--cursor-default, auto) !important;
}"""

if re.search(old_css, css):
    css = re.sub(old_css, new_css, css)
else:
    css = new_css + "\n" + css

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Update cache buster
for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'\?v=\d+', '?v=93', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    except FileNotFoundError:
        pass
