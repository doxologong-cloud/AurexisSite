import re

def patch_script():
    with open('static/script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # Add changeCursorShape global function
    if 'function changeCursorShape(' not in js:
        js += """\n
// === CURSOR SHAPE SETTING ===
window.changeCursorShape = function(shape) {
    localStorage.setItem('aurex_cursor_shape', shape);
    updateThemeColors(theme);
    
    // Update UI toggle buttons if they exist
    document.querySelectorAll('.cursor-btn').forEach(btn => btn.classList.remove('active'));
    let activeBtn = document.getElementById('cursor-btn-' + shape);
    if(activeBtn) activeBtn.classList.add('active');
};
"""
    
    # Locate updateThemeColors cursor string definitions
    old_svg_def = r"""        const svgDefaultStr = `<svg xmlns="http://www\.w3\.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#\$\{color1\}"/><stop offset="100%" stop-color="#\$\{color2\}"/></linearGradient></defs><g transform="translate\(12, 6\) rotate\(-25\)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="rgba\(0,0,0,0\.5\)" transform="translate\(1, 2\)"/><polygon points="1,0 9,18 4,18 1,12" fill="rgba\(0,0,0,0\.5\)" transform="translate\(1, 2\)"/><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url\(#theme-grad\)"/><polygon points="1,0 9,18 4,18 1,12" fill="url\(#theme-grad\)"/></g></svg>`;
        const svgPointerStr = `<svg xmlns="http://www\.w3\.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#\$\{ptrColor1\}"/><stop offset="100%" stop-color="#\$\{ptrColor2\}"/></linearGradient></defs><g transform="translate\(12, 6\) rotate\(-25\)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="rgba\(0,0,0,0\.5\)" transform="translate\(1, 2\)"/><polygon points="1,0 9,18 4,18 1,12" fill="rgba\(0,0,0,0\.5\)" transform="translate\(1, 2\)"/><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url\(#theme-grad-ptr\)"/><polygon points="1,0 9,18 4,18 1,12" fill="url\(#theme-grad-ptr\)"/></g></svg>`;"""

    new_svg_def = """        const shape = localStorage.getItem('aurex_cursor_shape') || 'triangle';
        
        let svgDefaultStr, svgPointerStr;
        if (shape === 'circle') {
            svgDefaultStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${color1}"/><stop offset="100%" stop-color="#${color2}"/></linearGradient></defs><circle cx="16" cy="16" r="10" fill="none" stroke="url(#theme-grad)" stroke-width="2"/><circle cx="16" cy="16" r="3" fill="url(#theme-grad)"/></svg>`;
            svgPointerStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${ptrColor1}"/><stop offset="100%" stop-color="#${ptrColor2}"/></linearGradient></defs><circle cx="16" cy="16" r="12" fill="none" stroke="url(#theme-grad-ptr)" stroke-width="3"/><circle cx="16" cy="16" r="4" fill="url(#theme-grad-ptr)"/></svg>`;
        } else {
            svgDefaultStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${color1}"/><stop offset="100%" stop-color="#${color2}"/></linearGradient></defs><g transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="1,0 9,18 4,18 1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(#theme-grad)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(#theme-grad)"/></g></svg>`;
            svgPointerStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${ptrColor1}"/><stop offset="100%" stop-color="#${ptrColor2}"/></linearGradient></defs><g transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="1,0 9,18 4,18 1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(#theme-grad-ptr)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(#theme-grad-ptr)"/></g></svg>`;
        }"""
    
    js = re.sub(old_svg_def, new_svg_def, js)
    
    old_hacker = r"const hackerCursorStr = `<svg xmlns=\"http://www\.w3\.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path d=\"M 2 2 L 10 22 L 13 13 L 22 10 Z\" fill=\"#ff0000\" stroke=\"#ff0000\" stroke-width=\"2\" stroke-linejoin=\"round\" stroke-opacity=\"0\.4\"/></svg>`;"
    new_hacker = r"const hackerCursorStr = shape === 'circle' ? `<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"32\" height=\"32\" viewBox=\"0 0 32 32\"><circle cx=\"16\" cy=\"16\" r=\"10\" fill=\"none\" stroke=\"#ff0000\" stroke-width=\"2\"/><circle cx=\"16\" cy=\"16\" r=\"3\" fill=\"#ff0000\"/></svg>` : `<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path d=\"M 2 2 L 10 22 L 13 13 L 22 10 Z\" fill=\"#ff0000\" stroke=\"#ff0000\" stroke-width=\"2\" stroke-linejoin=\"round\" stroke-opacity=\"0.4\"/></svg>`;"
    
    js = re.sub(old_hacker, new_hacker, js)

    # Need to replace the fixed hotspot numbers (12, 6) or (2, 2) with conditional hotspots
    # For rasterizeSVGToPNG(themeName === 'hacked' ? hackerCursorStr : svgDefaultStr, ...
    old_rasterize_default = r"rasterizeSVGToPNG\(themeName === 'hacked' \? hackerCursorStr : svgDefaultStr, themeName === 'hacked' \? 2 : 12, themeName === 'hacked' \? 2 : 6, function\(pngUrlDefault\) \{"
    new_rasterize_default = r"""let hotspotDefX = shape === 'circle' ? 16 : (themeName === 'hacked' ? 2 : 12);
        let hotspotDefY = shape === 'circle' ? 16 : (themeName === 'hacked' ? 2 : 6);
        let hotspotPtrX = shape === 'circle' ? 16 : (themeName === 'hacked' ? 2 : 12);
        let hotspotPtrY = shape === 'circle' ? 16 : (themeName === 'hacked' ? 2 : 6);
        
        rasterizeSVGToPNG(themeName === 'hacked' ? hackerCursorStr : svgDefaultStr, hotspotDefX, hotspotDefY, function(pngUrlDefault) {"""
    js = re.sub(old_rasterize_default, new_rasterize_default, js)

    old_rasterize_pointer = r"rasterizeSVGToPNG\(themeName === 'hacked' \? hackerCursorStr : svgPointerStr, themeName === 'hacked' \? 2 : 12, themeName === 'hacked' \? 2 : 6, function\(pngUrlPointer\) \{"
    new_rasterize_pointer = r"rasterizeSVGToPNG(themeName === 'hacked' ? hackerCursorStr : svgPointerStr, hotspotPtrX, hotspotPtrY, function(pngUrlPointer) {"
    js = re.sub(old_rasterize_pointer, new_rasterize_pointer, js)
    
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Patched script.js")

def patch_html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()

        # Add the cursor toggle UI to the settings view
        settings_html = """  <h3 style="color: var(--neon-color); text-transform: uppercase; margin-bottom: 20px; margin-top: 30px;">Выбор Курсора</h3>
  
  <div style="display: flex; gap: 15px; margin-bottom: 30px;">
      <button id="cursor-btn-triangle" class="cursor-btn active" onclick="changeCursorShape('triangle')" style="padding: 10px 20px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); border-radius: 5px; color: white; cursor: pointer; transition: 0.3s;">Классический (Треугольник)</button>
      <button id="cursor-btn-circle" class="cursor-btn" onclick="changeCursorShape('circle')" style="padding: 10px 20px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); border-radius: 5px; color: white; cursor: pointer; transition: 0.3s;">Неоновый (Кружок)</button>
  </div>"""

        if 'id="cursor-btn-triangle"' not in html:
            html = html.replace('<div class="settings-theme-cards">', settings_html + '\n\n  <label style="color: #fff; font-size: 1.1rem; display: block; margin-bottom: 10px;">Цветовая Тема:</label>\n  <div class="settings-theme-cards">')
            
        # We also need to fix the inline head rasterization in HTML so it respects shape on first load
        old_inline_raster = r"rasterizeSVGToPNG\(theme === 'hacked' \? hackerCursorStr : svgDefaultStr, theme === 'hacked' \? 2 : 12, theme === 'hacked' \? 2 : 6, function\(pngUrlDefault\) \{"
        new_inline_raster = r"""const shape = localStorage.getItem('aurex_cursor_shape') || 'triangle';
        let hotspotDefX = shape === 'circle' ? 16 : (theme === 'hacked' ? 2 : 12);
        let hotspotDefY = shape === 'circle' ? 16 : (theme === 'hacked' ? 2 : 6);
        let hotspotPtrX = shape === 'circle' ? 16 : (theme === 'hacked' ? 2 : 12);
        let hotspotPtrY = shape === 'circle' ? 16 : (theme === 'hacked' ? 2 : 6);
        
        rasterizeSVGToPNG(theme === 'hacked' ? hackerCursorStr : svgDefaultStr, hotspotDefX, hotspotDefY, function(pngUrlDefault) {"""
        html = re.sub(old_inline_raster, new_inline_raster, html)

        old_inline_raster_ptr = r"rasterizeSVGToPNG\(theme === 'hacked' \? hackerCursorStr : svgPointerStr, theme === 'hacked' \? 2 : 12, theme === 'hacked' \? 2 : 6, function\(pngUrlPointer\) \{"
        new_inline_raster_ptr = r"rasterizeSVGToPNG(theme === 'hacked' ? hackerCursorStr : svgPointerStr, hotspotPtrX, hotspotPtrY, function(pngUrlPointer) {"
        html = re.sub(old_inline_raster_ptr, new_inline_raster_ptr, html)

        # Also need to dynamically define the SVGs in the inline script
        # Wait, the inline script has `const svgDefaultStr = ...` hardcoded.
        old_inline_def = r"const svgDefaultStr = `<svg xmlns=\"http://www\.w3\.org/2000/svg\" width=\"32\" height=\"32\" viewBox=\"0 0 32 32\"><defs><linearGradient id=\"theme-grad\" x1=\"0\" y1=\"0\" x2=\"0\" y2=\"1\"><stop offset=\"0%\" stop-color=\"#\$\{color1\}\"/><stop offset=\"100%\" stop-color=\"#\$\{color2\}\"/></linearGradient></defs><g transform=\"translate\(12, 6\) rotate\(-25\)\"><polygon points=\"-1,0 -9,18 -4,18 -1,12\" fill=\"rgba\(0,0,0,0\.5\)\" transform=\"translate\(1, 2\)\"/><polygon points=\"1,0 9,18 4,18 1,12\" fill=\"rgba\(0,0,0,0\.5\)\" transform=\"translate\(1, 2\)\"/><polygon points=\"-1,0 -9,18 -4,18 -1,12\" fill=\"url\(#theme-grad\)\"/><polygon points=\"1,0 9,18 4,18 1,12\" fill=\"url\(#theme-grad\)\"/></g></svg>`;\s*const svgPointerStr = `<svg xmlns=\"http://www\.w3\.org/2000/svg\" width=\"32\" height=\"32\" viewBox=\"0 0 32 32\"><defs><linearGradient id=\"theme-grad-ptr\" x1=\"0\" y1=\"0\" x2=\"0\" y2=\"1\"><stop offset=\"0%\" stop-color=\"#\$\{ptrColor1\}\"/><stop offset=\"100%\" stop-color=\"#\$\{ptrColor2\}\"/></linearGradient></defs><g transform=\"translate\(12, 6\) rotate\(-25\)\"><polygon points=\"-1,0 -9,18 -4,18 -1,12\" fill=\"rgba\(0,0,0,0\.5\)\" transform=\"translate\(1, 2\)\"/><polygon points=\"1,0 9,18 4,18 1,12\" fill=\"rgba\(0,0,0,0\.5\)\" transform=\"translate\(1, 2\)\"/><polygon points=\"-1,0 -9,18 -4,18 -1,12\" fill=\"url\(#theme-grad-ptr\)\"/><polygon points=\"1,0 9,18 4,18 1,12\" fill=\"url\(#theme-grad-ptr\)\"/></g></svg>`;"
        new_inline_def = """let svgDefaultStr, svgPointerStr;
        if (localStorage.getItem('aurex_cursor_shape') === 'circle') {
            svgDefaultStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${color1}"/><stop offset="100%" stop-color="#${color2}"/></linearGradient></defs><circle cx="16" cy="16" r="10" fill="none" stroke="url(#theme-grad)" stroke-width="2"/><circle cx="16" cy="16" r="3" fill="url(#theme-grad)"/></svg>`;
            svgPointerStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${ptrColor1}"/><stop offset="100%" stop-color="#${ptrColor2}"/></linearGradient></defs><circle cx="16" cy="16" r="12" fill="none" stroke="url(#theme-grad-ptr)" stroke-width="3"/><circle cx="16" cy="16" r="4" fill="url(#theme-grad-ptr)"/></svg>`;
        } else {
            svgDefaultStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${color1}"/><stop offset="100%" stop-color="#${color2}"/></linearGradient></defs><g transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="1,0 9,18 4,18 1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(#theme-grad)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(#theme-grad)"/></g></svg>`;
            svgPointerStr = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${ptrColor1}"/><stop offset="100%" stop-color="#${ptrColor2}"/></linearGradient></defs><g transform="translate(12, 6) rotate(-25)"><polygon points="-1,0 -9,18 -4,18 -1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="1,0 9,18 4,18 1,12" fill="rgba(0,0,0,0.5)" transform="translate(1, 2)"/><polygon points="-1,0 -9,18 -4,18 -1,12" fill="url(#theme-grad-ptr)"/><polygon points="1,0 9,18 4,18 1,12" fill="url(#theme-grad-ptr)"/></g></svg>`;
        }"""
        html = re.sub(old_inline_def, new_inline_def, html)

        old_inline_hack = r"const hackerCursorStr = `<svg xmlns=\"http://www\.w3\.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path d=\"M 2 2 L 10 22 L 13 13 L 22 10 Z\" fill=\"#ff0000\" stroke=\"#ff0000\" stroke-width=\"2\" stroke-linejoin=\"round\" stroke-opacity=\"0\.4\"/></svg>`;"
        new_inline_hack = r"const hackerCursorStr = localStorage.getItem('aurex_cursor_shape') === 'circle' ? `<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"32\" height=\"32\" viewBox=\"0 0 32 32\"><circle cx=\"16\" cy=\"16\" r=\"10\" fill=\"none\" stroke=\"#ff0000\" stroke-width=\"2\"/><circle cx=\"16\" cy=\"16\" r=\"3\" fill=\"#ff0000\"/></svg>` : `<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path d=\"M 2 2 L 10 22 L 13 13 L 22 10 Z\" fill=\"#ff0000\" stroke=\"#ff0000\" stroke-width=\"2\" stroke-linejoin=\"round\" stroke-opacity=\"0.4\"/></svg>`;"
        html = re.sub(old_inline_hack, new_inline_hack, html)

        # Active state CSS for cursor buttons
        if '.cursor-btn.active' not in html:
            html = html.replace('</style>', '    .cursor-btn.active { border-color: var(--neon-primary) !important; background: rgba(0, 255, 170, 0.1) !important; color: var(--neon-primary) !important; }\n</style>')

        html = re.sub(r'\?v=\d+', '?v=104', html)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched {filepath}")
    except Exception as e:
        print(e)

patch_script()
patch_html('templates/index.html')
patch_html('templates/admin.html')
