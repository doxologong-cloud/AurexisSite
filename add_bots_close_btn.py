import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add X button to the Bots tab
old_header = """<span><i class="fa-solid fa-robot"></i> УПРАВЛЕНИЕ БОТАМИ</span>
                    <button style="background: transparent; border: 1px dashed #7f91a4; color: #7f91a4; cursor: pointer; padding: 5px 15px; border-radius: 4px;">+ ДОБАВИТЬ</button>"""
                    
new_header = """<span><i class="fa-solid fa-robot"></i> УПРАВЛЕНИЕ БОТАМИ</span>
                    <div style="display: flex; gap: 10px;">
                        <button style="background: transparent; border: 1px dashed #7f91a4; color: #7f91a4; cursor: pointer; padding: 5px 15px; border-radius: 4px;">+ ДОБАВИТЬ</button>
                        <button onclick="openTab('welcome')" style="background: transparent; border: none; color: #7f91a4; font-size: 1.2rem; cursor: pointer; transition: 0.2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#7f91a4'"><i class="fa-solid fa-xmark"></i></button>
                    </div>"""

text = text.replace(old_header, new_header)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Close button added to bots tab.")
