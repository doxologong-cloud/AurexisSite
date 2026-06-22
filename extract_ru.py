import re

def find_russian(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to find any text node or string literal containing Cyrillic
    # Simple regex to find Cyrillic letters
    strings = set()
    matches = re.findall(r'[^>\'"`;\n{}]*[А-Яа-яЁё]+[^<\'"`;\n{}]*', content)
    for m in matches:
        s = m.strip()
        if len(s) > 1 and not s.startswith('t_'):
            strings.add(s)
            
    print(f'--- {filepath} ---')
    for s in sorted(strings):
        print(s)

find_russian('static/script.js')
find_russian('templates/admin.html')
