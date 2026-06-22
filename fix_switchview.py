import re
with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

bad_switch = """    if (targetView) {
        targetView.classList.add('active');
        targetView.style.display = 'block'; // or flex if messenger, let's just let CSS handle it
        // Actually, restore original behavior:
        if (viewId === 'view-messenger') {
            targetView.style.display = 'flex';
        } else {
            targetView.style.display = 'block';
        }
    }"""

good_switch = """    if (targetView) {
        targetView.classList.add('active');
        targetView.classList.remove('hidden-view'); // Fix for hidden-view override!
        if (viewId === 'view-messenger') {
            targetView.style.display = 'flex';
        } else if (viewId === 'view-editor') {
            targetView.style.display = 'flex';
        } else {
            targetView.style.display = 'block';
        }
    }"""

if bad_switch in text:
    text = text.replace(bad_switch, good_switch)
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed switchView logic!")
else:
    print("Could not find bad switchView logic!")

