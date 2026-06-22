import re

def fix_svg_encoding(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # We will find the svgDefaultStr, svgPointerStr, and hackerCursorStr block and replace %23 -> # and %25 -> %
        # Just safely replacing them in the whole file since we only introduced these URL encodings for the SVG.
        
        # Check if they exist
        if '%23' in content or '%25' in content:
            content = content.replace('%23', '#').replace('%25', '%')
            
            # Increment cache buster in HTML files
            if filepath.endswith('.html'):
                content = re.sub(r'\?v=\d+', '?v=90', content)
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {filepath}")
    except FileNotFoundError:
        pass

for file in ['static/script.js', 'templates/index.html', 'templates/admin.html']:
    fix_svg_encoding(file)
