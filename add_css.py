css = """
/* Hacked Theme Effects */
.hacked-theme {
    animation: screen-glitch 0.2s linear infinite;
    overflow-x: hidden;
}

@keyframes screen-glitch {
    0% { transform: translate(0) }
    20% { transform: translate(-1px, 1px) }
    40% { transform: translate(-1px, -1px) }
    60% { transform: translate(1px, 1px) }
    80% { transform: translate(1px, -1px) }
    100% { transform: translate(0) }
}

.fake-bug {
    pointer-events: none;
    z-index: 9999;
    white-space: nowrap;
    text-shadow: 0 0 10px red, 0 0 20px red !important;
    animation: text-flicker 0.1s infinite;
}

@keyframes text-flicker {
    0% { opacity: 0.1; }
    50% { opacity: 1; }
    100% { opacity: 0.1; }
}

/* Disable Animations Toggle */
body.no-animations *, body.no-animations {
    animation: none !important;
    transition: none !important;
}
"""

with open('static/style.css', 'a', encoding='utf-8') as f:
    f.write(css)
