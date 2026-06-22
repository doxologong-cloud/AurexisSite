import os

css = """
#ai-stop-btn {
    background: transparent !important;
    border: none;
    color: #ff0033 !important;
    cursor: pointer;
    transition: 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
}
#ai-stop-btn:hover {
    color: #ff4444 !important;
    transform: scale(1.1);
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(css)
