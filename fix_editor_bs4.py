from bs4 import BeautifulSoup
import sys

# Ensure stdout uses utf-8 (fixes charmap error)
sys.stdout.reconfigure(encoding='utf-8')

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
    
    new_soup = BeautifulSoup(new_editor_html, 'html.parser')
    editor.replace_with(new_soup.div)
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Successfully replaced view-editor!")
else:
    print("view-editor not found!")
