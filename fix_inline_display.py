with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('<div id="view-messenger" class="view" style="display: none;">', '<div id="view-messenger" class="view hidden-view">')
text = text.replace('<div id="view-portfolio" class="view" style="display: none;">', '<div id="view-portfolio" class="view hidden-view">')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Fixed inline display styles")
