import re

server_path = r"C:\Users\user\Desktop\сайт\server.py"
with open(server_path, 'r', encoding='utf-8') as f:
    server_text = f.read()

bot_api_code = """
# --- BOTS MANAGEMENT API ---
import subprocess
import threading
import time

BOTS_DIR = r"C:\\Users\\user\\Desktop\\запуск ботов\\bots"
CREATE_NO_WINDOW = 0x08000000

bots_config = {
    "aurex_support": {"name": "Aurexis SUPPORT", "folder": "feedback_bot", "script": "bot.py", "is_exe": False, "desc": "Поддержка и обратная связь."},
    "aurex_games": {"name": "Aurexis GAMES", "folder": "economy_bot", "script": "bot.py", "is_exe": False, "desc": "Экономика и мини-игры."},
    "aurex_mafia": {"name": "Aurexis MAFIA", "folder": "mafia_bot", "script": "bot.py", "is_exe": False, "desc": "Игровой бот 'Мафия'."},
    "flora": {"name": "FLORA", "folder": "flora", "script": "Бот.exe", "is_exe": True, "desc": "Главный ИИ-ассистент."}
}

active_bots = {}

def check_bot_running(bot_id):
    if bot_id in active_bots:
        proc = active_bots[bot_id]["process"]
        if proc and proc.poll() is None:
            return True
        else:
            del active_bots[bot_id]
            
    bot = bots_config[bot_id]
    try:
        if bot['is_exe']:
            output = subprocess.check_output(f'wmic process where "name=\\'{bot["script"]}\\'" get ProcessId', shell=True, text=True)
            if len(output.strip().split('\\n')) > 1:
                return True
        else:
            output = subprocess.check_output('wmic process where "name=\\'python.exe\\'" get CommandLine', shell=True, text=True)
            for line in output.strip().split('\\n'):
                if bot["script"] in line and bot["folder"] in line:
                    return True
    except Exception:
        pass
    return False

@app.route('/api/bots', methods=['GET'])
def get_bots():
    results = []
    for bot_id, conf in bots_config.items():
        is_running = check_bot_running(bot_id)
        results.append({
            "id": bot_id,
            "name": conf["name"],
            "desc": conf["desc"],
            "status": "ONLINE" if is_running else "OFFLINE"
        })
    return jsonify({"success": True, "bots": results})

@app.route('/api/bots/<bot_id>/start', methods=['POST'])
def start_bot(bot_id):
    if bot_id not in bots_config:
        return jsonify({"success": False, "error": "Bot not found"})
    
    if check_bot_running(bot_id):
        return jsonify({"success": True, "message": "Already running"})
        
    bot = bots_config[bot_id]
    bot_path = os.path.join(BOTS_DIR, bot["folder"])
    
    try:
        cmd = [os.path.join(bot_path, bot["script"])] if bot["is_exe"] else ["python", bot["script"]]
        proc = subprocess.Popen(cmd, cwd=bot_path, creationflags=CREATE_NO_WINDOW)
        active_bots[bot_id] = {"process": proc, "pid": proc.pid}
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/bots/<bot_id>/stop', methods=['POST'])
def stop_bot(bot_id):
    if bot_id not in bots_config:
        return jsonify({"success": False, "error": "Bot not found"})
        
    bot = bots_config[bot_id]
    
    # Try kill by pid if we tracked it
    if bot_id in active_bots:
        pid = active_bots[bot_id]["pid"]
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True)
        del active_bots[bot_id]
        
    # Also kill by name/wmic just in case
    try:
        if bot['is_exe']:
            subprocess.run(["taskkill", "/F", "/IM", bot["script"]], capture_output=True)
        else:
            output = subprocess.check_output('wmic process where "name=\\'python.exe\\'" get CommandLine,ProcessId', shell=True, text=True)
            for line in output.strip().split('\\n'):
                if bot["script"] in line and bot["folder"] in line:
                    parts = line.strip().split()
                    if parts and parts[-1].isdigit():
                        pid = parts[-1]
                        subprocess.run(["taskkill", "/F", "/T", "/PID", pid], capture_output=True)
    except Exception:
        pass
        
    return jsonify({"success": True})
"""

# Inject before if __name__ == '__main__':
server_text = server_text.replace("if __name__ == '__main__':", bot_api_code + "\nif __name__ == '__main__':")

with open(server_path, 'w', encoding='utf-8') as f:
    f.write(server_text)

print("Backend API routes for bots injected.")
