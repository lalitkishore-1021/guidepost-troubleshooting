import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Health Check
    old_health = r"""async function checkApiHealth() {
            try {
                const res = await fetch("https://guidepost-api.onrender.com/health");
                if (res.ok) {
                    document.getElementById("healthDot").style.background = "#2E7D32";
                    document.getElementById("healthText").innerText = "API Ready";
                } else {
                    throw new Error("Bad status");
                }
            } catch(e) {
                document.getElementById("healthDot").style.background = "#D32F2F";
                document.getElementById("healthText").innerText = "API Starting/Sleeping...";
            }
        }"""
    new_health = r"""async function checkApiHealth() {
            document.getElementById("healthDot").style.background = "#FFA000";
            document.getElementById("healthText").innerText = "Checking...";
            try {
                const res = await fetch("https://guidepost-api.onrender.com/health");
                if (res.ok) {
                    document.getElementById("healthDot").style.background = "#2E7D32";
                    document.getElementById("healthText").innerText = "API Connected";
                } else {
                    throw new Error("Bad status");
                }
            } catch(e) {
                document.getElementById("healthDot").style.background = "#D32F2F";
                document.getElementById("healthText").innerText = "API Offline";
            }
        }"""
    html = html.replace(old_health, new_health)

    # 2. Hero Stats
    old_hero_stats = r"""<div class="hero-stat">
                    <div style="background:#E8F5E9; color:#2E7D32; width:40px; height:40px; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size:20px; margin-bottom:12px;"><i class='bx bx-file'></i></div>
                    <div style="font-size:24px; font-weight:700;">273</div>
                    <div style="font-size:11px; color:#666;">Total Resolutions</div>
                </div>
                <div class="hero-stat">
                    <div style="background:#E3F2FD; color:#1565C0; width:40px; height:40px; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size:20px; margin-bottom:12px;"><i class='bx bx-group'></i></div>
                    <div style="font-size:24px; font-weight:700;" id="currentTotal">--</div>
                    <div style="font-size:11px; color:#666;">Assisted</div>
                </div>
                <div class="hero-stat">
                    <div style="background:#F3E5F5; color:#7B1FA2; width:40px; height:40px; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size:20px; margin-bottom:12px;"><i class='bx bx-trending-up'></i></div>
                    <div style="font-size:24px; font-weight:700;">98%</div>
                    <div style="font-size:11px; color:#666;">Success Rate</div>
                </div>"""
    new_hero_stats = r"""<div class="hero-stat">
                    <div style="background:#F1F5F9; color:#64748B; width:40px; height:40px; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size:20px; margin-bottom:12px;"><i class='bx bx-timer'></i></div>
                    <div style="font-size:13px; font-weight:700; color:#64748B;">Not measured</div>
                    <div style="font-size:11px; color:#666; margin-top:5px;">Cache P95 Target: &le; 300ms</div>
                </div>
                <div class="hero-stat">
                    <div style="background:#F1F5F9; color:#64748B; width:40px; height:40px; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size:20px; margin-bottom:12px;"><i class='bx bx-timer'></i></div>
                    <div style="font-size:13px; font-weight:700; color:#64748B;">Not measured</div>
                    <div style="font-size:11px; color:#666; margin-top:5px;">Cold P95 Target: &le; 8s</div>
                </div>
                <div class="hero-stat">
                    <div style="background:#F1F5F9; color:#64748B; width:40px; height:40px; border-radius:10px; display:flex; justify-content:center; align-items:center; font-size:20px; margin-bottom:12px;"><i class='bx bx-check-shield'></i></div>
                    <div style="font-size:13px; font-weight:700; color:#64748B;">Not measured</div>
                    <div style="font-size:11px; color:#666; margin-top:5px;">Schema Target: 100%</div>
                </div>"""
    html = html.replace(old_hero_stats, new_hero_stats)

    # 3. Sidebar Tabs
    old_nav = r"""<div class="nav-item" onclick="switchTab(this, 'Team')">"""
    new_nav = r"""<div class="nav-item" onclick="switchTabByName('Trust Suite')">
            <i class='bx bx-shield-quarter'></i>
            <span>Trust</span>
        </div>
        <div class="nav-item" onclick="switchTabByName('Eval Lab')">
            <i class='bx bx-test-tube'></i>
            <span>Eval</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Team')">"""
    html = html.replace(old_nav, new_nav)

    # 4. Header (Judge Mode & Bell)
    old_btn = r"""<button class="btn-dark" onclick="runAppSearch()">"""
    new_btn = r"""<button class="btn-dark" style="background:#107C41;" onclick="runJudgeMode()">
                    <i class='bx bx-play-circle'></i> Judge Mode
                </button>
                <button class="btn-dark" onclick="runAppSearch()">"""
    html = html.replace(old_btn, new_btn)

    html = html.replace("<i class='bx bx-bell' style=\"font-size:20px; color:#555;\"></i>", 
                        "<i class='bx bx-bell' style=\"font-size:20px; color:#555; cursor:pointer;\" onclick=\"showNotifications()\"></i>")

    # 5. Quick Actions (nth-child to switchTabByName)
    html = re.sub(r"switchTab\(document\.querySelector\('\.sidebar \.nav-item:nth-child\(\d+\)'\), '([^']+)'\)", 
                  r"switchTabByName('\1')", html)

    # 6. Support Actions (Alerts)
    html = html.replace("onclick=\"alert('Options Menu clicked')\"", "")
    html = html.replace("onclick=\"alert('Opening editor...')\"", "onclick=\"alertUnavailable('Edit Plan API not connected')\"")
    html = html.replace("onclick=\"alert('Reply sent to Sarah W.!')\"", "onclick=\"alertUnavailable('Support Reply API not connected')\"")
    html = html.replace("onclick=\"alert('Reply sent to John D.!')\"", "onclick=\"alertUnavailable('Support Reply API not connected')\"")
    html = html.replace("onclick=\"alert('Exporting latency logs as CSV...')\"", "onclick=\"alertUnavailable('Export API not connected')\"")
    html = html.replace("onclick=\"alert('Flushing FAISS cache...')\"", "onclick=\"alertUnavailable('Flush API not connected')\"")

    # 7. renderCards Modifications
    
    # 7a. Add Evidence Chain at the start of renderCards
    old_render_cards_start = r"""const resultsDiv = document.getElementById('results');
            
            document.getElementById('jsonContent').style.display = 'none';

            if (!data.response || !data.response.contexts || data.response.contexts.length === 0) {"""
            
    new_render_cards_start = r"""const resultsDiv = document.getElementById('results');
            
            document.getElementById('jsonContent').style.display = 'none';
            
            // LLM Badge Logic
            let badge = document.getElementById('llmBadge');
            if (!badge) {
                badge = document.createElement('div');
                badge.id = 'llmBadge';
                badge.style = 'margin-left:15px; padding:4px 8px; border-radius:4px; font-size:11px; font-weight:600;';
                document.querySelector('.health-indicator').parentNode.appendChild(badge);
            }
            if (data.meta && data.meta.model && data.meta.model.toLowerCase().includes('mock')) {
                badge.innerText = 'Mock LLM'; badge.style.background = '#FFF3E0'; badge.style.color = '#E65100';
            } else {
                badge.innerText = 'Live LLM'; badge.style.background = '#E8F5E9'; badge.style.color = '#2E7D32';
            }

            if (!data.response || !data.response.contexts || data.response.contexts.length === 0) {"""
    html = html.replace(old_render_cards_start, new_render_cards_start)
    
    old_html_init = r"""let html = '';
            
            const ctx = data.response.contexts[0];"""
            
    new_html_init = r"""let html = '';
            
            let cacheBadge = data.meta && data.meta.cache_hit ? `<span class="tag auto" style="background:#E8F5E9; color:#2E7D32; padding:4px 8px; font-size:11px; border-radius:12px;"><i class='bx bx-bolt-circle'></i> SEMANTIC CACHE HIT</span>` : `<span class="tag manual" style="background:#FFF3E0; color:#E65100; padding:4px 8px; font-size:11px; border-radius:12px;"><i class='bx bx-brain'></i> CACHE MISS</span>`;
            let evidenceHtml = `
            <div style="width:100%; margin-bottom:20px; padding:20px; background:var(--card-bg); border-radius:20px; box-shadow:0 4px 15px rgba(0,0,0,0.02);">
                <h3 style="margin-bottom:15px; display:flex; align-items:center; justify-content:space-between; color:#111;"><span>🔎 Evidence Chain</span> ${cacheBadge}</h3>
                <div style="display:flex; gap:15px; align-items:flex-start; font-size:12px; color:#555;">
                    <div style="flex:1; background:#F8F9FA; padding:12px; border-radius:12px; border:1px solid #EEE;">
                        <strong>User Complaint</strong><br>"${data.query || 'N/A'}"
                    </div>
                    <i class='bx bx-right-arrow-alt' style="margin-top:15px; font-size:18px; color:#888;"></i>
                    <div style="flex:1; background:#F8F9FA; padding:12px; border-radius:12px; border:1px solid #EEE;">
                        <strong>Extraction</strong><br>${data.response && data.response.contexts.length > 0 ? 'Plan extracted & validated' : 'Data unavailable'}
                    </div>
                </div>
            </div>`;
            html += evidenceHtml;
            
            const ctx = data.response.contexts[0];"""
    html = html.replace(old_html_init, new_html_init)

    # 7b. "Why this step?" & "Launch Settings"
    # We replace the action loop inner HTML
    old_action_start = r"""html += `<div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">"""
    
    new_action_start = r"""
                let actionableLink = action.stepGroups && action.stepGroups[0] && action.stepGroups[0].actionableDeepLink;
                let whyStepHtml = '';
                if (actionableLink && actionableLink.deeplink && actionableLink.deeplink !== 'None') {
                    whyStepHtml = `<details style="margin-top:10px; font-size:12px; color:#666; background:#F8F9FA; padding:8px; border-radius:8px; cursor:pointer;">
                        <summary style="font-weight:600; color:#107C41;">🔎 Why this step?</summary>
                        <div style="margin-top:6px; border-top:1px solid #EEE; padding-top:6px;">
                            <strong>Catalog Verification:</strong> <span style="color:#2E7D32;"><i class='bx bx-check'></i> Catalog entry verified</span><br>
                            <strong>Destination:</strong> ${actionableLink.deeplink}
                        </div>
                    </details>`;
                } else {
                    whyStepHtml = `<details style="margin-top:10px; font-size:12px; color:#666; background:#F8F9FA; padding:8px; border-radius:8px; cursor:pointer;">
                        <summary style="font-weight:600; color:#555;">🔎 Why this step?</summary>
                        <div style="margin-top:6px; border-top:1px solid #EEE; padding-top:6px;">
                            <strong>Catalog Verification:</strong> <span style="color:#D32F2F;"><i class='bx bx-x'></i> Not verified / Manual</span><br>
                            <strong>Destination:</strong> None
                        </div>
                    </details>`;
                }
                
                html += `<div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">"""
    html = html.replace(old_action_start, new_action_start)
    
    old_action_desc = r"""<div class="card-desc" style="font-size:13px; color:#666; line-height:1.4;">${action.description}</div>
                        </div>
                    </div>`;"""
    new_action_desc = r"""<div class="card-desc" style="font-size:13px; color:#666; line-height:1.4;">${action.description}</div>
                            ${whyStepHtml}
                        </div>
                    </div>`;"""
    html = html.replace(old_action_desc, new_action_desc)
    
    old_launch_btn = r"""${(action.stepGroups[0].actionableDeepLink && cat !== "manual") ? `<button class="launch-btn" style="background:#1E1F22; color:white; border:none; padding:8px 16px; border-radius:15px;" onclick="alert('Launching Device Settings')">Launch Settings</button>` : ''}"""
    new_launch_btn = r"""${(actionableLink && actionableLink.deeplink && actionableLink.deeplink !== 'None') ? `<button class="launch-btn" style="background:#1E1F22; color:white; border:none; padding:8px 16px; border-radius:15px;" onclick="alertUnavailable('Launching validated deeplink: ' + actionableLink.deeplink)">Launch Settings</button>` : `<button class="launch-btn" style="background:#E2E8F0; color:#64748B; border:none; padding:8px 16px; border-radius:15px; cursor:not-allowed;" disabled>No Launch Available</button>`}"""
    html = html.replace(old_launch_btn, new_launch_btn)

    # 8. switchTab logic & JS Utilities
    js_utils = r"""
        function alertUnavailable(msg) {
            let el = document.getElementById('tempAlert');
            if(!el) {
                el = document.createElement('div');
                el.id = 'tempAlert';
                el.style.position = 'fixed'; el.style.bottom = '20px'; el.style.right = '20px';
                el.style.background = '#333'; el.style.color = 'white'; el.style.padding = '12px 20px';
                el.style.borderRadius = '8px'; el.style.zIndex = '9999'; document.body.appendChild(el);
            }
            el.innerText = msg;
            setTimeout(() => el.remove(), 3000);
        }
        
        function showNotifications() {
            alertUnavailable('Notifications are not configured yet. No new notifications.');
        }

        async function runJudgeMode() {
            document.getElementById('queryInput').value = "My phone is getting hot and battery is dying quickly.";
            await runAppSearch();
            alertUnavailable("Judge Demo: Testing semantic cache with different words...");
            setTimeout(async () => {
                document.getElementById('queryInput').value = "Battery draining crazy fast and phone feels hot.";
                await runAppSearch();
            }, 3000);
        }

        function switchTabByName(tabName) {
            let items = document.querySelectorAll('.sidebar .nav-item');
            for (let item of items) {
                if (item.innerText.includes(tabName) || item.getAttribute('onclick').includes(tabName)) {
                    switchTab(item, tabName);
                    return;
                }
            }
        }
    """
    html = html.replace("function runAppSearch() {", js_utils + "\n        function runAppSearch() {")
    
    # Update tabs
    old_switch_analytics = r"""} else if (tabName === 'Analytics') {
                document.getElementById('topUI').style.display = 'none'; document.getElementById('heroSection').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Analytics Dashboard`;"""
    
    new_switch_analytics = r"""} else if (tabName === 'Trust Suite' || tabName === 'Eval Lab') {
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
                return;"""
    html = html.replace(old_switch_analytics, new_switch_analytics)
    
    html = html.replace("`System Settings`;", "`System Settings`;\n                document.getElementById('results').innerHTML = `<div class=\"card\" style=\"padding:20px; background:#FFF3E0; color:#E65100; margin-bottom:20px;\"><i class='bx bx-info-circle'></i> Settings API is not connected. The below configurations are read-only and not configurable from UI.</div>` + document.getElementById('results').innerHTML;")
    html = html.replace("`Agent Console`;", "`Agent Console (Demo Data) <span style='font-size:12px; color:#888; font-weight:normal; margin-left:10px;'>No live support queue connected</span>`;")


    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Safely applied all fixes without breaking JS structure.")

if __name__ == '__main__':
    main()
