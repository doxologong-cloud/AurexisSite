import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

support_svg = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"></path><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path></svg>'
economy_svg = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="8" r="6"></circle><path d="M18.09 10.37A6 6 0 1 1 10.34 18"></path><path d="M7 6h1v4"></path><path d="M16.7 14.4l2.8 1.6"></path></svg>'
mafia_svg = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h20"></path><path d="M4 12v-2a8 8 0 0 1 16 0v2"></path><rect x="6" y="12" width="12" height="8" rx="2"></rect><circle cx="9" cy="16" r="1"></circle><circle cx="15" cy="16" r="1"></circle></svg>'
flora_svg = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M12 9A8.005 8.005 0 0 0 4.29 14"></path><path d="M12 15a8.005 8.005 0 0 0 7.71-5"></path><path d="M15 12a8.005 8.005 0 0 0-6 0"></path></svg>'

html = re.sub(r'<i class="fa-solid fa-headset"></i>', support_svg, html)
html = re.sub(r'<i class="fa-solid fa-coins"></i>', economy_svg, html)
html = re.sub(r'<i class="fa-solid fa-user-secret"></i>', mafia_svg, html)
html = re.sub(r'<i class="fa-solid fa-biohazard"></i>', flora_svg, html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

star_svg = '''<svg style="vertical-align: text-bottom; margin-right: 2px;" width="16" height="16" viewBox="0 0 24 24" fill="#ffc107" stroke="#ffc107" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'''
old_star_js = '''<i class="fa-solid fa-star" style="color: #ffc107;"></i>'''

js = js.replace(old_star_js, star_svg)

with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Icons replaced with inline SVGs!")
