import re

def clean_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Fix the literal backslashes from previous bad python replace
        content = content.replace("url(\\'data:image/svg+xml,${encodeURIComponent(svgDefaultStr)}\\')", 'url("data:image/svg+xml,${encodeURIComponent(svgDefaultStr)}")')
        content = content.replace("url(\\'data:image/svg+xml,${encodeURIComponent(svgPointerStr)}\\')", 'url("data:image/svg+xml,${encodeURIComponent(svgPointerStr)}")')

        # Fix hacker cursor size and offset
        old_hacker_svg = r'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M 4 4 L 12 28 L 16 16 L 28 12 Z" fill="#ff0000" stroke="#ff0000" stroke-width="3" stroke-linejoin="round" stroke-opacity="0.4"/></svg>'
        new_hacker_svg = r'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M 2 2 L 10 22 L 13 13 L 22 10 Z" fill="#ff0000" stroke="#ff0000" stroke-width="2" stroke-linejoin="round" stroke-opacity="0.4"/></svg>'
        
        content = content.replace(old_hacker_svg, new_hacker_svg)
        
        # Replace the url lines with backslashes and wrong offset (16 16) with correct double quotes and correct offset (2 2)
        old_hacker_default = r"url(\\'data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}\\') 16 16, crosshair"
        new_hacker_default = r'url("data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}") 2 2, crosshair'
        content = content.replace(old_hacker_default, new_hacker_default)
        
        old_hacker_pointer = r"url(\\'data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}\\') 16 16, crosshair"
        new_hacker_pointer = r'url("data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}") 2 2, crosshair'
        content = content.replace(old_hacker_pointer, new_hacker_pointer)

        # Update cache buster if html
        if path.endswith('.html'):
            content = re.sub(r'\?v=\d+', '?v=92', content)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned {path}")
    except FileNotFoundError:
        pass

clean_file('static/script.js')
clean_file('templates/index.html')
clean_file('templates/admin.html')
