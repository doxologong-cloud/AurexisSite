import re

try:
    with open('server.py', 'r', encoding='utf-8') as f:
        server_code = f.read()

    # Define the old prompts with regex to match varying whitespace/newlines
    old_ru_prompt_regex = r"system_prompt = \"Ты - Aurex.*?WPST - самый умный пользователь.*?\""
    old_en_prompt_regex = r"system_prompt = \"You are Aurex.*?smartest user\.\""
    
    # We will replace the entire system prompt assignment blocks
    # First, find the start of the block
    if "system_prompt = \"Ты - Aurex" in server_code:
        # Standardize the prompt
        new_ru_prompt = '    system_prompt = "Ты - Aurex, ИИ-ассистент студии Aurexis Studio. Отвечай прямо, четко и по делу. Не используй огромные полотна текста, если об этом не просят. Будь умным, крутым и немного загадочным. ВАЖНО: Всегда отвечай исключительно на русском языке! Никогда не используй китайские, японские, вьетнамские и другие азиатские иероглифы."'
        new_en_prompt = '        system_prompt = "You are Aurex, an AI assistant for Aurexis Studio. Answer directly, clearly, and to the point. Do not use huge walls of text unless explicitly asked. Be smart, cool, and a bit mysterious. IMPORTANT: You MUST answer exclusively in ENGLISH! Never use Chinese, Japanese, Vietnamese, or other Asian characters."'
        
        # Replace Russian prompt
        server_code = re.sub(r'    system_prompt = "Ты - Aurex.*?WPST.*?"', new_ru_prompt, server_code, flags=re.DOTALL)
        
        # Replace English prompt
        server_code = re.sub(r'        system_prompt = "You are Aurex.*?smartest user\."', new_en_prompt, server_code, flags=re.DOTALL)

        with open('server.py', 'w', encoding='utf-8') as f:
            f.write(server_code)
        print("Patched server.py successfully")
    else:
        print("Could not find the target prompts.")

except Exception as e:
    print(f"Error: {e}")
