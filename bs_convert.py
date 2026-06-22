from bs4 import BeautifulSoup

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

views = {
    'view-home': 'Главная',
    'view-store': 'Магазин Ботов',
    'view-ai': 'Нейро-Ассистент',
    'view-messenger': 'Лента',
    'view-portfolio': 'Портфолио'
}

for view_id, title in views.items():
    view_div = soup.find('div', id=view_id)
    if view_div:
        # Create a new window div
        window_div = soup.new_tag('div')
        window_div['id'] = view_id
        window_div['class'] = 'window'
        
        # Header
        header_div = soup.new_tag('div')
        header_div['class'] = 'window-header'
        header_div['onmousedown'] = f"startDrag(event, '{view_id}')"
        
        title_div = soup.new_tag('div')
        title_div['class'] = 'window-title'
        title_div.string = title
        
        controls_div = soup.new_tag('div')
        controls_div['class'] = 'window-controls'
        
        btn_min = soup.new_tag('button')
        btn_min['class'] = 'window-btn btn-min'
        btn_min['onclick'] = f"minimizeWindow('{view_id}')"
        
        btn_max = soup.new_tag('button')
        btn_max['class'] = 'window-btn btn-max'
        btn_max['onclick'] = f"maximizeWindow('{view_id}')"
        
        btn_close = soup.new_tag('button')
        btn_close['class'] = 'window-btn btn-close'
        btn_close['onclick'] = f"closeWindow('{view_id}')"
        
        controls_div.append(btn_min)
        controls_div.append(btn_max)
        controls_div.append(btn_close)
        
        header_div.append(title_div)
        header_div.append(controls_div)
        
        # Content
        content_div = soup.new_tag('div')
        content_div['class'] = 'window-content'
        
        # Move all children of view_div to content_div
        for child in list(view_div.children):
            content_div.append(child)
            
        window_div.append(header_div)
        window_div.append(content_div)
        
        # Replace original view_div with window_div
        view_div.replace_with(window_div)

# Save
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Successfully converted views to windows using BeautifulSoup.")
