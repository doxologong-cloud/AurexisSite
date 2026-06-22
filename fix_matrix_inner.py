import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

bad_code = "document.body.innerHTML += '<canvas id=\"matrix-canvas\" style=\"position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:9999;pointer-events:none;\"></canvas>';"
good_code = "document.body.insertAdjacentHTML('beforeend', '<canvas id=\"matrix-canvas\" style=\"position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:9999;pointer-events:none;\"></canvas>');"

if bad_code in text:
    text = text.replace(bad_code, good_code)
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed matrix injection!')
else:
    print('Bad code not found!')
