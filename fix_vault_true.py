import subprocess
import re

base_dir = r"C:\Users\user\Desktop\сайт"
vault_path = r"C:\Users\user\Desktop\сайт\templates\vault.html"

# Get the FULL index.html content from commit 7120654
proc = subprocess.run(['git', 'show', '7120654:templates/index.html'], cwd=base_dir, capture_output=True)
html = proc.stdout.decode('utf-8', errors='ignore')

# Now carefully remove the fake-front and the login script
fake_front_regex = r'<div id="fake-front"[\s\S]*?\(Ведутся РАБОТЫ\)[\s\S]*?</div>'
html = re.sub(fake_front_regex, '', html)

# Remove the key-sequence login logic script
login_logic_regex = r'// --- LOGIN LOGIC ---[\s\S]*?function unlockVault\(\) \{[\s\S]*?\}'
html = re.sub(login_logic_regex, '', html)

# Ensure the vault is visible by default
html = html.replace('style="display: none;" id="secret-vault"', 'id="secret-vault" style="display: flex;"')
# Also remove the `vault.style.display = 'flex';` part from other places if needed, but it's fine.

with open(vault_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("vault.html has been TRULY restored from the correct commit. Size:", len(html))
