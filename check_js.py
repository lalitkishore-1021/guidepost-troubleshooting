import re
import subprocess

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    scripts = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)
    
    if scripts:
        with open('temp.js', 'w', encoding='utf-8') as f:
            f.write(scripts[0])
            
        print("Wrote temp.js, now checking syntax...")
        result = subprocess.run(['node', '-c', 'temp.js'], capture_output=True, text=True)
        if result.returncode != 0:
            print("SYNTAX ERROR:")
            print(result.stderr)
        else:
            print("Syntax is OK.")
    else:
        print("No script tags found.")

if __name__ == '__main__':
    main()
