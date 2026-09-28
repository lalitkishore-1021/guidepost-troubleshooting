import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace the Analytics branch to include Trust Suite, Eval Lab, and neuter Analytics
    old_switch = r"\} else if \(tabName === 'Analytics'\) \{\s*renderAnalyticsDashboard\(\);\s*\}"
    new_switch = r"""} else if (tabName === 'Trust Suite' || tabName === 'Eval Lab') {
                document.getElementById('topUI').style.display = 'none'; document.getElementById('heroSection').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = tabName;
                document.getElementById('results').innerHTML = `<div class="card" style="padding:40px; text-align:center;">
                    <i class='bx bx-shield-quarter' style="font-size:48px; color:#64748B; margin-bottom:15px;"></i>
                    <h3 style="margin-bottom:10px;">Evaluation Data Unavailable</h3>
                    <p style="color:#666; font-size:14px;">The backend evaluation APIs have not been exposed yet. Metrics are not measured.</p>
                </div>`;
            } else if (tabName === 'Analytics') {
                document.getElementById('topUI').style.display = 'none'; document.getElementById('heroSection').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Analytics Dashboard`;
                document.getElementById('results').innerHTML = `<div class="card" style="padding:40px; text-align:center;">
                    <i class='bx bx-bar-chart-alt-2' style="font-size:48px; color:#64748B; margin-bottom:15px;"></i>
                    <h3 style="margin-bottom:10px;">Analytics Data Unavailable</h3>
                    <p style="color:#666; font-size:14px;">No live data available.</p>
                </div>`;
            }"""
    html = re.sub(old_switch, new_switch, html)

    # Completely remove function renderAnalyticsDashboard() { ... }
    # Because it is very long and has nested brackets, we will use a regex that goes from function renderAnalyticsDashboard() { up to just before // Anti-Sleep Ping & Health Indicator
    old_func = r"function renderAnalyticsDashboard\(\) \{.*?// Anti-Sleep Ping & Health Indicator"
    html = re.sub(old_func, "// Anti-Sleep Ping & Health Indicator", html, flags=re.DOTALL)

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Fixed switchTab branches and removed renderAnalyticsDashboard.")

if __name__ == '__main__':
    main()
