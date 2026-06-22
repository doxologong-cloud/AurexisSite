import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace all simple `cursor: pointer;` with the variable version
css = re.sub(r'cursor:\s*pointer\s*;?', 'cursor: var(--cursor-pointer, pointer) !important;', css)

# Replace the existing general block
old_block = r'a, button, input, textarea, select, \.theme-card, \.msgr-tab, \.dropdown-item \{\s*cursor: var\(--cursor-pointer, pointer\) !important;\s*\}'
new_block = """a, a:hover, a:active, a:focus,
button, button:hover, button:active, button:focus,
input, input:hover, input:active, input:focus,
textarea, textarea:hover, textarea:active, textarea:focus,
select, select:hover, select:active, select:focus,
.theme-card, .theme-card:hover, .theme-card:active,
.msgr-tab, .msgr-tab:hover, .msgr-tab:active,
.dropdown-item, .dropdown-item:hover, .dropdown-item:active,
[onclick], [onclick]:hover, [onclick]:active,
[onclick] *, a *, button * {
    cursor: var(--cursor-pointer, pointer) !important;
}

body:active, body *:active {
    /* Prevent default cursor flashing on any click */
}
"""

css = re.sub(old_block, new_block, css)

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Update inline cursors in script.js
with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("cursor: pointer;", "cursor: var(--cursor-pointer, pointer) !important;")
js = js.replace("cursor = 'pointer'", "style.setProperty('cursor', 'var(--cursor-pointer, pointer)', 'important')")

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

# Update cache buster
for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'\?v=\d+', '?v=86', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    except FileNotFoundError:
        pass
