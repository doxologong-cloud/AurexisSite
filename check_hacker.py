import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="view-hacker"')
if idx != -1:
    print(text[max(0, idx-100):idx+300])
