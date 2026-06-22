import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

forms = re.findall(r'<form id=".*?-form".*?</form>', text, re.DOTALL)
for form in forms:
    print(form)
    print("---")
