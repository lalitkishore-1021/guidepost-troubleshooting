import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update the tabs in switchTab
    old_tabs = r"\} else if \(tabName === 'Categories'\) \{.*?\} else if \(tabName === 'Settings'\) \{.*?\}\s*\n\s*\}"
    
    new_tabs = r"""} else if (tabName === 'Categories') {
                document.getElementById('topUI').style.display = 'none'; document.getElementById('heroSection').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Problem Categories <span class="badge-count">12 Active</span>`;
                document.getElementById('results').innerHTML = `
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#E3F2FD; color:#1565C0; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-chip'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Hardware</div><div style="color:#666; font-size:13px; margin-top:4px;">Physical device issues, broken screens, and port failures.</div></div>
                    </div>
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#E8F5E9; color:#2E7D32; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-code-alt'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Software</div><div style="color:#666; font-size:13px; margin-top:4px;">App crashes, operating system errors, and bugs.</div></div>
                    </div>
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#F3E5F5; color:#7B1FA2; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-wifi'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Network & Connectivity</div><div style="color:#666; font-size:13px; margin-top:4px;">Wi-Fi drops, mobile data issues, and router configs.</div></div>
                    </div>
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#FFF3E0; color:#E65100; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-battery'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Battery & Power</div><div style="color:#666; font-size:13px; margin-top:4px;">Fast battery drain, charging failures, and overheating.</div></div>
                    </div>
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#E0F7FA; color:#006064; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-desktop'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Display & Graphics</div><div style="color:#666; font-size:13px; margin-top:4px;">Screen freezing, blurry camera, and visual glitches.</div></div>
                    </div>
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#FCE4EC; color:#880E4F; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-bluetooth'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Bluetooth & Accessories</div><div style="color:#666; font-size:13px; margin-top:4px;">Pairing issues, earbud connectivity, and smartwatches.</div></div>
                    </div>
                `;
            } else if (tabName === 'Analytics') {
                renderAnalyticsDashboard();
            } else if (tabName === 'Team') {
                document.getElementById('topUI').style.display = 'none'; document.getElementById('heroSection').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Support Teams <span class="badge-count">4 Departments</span>`;
                document.getElementById('results').innerHTML = `
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#E3F2FD; color:#1565C0; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-headphone'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Technical Support</div><div style="color:#666; font-size:13px; margin-top:4px;">Handles first-level issues and general troubleshooting.</div></div>
                    </div>
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#E8F5E9; color:#2E7D32; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-wrench'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Device Diagnostics</div><div style="color:#666; font-size:13px; margin-top:4px;">Manages automated device checks and hardware diagnostics.</div></div>
                    </div>
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#F3E5F5; color:#7B1FA2; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-code-block'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Engineering</div><div style="color:#666; font-size:13px; margin-top:4px;">Resolves complex, deep-level software and firmware issues.</div></div>
                    </div>
                    <div class="card" style="display:flex; align-items:flex-start; gap:15px; padding:20px;">
                        <div style="background:#FFF5F5; color:#D32F2F; padding:12px; border-radius:12px; font-size:24px; flex-shrink:0;"><i class='bx bx-error-circle'></i></div>
                        <div><div style="font-weight:700; font-size:16px;">Escalation Team</div><div style="color:#666; font-size:13px; margin-top:4px;">Handles critical unresolved issues and VIP escalations.</div></div>
                    </div>
                `;
            } else if (tabName === 'Settings') {
                document.getElementById('topUI').style.display = 'none'; document.getElementById('heroSection').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `System Settings`;
                document.getElementById('results').innerHTML = `
                    <div class="card" style="padding:20px;">
                        <div style="font-weight:700; font-size:16px; margin-bottom:15px; display:flex; align-items:center; gap:8px;"><i class='bx bx-slider' style="color:#1565C0;"></i> General</div>
                        <div style="font-size:13px; color:#555; display:grid; gap:12px;">
                            <div style="display:flex; justify-content:space-between;"><span>Workspace Name</span><span style="font-weight:600; color:#111;">PlanForge Staging</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Default Language</span><span style="font-weight:600; color:#111;">English (US)</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Time Zone</span><span style="font-weight:600; color:#111;">UTC-08:00 (Pacific Time)</span></div>
                        </div>
                    </div>
                    <div class="card" style="padding:20px;">
                        <div style="font-weight:700; font-size:16px; margin-bottom:15px; display:flex; align-items:center; gap:8px;"><i class='bx bx-support' style="color:#2E7D32;"></i> Support Configurations</div>
                        <div style="font-size:13px; color:#555; display:grid; gap:12px;">
                            <div style="display:flex; justify-content:space-between;"><span>Default Support Team</span><span style="font-weight:600; color:#111;">Technical Support</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Critical Issues Team</span><span style="font-weight:600; color:#D32F2F;">Escalation Team</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Auto-assignment</span><span style="font-weight:600; color:#2E7D32;">Enabled</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Escalation Rules</span><span style="font-weight:600; color:#111;">After 24h Unresolved</span></div>
                        </div>
                    </div>
                    <div class="card" style="padding:20px;">
                        <div style="font-weight:700; font-size:16px; margin-bottom:15px; display:flex; align-items:center; gap:8px;"><i class='bx bx-brain' style="color:#7B1FA2;"></i> AI Engine</div>
                        <div style="font-size:13px; color:#555; display:grid; gap:12px;">
                            <div style="display:flex; justify-content:space-between;"><span>AI Guide Generation</span><span style="font-weight:600; color:#2E7D32;">Active</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Auto Diagnosis</span><span style="font-weight:600; color:#2E7D32;">Active</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Confidence Threshold</span><span style="font-weight:600; color:#111;">0.85 (High)</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Human Review</span><span style="font-weight:600; color:#E65100;">Required below 0.85</span></div>
                        </div>
                    </div>
                    <div class="card" style="padding:20px;">
                        <div style="font-weight:700; font-size:16px; margin-bottom:15px; display:flex; align-items:center; gap:8px;"><i class='bx bx-bell' style="color:#E65100;"></i> Notifications</div>
                        <div style="font-size:13px; color:#555; display:grid; gap:12px;">
                            <div style="display:flex; justify-content:space-between;"><span>New Issue</span><span style="font-weight:600; color:#111;">Email & Dashboard</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Critical Issue</span><span style="font-weight:600; color:#111;">SMS & Slack</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>System Alerts</span><span style="font-weight:600; color:#111;">Dashboard Only</span></div>
                        </div>
                    </div>
                    <div class="card" style="padding:20px;">
                        <div style="font-weight:700; font-size:16px; margin-bottom:15px; display:flex; align-items:center; gap:8px;"><i class='bx bx-server' style="color:#006064;"></i> System</div>
                        <div style="font-size:13px; color:#555; display:grid; gap:12px;">
                            <div style="display:flex; justify-content:space-between;"><span>API Status</span><span style="font-weight:600; color:#2E7D32;">Online</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Knowledge Base</span><span style="font-weight:600; color:#111;">FAISS Vector DB</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Data Retention</span><span style="font-weight:600; color:#111;">90 Days</span></div>
                            <div style="display:flex; justify-content:space-between;"><span>Audit Logs</span><span style="font-weight:600; color:#2E7D32;">Enabled</span></div>
                        </div>
                    </div>
                `;
            }
        }"""
    
    content = re.sub(old_tabs, new_tabs, content, flags=re.DOTALL)

    # 2. Update the Right Panel - Resolution Types to Resolution by Category & Team
    old_legend = r"<div><div class=\"dot\" style=\"background:#DCEE77;\"></div> Auto <span style=\"font-weight:700; color:#111; margin-left:10px;\">32%</span></div>\s*<div><div class=\"dot\" style=\"background:#698BFF;\"></div> Manual <span style=\"font-weight:700; color:#111; margin-left:10px;\">28%</span></div>\s*<div><div class=\"dot\" style=\"background:#82CDB3;\"></div> Critical <span style=\"font-weight:700; color:#111; margin-left:10px;\">22%</span></div>\s*<div><div class=\"dot\" style=\"background:#7A73AB;\"></div> Other <span style=\"font-weight:700; color:#111; margin-left:10px;\">18%</span></div>"
    
    new_legend = r"""<div><div class="dot" style="background:#DCEE77;"></div> Hardware <span style="font-weight:700; color:#111; margin-left:10px;">32%</span></div>
                <div><div class="dot" style="background:#698BFF;"></div> Software <span style="font-weight:700; color:#111; margin-left:10px;">28%</span></div>
                <div><div class="dot" style="background:#82CDB3;"></div> Network <span style="font-weight:700; color:#111; margin-left:10px;">22%</span></div>
                <div><div class="dot" style="background:#7A73AB;"></div> Battery <span style="font-weight:700; color:#111; margin-left:10px;">18%</span></div>
            </div>
            
            <div style="margin-top: 25px; border-top: 1px solid #EEE; padding-top: 20px;">
                <h4 style="font-size: 13px; font-weight:700; margin-bottom: 12px; color:#111;">Resolution by Team</h4>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px;"><span style="color:#666;">Technical Support</span><span style="font-weight:600; color:#1565C0;">64%</span></div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px;"><span style="color:#666;">Diagnostics</span><span style="font-weight:600; color:#2E7D32;">21%</span></div>
                <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px;"><span style="color:#666;">Engineering</span><span style="font-weight:600; color:#7B1FA2;">11%</span></div>
                <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#666;">Escalation</span><span style="font-weight:600; color:#D32F2F;">4%</span></div>"""
    
    content = re.sub(old_legend, new_legend, content)
    content = content.replace("<h3>Resolution Types</h3>", "<h3>Resolution by Category</h3>")

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully injected realistic demo data.")

if __name__ == '__main__':
    main()
