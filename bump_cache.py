import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'src="/static/script\.js\?v=\d+"', r'src="/static/script.js?v=4"', text)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Bumped cache bust version")
