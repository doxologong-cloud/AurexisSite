import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Cache bust script.js
text = re.sub(r'src="/static/script\.js(\?v=\d+)?"', r'src="/static/script.js?v=3"', text)
text = re.sub(r'href="/static/style\.css(\?v=\d+)?"', r'href="/static/style.css?v=3"', text)

# Just to be 100% sure we replace all occurrences of FLORA with Aurex
text = text.replace('FLORA', 'Aurex')
text = text.replace('AUREXIS Aurex', 'AUREX') # Fix potential duplicate

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added cache busting and cleared FLORA from HTML")
