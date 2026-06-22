import re

with open('templates/index_clean.html', 'r', encoding='utf-16') as f:
    content = f.read()

# Extract settings block
pattern = r'(?s)(\s*<!-- Settings View -->\s*<div id="view-settings".*?</section>\s*</div>)\s*</div> <!-- Close main container maybe\? Wait, where was it\? Let me just output it normally -->'
match = re.search(pattern, content)

if not match:
    # Try alternative matching
    pattern = r'(?s)(\s*<!-- Settings View -->\s*<div id="view-settings".*?</section>\s*</div>)\s*</div> <!-- Close main container -->'
    match = re.search(pattern, content)

if not match:
    # The clean file from 05b1e8d might just have the block and then nothing after it.
    pattern = r'(?s)(\s*<!-- Settings View -->\s*<div id="view-settings".*?</section>\s*</div>)'
    match = re.search(pattern, content)

if match:
    settings_block = match.group(1)
    
    # Remove the settings block from its original location
    # If the original location had an extra </div>, we should just replace it cleanly
    if '</div> <!-- Close main container maybe' in content:
        content = content.replace(settings_block + '\n    </div> <!-- Close main container maybe? Wait, where was it? Let me just output it normally -->', '')
    else:
        content = content.replace(settings_block, '')

    # Insert it before </main>
    content = content.replace('</main>', settings_block + '\n    </main>')
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully moved settings block in UTF-8')
else:
    print('Failed to find settings block')
