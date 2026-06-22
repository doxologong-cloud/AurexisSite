import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove inline styles from toggles
html = html.replace(
    '<label class="switch" style="position: relative; display: inline-block; width: 50px; height: 24px;">',
    '<label class="switch">'
)
html = html.replace(
    '<input type="checkbox" id="anim-toggle" checked onchange="toggleAnimations(this.checked)" style="opacity: 0; width: 0; height: 0;">',
    '<input type="checkbox" id="anim-toggle" checked onchange="toggleAnimations(this.checked)">'
)
html = html.replace(
    '<span class="slider" style="position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #333; transition: .4s; border-radius: 24px;"></span>',
    '<span class="slider round"></span>' # Wait, 'round' class might be needed for border-radius.
)
html = html.replace(
    '<input type="checkbox" id="particles-toggle" checked onchange="toggleParticles(this.checked)" style="opacity: 0; width: 0; height: 0;">',
    '<input type="checkbox" id="particles-toggle" checked onchange="toggleParticles(this.checked)">'
)

# Remove the <style> block I added earlier
style_block_pattern = r'<!-- Styles for settings switch -->\n<style>\s*\.switch input:checked \+ \.slider.*?</style>\n'
html = re.sub(style_block_pattern, '', html, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
