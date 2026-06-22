import re

def update_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return

    # Pattern to find the cursor assignment block
    # It starts with 'const svgDefault =' and ends with 'root.style.setProperty('--cursor-pointer', finalCursorPointer);'
    
    # We will just replace it with a robust btoa version
    old_pattern = r'const svgDefault = `data:image/svg\+xml;utf8,(<svg.*?</svg>)`;.*?root\.style\.setProperty\(\'--cursor-pointer\', finalCursorPointer\);'
    
    # Since regex can be tricky with multiline template literals, let's do targeted string replacements instead.
    # First, let's look at how it is structured:
    # const svgDefault = `data:image/svg+xml;utf8,<svg ... >`;
    # const svgPointer = `data:image/svg+xml;utf8,<svg ... >`;
    
    # Let's replace the whole block by finding everything between `const svgDefault = ` and `root.style.setProperty('--cursor-pointer', ...);`
    
    match = re.search(r'(const svgDefault = `data:image/svg\+xml;utf8,(<svg.*?)</svg>)`;.*?root\.style\.setProperty\(\'--cursor-pointer\', [^)]+\);', content, re.DOTALL)
    
    if match:
        new_block = """const svgDefaultStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${color1}"/><stop offset="100%25" stop-color="%23${color2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad)"/></g></svg>`;
        const svgPointerStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${ptrColor1}"/><stop offset="100%25" stop-color="%23${ptrColor2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad-ptr)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad-ptr)"/></g></svg>`;
        
        let finalCursorDefault = `url('data:image/svg+xml;base64,${btoa(svgDefaultStr)}') 12 6, auto`;
        let finalCursorPointer = `url('data:image/svg+xml;base64,${btoa(svgPointerStr)}') 12 6, pointer`;

        if (themeName === 'hacked') {
            const hackerCursorStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><filter id="glow"><feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#ff0000" flood-opacity="1"/></filter></defs><path d="M 4 4 L 12 28 L 16 16 L 28 12 Z" fill="#ff0000" filter="url(#glow)"/></svg>`;
            finalCursorDefault = `url('data:image/svg+xml;base64,${btoa(hackerCursorStr)}') 16 16, crosshair`;
            finalCursorPointer = `url('data:image/svg+xml;base64,${btoa(hackerCursorStr)}') 16 16, crosshair`;
        }

        root.style.setProperty('--cursor-default', finalCursorDefault);
        root.style.setProperty('--cursor-pointer', finalCursorPointer);"""
        
        # Note: in index.html, the variable is `theme`, not `themeName`.
        if 'theme === \'hacked\'' in match.group(0):
            new_block = new_block.replace("themeName === 'hacked'", "theme === 'hacked'")
            
        content = content[:match.start()] + new_block + content[match.end():]
        
        # update cache buster
        content = re.sub(r'\?v=\d+', '?v=85', content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {path}")
    else:
        print(f"Failed to match in {path}")

update_file('static/script.js')
update_file('templates/index.html')
update_file('templates/admin.html')
