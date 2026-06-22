import re

new_script = """<script>
    (function() {
        const theme = localStorage.getItem('aurex_theme') || 'matrix';
        const root = document.documentElement;
        let color1, color2, ptrColor1, ptrColor2;
        
        if (theme === 'matrix') {
            root.style.setProperty('--neon-color', '#ffcc00');
            root.style.setProperty('--bg-color', '#0a0a0a');
            root.style.setProperty('--glow-color', 'rgba(255, 204, 0, 0.5)');
            root.style.setProperty('--neon-primary', '#e5b322');
            color1 = 'FFE373'; color2 = 'D4AF37'; ptrColor1 = 'ffffff'; ptrColor2 = 'FFE373';
        } else if (theme === 'synthwave') {
            root.style.setProperty('--neon-color', '#ff00ff');
            root.style.setProperty('--bg-color', '#1a0b2e');
            root.style.setProperty('--glow-color', 'rgba(255, 0, 255, 0.5)');
            root.style.setProperty('--neon-primary', '#b026ff');
            color1 = 'ff66ff'; color2 = 'ff00ff'; ptrColor1 = 'ffffff'; ptrColor2 = 'ff66ff';
        } else if (theme === 'cyberpunk') {
            root.style.setProperty('--neon-color', '#00ffcc');
            root.style.setProperty('--bg-color', '#0b1a1a');
            root.style.setProperty('--glow-color', 'rgba(0, 255, 204, 0.5)');
            root.style.setProperty('--neon-primary', '#00ff88');
            color1 = '66ffeb'; color2 = '00ffcc'; ptrColor1 = 'ffffff'; ptrColor2 = '66ffeb';
        } else if (theme === 'vampire') {
            root.style.setProperty('--neon-color', '#ff0000');
            root.style.setProperty('--bg-color', '#1a0000');
            root.style.setProperty('--glow-color', 'rgba(255, 0, 0, 0.5)');
            root.style.setProperty('--neon-primary', '#ff0000');
            color1 = 'ff4d4d'; color2 = 'cc0000'; ptrColor1 = 'ffffff'; ptrColor2 = 'ff4d4d';
        } else if (theme === 'ocean') {
            root.style.setProperty('--neon-color', '#00ffff');
            root.style.setProperty('--bg-color', '#000a1a');
            root.style.setProperty('--glow-color', 'rgba(0, 255, 255, 0.5)');
            root.style.setProperty('--neon-primary', '#0088ff');
            color1 = '66ffff'; color2 = '0088ff'; ptrColor1 = 'ffffff'; ptrColor2 = '66ffff';
        } else if (theme === 'hacked') {
            root.style.setProperty('--neon-color', '#ff0000');
            root.style.setProperty('--bg-color', '#000000');
            root.style.setProperty('--glow-color', 'rgba(255, 0, 0, 0.8)');
            root.style.setProperty('--neon-primary', '#ff0000');
            color1 = 'ff0000'; color2 = '8b0000'; ptrColor1 = 'ff0000'; ptrColor2 = 'ff0000';
            document.body && document.body.classList.add('hacked-theme');
        }
        
        const svgDefault = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${color1}"/><stop offset="100%25" stop-color="%23${color2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad)"/></g></svg>`;
        const svgPointer = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%25" stop-color="%23${ptrColor1}"/><stop offset="100%25" stop-color="%23${ptrColor2}"/></linearGradient><filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="1" flood-color="%23000" flood-opacity="0.6"/></filter></defs><g filter="url(%23shadow)" transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(%23theme-grad-ptr)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(%23theme-grad-ptr)"/></g></svg>`;
        
        let finalCursorDefault = `url('${svgDefault}') 12 6, auto`;
        let finalCursorPointer = `url('${svgPointer}') 12 6, pointer`;

        if (theme === 'hacked') {
            const hackerCursor = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><line x1="16" y1="0" x2="16" y2="32" stroke="%23ff0000" stroke-width="2"/><line x1="0" y1="16" x2="32" y2="16" stroke="%23ff0000" stroke-width="2"/><circle cx="16" cy="16" r="10" fill="none" stroke="%23ff0000" stroke-width="2"/><circle cx="16" cy="16" r="2" fill="%23ff0000"/></svg>`;
            finalCursorDefault = `url('${hackerCursor}') 16 16, crosshair`;
            finalCursorPointer = `url('${hackerCursor}') 16 16, crosshair`;
        }

        root.style.setProperty('--cursor-default', finalCursorDefault);
        root.style.setProperty('--cursor-pointer', finalCursorPointer);
    })();
</script>"""

for path in ['templates/index.html', 'templates/admin.html']:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
            
        pattern = r'<script>\s*\(function\(\) \{\s*const theme = localStorage.getItem\(\'aurex_theme\'\).*?\}\)\(\);\s*</script>'
        html = re.sub(pattern, new_script, html, flags=re.DOTALL)
        
        # update cache buster
        html = re.sub(r'\?v=\d+', '?v=81', html)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    except FileNotFoundError:
        pass
