import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = """
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <button id="add-to-contacts-btn" class="glow-btn" style="padding: 5px 10px; font-size: 0.8rem; display: none;">+ В контакты</button>
                            <button id="chat-settings-btn" style="background: none; border: none; color: white; cursor: pointer; font-size: 1.2rem;">⋮</button>
                        </div>
"""

if 'id="add-to-contacts-btn"' not in text:
    text = text.replace('<button id="chat-settings-btn" style="background: none; border: none; color: white; cursor: pointer; font-size: 1.2rem;">⋮</button>', replacement.strip())
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added contacts button")
else:
    print("Contacts button already present")
