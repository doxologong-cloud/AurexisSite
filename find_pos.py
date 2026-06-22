import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.finditer(r'<div[^>]*class="[^"]*view[^"]*"[^>]*id="(view-[^"]+)"', text)
for m in matches:
    print(m.group(1), m.start())
