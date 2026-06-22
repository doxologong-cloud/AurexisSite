import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_logic = "window.addEventListener('hashchange', handleRoute);\n    }"
new_logic = """window.addEventListener('hashchange', handleRoute);
        
        // Prevent cursor flicker on navigation links by intercepting native hash scrolling
        document.querySelectorAll('a[href^=\"#\"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetHash = this.getAttribute('href');
                if (window.location.hash !== targetHash) {
                    window.history.pushState(null, null, targetHash);
                    handleRoute();
                }
            });
        });
    }"""

js = js.replace(old_logic, new_logic)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update cache buster
for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'\?v=\d+', '?v=87', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    except FileNotFoundError:
        pass
