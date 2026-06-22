import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_block = """    function handleRoute() {
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

        setTimeout(() => {
            cursorLock.style.display = 'none';
        }, 400); // 0.3s transition + 100ms buffer
        // ============================

        const hash = window.location.hash || '#home';"""

new_block = """    function handleRoute() {
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

    function _executeRouteDOMSwap() {
        const hash = window.location.hash || '#home';"""

if old_block in js:
    js = js.replace(old_block, new_block)
else:
    print("WARNING: old_block not found precisely. Falling back to regex.")
    # Fallback just in case
    pattern = r"function handleRoute\(\) \{.*?const hash = window\.location\.hash \|\| '#home';"
    js = re.sub(pattern, new_block, js, flags=re.DOTALL)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update cache buster
for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'\?v=\d+', '?v=97', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    except FileNotFoundError:
        pass

print("Patch applied.")
