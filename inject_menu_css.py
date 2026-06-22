with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

menu_css = """
.menu-item {
    padding: 8px 15px;
    cursor: pointer;
    color: #fff;
    transition: background 0.2s, color 0.2s;
    font-size: 14px;
}
.menu-item:hover {
    background: var(--glow-color);
    color: var(--neon-color);
}
"""

if '.menu-item' not in css:
    with open('static/style.css', 'a', encoding='utf-8') as f:
        f.write(menu_css)
    print("Added menu-item CSS")
