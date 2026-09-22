import re

def main():
    # 1. Read existing HTML
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 2. Extract script block
    script_match = re.search(r'<script>(.*?)</script>', html_content, re.DOTALL)
    if not script_match:
        print("Failed to find script")
        return
    js = script_match.group(1)

    # 3. Rewrite renderDefaultState
    old_default = r'html \+= `<div class="card" style="cursor:pointer; border: 1px solid transparent;" onmouseover="this\.style\.borderColor=\'#CCC\'" onmouseout="this\.style\.borderColor=\'transparent\'" onclick="fillAndSearch\(\'\$\{qSafe\}\'\)">.*?</div>`;'
    
    new_default = r"""
                    let iconBg = '#E8F5E9'; let iconCol = '#2E7D32'; let iconClass = 'bx-check-shield';
                    if(cat === 'manual') { iconBg = '#E3F2FD'; iconCol = '#1565C0'; iconClass = 'bx-download'; }
                    if(cat === 'critical') { iconBg = '#FFEbee'; iconCol = '#D32F2F'; iconClass = 'bx-reset'; }
                    
                    html += `<div class="card" style="background:white; border-radius:20px; padding:20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                            <span class="tag ${cat}" style="text-transform:capitalize; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600; background:${iconBg}; color:${iconCol};"><i class='bx bx-bolt-circle'></i> ${cat}</span>
                            <div style="display:flex; align-items:center; gap:10px; color:#888;">
                                <span style="font-size:11px;">Recently</span>
                                <i class='bx bx-dots-vertical-rounded' style="cursor:pointer;"></i>
                            </div>
                        </div>
                        <div style="display:flex; gap:15px; margin-bottom:20px;">
                            <div style="width:40px; height:40px; border-radius:50%; background:${iconBg}; color:${iconCol}; display:flex; justify-content:center; align-items:center; font-size:20px; flex-shrink:0;"><i class='bx ${iconClass}'></i></div>
                            <div>
                                <div style="font-size:15px; font-weight:700; margin-bottom:4px;">${rq.actionName}</div>
                                <div style="font-size:13px; color:#666; line-height:1.4;">${rq.description}</div>
                            </div>
                        </div>
                        <div style="display:flex; justify-content:flex-end;">
                            <button style="background:transparent; border:none; font-size:13px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:5px;" onclick="fillAndSearch('${qSafe}')">Re-run Search <i class='bx bx-right-arrow-alt'></i></button>
                        </div>
                    </div>`;
"""
    js = re.sub(old_default, new_default.strip(), js, flags=re.DOTALL)

    # 4. Modify the hardcoded fallback cards in renderDefaultState to match the design too
    old_fallback = r'resultsDiv\.innerHTML = `\s*<div class="card">.*?</div>\s*`;'
    new_fallback = r"""
            resultsDiv.innerHTML = `
                <div class="card" style="background:white; border-radius:20px; padding:20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                        <span class="tag auto" style="text-transform:capitalize; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600; background:#E8F5E9; color:#2E7D32;"><i class='bx bx-bolt-circle'></i> Auto</span>
                        <div style="display:flex; align-items:center; gap:10px; color:#888;">
                            <span style="font-size:11px;">2 mins ago</span>
                            <i class='bx bx-dots-vertical-rounded' style="cursor:pointer;"></i>
                        </div>
                    </div>
                    <div style="display:flex; gap:15px; margin-bottom:20px;">
                        <div style="width:40px; height:40px; border-radius:50%; background:#E8F5E9; color:#2E7D32; display:flex; justify-content:center; align-items:center; font-size:20px; flex-shrink:0;"><i class='bx bx-camera'></i></div>
                        <div>
                            <div style="font-size:15px; font-weight:700; margin-bottom:4px;">Reset Camera Settings</div>
                            <div style="font-size:13px; color:#666; line-height:1.4;">It will restore default camera configurations.</div>
                        </div>
                    </div>
                    <div style="display:flex; justify-content:flex-end;">
                        <button style="background:transparent; border:none; font-size:13px; font-weight:600; cursor:pointer; display:flex; align-items:center; gap:5px;" onclick="fillAndSearch('camera')">Re-run Search <i class='bx bx-right-arrow-alt'></i></button>
                    </div>
                </div>
            `;
    """
    js = re.sub(old_fallback, new_fallback.strip(), js, flags=re.DOTALL)

    # 5. Fix Clear History button layout
    js = js.replace(
        """<button class="launch-btn" style="margin-left:auto;" onclick="localStorage.removeItem('guidepost_recent'); location.reload();">Clear History</button>""",
        """<button class="launch-btn" style="margin-left:auto; background:white; color:#111; border:1px solid #DDD; padding:6px 14px; border-radius:20px; cursor:pointer; font-size:12px; display:flex; align-items:center; gap:5px;" onclick="localStorage.removeItem('guidepost_recent'); location.reload();"><i class='bx bx-trash'></i> Clear History</button>"""
    )
    
    # Also adjust the mainTitle to just say "Recent Queries" and the badge separately.
    js = js.replace('Recent Queries <span class="badge-count">${recentQueries.length}</span>', 'Recent Queries <span class="badge-count" style="background:#111; color:white; padding:2px 8px; border-radius:12px; font-size:12px; margin-left:8px;">${recentQueries.length}</span>')

    # Now define the full new HTML frame
    full_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guidepost Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-color: #F8F6F0; --sidebar-bg: #1E1F22; --card-bg: #FFFFFF;
            --text-main: #111111; --text-muted: #666666;
            --tag-auto: #DCEE77; --tag-manual: #698BFF; --tag-critical: #FFB3B3;
            --chart-dark: #1E1F22;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); height: 100vh; display: flex; overflow: hidden; padding: 10px; }

        /* Sidebar */
        .sidebar { background-color: var(--sidebar-bg); width: 90px; border-radius: 30px; display: flex; flex-direction: column; align-items: center; padding: 30px 0; gap: 15px; flex-shrink: 0; justify-content: flex-start; height: 100%; box-shadow: 4px 0 20px rgba(0,0,0,0.05); }
        .logo { color: #8ED58E; font-weight: 800; font-size: 28px; margin-bottom: 20px; }
        .nav-item { color: #888; display: flex; flex-direction: column; align-items: center; gap: 4px; cursor: pointer; transition: all 0.3s ease; padding: 12px 10px; border-radius: 20px; width: 70px; }
        .nav-item i { font-size: 22px; }
        .nav-item span { font-size: 10px; font-weight: 500; }
        .nav-item:hover { color: #FFF; background: rgba(255,255,255,0.05); }
        .nav-item.active { color: #8ED58E; background: #2B3B2B; }
        
        /* Main Content */
        .main-wrapper { flex-grow: 1; display: flex; flex-direction: column; overflow-y: auto; padding: 10px 30px; }
        
        /* Header */
        .header { display: flex; align-items: center; justify-content: space-between; gap: 20px; width: 100%; margin-bottom: 20px; }
        .search-container { flex-grow: 1; max-width: 800px; }
        .search-bar { background: var(--card-bg); border-radius: 40px; display: flex; align-items: center; padding: 6px 6px 6px 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
        .search-bar i { color: #888; font-size: 20px; margin-right: 10px; flex-shrink: 0;}
        .search-bar input { border: none; outline: none; width: 100%; font-size: 15px; background: transparent; padding: 10px 0; }
        .search-btn { background: #1E1F22; color: white; border: none; border-radius: 30px; padding: 10px 24px; font-weight: 500; cursor: pointer; transition: 0.2s; flex-shrink: 0;}
        
        .header-actions { display: flex; align-items: center; gap: 20px; }
        .btn-dark { background: #1E1F22; color: white; border: none; padding: 10px 20px; border-radius: 30px; font-size: 14px; font-weight: 500; cursor: pointer; display: flex; align-items: center; gap: 8px; }
        
        /* Hero */
        .hero { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .hero-title { font-size: 42px; font-weight: 700; color: #111; margin-bottom: 8px; }
        .hero-title span { color: #107C41; }
        .hero-stat { background: white; padding: 20px; border-radius: 20px; width: 140px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); display: flex; flex-direction: column; align-items: center; text-align: center; }
        
        /* Cards */
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .card { background: var(--card-bg); border-radius: 20px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }

        /* Right Panel */
        .right-panel { width: 340px; display: flex; flex-direction: column; gap: 20px; flex-shrink: 0; overflow-y: auto; padding-top: 10px; padding-right: 10px;}
        .widget { background: white; border-radius: 20px; padding: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); }
        .widget-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .widget-header h3 { font-size: 16px; font-weight: 600; }
        
        /* Quick Actions */
        .quick-actions { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .quick-action-btn { background: #F8F9FA; border: none; border-radius: 12px; padding: 12px; display: flex; align-items: center; gap: 10px; cursor: pointer; text-align: left; }
        .quick-action-btn:hover { background: #EEE; }

        /* Donut */
        .donut-wrapper { position: relative; width: 150px; height: 150px; margin: 0 auto; display: flex; justify-content: center; align-items: center; }
        .donut { width: 100%; height: 100%; border-radius: 50%; background: conic-gradient(#DCEE77 0% 32%, #698BFF 32% 60%, #82CDB3 60% 82%, #7A73AB 82% 100%); }
        .donut-center { position: absolute; width: 90px; height: 90px; background: white; border-radius: 50%; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .donut-center h2 { color: #111; font-size: 24px; margin: 0; font-weight: 700; }
        .donut-center p { color: #888; font-size: 11px; margin: 0; }
        .legend { display: flex; justify-content: space-between; margin-top: 20px; font-size: 11px; color: #555; }
        .legend div { display: flex; align-items: center; gap: 4px; }
        .dot { width: 8px; height: 8px; border-radius: 50%; }
        
        /* Utils */
        .suggested-queries { display: flex; gap: 8px; align-items: center; font-size: 12px; margin-top: 15px; margin-bottom: 25px; flex-wrap: wrap;}
        .suggested-queries span { color: #888; font-weight:500; }
        .suggestion-chip { background: white; border-radius: 20px; padding: 6px 12px; cursor: pointer; border: 1px solid #E0E0E0; transition: 0.2s; font-weight:500;}
        .suggestion-chip:hover { border-color: #888; background: #F8F9FA;}
        
        #jsonContent { display: none; background: #1E1F22; color: #D4D4D4; padding: 40px 20px 20px 20px; border-radius: 20px; font-family: monospace; font-size: 13px; overflow-x: auto; white-space: pre-wrap; position: relative;}
        
        .view-tabs { display: flex; gap: 10px; margin-bottom: 15px;}
        .view-tab { background: transparent; border: 1px solid #DDD; padding: 6px 16px; border-radius: 20px; font-size: 13px; font-weight: 500; cursor: pointer; transition: 0.2s;}
        .view-tab.active { background: var(--sidebar-bg); color: white; border-color: var(--sidebar-bg); }
        
        .meta-strip { background: var(--card-bg); border-radius: 12px; padding: 12px 20px; display: flex; gap: 20px; font-size: 12px; color: #555; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.02); flex-wrap: wrap; align-items: center;}
        
        .query-variations { background: #F8F9FA; border-radius: 12px; padding: 12px 20px; font-size: 12px; color: #555; margin-bottom: 20px;}
        .query-variations summary { font-weight: 600; cursor: pointer; outline: none; }
        .query-variations ul { margin-top: 10px; padding-left: 20px; }
        .query-variations li { margin-bottom: 4px; }
        .launch-btn { background: transparent; border: 1px solid #DDD; padding: 6px 12px; border-radius: 15px; font-size: 12px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .launch-btn:hover { background: var(--sidebar-bg); color: white; border-color: var(--sidebar-bg); }
        
        .tag { font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 12px; color: #111; text-transform: capitalize; }
        .tag.auto { background: var(--tag-auto); }
        .tag.manual { background: var(--tag-manual); color: white; }
        .tag.critical { background: var(--tag-critical); }

        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #DDD; border-radius: 10px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo">G</div>
        <div class="nav-item active" onclick="switchTab(this, 'Home')">
            <i class='bx bxs-home' ></i>
            <span>Home</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Library')">
            <i class='bx bx-collection' ></i>
            <span>Library</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Analytics')">
            <i class='bx bx-bar-chart-alt-2' ></i>
            <span>Analytics</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Agent Console')">
            <i class='bx bx-user' ></i>
            <span>Users</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Settings')">
            <i class='bx bx-cog' ></i>
            <span>Settings</span>
        </div>
    </div>

    <div class="main-wrapper">
        <div class="header">
            <div class="search-container">
                <div class="search-bar">
                    <i class='bx bx-search'></i>
                    <input type="text" id="queryInput" placeholder="Describe issue (e.g. Battery drains fast)..." />
                    <button class="search-btn" onclick="runAppSearch()">Search</button>
                </div>
                <div class="suggested-queries">
                    <span>Try:</span>
                    <div class="suggestion-chip" onclick="fillAndSearch('My battery dies really fast')">Battery drains fast</div>
                    <div class="suggestion-chip" onclick="fillAndSearch('Cannot connect to Wi-Fi')">Wi-Fi drops</div>
                    <div class="suggestion-chip" onclick="fillAndSearch('Screen is completely frozen')">Screen frozen</div>
                    <div class="suggestion-chip" onclick="fillAndSearch('Camera is blurry')">Camera blurry</div>
                    <div class="suggestion-chip" onclick="fillAndSearch('Bluetooth issue')">Bluetooth issue</div>
                    <div class="suggestion-chip" onclick="fillAndSearch('Overheating')">Overheating</div>
                </div>
            </div>
            
            <div class="header-actions">
                <button class="btn-dark" onclick="runAppSearch()">
                    <i class='bx bx-sparkles'></i> Generate Guide
                </button>
                <div style="background:white; padding:8px 16px; border-radius:30px; display:flex; align-items:center; gap:8px; box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                    <div id="healthDot" style="width:8px; height:8px; border-radius:50%; background:#FFB3B3;"></div>
                    <span id="healthText" style="font-size:12px; font-weight:600;">API Starting...</span>
                </div>
                <div style="position:relative; cursor:pointer; background:white; width:40px; height:40px; border-radius:50%; display:flex; justify-content:center; align-items:center; box-shadow:0 2px 10px rgba(0,0,0,0.02);">
                    <i class='bx bx-bell' style="font-size:20px; color:#555;"></i>
                    <div style="position:absolute; top:10px; right:12px; width:6px; height:6px; background:red; border-radius:50%;"></div>
                </div>
                <div style="display:flex; align-items:center; gap:10px; cursor:pointer;">
                    <div style="width:36px; height:36px; background:#1E1F22; border-radius:50%; display:flex; justify-content:center; align-items:center; color:white;"><i class='bx bx-user'></i></div>
                    <span style="font-weight:600; font-size:14px; color:#111;">Team Member</span>
                    <i class='bx bx-chevron-down' style="color:#888;"></i>
                </div>
            </div>
        </div>
        
        <div id="heroSection" class="hero">
            <div>
                <div style="color:#666; font-weight:500; margin-bottom:8px;">Welcome back!</div>
                <div class="hero-title">Find a fix. <span>In seconds.</span></div>
                <div style="color:#666; font-size:15px;">Describe your issue in natural language and get step-by-step guidance.</div>
            </div>
            <div style="display:flex; gap:15px;">
                <div class="hero-stat">
                    <div style="background:#E8F5E9; color:#2E7D32; width:40px; height:40px; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size:20px; margin-bottom:12px;"><i class='bx bx-file'></i></div>
                    <div style="font-size:24px; font-weight:700;">273</div>
                    <div style="font-size:11px; color:#666;">Total Resolutions</div>
                </div>
                <div class="hero-stat">
                    <div style="background:#E3F2FD; color:#1565C0; width:40px; height:40px; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size:20px; margin-bottom:12px;"><i class='bx bx-group'></i></div>
                    <div style="font-size:24px; font-weight:700;">12,450</div>
                    <div style="font-size:11px; color:#666;">Users Assisted</div>
                </div>
                <div class="hero-stat">
                    <div style="background:#F3E5F5; color:#7B1FA2; width:40px; height:40px; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size:20px; margin-bottom:12px;"><i class='bx bx-trending-up'></i></div>
                    <div style="font-size:24px; font-weight:700;">98%</div>
                    <div style="font-size:11px; color:#666;">Success Rate</div>
                </div>
            </div>
        </div>

        <div id="contentArea">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;">
                <div class="section-title" id="mainTitle" style="font-size:20px; font-weight:700; display:flex; align-items:center;">Recent Queries</div>
            </div>
            <div id="topUI"></div>
            <div id="guideContent">
                <div class="cards-grid" id="results"></div>
            </div>
            <pre id="jsonContent"></pre>
        </div>
    </div>

    <div class="right-panel">
        <div class="widget">
            <div class="widget-header">
                <h3>Resolution Types</h3>
                <span style="font-size:12px; color:#888; display:flex; align-items:center; gap:4px;"><i class='bx bx-calendar'></i> All time <i class='bx bx-chevron-down'></i></span>
            </div>
            <div class="donut-wrapper">
                <div class="donut" id="cssDonut"></div>
                <div class="donut-center">
                    <h2 id="totalActions">273</h2>
                    <p>Total</p>
                </div>
            </div>
            <div class="legend">
                <div><div class="dot" style="background:#DCEE77;"></div> Auto <span style="font-weight:700; color:#111; margin-left:10px;">32%</span></div>
                <div><div class="dot" style="background:#698BFF;"></div> Manual <span style="font-weight:700; color:#111; margin-left:10px;">28%</span></div>
                <div><div class="dot" style="background:#82CDB3;"></div> Critical <span style="font-weight:700; color:#111; margin-left:10px;">22%</span></div>
                <div><div class="dot" style="background:#7A73AB;"></div> Other <span style="font-weight:700; color:#111; margin-left:10px;">18%</span></div>
            </div>
        </div>

        <div class="widget">
            <div class="widget-header">
                <h3>System Eval Stats</h3>
                <span style="font-size:12px; color:#888; display:flex; align-items:center; gap:4px;"><i class='bx bx-calendar'></i> Last Eval <i class='bx bx-chevron-down'></i></span>
            </div>
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:5px;">
                <div style="background:#E8F5E9; color:#2E7D32; width:30px; height:30px; border-radius:50%; display:flex; justify-content:center; align-items:center;"><i class='bx bx-target-lock'></i></div>
                <div style="font-size: 20px; font-weight:700;">Target Met</div>
            </div>
            <div style="font-size:12px; color:#888; margin-bottom:20px; margin-left:40px;">Measured on Node-01 (Prod)</div>
            
            <div style="display:flex; flex-direction:column; gap:12px;">
                <div style="display:flex; justify-content:space-between; font-size:13px;">
                    <span style="color:#666;">Cache Hit Rate</span>
                    <span style="font-weight:600; color:#2E7D32;">84.2%</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:13px;">
                    <span style="color:#666;">P95 Latency</span>
                    <span style="font-weight:600;">1,240 ms</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:13px;">
                    <span style="color:#666;">Avg Cost/Query</span>
                    <span style="font-weight:600;">$0.0012</span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:13px;">
                    <span style="color:#666;">Schema-Valid %</span>
                    <span style="font-weight:600; color:#2E7D32;">100%</span>
                </div>
            </div>
            
            <button style="width:100%; margin-top:20px; background:transparent; border:1px solid #DDD; padding:10px; border-radius:10px; cursor:pointer; font-weight:600; display:flex; align-items:center; justify-content:center; gap:8px;" onclick="alert('Running Trust Suite adversarial tests...')"><i class='bx bx-test-tube'></i> Run Trust Suite Tests</button>
        </div>

        <div style="margin-top:10px;">
            <h3 style="font-size:16px; font-weight:600; margin-bottom:15px;">Quick Actions</h3>
            <div class="quick-actions">
                <button class="quick-action-btn" onclick="document.getElementById('queryInput').focus()">
                    <div style="background:#E3F2FD; color:#1565C0; padding:8px; border-radius:8px;"><i class='bx bx-file'></i></div>
                    <div>
                        <div style="font-weight:600; font-size:12px;">Generate Guide</div>
                        <div style="font-size:10px; color:#888;">Create new guide</div>
                    </div>
                </button>
                <button class="quick-action-btn" onclick="switchTab(document.querySelector('.sidebar .nav-item:nth-child(3)'), 'Library')">
                    <div style="background:#E8F5E9; color:#2E7D32; padding:8px; border-radius:8px;"><i class='bx bx-book-open'></i></div>
                    <div>
                        <div style="font-weight:600; font-size:12px;">Browse Library</div>
                        <div style="font-size:10px; color:#888;">Knowledge base</div>
                    </div>
                </button>
                <button class="quick-action-btn" onclick="switchTab(document.querySelector('.sidebar .nav-item:nth-child(4)'), 'Analytics')">
                    <div style="background:#F3E5F5; color:#7B1FA2; padding:8px; border-radius:8px;"><i class='bx bx-bar-chart-alt-2'></i></div>
                    <div>
                        <div style="font-weight:600; font-size:12px;">View Analytics</div>
                        <div style="font-size:10px; color:#888;">Check usage</div>
                    </div>
                </button>
                <button class="quick-action-btn" onclick="switchTab(document.querySelector('.sidebar .nav-item:nth-child(6)'), 'Settings')">
                    <div style="background:#F5F5F5; color:#555; padding:8px; border-radius:8px;"><i class='bx bx-cog'></i></div>
                    <div>
                        <div style="font-weight:600; font-size:12px;">Manage Settings</div>
                        <div style="font-size:10px; color:#888;">Preferences</div>
                    </div>
                </button>
            </div>
        </div>
    </div>

    <script>
""" + js + """
    </script>
</body>
</html>"""

    # 6. Update the checkApiHealth to change the background dot
    full_html = full_html.replace('document.getElementById("healthDot").className = "status-dot green";', 'document.getElementById("healthDot").style.background = "#2E7D32";')
    full_html = full_html.replace('document.getElementById("healthDot").className = "status-dot red";', 'document.getElementById("healthDot").style.background = "#D32F2F";')

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("Successfully replaced index.html with new Apple-style UI.")

if __name__ == '__main__':
    main()
