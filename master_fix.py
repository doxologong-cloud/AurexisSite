"""
Fix vault.html:
1. Create default-avatar.png (solid dark circle) - DONE by previous run
2. Add missing profile-modal div  
3. Remove broken console JS (console is on /console page, not vault)
4. Fix initVault() not being called
"""
import os
import sys

# Set stdout encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

vault_path = r'C:\Users\user\Desktop\сайт\templates\vault.html'
html = open(vault_path, encoding='utf-8').read()

# --- Problem A: Remove broken console JS ---
# It references console-input and console-output which don't exist on this page
# This causes a TypeError crash that breaks ALL subsequent JS including sidebar
import re

# Remove the console logic block
console_block = re.search(
    r'// --- CONSOLE LOGIC ---.*?(?=// --- VAULT LOGIC ---)',
    html, re.DOTALL
)
if console_block:
    html = html[:console_block.start()] + '    // Console is on /console page\n\n    ' + html[console_block.end():]
    print("Removed broken console JS block")
else:
    print("Console block not found by regex - trying manual")
    # Find just the two crashing lines
    for bad_line in [
        "    const consoleInput = document.getElementById('console-input');",
        "    const consoleOutput = document.getElementById('console-output');"
    ]:
        if bad_line in html:
            html = html.replace(bad_line, '    // ' + bad_line.strip())
            print(f"Commented out: {bad_line.strip()}")

# --- Problem B: Add missing profile-modal ---
if 'id="profile-modal"' not in html:
    modal_css = '''<style>
        .modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.75); z-index: 99999; align-items: center; justify-content: center; }
        .modal-overlay.active { display: flex !important; }
        .settings-card { background: #17212b; border-radius: 12px; width: 90%; max-width: 480px; box-shadow: 0 20px 60px rgba(0,0,0,0.9); overflow: hidden; }
        .settings-header { padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #2b3a4a; background: #242f3d; }
        .settings-header h3 { margin: 0; color: #fff; font-size: 1.1rem; }
        .settings-body { padding: 20px; }
        .icon-btn { background: transparent; border: none; color: #7f91a4; font-size: 1.1rem; cursor: pointer; padding: 5px 8px; border-radius: 4px; transition: 0.2s; }
        .icon-btn:hover { color: #fff; background: rgba(255,255,255,0.1); }
        .edit-group { margin-bottom: 12px; }
        .edit-group label { display: block; color: #7f91a4; font-size: 0.82rem; margin-bottom: 5px; }
        .edit-group input, .edit-group textarea { width: 100%; background: #242f3d; color: #fff; border: 1px solid #2b3a4a; padding: 8px 10px; border-radius: 6px; box-sizing: border-box; font-family: inherit; font-size: 0.9rem; }
        .edit-group textarea { resize: vertical; min-height: 60px; }
        .save-btn { width: 100%; background: #4caf50; color: #fff; border: none; padding: 10px; border-radius: 6px; cursor: pointer; font-size: 0.95rem; font-weight: 600; margin-top: 5px; }
        .save-btn:hover { background: #43a047; }
    </style>'''
    
    profile_modal = '''
    <!-- Profile Modal -->
    <div id="profile-modal" class="modal-overlay">
        <div class="settings-card">
            <div class="settings-header">
                <h3>Профиль</h3>
                <div style="display:flex;gap:8px;">
                    <button class="icon-btn" onclick="toggleProfileEdit()" title="Редактировать"><i class="fa-solid fa-pen"></i></button>
                    <button class="icon-btn close-btn" onclick="closeProfile()"><i class="fa-solid fa-xmark"></i></button>
                </div>
            </div>
            <div class="settings-body">
                <div style="text-align:center;margin-bottom:20px;">
                    <div style="position:relative;display:inline-block;">
                        <img src="/static/assets/default-avatar.png" id="profile-avatar-img-lrg" style="width:80px;height:80px;border-radius:50%;object-fit:cover;border:3px solid #8774e1;">
                        <div onclick="changeAvatar()" style="position:absolute;bottom:0;right:0;background:#8774e1;border-radius:50%;width:26px;height:26px;display:flex;align-items:center;justify-content:center;cursor:pointer;"><i class="fa-solid fa-camera" style="font-size:11px;color:#fff;"></i></div>
                    </div>
                    <div id="profile-name-text" style="color:#fff;font-weight:700;font-size:1.2rem;margin-top:10px;">ДомадOX</div>
                    <div class="profile-status" style="color:#7f91a4;font-size:0.85rem;">в сети</div>
                </div>
                <div id="profile-display-mode">
                    <div style="padding:10px 0;border-bottom:1px solid #1e2c38;">
                        <div id="disp-phone" style="color:#fff;font-size:0.95rem;">+7 983 323 7549</div>
                        <div style="color:#7f91a4;font-size:0.78rem;margin-top:2px;">Телефон</div>
                    </div>
                    <div style="padding:10px 0;border-bottom:1px solid #1e2c38;">
                        <div id="disp-bio" style="color:#fff;font-size:0.95rem;">возвращенипе челика под названием doxчеловекglitchитд. заброший акк</div>
                        <div style="color:#7f91a4;font-size:0.78rem;margin-top:2px;">О себе</div>
                    </div>
                    <div style="padding:10px 0;">
                        <div id="disp-username" style="color:#fff;font-size:0.95rem;">@dxdplayersnow</div>
                        <div style="color:#7f91a4;font-size:0.78rem;margin-top:2px;">Имя пользователя</div>
                    </div>
                </div>
                <div id="profile-edit-mode" style="display:none;">
                    <div class="edit-group"><label>Имя</label><input type="text" id="edit-name" value="ДомадOX"></div>
                    <div class="edit-group"><label>Телефон</label><input type="text" id="edit-phone" value="+7 983 323 7549"></div>
                    <div class="edit-group"><label>О себе</label><textarea id="edit-bio">возвращенипе челика под названием doxчеловекglitchитд. заброший акк</textarea></div>
                    <div class="edit-group"><label>Имя пользователя</label><input type="text" id="edit-username" value="@dxdplayersnow"></div>
                    <button class="save-btn" onclick="saveProfile()">Сохранить</button>
                    <button onclick="toggleProfileEdit()" style="width:100%;margin-top:6px;background:transparent;color:#7f91a4;border:1px solid #2b3a4a;padding:8px;border-radius:6px;cursor:pointer;">Отмена</button>
                </div>
            </div>
        </div>
    </div>'''
    
    html = html.replace('</head>', modal_css + '\n</head>', 1)
    html = html.replace('</body>', profile_modal + '\n</body>', 1)
    print("Added profile-modal")
else:
    print("profile-modal already exists")

# --- Problem C: Remove orphaned profile HTML that floats outside vault container ---
# This is the duplicate profile HTML not inside any modal that was accidentally kept
import re
orphaned = re.search(
    r'<div class="profile-actions">.*?</div>\s*</div>\s*</div>\s*\n\s*<!-- Hidden file inputs',
    html, re.DOTALL
)
if orphaned:
    html = html[:orphaned.start()] + '\n    <!-- Hidden file inputs' + html[orphaned.end()-len('<!-- Hidden file inputs'):]
    print("Removed orphaned profile HTML")
else:
    print("Orphaned profile not found (may already be clean)")

# --- Problem D: Ensure initVault() is called ---
if 'initVault();' not in html:
    html = html.replace('</script>\n</body>', '    initVault();\n</script>\n</body>', 1)
    print("Added initVault() call")
else:
    print("initVault() already called")

with open(vault_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"vault.html saved! Size: {len(html)} bytes")

# Verify no duplicate IDs
import re
ids = re.findall(r'id="([^"]+)"', html)
from collections import Counter
dupes = {id_: count for id_, count in Counter(ids).items() if count > 1}
if dupes:
    print(f"WARNING: Duplicate IDs found: {dupes}")
else:
    print("No duplicate IDs - clean!")
