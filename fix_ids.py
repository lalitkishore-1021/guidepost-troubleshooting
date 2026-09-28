import re

def main():
    with open('revert_ui_features.py', 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace("globalQueryInput", "queryInput")
    content = content.replace("executeSearch()", "runAppSearch()")

    with open('revert_ui_features.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed IDs in python script.")

if __name__ == '__main__':
    main()
