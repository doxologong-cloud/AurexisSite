with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

editor_idx = text.find('id="view-editor"')
if editor_idx != -1:
    print(text[editor_idx-100:editor_idx+500])
