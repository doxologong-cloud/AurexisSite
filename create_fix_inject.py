with open('inject_api.py', 'r', encoding='utf-8') as f:
    script_text = f.read()

script_text = script_text.replace('if __name__ == "__main__":', "if __name__ == '__main__':")

with open('fix_inject_api.py', 'w', encoding='utf-8') as f:
    f.write(script_text)
