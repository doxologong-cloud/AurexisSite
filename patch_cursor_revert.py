import re

# 1. Fix script.js and index.html: remove btoa, use encodeURIComponent
def fix_js(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # We have lines like:
        # let finalCursorDefault = `url('data:image/svg+xml;base64,${btoa(svgDefaultStr)}') 12 6, auto`;
        # finalCursorPointer = `url('data:image/svg+xml;base64,${btoa(hackerCursorStr)}') 16 16, crosshair`;
        
        content = content.replace("url('data:image/svg+xml;base64,${btoa(svgDefaultStr)}')", "url(\\'data:image/svg+xml,${encodeURIComponent(svgDefaultStr)}\\')")
        content = content.replace("url('data:image/svg+xml;base64,${btoa(svgPointerStr)}')", "url(\\'data:image/svg+xml,${encodeURIComponent(svgPointerStr)}\\')")
        content = content.replace("url('data:image/svg+xml;base64,${btoa(hackerCursorStr)}')", "url(\\'data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}\\')")
        
        # In python replace, `\'` is just `'`. Wait, I shouldn't double escape in replace unless I want literally `\'`.
        # The original text in script.js has `url('data:image/svg+xml;base64,${btoa(...)}')`
        # I want `url("data:image/svg+xml,${encodeURIComponent(...)}")`
        
        content = content.replace("url('data:image/svg+xml;base64,${btoa(svgDefaultStr)}')", "url(\"data:image/svg+xml,${encodeURIComponent(svgDefaultStr)}\")")
        content = content.replace("url('data:image/svg+xml;base64,${btoa(svgPointerStr)}')", "url(\"data:image/svg+xml,${encodeURIComponent(svgPointerStr)}\")")
        content = content.replace("url('data:image/svg+xml;base64,${btoa(hackerCursorStr)}')", "url(\"data:image/svg+xml,${encodeURIComponent(hackerCursorStr)}\")")
        
        # Also ensure we don't have stray %23 or %25 in the SVG definitions since encodeURIComponent will handle # and % correctly
        # The SVG strings in script.js right now use `#` and `%` since my last patch decoded them. So encodeURIComponent is perfect.
        
        # Update cache buster if html
        if path.endswith('.html'):
            content = re.sub(r'\?v=\d+', '?v=91', content)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed JS cursors in {path}")
    except FileNotFoundError:
        pass

fix_js('static/script.js')
fix_js('templates/index.html')
fix_js('templates/admin.html')

# 2. Fix style.css: remove `*, html, body` and revert to `html, body`
def fix_css(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            css = f.read()
            
        css = css.replace("*, html, body {\n    cursor: var(--cursor-default, auto) !important;\n}", "html, body {\n    cursor: var(--cursor-default, auto) !important;\n}")
        
        # Also remove [onclick] *, a *, button * which might cause massive style recalculation lags
        css = css.replace(",\n[onclick] *, a *, button * {\n    cursor: var(--cursor-pointer, pointer) !important;\n}", " {\n    cursor: var(--cursor-pointer, pointer) !important;\n}")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(css)
        print(f"Fixed CSS in {path}")
    except FileNotFoundError:
        pass

fix_css('static/style.css')
