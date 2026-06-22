import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js_text = f.read()

# Replace changeLang
old_change_lang = """function changeLang(lang) {
    // Simple alert for now, full localization requires mapping
    alert('Язык изменен на: ' + lang + '. (Локализация будет добавлена в следующих фазах)');
    localStorage.setItem('aurex_lang', lang);
}"""

new_change_lang = """function applyTranslations(lang) {
    if (typeof translations === 'undefined') return;
    const dict = translations[lang] || translations['ru'];
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) el.textContent = dict[key];
    });
    
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) el.placeholder = dict[key];
    });
    
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (dict[key]) el.title = dict[key];
    });
    
    document.querySelectorAll('[data-i18n-data-text]').forEach(el => {
        const key = el.getAttribute('data-i18n-data-text');
        if (dict[key]) el.setAttribute('data-text', dict[key]);
    });
}

function changeLang(lang) {
    localStorage.setItem('aurex_lang', lang);
    applyTranslations(lang);
}"""

js_text = js_text.replace(old_change_lang, new_change_lang)

# Find the DOMContentLoaded part where changeLang is called
old_init_lang = """    const savedLang = localStorage.getItem('aurex_lang');
    if (savedLang) {
        const sel = document.getElementById('lang-selector');
        if (sel) sel.value = savedLang;
    }"""

new_init_lang = """    const savedLang = localStorage.getItem('aurex_lang') || 'ru';
    const sel = document.getElementById('lang-selector');
    if (sel) sel.value = savedLang;
    applyTranslations(savedLang);"""

js_text = js_text.replace(old_init_lang, new_init_lang)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js_text)

print("Injected localization engine into script.js")
