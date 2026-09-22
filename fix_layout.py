import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Make sure we reset the class at the start of switchTab
    old_switch = r"function switchTab\(element, tabName\) \{(.*?)(if\(tabName === 'Home'\))"
    new_switch = r"function switchTab(element, tabName) {\1document.getElementById('results').className = 'cards-grid';\n            \2"
    
    content = re.sub(old_switch, new_switch, content, flags=re.DOTALL)

    # Now inside specific tabs that need full width, clear the class
    
    # 1. Agent Console
    content = content.replace(
        "document.getElementById('mainTitle').innerHTML = `Support Agent Console <span class=\"badge-count\">Live Queue</span>`;",
        "document.getElementById('mainTitle').innerHTML = `Support Agent Console <span class=\"badge-count\">Live Queue</span>`;\n                document.getElementById('results').className = '';"
    )

    # 2. Analytics Dashboard
    content = content.replace(
        "function renderAnalyticsDashboard() {",
        "function renderAnalyticsDashboard() {\n            document.getElementById('results').className = '';"
    )

    # Let's also ensure renderCards (when a search happens) sets cards-grid in case they searched from somewhere else (though usually they do it from Home)
    content = content.replace(
        "function renderCards(data) {",
        "function renderCards(data) {\n            document.getElementById('results').className = 'cards-grid';"
    )

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed layout overlap by managing cards-grid class.")

if __name__ == '__main__':
    main()
