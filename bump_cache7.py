import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'src="/static/script.js\?v=\d+"', 'src="/static/script.js?v=7"', text)
text = re.sub(r'href="/static/style.css\?v=\d+"', 'href="/static/style.css?v=7"', text)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Bumped cache bust to v=7")
