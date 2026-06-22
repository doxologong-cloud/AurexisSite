import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    css_text = f.read()

old_nav_links = """.nav-links {
    display: flex;
    gap: 30px;
    font-size: 1.1rem;
    font-weight: 600;
}"""

new_nav_links = """.nav-links {
    display: flex;
    align-items: center;
    gap: 30px;
    font-size: 1.1rem;
    font-weight: 600;
}"""

if old_nav_links in css_text:
    css_text = css_text.replace(old_nav_links, new_nav_links)
    with open('static/style.css', 'w', encoding='utf-8') as f:
        f.write(css_text)
    print("Fixed vertical alignment in navbar.")
else:
    print("Could not find .nav-links block exactly as expected.")
