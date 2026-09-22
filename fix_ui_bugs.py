import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add .badge-count to CSS
    if '.badge-count' not in content:
        content = content.replace("::-webkit-scrollbar { width: 5px; }", ".badge-count { background:#111; color:white; padding:4px 10px; border-radius:12px; font-size:12px; margin-left:12px; vertical-align: middle; }\n        ::-webkit-scrollbar { width: 5px; }")

    # 2. Fix the switchTab javascript bug where nav-icon wasn't changed to nav-item
    content = content.replace("document.querySelectorAll('.nav-icon')", "document.querySelectorAll('.nav-item')")
    content = content.replace("const activeTab = document.querySelector('.nav-icon.active');", "const activeTab = document.querySelector('.nav-item.active');")

    # 3. Rewrite Sidebar HTML to replace Library with Agent Console
    old_sidebar = r'<div class="sidebar">.*?</div>\s*<div class="main-wrapper">'
    new_sidebar = r"""<div class="sidebar">
        <div class="logo">G</div>
        <div class="nav-item active" onclick="switchTab(this, 'Home')">
            <i class='bx bxs-home' ></i>
            <span>Home</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Agent Console')">
            <i class='bx bx-support' ></i>
            <span>Support</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Categories')">
            <i class='bx bx-grid-alt' ></i>
            <span>Categories</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Analytics')">
            <i class='bx bx-bar-chart-alt-2' ></i>
            <span>Analytics</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Team')">
            <i class='bx bx-user' ></i>
            <span>Team</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Settings')">
            <i class='bx bx-cog' ></i>
            <span>Settings</span>
        </div>
    </div>
    
    <div class="main-wrapper">"""
    
    content = re.sub(old_sidebar, new_sidebar, content, flags=re.DOTALL)

    # 4. Improve Agent Console UI
    # Replace the HTML generated in switchTab for 'Agent Console'
    old_agent_console = r"document\.getElementById\('results'\)\.innerHTML = `\s*<div style=\"display:flex; gap:30px; width:100%; align-items: flex-start;\">.*?</div>\s*</div>\s*`;"
    new_agent_console = r"""document.getElementById('results').innerHTML = `
                    <div style="display:flex; gap:30px; width:100%; align-items: stretch;">
                        <div style="flex:1; display:flex; flex-direction:column; gap:12px; min-width: 250px; max-width: 320px;">
                            <h4 style="font-size: 14px; color: #888; margin-bottom: 5px;">Active Queue (2)</h4>
                            <div class="card ticket-card" style="border-left: 4px solid #DCEE77; cursor:pointer; padding: 15px;" onclick="selectTicket(this, 8921)">
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                                    <span style="font-size:12px; font-weight:600; color:#555;">#8921</span>
                                    <span style="font-size:11px; background:#FFE2E2; color:#D32F2F; padding:2px 6px; border-radius:10px;">High Priority</span>
                                </div>
                                <div style="font-size:12px; color:#888; margin-bottom:4px;"><i class='bx bx-user'></i> John D.</div>
                                <div class="card-title" style="font-size: 14px; line-height:1.4;">"My battery is dying so fast since update"</div>
                            </div>
                            <div class="card ticket-card" style="opacity:0.6; cursor:pointer; padding: 15px;" onclick="selectTicket(this, 8922)">
                                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                                    <span style="font-size:12px; font-weight:600; color:#555;">#8922</span>
                                    <span style="font-size:11px; background:#E2F0FF; color:#1565C0; padding:2px 6px; border-radius:10px;">Normal</span>
                                </div>
                                <div style="font-size:12px; color:#888; margin-bottom:4px;"><i class='bx bx-user'></i> Sarah W.</div>
                                <div class="card-title" style="font-size: 14px; line-height:1.4;">"Can't connect to home wifi"</div>
                            </div>
                        </div>
                        <div style="flex:2; min-width: 400px; padding: 30px;" class="card" id="ai-preview">
                            <div class="card-header"><span class="tag auto" style="display:flex; align-items:center; gap:5px; width: fit-content;"><i class='bx bx-bot'></i> AI Suggested Reply</span></div>
                            <div class="card-title" style="margin-top:20px; font-size:22px;">Battery Optimization Plan</div>
                            <div class="card-desc" style="margin-top:10px; font-size: 15px;">Automatically generated response based on the FAISS knowledge base.</div>
                            <div class="card-steps" style="margin-top:25px; font-size:15px; padding:20px 25px; background: #F8F9FA; border-radius: 12px;">
                                <ul style="line-height:2;">
                                    <li>Navigate to Settings</li>
                                    <li>Tap Device Care</li>
                                    <li>Tap Battery</li>
                                    <li>Tap Optimize Now</li>
                                </ul>
                            </div>
                            <div style="margin-top:30px; display:flex; gap:15px;">
                                <button class="header-btn" style="background:#111; color:white; font-size:15px; padding: 12px 24px; border-radius:8px;" onclick="alert('Reply sent to John D.!')"><i class='bx bx-send'></i> Send to Customer</button>
                                <button class="launch-btn" style="padding:12px 24px; font-size:15px;" onclick="alert('Opening editor...')"><i class='bx bx-edit-alt'></i> Edit Plan</button>
                            </div>
                        </div>
                    </div>
                `;"""
    
    content = re.sub(old_agent_console, new_agent_console, content, flags=re.DOTALL)
    
    # 5. Fix Quick Actions grid links to point to the correct ones
    # Generate Guide -> Focus search
    # Browse Library (now Categories) -> switchTab(..., 'Categories')
    # View Analytics -> switchTab(..., 'Analytics')
    # Manage Settings -> switchTab(..., 'Settings')
    content = content.replace("switchTab(document.querySelector('.sidebar .nav-item:nth-child(3)'), 'Library')", "switchTab(document.querySelector('.sidebar .nav-item:nth-child(4)'), 'Categories')")
    content = content.replace("switchTab(document.querySelector('.sidebar .nav-item:nth-child(4)'), 'Analytics')", "switchTab(document.querySelector('.sidebar .nav-item:nth-child(5)'), 'Analytics')")
    content = content.replace("switchTab(document.querySelector('.sidebar .nav-item:nth-child(6)'), 'Settings')", "switchTab(document.querySelector('.sidebar .nav-item:nth-child(7)'), 'Settings')")

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("UI bugs fixed successfully.")

if __name__ == '__main__':
    main()
