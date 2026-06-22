import re
with open("templates/index.html", "r", encoding="utf-8") as f:
    text = f.read()
text = re.sub(r"v=\d+", "v=9", text)
with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(text)
