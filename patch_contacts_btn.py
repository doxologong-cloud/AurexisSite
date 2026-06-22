import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

new_js = """
// Bind Add to Contacts button
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('add-to-contacts-btn');
    if (btn) {
        btn.addEventListener('click', () => {
            if (window.currentChatEmail) {
                addContact(window.currentChatEmail);
                btn.style.display = 'none';
            }
        });
    }
});

// Patch loadChatMessages or click handler to store email and show button
"""

patch = """
            list.appendChild(div);

            // OPTIMISTIC: Store current chat email when clicking
            div.addEventListener('click', () => {
                const myEmail = window.currentUser ? window.currentUser.email : '';
                const otherEmails = c.participants.filter(e => e !== myEmail);
                if (otherEmails.length === 1 && c.type === 'chat_dm') {
                    window.currentChatEmail = otherEmails[0];
                    const btn = document.getElementById('add-to-contacts-btn');
                    if (btn) {
                        // Ideally check if already in contacts, but for now just show it
                        btn.style.display = 'block';
                    }
                } else {
                    window.currentChatEmail = null;
                    const btn = document.getElementById('add-to-contacts-btn');
                    if (btn) btn.style.display = 'none';
                }
            });
"""

if 'window.currentChatEmail' not in text:
    text = text.replace("list.appendChild(div);", patch)
    text = text + "\n" + new_js
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Patched script for contacts button")
else:
    print("Already patched")
