import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove JS custom cursor logic
js_to_remove = r"""// ==========================================
// Custom Cursor Logic
// ==========================================
const cursor = document\.getElementById\('custom-cursor'\);
if \(cursor\) \{
    document\.addEventListener\('mousemove', e => \{
        cursor\.style\.left = e\.clientX \+ 'px';
        cursor\.style\.top = e\.clientY \+ 'px';
    \}\);

    document\.addEventListener\('mousedown', \(\) => cursor\.classList\.add\('clicking'\)\);
    document\.addEventListener\('mouseup', \(\) => cursor\.classList\.remove\('clicking'\)\);

    // Hover effect on interactive elements
    const interactiveElements = document\.querySelectorAll\('a, button, input, textarea, select, \.theme-card, \.msgr-tab, \.dropdown-item'\);
    interactiveElements\.forEach\(el => \{
        el\.addEventListener\('mouseenter', \(\) => cursor\.classList\.add\('hovering'\)\);
        el\.addEventListener\('mouseleave', \(\) => cursor\.classList\.remove\('hovering'\)\);
    \}\);
\}"""

text = re.sub(js_to_remove, '', text, flags=re.MULTILINE)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(text)

# Now index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html_text = f.read()

html_text = html_text.replace('<div id="custom-cursor"></div>\n', '')
html_text = html_text.replace('<select id="lang-selector" onchange="changeLang(this.value)" style="background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 10px; border-radius: 8px; cursor: none; font-size: 1rem; width: 200px;">', '<select id="lang-selector" onchange="changeLang(this.value)" style="background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.2); color: white; padding: 10px; border-radius: 8px; cursor: pointer; font-size: 1rem; width: 200px;">')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_text)

print("JS and HTML custom cursor removed.")
