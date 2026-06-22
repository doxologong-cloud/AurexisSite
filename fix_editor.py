import re
from bs4 import BeautifulSoup

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')

editor = soup.find(id='view-editor')
if editor:
    new_editor_html = """
    <div id="view-editor" class="view" style="display: none; flex-direction: column; height: calc(100vh - 60px); width: 100%; box-sizing: border-box; background: #0a0a0a; padding: 20px;">
        <h2 style="color: #00a8ff; margin-bottom: 10px;">Live-Code Editor</h2>
        <div style="background: #111; border: 1px solid #333; border-bottom: none; padding: 10px; border-top-left-radius: 5px; border-top-right-radius: 5px;">
            <button onclick="runCode()" style="background: #2ed573; color: #000; border: none; padding: 8px 20px; border-radius: 3px; cursor: pointer; font-weight: bold;">▶ Run Code</button>
        </div>
        <textarea id="code-textarea" style="flex: 1; background: #000; color: #00a8ff; font-family: monospace; font-size: 16px; border: 1px solid #333; padding: 15px; outline: none; resize: none;" spellcheck="false"># Пиши код бота здесь...
def on_message(msg):
    if msg == 'ping':
        return 'pong'</textarea>
        <div id="code-output" style="height: 150px; background: #111; color: #fff; padding: 15px; font-family: monospace; font-size: 14px; overflow-y: auto; border: 1px solid #333; border-top: none; border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;">Output will appear here...</div>
    </div>
    """
    new_editor = BeautifulSoup(new_editor_html, 'html.parser')
    # Because replace_with can be tricky with a single tag vs a soup document, let's just replace the raw text
    pass
    
# Let's use simple string replacement instead to avoid bs4 wrapper issues
text = re.sub(r'<div class="view" id="view-editor".*?</textarea>\s*<div id="code-output".*?</div>\s*</div>', new_editor_html, text, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed view-editor HTML via regex')
