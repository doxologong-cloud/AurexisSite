import re

# Old SVG patterns with filters
old_default = r'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23\$\{color1\}"/><stop offset="100%25" stop-color="%23\$\{color2\}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0\.6"/></filter></defs><g filter="url\(%23shadow\)" transform="translate\(12, 6\) rotate\(-25\)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url\(%23theme-grad\)"/><polygon points="1,0 9,18 4,18 1,12" fill="url\(%23theme-grad\)"/></g></svg>'
old_pointer = r'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23\$\{ptrColor1\}"/><stop offset="100%25" stop-color="%23\$\{ptrColor2\}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0\.6"/></filter></defs><g filter="url\(%23shadow\)" transform="translate\(12, 6\) rotate\(-25\)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url\(%23theme-grad-ptr\)"/><polygon points="1,0 9,18 4,18 1,12" fill="url\(%23theme-grad-ptr\)"/></g></svg>'
old_hacker = r'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><filter id="glow"><feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="%23ff0000" flood-opacity="1"/></filter></defs><path d="M 4 4 L 12 28 L 16 16 L 28 12 Z" fill="%23ff0000" filter="url\(%23glow\)"/></svg>'

old_hacker_unencoded = r'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><filter id="glow"><feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#ff0000" flood-opacity="1"/></filter></defs><path d="M 4 4 L 12 28 L 16 16 L 28 12 Z" fill="#ff0000" filter="url\(#glow\)"/></svg>'


# New filter-less SVGs
# For default/pointer, we simulate shadow by drawing black polygons behind with opacity.
new_default = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${color1}"/><stop offset="100%25" stop-color="%23${color2}"/></linearGradient></defs><g transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="1,0 9,18 4,18 1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad)"/></g></svg>'
new_pointer = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${ptrColor1}"/><stop offset="100%25" stop-color="%23${ptrColor2}"/></linearGradient></defs><g transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="1,0 9,18 4,18 1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad-ptr)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad-ptr)"/></g></svg>'
# For hacker, we use stroke to simulate a glow
new_hacker = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M 4 4 L 12 28 L 16 16 L 28 12 Z" fill="#ff0000" stroke="#ff0000" stroke-width="3" stroke-linejoin="round" stroke-opacity="0.4"/></svg>'


def apply_patch(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content = re.sub(old_default, new_default, content)
        content = re.sub(old_pointer, new_pointer, content)
        content = re.sub(old_hacker, new_hacker, content)
        content = re.sub(old_hacker_unencoded, new_hacker, content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")
    except FileNotFoundError:
        pass

apply_patch('static/script.js')
apply_patch('templates/index.html')
apply_patch('templates/admin.html')

# Update cache buster
for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = re.sub(r'\?v=\d+', '?v=89', html)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    except FileNotFoundError:
        pass
