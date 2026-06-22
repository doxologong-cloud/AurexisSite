import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

new_support = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>'
new_economy = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 13L2 9Z"></path><path d="M11 3 8 9l4 13"></path><path d="M12 15V3"></path></svg>'
new_mafia = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 10h.01"></path><path d="M15 10h.01"></path><path d="M12 2a8 8 0 0 0-8 8v12l3-3 2.5 2.5L12 19l2.5 2.5L17 19l3 3V10a8 8 0 0 0-8-8z"></path></svg>'
new_flora = '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"></path></svg>'

# We use regex to find the .bot-icon div and replace its content
text = re.sub(r'<div class="bot-icon support-icon".*?>\s*<svg.*?</svg>\s*</div>', f'<div class="bot-icon support-icon" style="display:flex; justify-content:center; align-items:center; color: var(--neon-primary);">\n{new_support}\n</div>', text, flags=re.DOTALL)
text = re.sub(r'<div class="bot-icon games-icon".*?>\s*<svg.*?</svg>\s*</div>', f'<div class="bot-icon games-icon" style="display:flex; justify-content:center; align-items:center; color: var(--neon-secondary);">\n{new_economy}\n</div>', text, flags=re.DOTALL)
text = re.sub(r'<div class="bot-icon mafia-icon".*?>\s*<svg.*?</svg>\s*</div>', f'<div class="bot-icon mafia-icon" style="display:flex; justify-content:center; align-items:center; color: #ff4444;">\n{new_mafia}\n</div>', text, flags=re.DOTALL)
text = re.sub(r'<div class="bot-icon flora-icon".*?>\s*<svg.*?</svg>\s*</div>', f'<div class="bot-icon flora-icon" style="display:flex; justify-content:center; align-items:center; color: var(--neon-green);">\n{new_flora}\n</div>', text, flags=re.DOTALL)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated bot shop icons!')
