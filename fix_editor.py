import json

# Let's parse translations.js properly by just finding the exact t_100 in the "en" section.
with open('static/translations.js', 'r', encoding='utf-8') as f:
    text = f.read()

# We know t_100 in "en" is around line 298.
# The easiest way is to just do a direct string replace of the exact block inside the 'en' dictionary.
# The string is:
old_str = '''"t_100": "# Пиши код бота здесь...\\ndef on_message(msg):\\n    if msg == 'ping':\\n        return 'pong'",'''
new_str = '''"t_100": "# Write your bot code here...\\ndef on_message(msg):\\n    if msg == 'ping':\\n        return 'pong'",'''

# We also need to be careful because the previous replace might have failed.
# Let's do it manually line by line
lines = text.split('\\n')
in_en = False
for i in range(len(lines)):
    if '"en": {' in lines[i]:
        in_en = True
    if in_en and '"t_100":' in lines[i]:
        # we found it in the EN dictionary
        # Let's replace the next few lines or the current line.
        # Since it's multi-line, wait, the JSON might have literal \n string in the line.
        # Let's just blindly replace 'Пиши код бота здесь...' with 'Write your bot code here...' ONLY if in_en is True
        lines[i] = lines[i].replace('Пиши код бота здесь...', 'Write your bot code here...')

# Join and write back
with open('static/translations.js', 'w', encoding='utf-8') as f:
    f.write('\\n'.join(lines))

# Cache bust
import re
for path in ['templates/index.html', 'templates/admin.html']:
    with open(path, 'r', encoding='utf-8') as html_f:
        html = html_f.read()
    html = re.sub(r'\?v=\d+', '?v=74', html)
    with open(path, 'w', encoding='utf-8') as html_f:
        html_f.write(html)
