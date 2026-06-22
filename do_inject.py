with open('server.py', 'r', encoding='utf-8') as f:
    server_text = f.read()

with open('inject_api.py', 'r', encoding='utf-8') as f:
    inject_text = f.read()

import re
endpoints = re.search(r'endpoints = """(.*?)"""\n\nif', inject_text, re.DOTALL).group(1)

if 'def get_chats(' not in server_text:
    server_text = server_text.replace("if __name__ == '__main__':", endpoints + "\nif __name__ == '__main__':")
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(server_text)
    print("Injected Messenger & Profiles API successfully.")
else:
    print("API already injected.")
