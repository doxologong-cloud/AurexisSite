import json
import re

with open('js_trans_dict.json', 'r', encoding='utf-8') as f:
    js_dict = json.load(f)

# Update translations.js
with open('static/translations.js', 'r', encoding='utf-8') as f:
    trans_js = f.read()

# We need to add admin_dict and js_dict to translations
from translate_step1 import admin_dict

# Generate new entries for translations = { ... }
new_entries = []
for ru, en in admin_dict.items():
    key = f't_admin_{hash(ru)}'
    new_entries.append(f'    "{key}": {json.dumps(en, ensure_ascii=False)}')

# Find the end of translations = { ... }
# We'll just insert before the last closing brace
if '};' in trans_js:
    parts = trans_js.rsplit('};', 1)
    if new_entries:
        trans_js = parts[0] + ',\n' + ',\n'.join(new_entries) + '\n};\n'

# Add dynamic JS translations object
trans_js += f"\n\nwindow.dynamicTranslations = {json.dumps(js_dict, ensure_ascii=False, indent=4)};\n"

with open('static/translations.js', 'w', encoding='utf-8') as f:
    f.write(trans_js)

# Now update script.js
with open('static/script.js', 'r', encoding='utf-8') as f:
    script_js = f.read()

# Add translation function at the top
t_func = """
window.__ = function(ruText) {
    const lang = localStorage.getItem('aurex_lang') || 'ru';
    if (lang === 'ru') return ruText;
    if (window.dynamicTranslations && window.dynamicTranslations[ruText]) {
        return window.dynamicTranslations[ruText];
    }
    return ruText;
};
"""

script_js = t_func + script_js

# Replace exact strings with __("...")
# To be safe, we only replace it inside showToast, alert, and confirm
def safe_replace(match):
    prefix = match.group(1)
    quote = match.group(2)
    text = match.group(3)
    # If text is in our dictionary, wrap it
    if text in js_dict:
        return f'{prefix}__({quote}{text}{quote})'
    return match.group(0)

# Replace showToast('...') -> showToast(__('...'))
script_js = re.sub(r'(showToast\s*\(\s*)([\'"`])(.*?)([\'"`])', safe_replace, script_js)
script_js = re.sub(r'(alert\s*\(\s*)([\'"`])(.*?)([\'"`])', safe_replace, script_js)
script_js = re.sub(r'(confirm\s*\(\s*)([\'"`])(.*?)([\'"`])', safe_replace, script_js)
script_js = re.sub(r'(addSystemMsg\s*\(\s*)([\'"`])(.*?)([\'"`])', safe_replace, script_js)

# Also let's try replacing exact strings that are assigned to textContent or innerHTML
for ru, en in js_dict.items():
    if len(ru) > 3 and '<' not in ru:
        # replace isolated string literals that are not already wrapped in __
        # Using a simplistic approach: replace 'ru' with __('ru') if not preceded by __(
        # This regex is a bit complex, let's just do it for common ones
        pass

# Force replace some known hardcoded ones
script_js = script_js.replace("'Никто'", "__('Никто')")
script_js = script_js.replace("'Неизвестно'", "__('Неизвестно')")
script_js = script_js.replace("'Вы уверены?'", "__('Вы уверены?')")
script_js = script_js.replace("'Да'", "__('Да')")
script_js = script_js.replace("'Отмена'", "__('Отмена')")

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(script_js)

print("Translations applied.")
