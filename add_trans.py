import json
import re

with open('static/translations.js', 'r', encoding='utf-8') as f:
    content = f.read()

ru_additions = '''
        "t_vampire_title": "Кровавая",
        "t_vampire_desc": "Тьма и Кровь",
        "t_ocean_title": "Океан",
        "t_ocean_desc": "Глубина Неона",
        "t_hacked_title": "HACKED",
        "t_hacked_desc": "Только Owner",
        "t_adv_settings": "Дополнительные функции",
        "t_anim_toggle": "Анимации интерфейса",
        "t_particles_toggle": "Частицы на фоне",
'''

en_additions = '''
        "t_vampire_title": "Vampire",
        "t_vampire_desc": "Dark & Blood",
        "t_ocean_title": "Ocean",
        "t_ocean_desc": "Deep Neon",
        "t_hacked_title": "HACKED",
        "t_hacked_desc": "Owner Only",
        "t_adv_settings": "Advanced Settings",
        "t_anim_toggle": "UI Animations",
        "t_particles_toggle": "Background Particles",
'''

# Insert after t_85
content = content.replace('"t_85": "Токсичный Неон",', '"t_85": "Токсичный Неон",' + ru_additions)
content = content.replace('"t_85": "Toxic Neon",', '"t_85": "Toxic Neon",' + en_additions)

with open('static/translations.js', 'w', encoding='utf-8') as f:
    f.write(content)
