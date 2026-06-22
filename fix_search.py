with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_q = """    q = request.args.get('q', '').lower()
    if not q or len(q) < 2:
        return jsonify({'users': []}), 200"""

new_q = """    q = request.args.get('q', '').lower()
    if q.startswith('@'):
        q = q[1:]
    if not q or len(q) < 2:
        return jsonify({'users': []}), 200"""

if old_q in text:
    text = text.replace(old_q, new_q)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed search query strip @')
else:
    print('old_q not found')
