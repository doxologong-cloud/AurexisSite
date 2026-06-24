import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_body = """<body>
<div style="display: flex; justify-content: center; align-items: center; height: 100vh; width: 100vw; background: #000; color: #ff0000; font-family: 'Space Grotesk', sans-serif; font-size: 3rem; text-shadow: 0 0 20px #ff0000;">
    (Ведутся РАБОТЫ)
</div>
</body>"""

new_text = re.sub(r'<body>.*</body>', new_body, text, flags=re.DOTALL)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated index.html")
