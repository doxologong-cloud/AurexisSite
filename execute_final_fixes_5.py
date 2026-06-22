import re

# 1. Update style.css for feature cards word-wrap
with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

feature_fix = """
.feature-item h3 {
    word-break: break-word;
    hyphens: auto;
}
"""
if ".feature-item h3 {" not in css:
    css += feature_fix

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)


# 2. Update script.js for FontAwesome stars
with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_star = "const stars = '⭐'.repeat(r.rating);"
new_star = "const stars = '<i class=\"fa-solid fa-star\" style=\"color: #ffc107;\"></i>'.repeat(r.rating);"

if old_star in js:
    js = js.replace(old_star, new_star)
else:
    # Just in case it was modified
    pass

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)


# 3. Update index.html bot icons
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Support SVG
old_support = """<div class="bot-icon support-icon">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
</div>"""
new_support = """<div class="bot-icon support-icon" style="display:flex; justify-content:center; align-items:center; font-size: 2rem; color: var(--neon-primary);">
<i class="fa-solid fa-headset"></i>
</div>"""

# Replace Economy SVG
old_economy = """<div class="bot-icon games-icon">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><path d="M12 8v4l3 3"></path></svg>
</div>"""
new_economy = """<div class="bot-icon games-icon" style="display:flex; justify-content:center; align-items:center; font-size: 2rem; color: var(--neon-secondary);">
<i class="fa-solid fa-coins"></i>
</div>"""

# Replace Mafia SVG
old_mafia = """<div class="bot-icon mafia-icon">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
</div>"""
new_mafia = """<div class="bot-icon mafia-icon" style="display:flex; justify-content:center; align-items:center; font-size: 2rem; color: #ff4444;">
<i class="fa-solid fa-user-secret"></i>
</div>"""

# Replace Flora SVG
old_flora = """<div class="bot-icon flora-icon">
<svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewbox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
</div>"""
new_flora = """<div class="bot-icon flora-icon" style="display:flex; justify-content:center; align-items:center; font-size: 2rem; color: var(--neon-green);">
<i class="fa-solid fa-biohazard"></i>
</div>"""

html = html.replace(old_support, new_support)
html = html.replace(old_economy, new_economy)
html = html.replace(old_mafia, new_mafia)
html = html.replace(old_flora, new_flora)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 4. Custom Confirm in admin.html
with open('templates/admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

custom_confirm_html = """
    <!-- Custom Confirm Modal -->
    <div id="custom-confirm-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.8); z-index: 10000; justify-content: center; align-items: center; backdrop-filter: blur(5px);">
        <div style="background: var(--bg-color); border: 1px solid var(--neon-primary); border-radius: 16px; padding: 30px; width: 400px; max-width: 90%; text-align: center;">
            <h3 id="confirm-msg" style="color: white; margin-bottom: 25px; margin-top: 0;">Вы уверены?</h3>
            <div style="display: flex; gap: 15px; justify-content: center;">
                <button id="confirm-yes" class="flora-toggle" style="background: rgba(255, 68, 68, 0.2); border-color: #ff4444; color: #ff4444; flex: 1;">Да, уверен</button>
                <button id="confirm-no" class="flora-toggle" style="flex: 1; border-color: rgba(255,255,255,0.2); color: white;">Отмена</button>
            </div>
        </div>
    </div>
"""

custom_confirm_js = """
        function customConfirm(msg) {
            return new Promise(resolve => {
                const modal = document.getElementById('custom-confirm-modal');
                document.getElementById('confirm-msg').textContent = msg;
                modal.style.display = 'flex';
                
                const yesBtn = document.getElementById('confirm-yes');
                const noBtn = document.getElementById('confirm-no');
                
                const cleanup = () => {
                    modal.style.display = 'none';
                    yesBtn.removeEventListener('click', onYes);
                    noBtn.removeEventListener('click', onNo);
                };
                
                const onYes = () => { cleanup(); resolve(true); };
                const onNo = () => { cleanup(); resolve(false); };
                
                yesBtn.addEventListener('click', onYes);
                noBtn.addEventListener('click', onNo);
            });
        }
"""

if "customConfirm" not in admin_html:
    # Insert HTML before scripts
    admin_html = admin_html.replace('<!-- Scripts -->', custom_confirm_html + '\n    <!-- Scripts -->')
    # Insert JS at the start of script tag
    admin_html = admin_html.replace("<script>\n        particlesJS", "<script>\n" + custom_confirm_js + "\n        particlesJS")

# Replace confirms
admin_html = admin_html.replace("if(!confirm('Точно удалить новость?')) return;", "if(!(await customConfirm('Точно удалить новость?'))) return;")
admin_html = admin_html.replace("if(!confirm('Закрыть тикет?')) return;", "if(!(await customConfirm('Закрыть тикет?'))) return;")
admin_html = admin_html.replace("if(!confirm('Удалить тикет?')) return;", "if(!(await customConfirm('Удалить тикет?'))) return;")

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("Updates successful!")
