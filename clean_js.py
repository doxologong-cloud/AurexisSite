with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Find the start of the Window Manager
start_idx = text.find('// ==========================================\n// WEB-OS WINDOW MANAGER')
if start_idx != -1:
    # Find the end of the Window Manager (the next section or end of file)
    end_idx = text.find('// ==========================================\n// THEME & LANG SETTINGS')
    if end_idx != -1:
        text = text[:start_idx] + text[end_idx:]
    else:
        text = text[:start_idx]
        
# Ensure switchView is defined
if 'function switchView(' not in text and 'window.switchView' not in text:
    switch_view_js = """
// ==========================================
// NAVIGATION (Restored)
// ==========================================
function switchView(viewId) {
    document.querySelectorAll('.view').forEach(v => {
        v.classList.remove('active');
        v.style.display = 'none';
    });
    
    document.querySelectorAll('.nav-link').forEach(l => {
        l.classList.remove('active');
    });

    const targetView = document.getElementById(viewId);
    if (targetView) {
        targetView.classList.add('active');
        targetView.style.display = 'block'; // or flex if messenger, let's just let CSS handle it
        // Actually, restore original behavior:
        if (viewId === 'view-messenger') {
            targetView.style.display = 'flex';
        } else {
            targetView.style.display = 'block';
        }
    }

    // Attempt to highlight nav link
    const links = document.querySelectorAll('.nav-link');
    for (let link of links) {
        if (link.getAttribute('onclick') && link.getAttribute('onclick').includes(viewId)) {
            link.classList.add('active');
            break;
        }
    }
}
"""
    text += "\n" + switch_view_js

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Removed Window Manager JS")
