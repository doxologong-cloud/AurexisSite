import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update changeTheme to handle cards
old_change_theme = "function changeTheme(theme) {\n    document.body.className = theme;"
new_change_theme = """function changeTheme(theme) {
    document.documentElement.className = theme;
    document.body.className = theme;
    localStorage.setItem('theme', theme);
    
    // Update active card
    document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
    const activeCard = document.getElementById('card-' + theme.replace('theme-', ''));
    if(activeCard) activeCard.classList.add('active');
"""
text = text.replace(old_change_theme, new_change_theme)


# 2. Add cursor logic at the end of the file
cursor_logic = """
// ==========================================
// Custom Cursor Logic
// ==========================================
const cursor = document.getElementById('custom-cursor');
if (cursor) {
    document.addEventListener('mousemove', e => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    document.addEventListener('mousedown', () => cursor.classList.add('clicking'));
    document.addEventListener('mouseup', () => cursor.classList.remove('clicking'));

    // Hover effect on interactive elements
    const interactiveElements = document.querySelectorAll('a, button, input, textarea, select, .theme-card, .msgr-tab, .dropdown-item');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('hovering'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('hovering'));
    });
}
"""
text += cursor_logic


# 3. Update stars in loadReviews
# Look for: const stars = '<svg style="vertical-align: text-bottom; margin-right: 2px;" width="16" height="16" viewBox="0 0 24 24" fill="#ffc107" stroke="#ffc107" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'.repeat(r.rating);
old_stars_regex = r"const stars = '<svg[^>]*><polygon[^>]*></polygon></svg>'\.repeat\(r\.rating\);"
new_stars = """
                    let stars = '';
                    for (let i = 1; i <= 5; i++) {
                        if (i <= r.rating) {
                            stars += `<svg class="review-star filled" style="vertical-align: text-bottom; margin-right: 4px;" width="20" height="20" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>`;
                        } else {
                            stars += `<svg class="review-star" style="vertical-align: text-bottom; margin-right: 4px;" width="20" height="20" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>`;
                        }
                    }
"""
text = re.sub(old_stars_regex, new_stars, text)


# 4. Replace Easter Egg Trigger
# Find Easter Egg Logic
old_ee_trigger = """    // Easter Egg Logic
    let keySequence = '';
    const secretWord = 'flora';
    const nukeWord = 'wpst';
    let easterEggActive = false;

    window.addEventListener('keydown', (e) => {
        if (easterEggActive) return;
        
        // Ignore if typing in an input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        keySequence += e.key.toLowerCase();
        
        if (keySequence.length > secretWord.length) {
            keySequence = keySequence.substring(1);
        }

        if (keySequence.endsWith('dox')) {"""

new_ee_trigger = """    // Easter Egg Logic
    let easterEggActive = false;
    
    const codeArea = document.getElementById('code-textarea');
    if (codeArea) {
        codeArea.addEventListener('input', (e) => {
            if (easterEggActive) return;
            const val = e.target.value.toLowerCase();
            if (val.includes('new proccess create: "dox"')) {"""
text = text.replace(old_ee_trigger, new_ee_trigger)


# Now fix the ending braces for the easter egg if block
# In the original, there was an `} else if (keySequence.endsWith(secretWord)) { ... }` block
# Let's replace the other key sequences to be triggered via editor too, or just handle dox.
# The user only specifically mentioned: "надо будет написать new proccess create: "имя "секретки"" и откроется например докс и т.д."

text = text.replace("} else if (keySequence.endsWith(secretWord)) {", "} else if (val.includes('new proccess create: \"flora\"')) {")
text = text.replace("} else if (keySequence.endsWith(nukeWord)) {", "} else if (val.includes('new proccess create: \"wpst\"')) {")

# Finally, change the closing bracket of the event listener from window to codeArea
# We replaced `window.addEventListener('keydown', (e) => {` with `codeArea.addEventListener('input', (e) => {`
# The closing brackets should be identical.

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("script.js updated successfully!")
