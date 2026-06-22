import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define the views and their titles
views = {
    'view-home': 'Главная',
    'view-store': 'Магазин Ботов',
    'view-ai': 'Нейро-Ассистент',
    'view-messenger': 'Лента',
    'view-portfolio': 'Портфолио'
}

for view_id, title in views.items():
    # Find the opening div of the view
    match = re.search(r'<div id="{}" class="view"[^>]*>'.format(view_id), html)
    if not match:
        # Maybe it doesn't have class="view" exactly like that, try a more flexible regex
        match = re.search(r'<div[^>]*id="{}"[^>]*class="[^"]*view[^"]*"[^>]*>'.format(view_id), html)
    
    if match:
        original_tag = match.group(0)
        # Create the window wrapper
        window_wrapper = f"""<div id="{view_id}" class="window">
    <div class="window-header">
        <div class="window-title">{title}</div>
        <div class="window-controls">
            <button class="window-btn btn-min" onclick="minimizeWindow('{view_id}')"></button>
            <button class="window-btn btn-max" onclick="maximizeWindow('{view_id}')"></button>
            <button class="window-btn btn-close" onclick="closeWindow('{view_id}')"></button>
        </div>
    </div>
    <div class="window-content">
"""
        # We also need to change the id of the original view to avoid duplicate IDs, or just remove the ID from the inner div.
        # Let's remove the ID and class="view" from the inner div.
        inner_div = original_tag.replace(f'id="{view_id}"', '').replace('class="view"', 'class="view-inner"').replace('class="view active"', 'class="view-inner"')
        
        replacement = window_wrapper + inner_div
        html = html.replace(original_tag, replacement)

        # Now we need to find the closing div of the view. This is tricky with regex, 
        # but since we appended view-messenger and view-portfolio at the bottom, 
        # let's just append `</div>` before the next view or at the end of `<main>`.
        # Actually, it's much safer to do this manually in a cleaner way, or use BeautifulSoup.

with open('convert.py', 'w') as f:
    f.write('print("use beautifulsoup")')

