import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# We need to replace the message formatting part in loadMessages.
# It currently is:
# msgDiv.innerHTML = `<span class='msg-time'>[${timeStr}]</span> <b>${sender}</b>: ${msg.text}` + (isMine ? ` <span style='color: var(--neon-color); font-size: 10px; margin-left: 5px;'>✔✔</span>` : '');
# We will create a function parseRichText(text)

embed_js = """
// ==========================================
// RICH EMBEDS
// ==========================================
function parseRichText(text) {
    // Escape HTML first
    let html = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    
    // Youtube matching
    const ytRegex = /(?:https?:\\/\\/)?(?:www\\.)?(?:youtube\\.com\\/watch\\?v=|youtu\\.be\\/)([a-zA-Z0-9_-]{11})/g;
    html = html.replace(ytRegex, (match, videoId) => {
        return `<br><iframe width="300" height="170" src="https://www.youtube.com/embed/${videoId}" frameborder="0" allowfullscreen style="border-radius: 5px; border: 1px solid var(--neon-color); margin-top: 5px;"></iframe><br>`;
    });
    
    // Image matching (basic)
    const imgRegex = /(https?:\\/\\/\\S+\\.(?:png|jpg|jpeg|gif|webp))/gi;
    html = html.replace(imgRegex, (match) => {
        return `<br><img src="${match}" style="max-width: 300px; max-height: 200px; border-radius: 5px; border: 1px solid var(--neon-color); margin-top: 5px;"><br>`;
    });
    
    return html;
}
"""

if 'parseRichText(' not in js_text:
    js_text += "\n" + embed_js
    
    # Replace the text assignment
    old_line = "msgDiv.innerHTML = `<span class='msg-time'>[${timeStr}]</span> <b>${sender}</b>: ${msg.text}` + (isMine ? ` <span style='color: var(--neon-color); font-size: 10px; margin-left: 5px;'>✔✔</span>` : '');"
    new_line = "msgDiv.innerHTML = `<span class='msg-time'>[${timeStr}]</span> <b>${sender}</b>: ${parseRichText(msg.text)}` + (isMine ? ` <span style='color: var(--neon-color); font-size: 10px; margin-left: 5px;'>✔✔</span>` : '');"
    
    js_text = js_text.replace(old_line, new_line)
    
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js_text)
    print("Injected Rich Embeds JS.")
else:
    print("Rich Embeds JS already exists.")
