import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'href="/static/style\.css\?v=\d+"', r'href="/static/style.css?v=5"', text)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Bumped cache bust version for CSS")
