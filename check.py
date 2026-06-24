html=open('original_index.html', 'rb').read().decode('utf-16le')
start=html.find('<div id="fake-front"')
end=html.find('<div id="secret-vault"')
with open('dump.txt', 'w', encoding='utf-8') as f:
    f.write(html[start:end])
