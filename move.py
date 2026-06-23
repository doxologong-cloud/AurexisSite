import os

path = r'C:\Users\user\Desktop\сайт\templates\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = next(i for i, l in enumerate(lines) if '<!-- Services Catalog Section -->' in l)
end_idx = next(i for i, l in enumerate(lines) if '<!-- News Section -->' in l)

chunk = lines[start_idx:end_idx]
del lines[start_idx:end_idx]

stats_idx = next(i for i, l in enumerate(lines) if '<!-- Stats View -->' in l)

new_view = [
    '\n<!-- Services View -->\n',
    '<div class="view hidden-view" id="view-services">\n'
] + chunk + [
    '</div>\n\n'
]

lines = lines[:stats_idx] + new_view + lines[stats_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Success')
