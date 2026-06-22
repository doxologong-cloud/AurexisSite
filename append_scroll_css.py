import os

css = """
/* CUSTOM SCROLLBARS */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb {
    background: var(--neon-primary);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #e6b800; /* slightly darker gold */
}

/* Specific scrollbar for AI chat box to look like a terminal */
#ai-chat-box::-webkit-scrollbar-thumb {
    background: var(--neon-primary);
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(css)

print("Scrollbar CSS appended.")
