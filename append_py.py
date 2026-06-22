import os

py_code = """
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Пустое сообщение"}), 400
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({"error": "Ключ GEMINI_API_KEY не настроен на сервере."}), 500
        
    # Системный промпт (задаем личность FLORA)
    system_prompt = "Ты - AUREXIS FLORA, передовой искусственный интеллект-ассистент студии Aurexis Studio. Ты помогаешь клиентам заказывать и придумывать Discord ботов. Ты общаешься дерзко, в стиле киберпанка, с легкой надменностью превосходного ИИ, но всегда полезно и профессионально. Не пиши код. Если клиент просит сделать бота, скажи ему нажать кнопку заказа тикета."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": system_prompt + "\\n\\nПользователь: " + user_msg}]
            }
        ]
    }
    
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        if res.status_code == 200:
            result = res.json()
            reply_text = result["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": reply_text})
        else:
            return jsonify({"error": "Сбой нейросети. Статус: " + str(res.status_code)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""

filepath = 'server.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.rfind("if __name__ == '__main__':")
if idx != -1:
    content = content[:idx] + py_code + "\n" + content[idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Appended AI endpoint.')
else:
    print('Could not find __main__ block.')
