import re

def main():
    with open('original_utf8.html', 'r', encoding='utf-8') as f:
        orig = f.read()

    match = re.search(r"function renderAnalyticsDashboard\(\) \{.*?// Anti-Sleep Ping & Health Indicator", orig, re.DOTALL)
    if not match:
        print("Could not find renderAnalyticsDashboard")
        return
        
    func_text = match.group(0)
    func_text = func_text.replace("// Anti-Sleep Ping & Health Indicator", "")
    
    # NEUTER THE FAKE METRICS
    func_text = re.sub(r'99\.2%', '--', func_text)
    func_text = re.sub(r'97\.8%', '--', func_text)
    func_text = re.sub(r'94\.2%', '--', func_text)
    func_text = re.sub(r'18 ms', '--', func_text)
    func_text = re.sub(r'\$0\.0012', '--', func_text)
    func_text = re.sub(r'\$0\.001', '--', func_text)
    func_text = re.sub(r'100%<br><span style="font-size:11px; color:#888;">Perfect</span>', '--', func_text)
    
    # Sub-text in matrix cards
    func_text = re.sub(r"<i class='bx bx-up-arrow-alt'></i> 0\.4% vs last", "Not measured", func_text)
    func_text = re.sub(r"<i class='bx bx-up-arrow-alt'></i> 1\.2%", "Not measured", func_text)
    func_text = re.sub(r"<i class='bx bx-up-arrow-alt'></i> 2\.1%", "Not measured", func_text)
    func_text = re.sub(r"<i class='bx bx-down-arrow-alt'></i> 4ms", "Not measured", func_text)
    func_text = re.sub(r"\+ 12%", "Not measured", func_text)
    func_text = re.sub(r'100%</div>', '--</div>', func_text)
    func_text = re.sub(r'<i class=\'bx bx-check\'></i> Perfect', 'Not measured', func_text)
    
    # Right panel fake stats
    func_text = re.sub(r'84\.2%', '--', func_text)
    func_text = re.sub(r'1,240 ms', '--', func_text)
    
    # Eval table rows
    func_text = re.sub(r'<td>96\.1%</td>', '<td>--</td>', func_text)
    func_text = re.sub(r'<td>92\.4%</td>', '<td>--</td>', func_text)
    func_text = re.sub(r'<td>420 ms</td>', '<td>--</td>', func_text)
    func_text = re.sub(r'<td>41\.5%</td>', '<td>--</td>', func_text)
    
    func_text = re.sub(r'<td>98\.5%</td>', '<td>--</td>', func_text)
    func_text = re.sub(r'<td>95\.2%</td>', '<td>--</td>', func_text)
    func_text = re.sub(r'<td>24 ms</td>', '<td>--</td>', func_text)
    func_text = re.sub(r'<td>88\.9%</td>', '<td>--</td>', func_text)
    func_text = re.sub(r'<td>99\.9%</td>', '<td>--</td>', func_text)
    func_text = re.sub(r'<td>100%</td>', '<td>--</td>', func_text)
    
    # Alerts inside renderAnalyticsDashboard
    func_text = func_text.replace("alert('Exporting latency logs as CSV...')", "alertUnavailable('Export API not connected')")
    func_text = func_text.replace("alert('Flushing FAISS cache...')", "alertUnavailable('Flush API not connected')")
    func_text = func_text.replace("alert('Deploying v2.5 to Staging...')", "alertUnavailable('Deploy API not connected')")
    
    with open('web/index.html', 'r', encoding='utf-8') as f:
        curr = f.read()

    # The current switchTab for Eval and Trust is:
    # } else if (tabName === 'Trust Suite' || tabName === 'Eval Lab') { ... } else if (tabName === 'Analytics') { ... }
    # We will replace that whole block with:
    # } else if (tabName === 'Trust Suite' || tabName === 'Eval Lab' || tabName === 'Analytics') { renderAnalyticsDashboard(); }
    
    old_switch = r"\} else if \(tabName === 'Trust Suite' \|\| tabName === 'Eval Lab'\) \{.*?\} else if \(tabName === 'Analytics'\) \{.*?\}"
    new_switch = r"""} else if (tabName === 'Trust Suite' || tabName === 'Eval Lab' || tabName === 'Analytics') {
                renderAnalyticsDashboard();
            }"""
            
    curr = re.sub(old_switch, new_switch, curr, flags=re.DOTALL)
    
    curr = curr.replace("// Anti-Sleep Ping & Health Indicator", func_text + "\n\n        // Anti-Sleep Ping & Health Indicator")
    
    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(curr)

    print("Successfully restored and neutered analytics dashboard.")

if __name__ == '__main__':
    main()
