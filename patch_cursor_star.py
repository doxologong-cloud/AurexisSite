import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make the default cursor apply to absolutely everything
old_rule = r'html, body \{[\s\n]*cursor: var\(--cursor-default, auto\) !important;[\s\n]*\}'
new_rule = """*, html, body {
    cursor: var(--cursor-default, auto) !important;
}"""

if re.search(old_rule, css):
    css = re.sub(old_rule, new_rule, css)
else:
    # If not found, just prepend it
    css = new_rule + "\n" + css

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# Update cache buster
for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'\?v=\d+', '?v=88', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    except FileNotFoundError:
        pass
