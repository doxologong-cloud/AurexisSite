import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    css_text = f.read()

# 1. Remove the custom cursor block
cursor_block = r"""/\* CUSTOM CURSOR \*/.*?#custom-cursor\.hovering \{.*?\}"""
css_text = re.sub(cursor_block, '', css_text, flags=re.MULTILINE | re.DOTALL)

# 2. Add the original Aurexis logo cursor to the body and links
logo_cursor_css = """
body {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23FFE373"/><stop offset="100%25" stop-color="%23D4AF37"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23gold)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23gold)"/></g></svg>') 12 6, auto !important;
}

a, button, input, textarea, select, .theme-card, .msgr-tab, .dropdown-item {
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23ffffff"/><stop offset="100%25" stop-color="%23FFE373"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23gold)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23gold)"/></g></svg>') 12 6, pointer !important;
}
"""

css_text += logo_cursor_css

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css_text)

# 3. Remove custom cursor JS
with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

js_cursor_block = r"""// ==========================================
// Custom Cursor Logic
// ==========================================
const cursor = document\.getElementById\('custom-cursor'\);
if \(cursor\) \{.*?\}\);
\}"""
js_text = re.sub(js_cursor_block, '', js_text, flags=re.MULTILINE | re.DOTALL)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

# 4. Remove custom cursor HTML
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

html_text = html_text.replace('<body class="custom-cursor-enabled">\n<div id="custom-cursor"></div>', '<body>')
html_text = html_text.replace('<div id="custom-cursor"></div>\n', '')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_text)

print("Restored original logo cursor successfully!")
