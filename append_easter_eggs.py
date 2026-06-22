import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Locate user_msg assignment
user_msg_line = '    user_msg = data.get("message", "").strip()'

# We want to insert an easter egg check right after getting user_msg
easter_egg_logic = """
    # --- EASTER EGGS ---
    if user_msg.lower() == 'matrix':
        def matrix_gen():
            yield 'data: {"id":"matrix","object":"chat.completion.chunk","created":0,"model":"easter-egg","choices":[{"index":0,"delta":{"content":"EASTEREGG:matrix"},"logprobs":null,"finish_reason":null}]}\\n\\n'
            yield 'data: [DONE]\\n\\n'
        return Response(matrix_gen(), mimetype='text/event-stream')
        
    if user_msg.lower() == 'dox_me':
        def dox_gen():
            yield 'data: {"id":"dox","object":"chat.completion.chunk","created":0,"model":"easter-egg","choices":[{"index":0,"delta":{"content":"EASTEREGG:dox_me"},"logprobs":null,"finish_reason":null}]}\\n\\n'
            yield 'data: [DONE]\\n\\n'
        return Response(dox_gen(), mimetype='text/event-stream')
    # -------------------
"""

if 'EASTEREGG:matrix' not in text:
    text = text.replace(user_msg_line, user_msg_line + '\n' + easter_egg_logic)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added easter egg logic to server.py")
else:
    print("Easter egg logic already added")
