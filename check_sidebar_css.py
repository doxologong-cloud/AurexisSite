html = open('C:/Users/user/Desktop/сайт/templates/vault.html', encoding='utf-8').read()
start = html.find('.sidebar {')
print(html[max(0, start-100):start+1000])
