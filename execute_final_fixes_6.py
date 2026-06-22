import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

fontawesome_link = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">'

if 'font-awesome' not in index_html:
    index_html = index_html.replace('<!-- Styles -->', '<!-- Styles -->\n    ' + fontawesome_link)
    
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)


with open('templates/admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

if 'font-awesome' not in admin_html:
    admin_html = admin_html.replace('<!-- Styles -->', '<!-- Styles -->\n    ' + fontawesome_link)

with open('templates/admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html)

print("FontAwesome added!")
