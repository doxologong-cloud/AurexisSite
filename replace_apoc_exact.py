import os

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('function triggerApocalypse()')
if start_idx == -1:
    print("Not found")
    exit()

# find matching brace
brace_count = 0
in_func = False
end_idx = -1
for i in range(start_idx, len(text)):
    if text[i] == '{':
        brace_count += 1
        in_func = True
    elif text[i] == '}':
        brace_count -= 1
    if in_func and brace_count == 0:
        end_idx = i
        break

with open('plot_apoc.py', 'r', encoding='utf-8') as f:
    plot_code = f.read()
    js_new = plot_code.split('js_new = """')[1].split('"""')[0]

if end_idx != -1:
    new_text = text[:start_idx] + js_new + text[end_idx+1:]
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("JS successfully replaced.")
else:
    print("Failed to find end brace.")
