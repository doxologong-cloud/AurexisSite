import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'<a[^>]*id="open-auth"[^>]*>', text)
if match:
    print(match.group())
