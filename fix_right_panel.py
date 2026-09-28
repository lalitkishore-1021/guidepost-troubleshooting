import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Right panel fake stats
    html = re.sub(r'<span style="font-weight:600; color:#2E7D32;">84\.2%</span>', '<span style="font-weight:600; color:#2E7D32;">--</span>', html)
    html = re.sub(r'<span style="font-weight:600;">\$0\.0012</span>', '<span style="font-weight:600;">--</span>', html)
    html = re.sub(r'<span style="font-weight:600;">100%</span>', '<span style="font-weight:600;">--</span>', html)
    
    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Right panel stats neutered.")

if __name__ == '__main__':
    main()
