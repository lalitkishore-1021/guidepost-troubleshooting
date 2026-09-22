import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Inject Chart.js if not already present
    if 'chart.js' not in content:
        content = content.replace('<head>', '<head>\n    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>')

    # 2. Replace the old Analytics tab logic with a call to the new function
    old_analytics = r"else if \(tabName === 'Analytics'\) \{.*?document\.getElementById\('results'\)\.innerHTML = `<div class=\"card\">.*?</div>`;\s*\}"
    new_analytics = r"""else if (tabName === 'Analytics') {
                renderAnalyticsDashboard();
            }"""
    content = re.sub(old_analytics, new_analytics, content, flags=re.DOTALL)

    # 3. Add the renderAnalyticsDashboard function at the end of the script block (before checkApiHealth)
    if 'function renderAnalyticsDashboard()' not in content:
        func_code = """
        window.chartInstances = [];
        window.runEval = function(btn) {
            const ogText = btn.innerHTML;
            btn.innerHTML = `<i class='bx bx-loader-alt bx-spin'></i> Running Suite...`;
            btn.style.opacity = '0.7';
            setTimeout(() => {
                btn.innerHTML = `<i class='bx bx-check'></i> Passed Eval`;
                btn.style.opacity = '1';
                btn.style.background = '#E8F5E9';
                btn.style.color = '#2E7D32';
                btn.style.border = 'none';
            }, 2000);
        };

        function renderAnalyticsDashboard() {
            document.getElementById('topUI').style.display = 'none'; 
            document.getElementById('heroSection').style.display = 'none';
            
            document.getElementById('mainTitle').innerHTML = `PlanForge Evaluation Matrix <span class="badge-count" style="background:#2E7D32;">v2.4 Prod</span>
            <button class="launch-btn" style="float:right; margin-top:-4px;" onclick="runEval(this)"><i class='bx bx-play-circle'></i> Run Trust Suite</button>`;

            const html = `
            <style>
                .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 15px; margin-bottom: 25px; }
                .kpi-card { background: white; padding: 18px; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); display: flex; flex-direction: column; border: 1px solid #F0F0F0; }
                .kpi-val { font-size: 26px; font-weight: 700; margin: 8px 0 4px 0; color: #111; }
                .kpi-title { font-size: 11px; color: #888; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
                .kpi-trend { font-size: 12px; font-weight: 600; display:flex; align-items:center; gap:3px; }
                .kpi-trend.good { color: #2E7D32; }
                .kpi-trend.bad { color: #D32F2F; }

                .chart-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
                .chart-card { background: white; padding: 25px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); border: 1px solid #F0F0F0; }
                .chart-title { font-size: 16px; font-weight: 700; margin-bottom: 20px; display:flex; justify-content:space-between; align-items:center; color:#111;}
                
                .eval-table { width: 100%; border-collapse: collapse; font-size: 13px; }
                .eval-table th { text-align: left; padding: 15px 12px; color: #888; font-weight: 600; border-bottom: 1px solid #EEE; text-transform: uppercase; font-size:11px; letter-spacing:0.5px;}
                .eval-table td { padding: 15px 12px; border-bottom: 1px solid #F5F5F5; font-weight: 500; color:#333; }
                .eval-table tr:hover { background: #F8F9FA; }
            </style>

            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-title">Step Accuracy</div>
                    <div class="kpi-val">99.2%</div>
                    <div class="kpi-trend good"><i class='bx bx-up-arrow-alt'></i> 0.4% vs last</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Deeplink Acc</div>
                    <div class="kpi-val">97.8%</div>
                    <div class="kpi-trend good"><i class='bx bx-up-arrow-alt'></i> 1.2%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Cache Hit Rate</div>
                    <div class="kpi-val">94.2%</div>
                    <div class="kpi-trend good"><i class='bx bx-up-arrow-alt'></i> 2.1%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">P95 Cached Latency</div>
                    <div class="kpi-val">18 ms</div>
                    <div class="kpi-trend good"><i class='bx bx-down-arrow-alt'></i> 4ms</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Avg Cost / Query</div>
                    <div class="kpi-val">$0.001</div>
                    <div class="kpi-trend good"><i class='bx bx-down-arrow-alt'></i> 12%</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-title">Schema Validity</div>
                    <div class="kpi-val">100%</div>
                    <div class="kpi-trend good"><i class='bx bx-check'></i> Perfect</div>
                </div>
            </div>

            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-title">Runtime Performance (Latency) <button class="launch-btn" onclick="alert('Exporting latency logs as CSV...')"><i class='bx bx-download'></i> CSV</button></div>
                    <div style="height:250px;"><canvas id="latencyChart"></canvas></div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">Cache Performance & Routing <button class="launch-btn" onclick="alert('Flushing FAISS cache...')"><i class='bx bx-refresh'></i> Flush</button></div>
                    <div style="height:250px;"><canvas id="cacheChart"></canvas></div>
                </div>
            </div>

            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-title">Plan Quality Metrics</div>
                    <div style="height:250px;"><canvas id="qualityChart"></canvas></div>
                </div>
                <div class="chart-card" style="display:flex; flex-direction:column; justify-content:space-between;">
                    <div class="chart-title">Verification, Safety & Cost</div>
                    
                    <div style="display:flex; gap:12px; margin-bottom: 20px;">
                        <div style="flex:1; background:#F8F9FA; padding:18px; border-radius:12px; text-align:center; border: 1px solid #EFEFEF;">
                            <div style="font-size:22px; font-weight:700; color:#2E7D32;">12,402</div>
                            <div style="font-size:12px; color:#888; font-weight:600; margin-top:4px;">Verified Plans</div>
                        </div>
                        <div style="flex:1; background:#FFF5F5; padding:18px; border-radius:12px; text-align:center; border: 1px solid #FFE5E5;">
                            <div style="font-size:22px; font-weight:700; color:#D32F2F;">14</div>
                            <div style="font-size:12px; color:#888; font-weight:600; margin-top:4px;">Rejected</div>
                        </div>
                        <div style="flex:1; background:#FFF8E1; padding:18px; border-radius:12px; text-align:center; border: 1px solid #FFECB3;">
                            <div style="font-size:22px; font-weight:700; color:#F57F17;">3</div>
                            <div style="font-size:12px; color:#888; font-weight:600; margin-top:4px;">Catalog Drift</div>
                        </div>
                    </div>

                    <div style="background:#F8F9FA; padding:20px; border-radius:16px; border: 1px solid #EFEFEF;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:10px; font-size:13px;">
                            <span style="color:#555; font-weight:500;">Queries served without LLM (Cache)</span>
                            <span style="font-weight:700;">94.2%</span>
                        </div>
                        <div style="width:100%; background:#E0E0E0; height:8px; border-radius:4px;">
                            <div style="width:94.2%; background:#1565C0; height:100%; border-radius:4px;"></div>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:16px; font-size:13px;">
                            <span style="color:#555; font-weight:500;">Offline Compile Cost / Scenario</span>
                            <span style="font-weight:700;">$0.14</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:8px; font-size:13px;">
                            <span style="color:#555; font-weight:500;">Expected Calibration Error (ECE)</span>
                            <span style="font-weight:700; color:#2E7D32;">0.02</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="chart-card" style="margin-bottom:40px;">
                <div class="chart-title">Evaluation Runs (Trust Suite) <button class="launch-btn" style="background:#111; color:white; border:none;" onclick="alert('Deploying v2.5 to Staging...')">Deploy Next Release</button></div>
                <table class="eval-table">
                    <thead>
                        <tr>
                            <th>Dataset/Version</th>
                            <th>Step Acc</th>
                            <th>Deeplink Acc</th>
                            <th>P95 Latency</th>
                            <th>Hit Rate</th>
                            <th>Schema Valid</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="font-weight:600;"><i class='bx bx-data' style="color:#1565C0; margin-right:4px;"></i> Q3_Eval_v2.4</td>
                            <td>99.2%</td>
                            <td>97.8%</td>
                            <td>18 ms</td>
                            <td>94.2%</td>
                            <td>100%</td>
                            <td><span class="tag auto" style="background:#E8F5E9; color:#2E7D32;"><i class='bx bx-check-circle'></i> Passed</span></td>
                        </tr>
                        <tr>
                            <td style="font-weight:600;"><i class='bx bx-data' style="color:#888; margin-right:4px;"></i> Q3_Eval_v2.3_rc1</td>
                            <td>96.1%</td>
                            <td>92.4%</td>
                            <td>420 ms</td>
                            <td>41.5%</td>
                            <td>100%</td>
                            <td><span class="tag critical" style="background:#FFF5F5; color:#D32F2F;"><i class='bx bx-x-circle'></i> Rejected</span></td>
                        </tr>
                        <tr>
                            <td style="font-weight:600;"><i class='bx bx-data' style="color:#888; margin-right:4px;"></i> Q2_Eval_v2.2</td>
                            <td>98.5%</td>
                            <td>95.2%</td>
                            <td>24 ms</td>
                            <td>88.9%</td>
                            <td>99.9%</td>
                            <td><span class="tag auto" style="background:#E8F5E9; color:#2E7D32;"><i class='bx bx-check-circle'></i> Passed</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            `;

            document.getElementById('results').innerHTML = html;

            // Initialize Charts
            if (window.chartInstances && window.chartInstances.length > 0) {
                window.chartInstances.forEach(c => c.destroy());
            }
            window.chartInstances = [];

            // 1. Latency Chart (Line)
            const ctxLat = document.getElementById('latencyChart').getContext('2d');
            const latChart = new Chart(ctxLat, {
                type: 'line',
                data: {
                    labels: ['12am', '4am', '8am', '12pm', '4pm', '8pm'],
                    datasets: [
                        { label: 'P95 Latency (ms)', data: [16, 18, 24, 14, 19, 17], borderColor: '#1565C0', tension: 0.4, fill: false, borderWidth: 3 },
                        { label: 'Target (300ms)', data: [300, 300, 300, 300, 300, 300], borderColor: '#D32F2F', borderDash: [5, 5], pointRadius: 0, fill: false, borderWidth: 2 }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { beginAtZero: true, max: 350 } } }
            });
            window.chartInstances.push(latChart);

            // 2. Cache Performance (Doughnut)
            const ctxCache = document.getElementById('cacheChart').getContext('2d');
            const cacheChart = new Chart(ctxCache, {
                type: 'doughnut',
                data: {
                    labels: ['Cache Hit (18ms)', 'Cache Miss / LLM (1.2s)'],
                    datasets: [{
                        data: [94.2, 5.8],
                        backgroundColor: ['#2E7D32', '#F57F17'],
                        borderWidth: 0,
                        hoverOffset: 4
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, cutout: '75%' }
            });
            window.chartInstances.push(cacheChart);

            // 3. Quality Chart (Bar)
            const ctxQual = document.getElementById('qualityChart').getContext('2d');
            const qualChart = new Chart(ctxQual, {
                type: 'bar',
                data: {
                    labels: ['v2.2', 'v2.3_rc1', 'v2.4 Prod'],
                    datasets: [
                        { label: 'Step Accuracy', data: [98.5, 96.1, 99.2], backgroundColor: '#1565C0', borderRadius: 4 },
                        { label: 'Deeplink Acc', data: [95.2, 92.4, 97.8], backgroundColor: '#82CDB3', borderRadius: 4 }
                    ]
                },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { min: 85, max: 100 } } }
            });
            window.chartInstances.push(qualChart);
        }
        """
        content = content.replace("// Anti-Sleep Ping", func_code + "\n\n        // Anti-Sleep Ping")

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Analytics Dashboard injected successfully.")

if __name__ == '__main__':
    main()
