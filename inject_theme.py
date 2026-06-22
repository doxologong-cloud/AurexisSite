import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

theme_js = """
// ==========================================
// THEME & LANG SETTINGS
// ==========================================

function changeTheme(themeName) {
    const root = document.documentElement;
    if (themeName === 'matrix') {
        root.style.setProperty('--neon-color', '#ffcc00');
        root.style.setProperty('--bg-color', '#0a0a0a');
        root.style.setProperty('--glow-color', 'rgba(255, 204, 0, 0.5)');
    } else if (themeName === 'synthwave') {
        root.style.setProperty('--neon-color', '#ff00ff');
        root.style.setProperty('--bg-color', '#1a0b2e');
        root.style.setProperty('--glow-color', 'rgba(255, 0, 255, 0.5)');
    } else if (themeName === 'cyberpunk') {
        root.style.setProperty('--neon-color', '#00ffcc');
        root.style.setProperty('--bg-color', '#0b1a1a');
        root.style.setProperty('--glow-color', 'rgba(0, 255, 204, 0.5)');
    }
    localStorage.setItem('aurex_theme', themeName);
}

function changeLang(lang) {
    // Simple alert for now, full localization requires mapping
    alert('Язык изменен на: ' + lang + '. (Локализация будет добавлена в следующих фазах)');
    localStorage.setItem('aurex_lang', lang);
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('aurex_theme');
    if (savedTheme) {
        changeTheme(savedTheme);
        const sel = document.getElementById('theme-selector');
        if (sel) sel.value = savedTheme;
    }
    const savedLang = localStorage.getItem('aurex_lang');
    if (savedLang) {
        const sel = document.getElementById('lang-selector');
        if (sel) sel.value = savedLang;
    }
});
"""

if 'changeTheme(themeName)' not in js_text:
    js_text += "\n" + theme_js
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js_text)
    print("Injected Theme JS.")
else:
    print("Theme JS already exists.")
