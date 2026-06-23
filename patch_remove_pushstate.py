import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Modify the anchor click listener
old_listener = """        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetHash = this.getAttribute('href');
                if (window.location.hash !== targetHash) {
                    window.history.pushState(null, null, targetHash);
                    handleRoute();
                }
            });
        });"""

new_listener = """        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetHash = this.getAttribute('href');
                // Instead of pushState, we just manually update the route without triggering the browser's navigation history
                // This prevents Chromium from executing its hardcoded security cursor reset on URL change
                
                // We keep a custom variable to track the fake hash if needed
                window._currentFakeHash = targetHash;
                handleRoute();
            });
        });"""

js = js.replace(old_listener, new_listener)

# Modify handleRoute to read the fake hash
old_handle_route = "function _executeRouteDOMSwap() {\n        const hash = window.location.hash || '#home';"
new_handle_route = "function _executeRouteDOMSwap() {\n        const hash = window._currentFakeHash || window.location.hash || '#home';"
js = js.replace(old_handle_route, new_handle_route)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Removed pushState from script.js")

# Bump cache
for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'\?v=\d+', '?v=103', html)
        html = re.sub(r'Последнее обновление: v[\d\.]+', 'Последнее обновление: v1.13', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Bumped cache in {path}")
    except FileNotFoundError:
        pass
