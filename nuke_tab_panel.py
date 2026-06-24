import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. NUKE tab-panel entirely
html = re.sub(r'<!-- Panel \(Console\) Tab -->.*?<!-- Journal Tab -->', '<!-- Journal Tab -->', html, flags=re.DOTALL)

# 2. Make sure tab-welcome is visible by default when vault opens
# I'll just rely on `openTab('welcome')` inside `unlockVault`
if "initVault();" in html and "openTab('welcome');" not in html:
    html = html.replace("initVault();", "initVault();\n            openTab('welcome');")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Nuked tab-panel from index.html and set default tab to welcome.")
