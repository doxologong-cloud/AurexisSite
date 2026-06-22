with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if 'def generate():' in line:
        skip = True
        new_lines.append('    def generate():\n')
        new_lines.append('        for line in res.iter_lines():\n')
        new_lines.append('            if line:\n')
        new_lines.append('                line = line.decode("utf-8")\n')
        new_lines.append('                yield line + "\\n\\n"\n')
        new_lines.append("    return Response(generate(), mimetype='text/event-stream')\n")
    elif 'return Response(generate()' in line:
        skip = False
    elif skip:
        continue
    else:
        new_lines.append(line)

with open('server.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
