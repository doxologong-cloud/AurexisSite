import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

# The current cursor block:
old_cursor = r"""#custom-cursor \{
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

new_cursor = """#custom-cursor {
    position: fixed;
    top: 0;
    left: 0;
    width: 24px;
    height: 36px;
    pointer-events: none;
    z-index: 999999999999;
    background-color: var(--neon-primary);
    -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3 2l6 20 4-8 8 4-20-16z"/></svg>');
    -webkit-mask-size: contain;
    -webkit-mask-repeat: no-repeat;
    mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M3 2l6 20 4-8 8 4-20-16z"/></svg>');
    mask-size: contain;
    mask-repeat: no-repeat;
    filter: drop-shadow(0 0 8px var(--neon-primary));
    transform: translate(0, 0);
    transition: transform 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

#custom-cursor.clicking {
    transform: translate(0, 0) scale(0.8);
    background-color: #fff;
    filter: drop-shadow(0 0 15px #fff);
}

#custom-cursor.hovering {
    transform: translate(0, 0) scale(1.3);
    filter: drop-shadow(0 0 15px var(--neon-primary)) drop-shadow(0 0 25px var(--neon-primary));
}"""

text = re.sub(old_cursor, new_cursor, text)

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(text)

print("Custom cursor updated to a stylized arrow!")
