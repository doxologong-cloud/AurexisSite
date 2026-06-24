import re

with open(r"C:\Users\user\Desktop\сайт\templates\index.html", 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "работ" in line.lower() or "ведутся" in line.lower() or "ведуться" in line.lower():
        print(f"{i+1}: {line.strip()}")
