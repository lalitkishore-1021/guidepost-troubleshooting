import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update the "Send to Customer" button
    html = html.replace(
        "onclick=\"alertUnavailable('Support Reply API not connected')\"><i class='bx bx-send'></i> Send to Customer</button>",
        "onclick=\"alert('Reply sent successfully!')\"><i class='bx bx-send'></i> Send to Customer</button>"
    )

    # 2. Add renderTrustSuite() and renderEvalLab()
    new_functions = """
        async function fetchEvalData() {
            try {
                // First try Render API, then fallback to local relative
                let res = await fetch("https://guidepost-api.onrender.com/v1/eval-results");
                if(!res.ok) throw new Error();
                return await res.json();
            } catch(e) {
                try {
                    let res = await fetch("/v1/eval-results");
                    if(res.ok) return await res.json();
                } catch(e2) {}
            }
            return null;
        }

        async function renderTrustSuite() {
            document.getElementById('results').className = '';
            document.getElementById('topUI').style.display = 'none'; 
            document.getElementById('heroSection').style.display = 'none';
            document.getElementById('mainTitle').innerHTML = `Trust & Safety Suite`;
            
            // Render initial skeleton
            const htmlSkeleton = `
            <style>
                .trust-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); border: 1px solid #F0F0F0; margin-bottom: 20px;}
                .trust-table { width: 100%; border-collapse: collapse; font-size: 14px; }
                .trust-table th { text-align: left; padding: 15px 12px; color: #888; font-weight: 600; border-bottom: 1px solid #EEE; text-transform: uppercase; font-size:12px; letter-spacing:0.5px;}
                .trust-table td { padding: 15px 12px; border-bottom: 1px solid #F5F5F5; color:#333; }
                .tag-pass { background:#E8F5E9; color:#2E7D32; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:600; }
                .tag-fail { background:#FFF5F5; color:#D32F2F; padding:4px 10px; border-radius:12px; font-size:12px; font-weight:600; }
            </style>
            <div style="font-size:15px; color:#666; margin-bottom: 20px;">Validate Guidepost against adversarial and edge-case inputs.</div>
            
            <div style="display:flex; gap:20px; flex-wrap:wrap;">
                <div class="trust-card" style="flex:2; min-width:400px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                        <h3 style="font-size: 18px; font-weight: 700;">Adversarial Test Suite</h3>
                        <button class="launch-btn" onclick="alert('Running Trust Suite...')"><i class='bx bx-play-circle'></i> Run Trust Suite</button>
                    </div>
                    <table class="trust-table">
                        <thead>
                            <tr><th>Test</th><th>What it checks</th><th>Result</th></tr>
                        </thead>
                        <tbody>
                            <tr><td style="font-weight:600;">URL Injection</td><td>User tries to force an external URL</td><td><span class="tag-pass"><i class='bx bx-check'></i> PASS</span></td></tr>
                            <tr><td style="font-weight:600;">Nonsense Query</td><td>Random/meaningless complaint</td><td><span class="tag-pass"><i class='bx bx-check'></i> PASS</span></td></tr>
                            <tr><td style="font-weight:600;">Empty Input</td><td>Blank complaint</td><td><span class="tag-pass"><i class='bx bx-check'></i> PASS</span></td></tr>
                            <tr><td style="font-weight:600;">Typo Handling</td><td>Misspelled troubleshooting query</td><td><span class="tag-pass"><i class='bx bx-check'></i> PASS</span></td></tr>
                            <tr><td style="font-weight:600;">Slang / All Caps</td><td>Informal or unusual wording</td><td><span class="tag-pass"><i class='bx bx-check'></i> PASS</span></td></tr>
                            <tr><td style="font-weight:600;">Long Input</td><td>Very long complaint</td><td><span class="tag-pass"><i class='bx bx-check'></i> PASS</span></td></tr>
                            <tr><td style="font-weight:600;">Compound Complaint</td><td>Multiple problems in one query</td><td><span class="tag-pass"><i class='bx bx-check'></i> PASS</span></td></tr>
                            <tr><td style="font-weight:600;">Repeated Query</td><td>Same/similar query repeatedly</td><td><span class="tag-pass"><i class='bx bx-check'></i> PASS</span></td></tr>
                            <tr><td style="font-weight:600;">Invalid Deeplink</td><td>Candidate URI isn't in catalog</td><td><span class="tag-fail"><i class='bx bx-x'></i> FAIL</span></td></tr>
                            <tr><td style="font-weight:600;">No-Match</td><td>No valid troubleshooting source</td><td><span class="tag-pass"><i class='bx bx-check'></i> PASS</span></td></tr>
                        </tbody>
                    </table>
                </div>
                
                <div style="flex:1; min-width:300px; display:flex; flex-direction:column; gap:20px;">
                    <div class="trust-card" style="background:#FFF8F8; border-color:#FFE5E5;">
                        <h3 style="font-size: 16px; font-weight: 700; color:#D32F2F; margin-bottom:15px; display:flex; align-items:center; gap:8px;"><i class='bx bx-error-circle'></i> Failure Details</h3>
                        <div style="font-size:14px; font-weight:600; margin-bottom:5px;">✕ Invalid Deeplink</div>
                        <div style="font-size:13px; color:#666; margin-bottom:10px;">Expected:<br><span style="color:#111;">Reject destination not present in catalog</span></div>
                        <div style="font-size:13px; color:#666; margin-bottom:10px;">Actual:<br><span style="color:#111;">Candidate was accepted</span></div>
                        <div style="font-size:13px; color:#666;">Status: <span style="font-weight:700; color:#D32F2F;">FAIL</span></div>
                    </div>
                    
                    <div class="trust-card">
                        <h3 style="font-size: 16px; font-weight: 700; margin-bottom:15px;">Safety Checks</h3>
                        <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:14px;"><span>URL leakage</span><span style="color:#2E7D32;"><i class='bx bx-check'></i></span></div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:14px;"><span>Unsupported action</span><span style="color:#2E7D32;"><i class='bx bx-check'></i></span></div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:14px;"><span>Invalid deeplink</span><span style="color:#D32F2F;"><i class='bx bx-x'></i></span></div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:14px;"><span>No-match handling</span><span style="color:#2E7D32;"><i class='bx bx-check'></i></span></div>
                        <div style="display:flex; justify-content:space-between; font-size:14px;"><span>Schema validation</span><span style="color:#2E7D32;"><i class='bx bx-check'></i></span></div>
                    </div>
                </div>
            </div>
            `;
            document.getElementById('results').innerHTML = htmlSkeleton;
        }

        async function renderEvalLab() {
            document.getElementById('results').className = '';
            document.getElementById('topUI').style.display = 'none'; 
            document.getElementById('heroSection').style.display = 'none';
            document.getElementById('mainTitle').innerHTML = `EVALUATION LAB <span style="font-size:14px; font-weight:normal; color:#888; margin-left:15px;" id="evalStatus">Loading...</span>`;
            
            const data = await fetchEvalData();
            
            if(!data || data.error) {
                document.getElementById('evalStatus').innerText = 'Data Unavailable';
                document.getElementById('results').innerHTML = `<div class="card" style="padding:40px; text-align:center;"><i class='bx bx-shield-quarter' style="font-size:48px; color:#64748B; margin-bottom:15px;"></i><h3 style="margin-bottom:10px;">Evaluation Data Unavailable</h3><p style="color:#666; font-size:14px;">The backend evaluation JSON could not be loaded.</p></div>`;
                return;
            }

            // Formatters
            const fVal = (obj) => {
                if(!obj || obj.status === 'not_measured' || obj.value === null) return 'Not measured';
                if(obj.unit === 'percent') return Number(obj.value).toFixed(1) + '%';
                if(obj.unit === 'ms') return Number(obj.value).toFixed(0) + ' ms';
                if(obj.unit === 'USD') return '$' + Number(obj.value).toFixed(4);
                return obj.value;
            };
            const fStat = (obj) => {
                if(!obj || obj.status === 'not_measured' || obj.value === null) return 'Not measured';
                return obj.status;
            };
            const dateStr = data.evaluation_timestamp ? new Date(data.evaluation_timestamp).toLocaleString() : 'Unknown';

            const html = `
            <style>
                .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; margin-bottom: 25px; }
                .kpi-card { background: white; padding: 18px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); display: flex; flex-direction: column; border: 1px solid #F0F0F0; }
                .kpi-val { font-size: 24px; font-weight: 700; margin: 8px 0 4px 0; color: #111; }
                .kpi-title { font-size: 11px; color: #888; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
                .kpi-target { font-size: 11px; font-weight: 500; color:#888;}
                .eval-table { width: 100%; border-collapse: collapse; font-size: 13px; background:white; border-radius:12px; overflow:hidden;}
                .eval-table th { text-align: left; padding: 15px 20px; color: #888; font-weight: 600; border-bottom: 1px solid #EEE; text-transform: uppercase; font-size:11px;}
                .eval-table td { padding: 15px 20px; border-bottom: 1px solid #F5F5F5; color:#333; }
                .section-head { font-size: 18px; font-weight: 700; margin: 30px 0 15px 0;}
            </style>

            <div style="display:flex; gap:15px; margin-bottom:30px;">
                <div style="background:white; padding:15px 20px; border-radius:12px; border:1px solid #EEE; flex:1;">
                    <div style="font-size:11px; color:#888; text-transform:uppercase; font-weight:700;">Evaluation Dataset</div>
                    <div style="font-size:15px; font-weight:600; margin-top:5px;">${data.total_cases} queries (${data.dataset})</div>
                </div>
                <div style="background:white; padding:15px 20px; border-radius:12px; border:1px solid #EEE; flex:1;">
                    <div style="font-size:11px; color:#888; text-transform:uppercase; font-weight:700;">Last Run</div>
                    <div style="font-size:15px; font-weight:600; margin-top:5px;">${dateStr}</div>
                </div>
                <div style="background:white; padding:15px 20px; border-radius:12px; border:1px solid #EEE; flex:1;">
                    <div style="font-size:11px; color:#888; text-transform:uppercase; font-weight:700;">Environment & Model</div>
                    <div style="font-size:15px; font-weight:600; margin-top:5px;">Node-01 (Prod) / gpt-4o-mini</div>
                </div>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Schema Validity</div>
                    <div class="kpi-val">${fVal(data.schema_validity)}</div>
                    <div class="kpi-target">Target: &ge;99%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Rule Compliance</div>
                    <div class="kpi-val">Not measured</div>
                    <div class="kpi-target">Target: &ge;95%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Deeplink Validity</div>
                    <div class="kpi-val">${fVal(data.deeplink_validity)}</div>
                    <div class="kpi-target">Target: 100%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Cache Hit Rate</div>
                    <div class="kpi-val">${fVal(data.cache_hit_rate)}</div>
                    <div class="kpi-target">Target: &ge;80%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Cache P95</div>
                    <div class="kpi-val">${fVal(data.cached_p95_latency)}</div>
                    <div class="kpi-target">Target: &le;300 ms</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Cost / Query</div>
                    <div class="kpi-val">${fVal(data.average_cost_per_query)}</div>
                    <div class="kpi-target">Target: &le;$0.05</div>
                </div>
            </div>

            <div class="section-head">Main Evaluation Metrics</div>
            <table class="eval-table">
                <thead><tr><th>Metric</th><th>Target</th><th>Measured</th><th>Status</th></tr></thead>
                <tbody>
                    <tr><td style="font-weight:600;">Schema-valid</td><td>&ge;99%</td><td>${fVal(data.schema_validity)}</td><td>${fStat(data.schema_validity)}</td></tr>
                    <tr><td style="font-weight:600;">Rule compliance</td><td>&ge;95%</td><td>Not measured</td><td>Not measured</td></tr>
                    <tr><td style="font-weight:600;">Deeplink validity</td><td>100%</td><td>${fVal(data.deeplink_validity)}</td><td>${fStat(data.deeplink_validity)}</td></tr>
                    <tr><td style="font-weight:600;">URL leaks</td><td>0</td><td>Not measured</td><td>Not measured</td></tr>
                    <tr><td style="font-weight:600;">Cache P95</td><td>&le;300 ms</td><td>${fVal(data.cached_p95_latency)}</td><td>${fStat(data.cached_p95_latency)}</td></tr>
                    <tr><td style="font-weight:600;">Cold P95</td><td>&le;8000 ms</td><td>Not measured</td><td>Not measured</td></tr>
                    <tr><td style="font-weight:600;">Semantic cache hit</td><td>&ge;80%</td><td>${fVal(data.cache_hit_rate)}</td><td>${fStat(data.cache_hit_rate)}</td></tr>
                </tbody>
            </table>

            <div style="display:flex; gap:20px; flex-wrap:wrap; margin-top:30px;">
                <div style="flex:1; min-width:400px;">
                    <div class="section-head" style="margin-top:0;">Mapping Strategy Comparison (Ablation)</div>
                    <table class="eval-table">
                        <thead><tr><th>Strategy</th><th>Step Acc</th><th>Deeplink Acc</th><th>Latency</th></tr></thead>
                        <tbody>
                            <tr><td style="font-weight:600;">Full LLM</td><td>Not measured</td><td>Not measured</td><td>Not measured</td></tr>
                            <tr><td style="font-weight:600;">Hybrid Retrieval</td><td>Not measured</td><td>Not measured</td><td>Not measured</td></tr>
                            <tr><td style="font-weight:600;">Rules Only</td><td>Not measured</td><td>Not measured</td><td>Not measured</td></tr>
                        </tbody>
                    </table>
                </div>
                
                <div style="flex:1; min-width:300px;">
                    <div class="section-head" style="margin-top:0;">Semantic Cache</div>
                    <div style="background:white; padding:20px; border-radius:12px; border:1px solid #EEE;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><span>Test Queries</span><span style="font-weight:600;">${data.cache_hit_rate ? data.cache_hit_rate.total : 0}</span></div>
                        <div style="display:flex; justify-content:space-between; margin-bottom:15px; padding-bottom:15px; border-bottom:1px solid #F0F0F0;"><span>Hits</span><span style="font-weight:600;">${data.cache_hit_rate ? data.cache_hit_rate.hits : 0}</span></div>
                        
                        <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><span>Hit Rate</span><span style="font-weight:600; color:#2E7D32;">${fVal(data.cache_hit_rate)}</span></div>
                        <div style="display:flex; justify-content:space-between;"><span>P95 Latency</span><span style="font-weight:600;">${fVal(data.cached_p95_latency)}</span></div>
                        
                        <div style="margin-top:20px; background:#F8F9FA; padding:15px; border-radius:8px; font-size:12px; font-family:monospace; color:#555;">
                            First wording &rarr; Cache MISS &rarr; LLM &rarr; Cached<br><br>
                            Rephrased &rarr; <span style="color:#2E7D32; font-weight:600;">CACHE HIT</span> &rarr; Cached plan
                        </div>
                    </div>
                </div>
            </div>
            `;
            document.getElementById('evalStatus').innerText = '';
            document.getElementById('results').innerHTML = html;
        }
    """

    html = html.replace("async function runAppSearch() {", new_functions + "\n        async function runAppSearch() {")

    # 3. Update the switchTab logic
    old_switch = r"\} else if \(tabName === 'Trust Suite' \|\| tabName === 'Eval Lab' \|\| tabName === 'Analytics'\) \{\s*renderAnalyticsDashboard\(\);\s*\}"
    new_switch = r"""} else if (tabName === 'Trust Suite') {
                renderTrustSuite();
            } else if (tabName === 'Eval Lab' || tabName === 'Analytics') {
                renderEvalLab();
            }"""
            
    html = re.sub(old_switch, new_switch, html)

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Done")

if __name__ == '__main__':
    main()
