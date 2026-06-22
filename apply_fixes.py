import re

# 1. Add .active to view-home in index.html
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make home view active by default so it doesn't blink
if '<div class="view" id="view-home">' in html:
    html = html.replace('<div class="view" id="view-home">', '<div class="view active" id="view-home">')

# Hide welcome screen natively
if '<div id="welcome-screen">' in html:
    html = html.replace('<div id="welcome-screen">', '<div id="welcome-screen" style="display: none;">')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Fix switchAuthTab and 0ms preloader in script.js
with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

bad_auth = """window.switchAuthTab = function(tabName) {
    window.location.hash = '#account';
    setTimeout(() => {"""

good_auth = """window.switchAuthTab = function(tabName) {
    setTimeout(() => {"""

if bad_auth in js:
    js = js.replace(bad_auth, good_auth)

bad_preloader = """    // Instant load
    welcomeScreen.style.opacity = '0';
    setTimeout(() => {
        welcomeScreen.style.visibility = 'hidden';
        document.querySelector('.hero')?.classList.add('show');
        initScrollAnimations();
    }, 100);"""

good_preloader = """    // Instant load
    if (welcomeScreen) welcomeScreen.style.display = 'none';
    document.querySelector('.hero')?.classList.add('show');
    initScrollAnimations();"""

if bad_preloader in js:
    js = js.replace(bad_preloader, good_preloader)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 3. Faster blink animation
with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

if 'animation: blink 2s infinite;' in css:
    css = css.replace('animation: blink 2s infinite;', 'animation: blink 0.5s infinite;')
if 'animation: pulse 2s infinite;' in css:
    css = css.replace('animation: pulse 2s infinite;', 'animation: pulse 0.5s infinite;')

with open('static/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Applied 3 fixes successfully!")
