import re

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure Response is imported
if "from flask import Response" not in text:
    text = text.replace("from flask import Flask,", "from flask import Flask, Response,")

old_ai_chat = """@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Пустое сообщение"}), 400
        
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "Ключ GROQ_API_KEY не найден на сервере."}), 500
        
    system_prompt = "Ты - AUREXIS FLORA, нейро-ассистент студии Aurexis Studio. Ты общаешься с клиентами в терминале. Ты дерзкая, немного токсичная, но очень умная и полезная. Ты любишь сарказм. Отвечай кратко, как в терминале, без лишней воды."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})
        if res.status_code == 200:
            result = res.json()
            reply_text = result["choices"][0]["message"]["content"]
            return jsonify({"reply": reply_text})
        else:
            return jsonify({"error": f"Ошибка от GROQ. Статус: {res.status_code}. Текст: {res.text}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500"""

new_ai_chat = """@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    history = data.get("history", [])
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Пустое сообщение"}), 400
        
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "Ключ GROQ_API_KEY не найден на сервере."}), 500
        
    system_prompt = "Ты - AUREXIS FLORA, нейро-ассистент студии Aurexis Studio. Ты общаешься с клиентами в терминале. Ты дерзкая, немного токсичная, но очень умная и полезная. Ты любишь сарказм. Отвечай кратко, как в терминале, без лишней воды."
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Append history (limit to last 10 turns to avoid token bloat)
    for msg in history[-10:]:
        role = msg.get("role", "user")
        if role not in ["user", "assistant"]:
            role = "user"
        messages.append({"role": role, "content": msg.get("content", "")})
        
    messages.append({"role": "user", "content": user_msg})
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": True
    }
    
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}, stream=True)
        if res.status_code != 200:
            return jsonify({"error": f"Ошибка от GROQ. Статус: {res.status_code}. Текст: {res.text}"}), 500

        def generate():
            for line in res.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: '):
                        data_str = line[6:]
                        if data_str == '[DONE]':
                            break
                        try:
                            import json
                            data_json = json.loads(data_str)
                            delta = data_json['choices'][0]['delta']
                            if 'content' in delta:
                                yield delta['content']
                        except Exception as e:
                            pass
        return Response(generate(), mimetype='text/plain')
    except Exception as e:
        return jsonify({"error": str(e)}), 500"""

if old_ai_chat in text:
    text = text.replace(old_ai_chat, new_ai_chat)
else:
    # Use regex if exact match fails
    text = re.sub(r'@app\.route\(\'/api/ai/chat\', methods=\[\'POST\'\]\)[\s\S]*?(?=if __name__ == \'__main__\':)', new_ai_chat + '\n\n', text)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated server.py")
