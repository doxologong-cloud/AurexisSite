import re

def fix_cursor_inheritance(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update the injected cursor styles
        old_default_list = "html, body, div, p, span, h1, h2, h3, h4, h5, h6, section, article, nav, header, footer, main, ul, li, label,\n                        .view, .view * {"
        new_default_list = "html, body, div, p, span, h1, h2, h3, h4, h5, h6, section, article, nav, header, footer, main, ul, li, label,\n                        .view, .view *, nav.navbar, nav.navbar * {"
        
        old_pointer_list = "a, a:hover, a:active, a:focus,\n                        button, button:hover, button:active, button:focus,"
        new_pointer_list = "a, a:hover, a:active, a:focus, a *,\n                        button, button:hover, button:active, button:focus, button *,"
        
        content = content.replace(old_default_list, new_default_list)
        content = content.replace(old_pointer_list, new_pointer_list)

        if filepath.endswith('.html'):
            content = re.sub(r'\?v=\d+', '?v=102', content)
            content = re.sub(r'Последнее обновление: v[\d\.]+', 'Последнее обновление: v1.12', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed inheritance in {filepath}")
    except FileNotFoundError:
        pass

fix_cursor_inheritance('templates/index.html')
fix_cursor_inheritance('templates/admin.html')
fix_cursor_inheritance('static/script.js')

# Also add user-select: none to the navbar links in style.css
try:
    with open('static/style.css', 'r', encoding='utf-8') as f:
        css = f.read()
    
    if 'user-select: none;' not in css.split('.nav-links a {')[1].split('}')[0]:
        css = css.replace('.nav-links a {', '.nav-links a {\n    user-select: none;\n    -webkit-user-drag: none;')
        css = css.replace('.navbar {', '.navbar {\n    user-select: none;')
        with open('static/style.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("Fixed user-select in style.css")
except Exception as e:
    print(e)
