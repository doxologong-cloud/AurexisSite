import re

with open('static/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the old cursors
text = re.sub(r'cursor:\s*url\([^)]+\)[^;]+;', '', text)

# Add custom cursor CSS
custom_cursor_css = """
/* CUSTOM CURSOR */
* {
    cursor: none !important;
}

#custom-cursor {
    position: fixed;
    top: 0;
    left: 0;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 999999999999;
    transform: translate(-50%, -50%);
    background: var(--neon-primary);
    box-shadow: 0 0 15px var(--neon-primary), 0 0 30px var(--neon-primary);
    transition: transform 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275), width 0.2s, height 0.2s;
    mix-blend-mode: screen;
}

#custom-cursor.clicking {
    transform: translate(-50%, -50%) scale(0.5);
    background: #fff;
    box-shadow: 0 0 20px #fff;
}

#custom-cursor.hovering {
    width: 40px;
    height: 40px;
    background: transparent;
    border: 2px solid var(--neon-primary);
    box-shadow: inset 0 0 10px var(--neon-primary), 0 0 10px var(--neon-primary);
}

/* SETTINGS REDESIGN */
.settings-theme-cards {
    display: flex;
    gap: 15px;
    margin-top: 15px;
}

.theme-card {
    flex: 1;
    background: rgba(0,0,0,0.5);
    border: 2px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    cursor: none;
    transition: all 0.3s;
}

.theme-card:hover {
    background: rgba(255,255,255,0.05);
    transform: translateY(-5px);
}

.theme-card.active {
    border-color: var(--neon-primary);
    box-shadow: 0 0 15px rgba(var(--neon-primary-rgb, 255,255,255), 0.3);
}

.theme-card-color {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin: 0 auto 10px auto;
}

/* BEAUTIFUL STARS */
.review-star {
    fill: transparent;
    stroke: var(--neon-primary);
    stroke-width: 2px;
    transition: all 0.3s ease;
    filter: drop-shadow(0 0 2px var(--neon-primary));
}

.review-star.filled {
    fill: var(--neon-primary);
    filter: drop-shadow(0 0 8px var(--neon-primary));
    animation: star-pulse 2s infinite alternate;
}

@keyframes star-pulse {
    0% { filter: drop-shadow(0 0 5px var(--neon-primary)); transform: scale(1); }
    100% { filter: drop-shadow(0 0 12px var(--neon-primary)); transform: scale(1.1); }
}

"""

# Append custom cursor CSS
text += custom_cursor_css

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(text)

print("CSS updated successfully!")
