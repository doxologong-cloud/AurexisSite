import os

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = """                                setTimeout(() => {
                                    finalTerminal.style.transition = 'opacity 2s';
                                    finalTerminal.style.opacity = '0';
                                    setTimeout(() => {
                                        finalTerminal.remove();
                                    }, 2000);
                                }, 3000);"""

replacement = """                                setTimeout(() => {
                                    finalTerminal.style.transition = 'opacity 2s';
                                    finalTerminal.style.opacity = '0';
                                    const face = document.querySelector('.creepy-face');
                                    if(face) {
                                        face.style.transition = 'opacity 2s';
                                        face.style.opacity = '0';
                                    }
                                    setTimeout(() => {
                                        finalTerminal.remove();
                                        if(face) face.remove();
                                        document.body.classList.remove('apocalypse-mode'); // Clean up any remaining classes
                                    }, 2000);
                                }, 3000);"""

# The indentations might not match exactly, so I'll use regex.
import re
new_text = re.sub(
    r"setTimeout\(\(\) => \{\s*finalTerminal\.style\.transition = 'opacity 2s';\s*finalTerminal\.style\.opacity = '0';\s*setTimeout\(\(\) => \{\s*finalTerminal\.remove\(\);\s*\}, 2000\);\s*\}, 3000\);",
    replacement,
    text
)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Face removal patched.")
