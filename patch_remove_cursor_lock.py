import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Remove the cursorLock logic from handleRoute
old_handle_route = """    // SPA Routing Logic
    function handleRoute() {
        // === ADVANCED CURSOR LOCK OVERLAY ===
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
            
            // Hardware Acceleration + Persistent Render Tree
            cursorLock.style.transform = 'translateZ(0)';
            cursorLock.style.willChange = 'visibility';
            cursorLock.style.visibility = 'hidden';
            
            document.body.appendChild(cursorLock);
        }
        
        // Show shield without remounting DOM
        cursorLock.style.visibility = 'visible';

        // Shield lifetime
        setTimeout(() => {
            cursorLock.style.visibility = 'hidden';
        }, 400);

        // Yield main thread to guarantee shield paint BEFORE heavy DOM swap
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                _executeRouteDOMSwap();
            });
        });
    }

    function _executeRouteDOMSwap() {"""

new_handle_route = """    // SPA Routing Logic
    function handleRoute() {"""

js = js.replace(old_handle_route, new_handle_route)

# 2. Remove `#cursor-lock` styling from script.js
js = js.replace("#cursor-lock, .view, .view * {", ".view, .view * {")
js = re.sub(r"#cursor-lock \{\s*cursor: \$\{pngUrlDefault\}, auto !important;\s*\}", "", js)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Cleaned script.js")

# 3. Remove `#cursor-lock` styling from HTML files and bump cache
for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        html = html.replace("#cursor-lock, .view, .view * {", ".view, .view * {")
        html = re.sub(r"#cursor-lock \{\s*cursor: \$\{pngUrlDefault\}, auto !important;\s*\}", "", html)
        
        # Bump cache
        html = re.sub(r'\?v=\d+', '?v=101', html)
        html = re.sub(r'Последнее обновление: v[\d\.]+', 'Последнее обновление: v1.11', html)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Cleaned {path}")
    except FileNotFoundError:
        pass
