import subprocess
import re

base_dir = r"C:\Users\user\Desktop\сайт"
vault_path = r"C:\Users\user\Desktop\сайт\templates\vault.html"

# Get the original index.html content from git
proc = subprocess.run(['git', 'show', 'HEAD~1:templates/index.html'], cwd=base_dir, capture_output=True)
html = proc.stdout.decode('utf-8', errors='ignore')

# We need to extract the fake-front and login logic to remove them
# The fake front is from '<div id="fake-front"' to the matching closing div.
# But it's easier to use a targeted regex that we know works safely.
fake_front_regex = r'<div id="fake-front"[\s\S]*?\(Ведутся РАБОТЫ\)[\s\S]*?</div>'
html = re.sub(fake_front_regex, '', html)

# Remove the key-sequence login logic script
login_logic_regex = r'// --- LOGIN LOGIC ---[\s\S]*?function unlockVault\(\) \{[\s\S]*?\}'
html = re.sub(login_logic_regex, '', html)

# Ensure the vault is visible by default
html = html.replace('style="display: none;" id="secret-vault"', 'id="secret-vault" style="display: flex;"')

with open(vault_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("vault.html has been fully restored with CSS and styles intact.")
