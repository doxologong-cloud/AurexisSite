import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(?s)(\s*<!-- Settings View -->\s*<div id="view-settings".*?</section>\s*</div>)\s*</div> <!-- Close main container maybe\? Wait, where was it\? Let me just output it normally -->'
match = re.search(pattern, content)

if not match:
    pattern = r'(?s)(\s*<!-- Settings View -->\s*<div id="view-settings".*?</section>\s*</div>)'
    match = re.search(pattern, content)

if match:
    settings_block = match.group(1)
    
    if '</div> <!-- Close main container maybe' in content:
        content = content.replace(settings_block + '\n    </div> <!-- Close main container maybe? Wait, where was it? Let me just output it normally -->', '')
    else:
        content = content.replace(settings_block, '')

    content = content.replace('</main>', settings_block + '\n    </main>')
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully moved settings block in UTF-8!')
else:
    print('Failed to find settings block')
