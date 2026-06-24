html = open('C:/Users/user/Desktop/сайт/templates/vault.html', encoding='utf-8').read()
start = html.find('default-avatar.png')
print(html[max(0, start-300):start+300])
