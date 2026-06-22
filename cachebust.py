import os

def cachebust(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace("filename='style.css') }}\"", "filename='style.css') }}\"?v=43\"")
    text = text.replace("filename='script.js') }}\"", "filename='script.js') }}\"?v=43\"")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

cachebust('templates/admin.html')
cachebust('templates/index.html')
print("Cachebust done!")
