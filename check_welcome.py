import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()
match = re.search(r'<div id="welcome-screen"[^>]*>.*?</div>', text, flags=re.DOTALL)
if match:
    print("Found welcome screen length:", len(match.group()))
else:
    print("Not found")
