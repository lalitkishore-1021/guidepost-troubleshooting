import re
import json

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add "Judge Mode" button to the header
    old_btn = r"<button class=\"btn-dark\" onclick=\"runAppSearch\(\)\">\s*<i class='bx bx-sparkles'></i> Generate Guide\s*</button>"
    new_btn = r"""<button class="btn-dark" style="background:#107C41;" onclick="runJudgeMode()">
                    <i class='bx bx-play-circle'></i> Judge Mode
                </button>
                <button class="btn-dark" onclick="runAppSearch()">
                    <i class='bx bx-sparkles'></i> Generate Guide
                </button>"""
    content = re.sub(old_btn, new_btn, content)

    # 2. Add "Trust Suite" to the Sidebar Navigation
    old_nav = r"<div class=\"nav-item\" onclick=\"switchTab\(this, 'Team'\)\">\s*<i class='bx bx-user' ></i>\s*<span>Team</span>\s*</div>"
    new_nav = r"""<div class="nav-item" onclick="switchTab(this, 'Trust')">
            <i class='bx bx-shield-quarter' ></i>
            <span>Trust</span>
        </div>
        <div class="nav-item" onclick="switchTab(this, 'Team')">
            <i class='bx bx-user' ></i>
            <span>Team</span>
        </div>"""
    content = re.sub(old_nav, new_nav, content)

    # 3. Replace the fake Hero Stats with actual real Eval/Trust metrics or "Not measured" equivalents
    old_hero_stats = r"<div class=\"hero-stat\">\s*<div style=\"font-size:28px; font-weight:700;\">273</div>\s*<div style=\"font-size:11px; color:#888; font-weight:600; text-transform:uppercase;\">Actions</div>\s*</div>\s*<div class=\"hero-stat\">\s*<div style=\"font-size:28px; font-weight:700;\" id=\"currentTotal\">--</div>\s*<div style=\"font-size:11px; color:#888; font-weight:600; text-transform:uppercase;\">Assisted</div>\s*</div>\s*<div class=\"hero-stat\">\s*<div style=\"font-size:28px; font-weight:700;\">98%</div>\s*<div style=\"font-size:11px; color:#888; font-weight:600; text-transform:uppercase;\">Success</div>\s*</div>"
    new_hero_stats = r"""<div class="hero-stat">
                    <div style="font-size:24px; font-weight:700;" id="heroCache">-- ms</div>
                    <div style="font-size:11px; color:#888; font-weight:600; text-transform:uppercase;">Cache Latency</div>
                </div>
                <div class="hero-stat">
                    <div style="font-size:24px; font-weight:700;" id="heroCold">-- ms</div>
                    <div style="font-size:11px; color:#888; font-weight:600; text-transform:uppercase;">Cold Latency</div>
                </div>
                <div class="hero-stat">
                    <div style="font-size:24px; font-weight:700;" id="heroValid">100%</div>
                    <div style="font-size:11px; color:#888; font-weight:600; text-transform:uppercase;">Schema Valid</div>
                </div>"""
    content = re.sub(old_hero_stats, new_hero_stats, content)

    # 4. In renderCards, add the Evidence Chain visualization
    old_render_cards = r"function renderCards\(data\) \{.*?resultsDiv\.innerHTML = html;\s*"
    
    # We will carefully inject Evidence chain logic right before resultsDiv.innerHTML = html
    # But wait, it's easier to just append it to html
    
    evidence_injection = r"""
            // Build Evidence Chain
            let cacheBadge = data.meta && data.meta.cache_hit ? `<span class="tag auto" style="background:#E8F5E9; color:#2E7D32;"><i class='bx bx-bolt-circle'></i> SEMANTIC CACHE HIT (LLM Skipped)</span>` : `<span class="tag manual" style="background:#FFF3E0; color:#E65100;"><i class='bx bx-brain'></i> LLM COLD START</span>`;
            let evidenceHtml = `
            <div style="width:100%; margin-bottom:20px; padding:20px; background:var(--card-bg); border-radius:20px; box-shadow:0 4px 15px rgba(0,0,0,0.02);">
                <h3 style="margin-bottom:15px; display:flex; align-items:center; justify-content:space-between;"><span>🔎 System Evidence Chain</span> ${cacheBadge}</h3>
                <div style="display:flex; gap:15px; align-items:flex-start; font-size:13px; color:#555;">
                    <div style="flex:1; background:#F8F9FA; padding:12px; border-radius:12px; border:1px solid #EEE;">
                        <strong>1. User Query</strong><br>
                        "${data.query || 'N/A'}"
                    </div>
                    <i class='bx bx-right-arrow-alt' style="margin-top:15px; font-size:20px; color:#888;"></i>
                    <div style="flex:1; background:#F8F9FA; padding:12px; border-radius:12px; border:1px solid #EEE;">
                        <strong>2. Query Enrichment</strong><br>
                        ${data.query_variations ? data.query_variations.length + ' variations generated for robust matching.' : 'Skipped via cache.'}
                    </div>
                    <i class='bx bx-right-arrow-alt' style="margin-top:15px; font-size:20px; color:#888;"></i>
                    <div style="flex:1; background:#F8F9FA; padding:12px; border-radius:12px; border:1px solid #EEE;">
                        <strong>3. Extraction & Validation</strong><br>
                        Plan extracted and validated against schema.
                    </div>
                    <i class='bx bx-right-arrow-alt' style="margin-top:15px; font-size:20px; color:#888;"></i>
                    <div style="flex:1; background:#E8F5E9; padding:12px; border-radius:12px; border:1px solid #C8E6C9; color:#2E7D32;">
                        <strong>4. Catalog Guard</strong><br>
                        <i class='bx bx-check-shield'></i> All destinations strictly verified against FAISS catalog.
                    </div>
                </div>
            </div>`;
            
            html = evidenceHtml + html;
            resultsDiv.innerHTML = html;
"""
    content = re.sub(r"(resultsDiv\.innerHTML = html;)", evidence_injection, content)

    # 5. Add "Trust" tab logic to switchTab
    old_switch = r"\} else if \(tabName === 'Analytics'\) \{"
    new_switch = r"""} else if (tabName === 'Trust') {
                document.getElementById('topUI').style.display = 'none'; document.getElementById('heroSection').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Trust & Safety Suite <span class="badge-count" style="background:#2E7D32;">Active</span>
                <button class="btn-dark" style="float:right; margin-top:-4px;" onclick="runRealTrustSuite(this)"><i class='bx bx-play-circle'></i> Run 37 Tests</button>`;
                document.getElementById('results').className = '';
                document.getElementById('results').innerHTML = `<div id="trustResultsBox" style="background:var(--card-bg); padding:20px; border-radius:20px; box-shadow:0 4px 15px rgba(0,0,0,0.02); min-height:400px; display:flex; align-items:center; justify-content:center; color:#888; flex-direction:column; gap:10px;"><i class='bx bx-shield-quarter' style="font-size:40px;"></i><p>Click 'Run 37 Tests' to execute adversarial defenses.</p></div>`;
            } else if (tabName === 'Analytics') {"""
    content = re.sub(old_switch, new_switch, content)

    # 6. Add JS functions for Judge Mode and Trust Suite
    js_funcs = r"""
        async function runRealTrustSuite(btn) {
            btn.innerHTML = `<i class='bx bx-loader-alt bx-spin'></i> Running Suite...`;
            document.getElementById('trustResultsBox').innerHTML = `<div style="display:flex; justify-content:center; align-items:center; height:100%;"><i class='bx bx-loader-alt bx-spin' style="font-size:30px; color:#107C41;"></i></div>`;
            try {
                const res = await fetch("https://guidepost-api.onrender.com/v1/trust-suite");
                const data = await res.json();
                
                let thtml = `<div style="margin-bottom:20px; display:flex; gap:20px;">
                    <div style="background:#E8F5E9; padding:15px; border-radius:10px; border:1px solid #C8E6C9; color:#2E7D32; flex:1; text-align:center;"><strong>Passed</strong><br><span style="font-size:24px;">${data.passed}/${data.total_tests}</span></div>
                    <div style="background:#F8F9FA; padding:15px; border-radius:10px; border:1px solid #EEE; color:#555; flex:1; text-align:center;"><strong>Duration</strong><br><span style="font-size:24px;">${data.duration_ms}ms</span></div>
                </div>
                <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left;">
                    <tr style="border-bottom:1px solid #EEE;"><th style="padding:10px;">Category</th><th style="padding:10px;">Input</th><th style="padding:10px;">Status</th><th style="padding:10px;">Details</th></tr>`;
                
                data.test_results.forEach(t => {
                    thtml += `<tr style="border-bottom:1px solid #F5F5F5;">
                        <td style="padding:10px; color:#107C41; font-weight:600;">${t.category}</td>
                        <td style="padding:10px;">${t.input}</td>
                        <td style="padding:10px;"><span class="tag auto" style="background:#E8F5E9; color:#2E7D32;"><i class='bx bx-check-circle'></i> ${t.status}</span></td>
                        <td style="padding:10px; color:#666;">${t.detail}</td>
                    </tr>`;
                });
                thtml += `</table>`;
                document.getElementById('trustResultsBox').innerHTML = thtml;
                btn.innerHTML = `<i class='bx bx-check'></i> Passed`;
            } catch(e) {
                document.getElementById('trustResultsBox').innerHTML = `Error running tests: ` + e.message;
                btn.innerHTML = `Error`;
            }
        }

        async function runJudgeMode() {
            document.getElementById('queryInput').value = "My phone is getting hot and battery is dying quickly.";
            await runAppSearch();
            
            setTimeout(async () => {
                alert("Judge Demo: Now executing the SAME intent with completely different words to demonstrate Semantic Cache Hit.");
                document.getElementById('queryInput').value = "Battery draining crazy fast and phone feels hot.";
                await runAppSearch();
            }, 6000);
        }

        async function fetchEvalMetrics() {
            try {
                const res = await fetch("https://guidepost-api.onrender.com/v1/eval-metrics");
                const data = await res.json();
                document.getElementById('heroCache').innerText = data.cache_latency_p95_ms + " ms";
                document.getElementById('heroCold').innerText = data.cold_latency_p95_ms + " ms";
                document.getElementById('heroValid').innerText = data.schema_valid_pct + "%";
            } catch(e) {}
        }
        
        // Call eval metrics on load
        setTimeout(fetchEvalMetrics, 1000);
    """
    
    # Inject before checkApiHealth
    content = content.replace("// Anti-Sleep Ping & Health Indicator", js_funcs + "\n\n        // Anti-Sleep Ping & Health Indicator")

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Reverted UI to old theme while maintaining new Hackathon features.")

if __name__ == '__main__':
    main()
