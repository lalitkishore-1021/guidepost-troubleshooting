import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Resolution by Category
    html = re.sub(r'<span style="font-weight:700; color:#111; margin-left:10px;">32%</span>', '<span style="font-weight:700; color:#111; margin-left:10px;">--</span>', html)
    html = re.sub(r'<span style="font-weight:700; color:#111; margin-left:10px;">28%</span>', '<span style="font-weight:700; color:#111; margin-left:10px;">--</span>', html)
    html = re.sub(r'<span style="font-weight:700; color:#111; margin-left:10px;">22%</span>', '<span style="font-weight:700; color:#111; margin-left:10px;">--</span>', html)
    html = re.sub(r'<span style="font-weight:700; color:#111; margin-left:10px;">18%</span>', '<span style="font-weight:700; color:#111; margin-left:10px;">--</span>', html)

    # Resolution by Team
    html = re.sub(r'<span style="font-weight:600; color:#1565C0;">64%</span>', '<span style="font-weight:600; color:#1565C0;">--</span>', html)
    html = re.sub(r'<span style="font-weight:600; color:#2E7D32;">21%</span>', '<span style="font-weight:600; color:#2E7D32;">--</span>', html)
    html = re.sub(r'<span style="font-weight:600; color:#E65100;">11%</span>', '<span style="font-weight:600; color:#E65100;">--</span>', html)
    html = re.sub(r'<span style="font-weight:600; color:#D32F2F;">4%</span>', '<span style="font-weight:600; color:#D32F2F;">--</span>', html)
    
    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Right panel percentages neutered.")

if __name__ == '__main__':
    main()
