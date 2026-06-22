import os

css_code = """

/* --- AI TERMINAL --- */
.nav-ai-link {
    color: var(--neon-secondary);
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s ease;
}

.nav-ai-link:hover {
    color: #fff;
    text-shadow: 0 0 10px var(--neon-secondary);
}

.ai-section {
    padding-top: 40px;
    text-align: center;
}

.ai-terminal-container {
    max-width: 800px;
    margin: 2rem auto;
    background: rgba(10, 10, 15, 0.85);
    border: 1px solid var(--neon-secondary);
    border-radius: 12px;
    box-shadow: 0 0 30px rgba(0, 242, 254, 0.2);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    backdrop-filter: blur(10px);
}

.ai-terminal-header {
    background: rgba(0, 0, 0, 0.5);
    padding: 10px 15px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid rgba(0, 242, 254, 0.2);
}

.terminal-dots {
    display: flex;
    gap: 6px;
}

.terminal-dots .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.dot.red { background: #ff5f56; }
.dot.yellow { background: #ffbd2e; }
.dot.green { background: #27c93f; }

.terminal-title {
    flex: 1;
    text-align: center;
    color: var(--neon-secondary);
    font-family: monospace;
    font-size: 0.9rem;
    letter-spacing: 2px;
}

.ai-terminal-chat {
    height: 400px;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 15px;
    text-align: left;
}

.ai-msg {
    display: flex;
    gap: 15px;
    animation: fadeIn 0.3s ease;
}

.ai-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    box-shadow: 0 0 10px var(--neon-secondary);
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

.ai-text {
    background: rgba(0, 242, 254, 0.05);
    padding: 12px 18px;
    border-radius: 12px;
    border: 1px solid rgba(0, 242, 254, 0.1);
    color: #e0e0e0;
    font-size: 1rem;
    line-height: 1.5;
    max-width: 85%;
}

.user-msg .ai-text {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.1);
}

.flora-name {
    color: var(--neon-secondary);
    font-weight: bold;
    font-size: 0.85rem;
    display: block;
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.user-name {
    color: #aaa;
    font-weight: bold;
    font-size: 0.85rem;
    display: block;
    margin-bottom: 5px;
}

.ai-terminal-input-area {
    padding: 15px;
    background: rgba(0, 0, 0, 0.4);
    border-top: 1px solid rgba(0, 242, 254, 0.2);
    display: flex;
    gap: 10px;
}

#ai-input {
    flex: 1;
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 12px 15px;
    color: #fff;
    border-radius: 8px;
    font-size: 1rem;
    outline: none;
    transition: 0.3s;
}

#ai-input:focus {
    border-color: var(--neon-secondary);
    box-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
}

#ai-send-btn {
    background: var(--neon-secondary);
    border: none;
    width: 50px;
    border-radius: 8px;
    color: #000;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.3s;
}

#ai-send-btn:hover {
    box-shadow: 0 0 15px var(--neon-secondary);
    transform: scale(1.05);
}

#ai-send-btn svg {
    width: 20px;
    height: 20px;
}

.typing-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: var(--neon-secondary);
    border-radius: 50%;
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 100% { opacity: 0.2; }
    50% { opacity: 1; }
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(css_code)
print("CSS appended successfully.")
