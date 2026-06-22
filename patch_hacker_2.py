import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update checkSession
check_session_old = """    async function checkSession() {
        try {
            const res = await fetch('/api/me');
            const data = await res.json();
            if (data.success) {
                loginUser(data.user, false);
            }
        } catch (e) {
            console.error('Session check failed');
        }
    }"""

check_session_new = """    async function checkSession() {
        try {
            const res = await fetch('/api/me');
            const data = await res.json();
            if (data.success) {
                loginUser(data.user, false);
                if (localStorage.getItem('aurex_theme') === 'hacked') {
                    enableHackerMode();
                }
            } else {
                window.currentUser = null;
                if (localStorage.getItem('aurex_theme') === 'hacked') {
                    changeTheme('matrix');
                }
            }
        } catch (e) {
            console.error('Session check failed');
            window.currentUser = null;
            if (localStorage.getItem('aurex_theme') === 'hacked') {
                changeTheme('matrix');
            }
        }
    }"""

js = js.replace(check_session_old, check_session_new)

# 2. Update enableHackerMode
hacker_old = """function enableHackerMode() {
    if (!window.currentUser || !window.currentUser.is_admin) {
        showToast('ACCESS DENIED', 'error');
        changeTheme('matrix');
        return;
    }
    document.body.classList.add('hacked-theme');
    
    // Start generating falling code and occasional errors"""

hacker_new = """function enableHackerMode() {
    if (window.currentUser === undefined) {
        document.body.classList.add('hacked-theme');
        return; // wait for checkSession
    }
    if (!window.currentUser || !window.currentUser.is_admin) {
        showToast('ACCESS DENIED', 'error');
        changeTheme('matrix');
        return;
    }
    document.body.classList.add('hacked-theme');
    
    // Start generating falling code and occasional errors"""

js = js.replace(hacker_old, hacker_new)

# 3. Add custom hacker cursor to changeTheme
change_theme_cursor_pattern = r'const svgDefault = `.*?`;\n\s*const svgPointer = `.*?`;'

hacker_cursor_logic = """const svgDefault = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${color1}"/><stop offset="100%25" stop-color="%23${color2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad)"/></g></svg>`;
    const svgPointer = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${ptrColor1}"/><stop offset="100%25" stop-color="%23${ptrColor2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad-ptr)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad-ptr)"/></g></svg>`;
    
    let finalCursorDefault = `url('${svgDefault}') 12 6, auto`;
    let finalCursorPointer = `url('${svgPointer}') 12 6, pointer`;

    if (themeName === 'hacked') {
        const hackerCursor = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><line x1="16" y1="0" x2="16" y2="32" stroke="%23ff0000" stroke-width="2"/><line x1="0" y1="16" x2="32" y2="16" stroke="%23ff0000" stroke-width="2"/><circle cx="16" cy="16" r="10" fill="none" stroke="%23ff0000" stroke-width="2"/><circle cx="16" cy="16" r="2" fill="%23ff0000"/></svg>`;
        finalCursorDefault = `url('${hackerCursor}') 16 16, crosshair`;
        finalCursorPointer = `url('${hackerCursor}') 16 16, crosshair`;
    }"""

js = re.sub(change_theme_cursor_pattern, hacker_cursor_logic, js)

cursor_set_pattern = r"root\.style\.setProperty\('--cursor-default', `url\('\$\{svgDefault\}'\) 12 6, auto`\);\n\s*root\.style\.setProperty\('--cursor-pointer', `url\('\$\{svgPointer\}'\) 12 6, pointer`\);"
cursor_set_new = """root.style.setProperty('--cursor-default', finalCursorDefault);
    root.style.setProperty('--cursor-pointer', finalCursorPointer);"""

js = re.sub(cursor_set_pattern, cursor_set_new, js)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)
