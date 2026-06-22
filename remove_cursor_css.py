import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the custom cursor CSS block
css_to_remove = r"""/\* CUSTOM CURSOR \*/
\* \{
    cursor: none !important;
\}

#custom-cursor \{
    position: fixed;
    top: 0;
    left: 0;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 999999999999;
    transform: translate\(-50%, -50%\);
    background: var\(--neon-primary\);
    box-shadow: 0 0 15px var\(--neon-primary\), 0 0 30px var\(--neon-primary\);
    transition: transform 0\.1s cubic-bezier\(0\.175, 0\.885, 0\.32, 1\.275\), width 0\.2s, height 0\.2s;
    mix-blend-mode: screen;
\}

#custom-cursor\.clicking \{
    transform: translate\(-50%, -50%\) scale\(0\.5\);
    background: #fff;
    box-shadow: 0 0 20px #fff;
\}

#custom-cursor\.hovering \{
    width: 40px;
    height: 40px;
    background: transparent;
    border: 2px solid var\(--neon-primary\);
    box-shadow: inset 0 0 10px var\(--neon-primary\), 0 0 10px var\(--neon-primary\);
\}"""

text = re.sub(css_to_remove, '', text, flags=re.MULTILINE)

# Also remove the `cursor: none;` from .theme-card
text = text.replace('cursor: none;', 'cursor: pointer;')

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(text)

print("CSS custom cursor removed.")
