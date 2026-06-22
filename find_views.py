import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'<div[^>]*class="[^"]*view[^"]*"[^>]*id="(view-[^"]+)"', text)
print(matches)

# Let's also check if view-editor is inside view-home
home_idx = text.find('id="view-home"')
editor_idx = text.find('id="view-editor"')
print(f'home: {home_idx}, editor: {editor_idx}')
