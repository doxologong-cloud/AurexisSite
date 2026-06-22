import os

groq_code = """
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Пустое сообщение"}), 400
        
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"error": "Ключ GROQ_API_KEY не настроен на сервере."}), 500
        
    system_prompt = "Ты - AUREXIS FLORA, передовой искусственный интеллект-ассистент студии Aurexis Studio. Ты помогаешь клиентам заказывать и придумывать Discord ботов. Ты общаешься дерзко, в стиле киберпанка, с легкой надменностью превосходного ИИ, но всегда полезно и профессионально. Не пиши код. Если клиент просит сделать бота, скажи ему нажать кнопку заказа тикета."
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": "llama3-70b-8192",
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
            return jsonify({"error": f"Сбой нейросети GROQ. Статус: {res.status_code}. Ответ: {res.text}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""

filepath = 'server.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.rfind("@app.route('/api/ai/chat'")
end_idx = text.find("if __name__ == '__main__':")

if start_idx != -1 and end_idx != -1:
    new_text = text[:start_idx] + groq_code + "\n" + text[end_idx:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully replaced Gemini with Groq in server.py")
else:
    print("Could not find the function boundaries.")
