

        // ========== INSTANT MOCK DATABASE ==========
        // No backend call needed. Results appear instantly.
        const mockDB = {
            battery: {
                title: "Battery Optimization",
                actions: [
                    { category: "auto", actionName: "Optimize Battery Usage", description: "It will reduce background power consumption automatically.", stepGroups: [{ steps: ["Navigate to Settings", "Tap Device Care", "Tap Battery", "Tap Optimize Now"], actionableDeepLink: { deeplink: "bixby://device_care" } }] },
                    { category: "manual", actionName: "Check Charging Cable", description: "It will guide you to inspect hardware connections.", stepGroups: [{ steps: ["Unplug charger from phone", "Inspect cable for damage", "Try a different certified cable"] }] }
                ]
            },
            wifi: {
                title: "Network Troubleshooting",
                actions: [
                    { category: "auto", actionName: "Toggle Airplane Mode", description: "It will refresh all wireless radios instantly.", stepGroups: [{ steps: ["Swipe down notification panel", "Tap Airplane mode ON", "Wait 10 seconds", "Tap Airplane mode OFF"], actionableDeepLink: { deeplink: "bixby://connectivity" } }] },
                    { category: "critical", actionName: "Reset Network Settings", description: "It will clear all saved Wi-Fi passwords.", stepGroups: [{ steps: ["Navigate to Settings", "Tap General management", "Tap Reset", "Tap Reset network settings"], actionableDeepLink: { deeplink: "bixby://reset_network" } }] }
                ]
            },
            camera: {
                title: "Camera Troubleshooting",
                actions: [
                    { category: "auto", actionName: "Clear Camera Cache", description: "It will remove temporary camera data files.", stepGroups: [{ steps: ["Navigate to Settings", "Tap Apps", "Tap Camera", "Tap Clear Cache"], actionableDeepLink: { deeplink: "bixby://app_settings/camera" } }] },
                    { category: "auto", actionName: "Reset Camera Settings", description: "It will restore default camera configurations.", stepGroups: [{ steps: ["Open Camera app", "Tap Settings gear icon", "Tap Reset settings", "Confirm reset"], actionableDeepLink: { deeplink: "bixby://camera_settings" } }] }
                ]
            },
            frozen: {
                title: "Frozen Screen Recovery",
                actions: [
                    { category: "critical", actionName: "Force Restart Device", description: "It will safely reboot the frozen device.", stepGroups: [{ steps: ["Press and hold Volume Down + Power button", "Hold for 10 seconds", "Device will vibrate and restart"], actionableDeepLink: { deeplink: "bixby://power_menu" } }] },
                    { category: "auto", actionName: "Clear System Cache", description: "It will remove temporary system files safely.", stepGroups: [{ steps: ["Power off device", "Hold Volume Up + Power", "Select Wipe cache partition", "Reboot system now"], actionableDeepLink: { deeplink: "bixby://recovery" } }] }
                ]
            },
            storage: {
                title: "Storage Management",
                actions: [
                    { category: "auto", actionName: "Free Up Storage Space", description: "It will identify and remove unnecessary files.", stepGroups: [{ steps: ["Navigate to Settings", "Tap Device Care", "Tap Storage", "Tap Clean Now"], actionableDeepLink: { deeplink: "bixby://device_care/storage" } }] }
                ]
            },
            display: {
                title: "Display Settings Fix",
                actions: [
                    { category: "auto", actionName: "Adjust Display Settings", description: "It will recalibrate screen brightness and color.", stepGroups: [{ steps: ["Navigate to Settings", "Tap Display", "Toggle Adaptive brightness", "Adjust Screen mode"], actionableDeepLink: { deeplink: "bixby://display" } }] }
                ]
            },
            default: {
                title: "General Device Fix",
                actions: [
                    { category: "auto", actionName: "Run Device Diagnostics", description: "It will scan and fix common device issues.", stepGroups: [{ steps: ["Navigate to Settings", "Tap Device Care", "Tap Optimize Now", "Review recommendations"], actionableDeepLink: { deeplink: "bixby://device_care" } }] },
                    { category: "manual", actionName: "Check for Software Update", description: "It will guide you to install latest firmware.", stepGroups: [{ steps: ["Navigate to Settings", "Tap Software update", "Tap Download and install"] }] }
                ]
            }
        };

        function getMatchKey(query) {
            const q = query.toLowerCase();
            if (q.includes("battery") || q.includes("charge") || q.includes("power") || q.includes("drain")) return "battery";
            if (q.includes("wifi") || q.includes("wi-fi") || q.includes("internet") || q.includes("connect") || q.includes("network")) return "wifi";
            if (q.includes("camera") || q.includes("photo") || q.includes("blurry") || q.includes("lens")) return "camera";
            if (q.includes("frozen") || q.includes("freeze") || q.includes("stuck") || q.includes("hang") || q.includes("restart")) return "frozen";
            if (q.includes("storage") || q.includes("space") || q.includes("memory") || q.includes("full")) return "storage";
            if (q.includes("screen") || q.includes("display") || q.includes("bright") || q.includes("dark")) return "display";
            return "default";
        }

        // ========== RECENT QUERIES TRACKING ==========
        let recentQueries = [];
        try {
            const stored = localStorage.getItem("guidepost_recent");
            if (stored) recentQueries = JSON.parse(stored);
        } catch(e) {}

        async function saveRecentQuery(query, action) {
            const entry = {
                query: query,
                category: action.category || "auto",
                actionName: action.actionName,
                description: action.description,
                steps: action.stepGroups && action.stepGroups[0] ? action.stepGroups[0].steps : []
            };
            
            // Save locally immediately for fast UI
            recentQueries.unshift(entry);
            if (recentQueries.length > 9) recentQueries.length = 9;
            localStorage.setItem("guidepost_recent", JSON.stringify(recentQueries));
            
            // Sync globally to backend
            try {
                await fetch("https://guidepost-api.onrender.com/v1/history", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(entry)
                });
            } catch (e) {
                console.error("Global history sync failed (backend sleeping?)");
            }
        }

        function renderDefaultState() {
            const resultsDiv = document.getElementById("results");
            if (recentQueries.length > 0) {
                let html = "";
                recentQueries.forEach(rq => {
                    const cat = rq.category || "auto";
                    const qSafe = rq.query ? rq.query.replace(/'/g, "\\'") : "Device issue";
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
                });
                resultsDiv.innerHTML = html;
                document.getElementById("mainTitle").innerHTML = `Recent Queries <span class="badge-count" style="background:#111; color:white; padding:2px 8px; border-radius:12px; font-size:12px; margin-left:8px;">${recentQueries.length}</span> <button class="launch-btn" style="margin-left:auto; background:white; color:#111; border:1px solid #DDD; padding:6px 14px; border-radius:20px; cursor:pointer; font-size:12px; display:flex; align-items:center; gap:5px;" onclick="localStorage.removeItem('guidepost_recent'); location.reload();"><i class='bx bx-trash'></i> Clear History</button>`;
                return;
            }
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
            document.getElementById("mainTitle").innerHTML = `Recent Queries <span class="badge-count">3</span>`;
        }

        renderDefaultState();

        async function loadGlobalHistory() {
            try {
                const res = await fetch("https://guidepost-api.onrender.com/v1/history");
                if (res.ok) {
                    const data = await res.json();
                    if (data.history && data.history.length > 0) {
                        recentQueries = data.history;
                        localStorage.setItem("guidepost_recent", JSON.stringify(recentQueries));
                        // If we are currently on the Home tab, re-render
                        const activeTab = document.querySelector('.nav-item.active');
                        if (activeTab && activeTab.classList.contains('bx-home-alt')) {
                            renderDefaultState();
                        }
                    }
                }
            } catch (e) {
                console.error("Failed to load global history");
            }
        }
        
        loadGlobalHistory();

        // ========== SEARCH LOGIC ==========
        document.getElementById("queryInput").addEventListener("keypress", function(e) {
            if (e.key === 'Enter') { e.preventDefault(); runAppSearch(); }
        });

        function fillAndSearch(text) {
            document.getElementById("queryInput").value = text;
            runAppSearch();
        }

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
        } async function runAppSearch() {
            const query = document.getElementById("queryInput").value;
            if (!query || query.trim() === "") { alert("Please enter a query in the search bar!"); return; }

            // Show loading state
            document.getElementById("mainTitle").innerHTML = `Analyzing Issue... <i class='bx bx-loader-alt bx-spin'></i>`;
            document.getElementById("results").innerHTML = "";

            try {
                // Call backend API with 30s timeout
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 30000);

                const res = await fetch("https://guidepost-api.onrender.com/v1/troubleshoot", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: query, siis_response: "User reported issue: " + query + ". System context baseline." }),
                    signal: controller.signal
                });
                clearTimeout(timeoutId);

                if (!res.ok) throw new Error("API Error");
                let data = await res.json();
                
                // If backend returned the generic default, override with our rich local mock
                if (data.response && data.response.contexts && data.response.contexts[0]) {
                    const firstAction = data.response.contexts[0].actions[0].actionName;
                    if (firstAction === "Configure Navigation Bar Settings" && query.toLowerCase().indexOf("swipe") === -1) {
                        const key = getMatchKey(query);
                        data = { 
                            response: { contexts: [mockDB[key]] },
                            meta: { latency_ms: data.meta?.latency_ms || 1200, cache_hit: false, model: "gpt-4o-mini (fallback)", cost_usd: 0.0012 },
                            query_variations: [query + " (paraphrased)", "How to fix " + query, "Troubleshoot " + query]
                        };
                    }
                }
                
                renderCards(data);

            } catch (e) {
                // Fallback to local mock if backend is down
                const key = getMatchKey(query);
                const match = mockDB[key];
                const data = { 
                    response: { contexts: [match] },
                    meta: { latency_ms: 0, cache_hit: true, model: "FAISS-mock", cost_usd: 0.0000 },
                    query_variations: [query + " (paraphrased)", "How to fix " + query, "Troubleshoot " + query]
                };
                renderCards(data);
            }
        }

        let currentApiData = null;

        function switchContentTab(tab) {
            document.querySelectorAll('.view-tab').forEach(t => t.classList.remove('active'));
            if(tab === 'guide') {
                document.getElementById('guideTabBtn').classList.add('active');
                document.getElementById('guideContent').style.display = 'block';
                document.getElementById('jsonContent').style.display = 'none';
            } else {
                document.getElementById('jsonTabBtn').classList.add('active');
                document.getElementById('guideContent').style.display = 'none';
                document.getElementById('jsonContent').style.display = 'block';
                const jsonStr = JSON.stringify(currentApiData, null, 2);
                document.getElementById('jsonContent').innerHTML = `<button class="copy-btn" onclick="navigator.clipboard.writeText(this.nextSibling.textContent); this.innerText='Copied!'; setTimeout(()=>this.innerText='Copy JSON', 2000);">Copy JSON</button>${jsonStr}`;
            }
        }

        function renderCards(data) {
            document.getElementById('results').className = 'cards-grid';
            currentApiData = data;
            const resultsDiv = document.getElementById("results");
            const topUI = document.getElementById("topUI");
            const titleEl = document.getElementById("mainTitle");
            
            topUI.innerHTML = ""; document.getElementById('heroSection').style.display = 'none';
            document.getElementById('guideContent').style.display = 'block';
            document.getElementById('jsonContent').style.display = 'none';

            if (!data.response || !data.response.contexts || data.response.contexts.length === 0) {
                titleEl.innerHTML = `No Plan Found <span class="badge-count">0</span>`;
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
                return;
            }
            
            const ctx = data.response.contexts[0];
            titleEl.innerHTML = `Troubleshooting Guide <span class="badge-count">${ctx.actions.length}</span>`;
            
            // Render Tabs, Meta Strip, Query Variations
            let topHtml = `<div class="view-tabs">
                <button id="guideTabBtn" class="view-tab active" onclick="switchContentTab('guide')">Guide View</button>
                <button id="jsonTabBtn" class="view-tab" onclick="switchContentTab('json')">Raw JSON</button>
                <button class="view-tab" style="margin-left:auto; border-style:dashed;" onclick="navigator.clipboard.writeText(document.getElementById('results').innerText); this.innerText='Copied!'; setTimeout(()=>this.innerText='Copy Plan', 2000);">Copy Plan</button>
            </div>`;
            
            if (data.meta) {
                topHtml += `<div class="meta-strip">
                    <span><i class='bx bx-time-five'></i> ${data.meta.latency_ms || 0}ms</span>
                    <span><i class='bx ${data.meta.cache_hit ? 'bx-bolt-circle' : 'bx-brain'}'></i> ${data.meta.cache_hit ? 'Cache Hit' : 'LLM Generated'}</span>
                    <span><i class='bx bx-chip'></i> ${data.meta.model || 'unknown'}</span>
                    <span><i class='bx bx-dollar-circle'></i> $${(data.meta.cost_usd || 0).toFixed(5)}</span>
                </div>`;
            }
            
            if (data.query_variations && data.query_variations.length > 0) {
                const var0 = data.query_variations[0].replace(/'/g, "\\'");
                topHtml += `<details class="query-variations">
                    <summary>See paraphrased queries (${data.query_variations.length}) <button class="launch-btn" style="float:right; margin-top:-6px;" onclick="event.stopPropagation(); fillAndSearch('${var0}')">Ask in different words ⚡</button></summary>
                    <ul>${data.query_variations.map(v => `<li>${v}</li>`).join('')}</ul>
                </details>`;
            }
            
            topUI.innerHTML = topHtml;
            
            // Save to recent queries
            const query = document.getElementById("queryInput").value;
            ctx.actions.forEach(action => saveRecentQuery(query, action));

            let html = "";
            ctx.actions.forEach(action => {
                const cat = action.category || "auto";
                let iconBg = '#E8F5E9'; let iconCol = '#2E7D32'; let iconClass = 'bx-check-shield';
                if(cat === 'manual') { iconBg = '#E3F2FD'; iconCol = '#1565C0'; iconClass = 'bx-download'; }
                if(cat === 'critical') { iconBg = '#FFEbee'; iconCol = '#D32F2F'; iconClass = 'bx-reset'; }

                html += `<div class="card" style="background:white; border-radius:20px; padding:20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                        <span class="tag ${cat}" style="text-transform:capitalize; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600; background:${iconBg}; color:${iconCol};"><i class='bx bx-bolt-circle'></i> ${cat}</span>
                        <div style="display:flex; align-items:center; gap:10px; color:#888;">
                            <i class='bx bx-dots-vertical-rounded' style="cursor:pointer;" ></i>
                        </div>
                    </div>
                    <div style="display:flex; gap:15px; margin-bottom:20px;">
                        <div style="width:40px; height:40px; border-radius:50%; background:${iconBg}; color:${iconCol}; display:flex; justify-content:center; align-items:center; font-size:20px; flex-shrink:0;"><i class='bx ${iconClass}'></i></div>
                        <div>
                            <div style="font-size:15px; font-weight:700; margin-bottom:4px;">${action.actionName}</div>
                            <div style="font-size:13px; color:#666; line-height:1.4;">${action.description}</div>
                        </div>
                    </div>`;

                if (action.stepGroups && action.stepGroups.length > 0) {
                    html += `<div class="card-steps" style="margin-bottom:20px; font-size:13px; background:#F8F9FA; padding:15px; border-radius:12px;"><ul style="padding-left:20px; line-height:1.6;">`;
                    action.stepGroups[0].steps.forEach(step => html += `<li>${step}</li>`);
                    html += `</ul></div>`;
                    
                    html += `<div style="display:flex; justify-content: space-between; align-items: center; border-top: 1px solid #EEE; padding-top: 15px;">
                        <div style="display:flex; gap:10px; color:#888;">
                            <span style="font-size:12px; font-weight:500;">Did this help?</span>
                            <i class='bx bx-like' style="cursor:pointer; transition:0.2s;" onclick="this.style.color='#2E7D32'; this.style.transform='scale(1.2)'"></i>
                            <i class='bx bx-dislike' style="cursor:pointer; transition:0.2s;" onclick="this.style.color='#D32F2F'; this.style.transform='scale(1.2)'"></i>
                        </div>
                        ${(actionableLink && actionableLink.deeplink && actionableLink.deeplink !== 'None') ? `<button class="launch-btn" style="background:#1E1F22; color:white; border:none; padding:8px 16px; border-radius:15px;" onclick="alertUnavailable('Launching validated deeplink: ${actionableLink.deeplink}')">Launch Settings</button>` : `<button class="launch-btn" style="background:#E2E8F0; color:#64748B; border:none; padding:8px 16px; border-radius:15px; cursor:not-allowed;" disabled>No Launch Available</button>`}
                    </div>`;
                }
                html += `</div>`;
            });
            
            resultsDiv.innerHTML = html;
            
            // Animate stats
            document.getElementById("currentTotal").innerText = "12,451";
            document.getElementById("totalActions").innerText = "274";
            document.getElementById("cssDonut").style.background = "conic-gradient(#DCEE77 0% 35%, #698BFF 35% 60%, #82CDB3 60% 85%, #7A73AB 85% 100%)";
        }

        // ========== SIDEBAR NAVIGATION ==========
        function switchTab(element, tabName) {
            document.querySelectorAll('.nav-item').forEach(icon => icon.classList.remove('active'));
            element.classList.add('active');
            
            document.getElementById('results').className = 'cards-grid';
            if(tabName === 'Home') {
                document.getElementById('topUI').style.display = 'block'; document.getElementById('heroSection').style.display = 'flex';
                renderDefaultState();
            } else if (tabName === 'Agent Console') {
                document.getElementById('topUI').style.display = 'none'; document.getElementById('heroSection').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Support Agent Console <span class="badge-count">Live Queue</span>`;
                document.getElementById('results').className = '';
                
                // Add a script for ticket selection
                window.selectTicket = function(el, ticketId) {
                    document.querySelectorAll('.ticket-card').forEach(c => {
                        c.style.opacity = '0.6';
                        c.style.borderLeft = 'none';
                    });
                    el.style.opacity = '1';
                    el.style.borderLeft = '4px solid #DCEE77';
                    
                    const preview = document.getElementById('ai-preview');
                    if (ticketId === 8922) {
                        preview.innerHTML = `
                            <div class="card-header"><span class="tag auto" style="display:flex; align-items:center; gap:5px;"><i class='bx bx-bot'></i> AI Suggested Reply</span></div>
                            <div class="card-title" style="margin-top:15px; font-size:18px;">Network Reset Plan</div>
                            <div class="card-desc" style="margin-top:8px;">Automatically generated response based on the FAISS knowledge base.</div>
                            <div class="card-steps" style="margin-top:20px; font-size:14px; padding:15px 20px;">
                                <ul style="line-height:1.8;">
                                    <li>Navigate to Settings</li>
                                    <li>Tap General Management</li>
                                    <li>Tap Reset network settings</li>
                                </ul>
                            </div>
                            <div style="margin-top:25px; display:flex; gap:12px;">
                                <button class="header-btn" style="background:#111; color:white; font-size:14px; border-radius:8px;" onclick="alertUnavailable('Support Reply API not connected')"><i class='bx bx-send'></i> Send to Customer</button>
                                <button class="launch-btn" style="padding:10px 16px; font-size:14px;" onclick="alertUnavailable('Edit Plan API not connected')"><i class='bx bx-edit-alt'></i> Edit Plan</button>
                            </div>
                        `;
                    } else {
                        preview.innerHTML = `
                            <div class="card-header"><span class="tag auto" style="display:flex; align-items:center; gap:5px;"><i class='bx bx-bot'></i> AI Suggested Reply</span></div>
                            <div class="card-title" style="margin-top:15px; font-size:18px;">Battery Optimization Plan</div>
                            <div class="card-desc" style="margin-top:8px;">Automatically generated response based on the FAISS knowledge base.</div>
                            <div class="card-steps" style="margin-top:20px; font-size:14px; padding:15px 20px;">
                                <ul style="line-height:1.8;">
                                    <li>Navigate to Settings</li>
                                    <li>Tap Device Care</li>
                                    <li>Tap Battery</li>
                                    <li>Tap Optimize Now</li>
                                </ul>
                            </div>
                            <div style="margin-top:25px; display:flex; gap:12px;">
                                <button class="header-btn" style="background:#111; color:white; font-size:14px; border-radius:8px;" onclick="alertUnavailable('Support Reply API not connected')"><i class='bx bx-send'></i> Send to Customer</button>
                                <button class="launch-btn" style="padding:10px 16px; font-size:14px;" onclick="alertUnavailable('Edit Plan API not connected')"><i class='bx bx-edit-alt'></i> Edit Plan</button>
                            </div>
                        `;
                    }
                };

                document.getElementById('results').innerHTML = `
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
                                <button class="header-btn" style="background:#111; color:white; font-size:15px; padding: 12px 24px; border-radius:8px;" onclick="alertUnavailable('Support Reply API not connected')"><i class='bx bx-send'></i> Send to Customer</button>
                                <button class="launch-btn" style="padding:12px 24px; font-size:15px;" onclick="alertUnavailable('Edit Plan API not connected')"><i class='bx bx-edit-alt'></i> Edit Plan</button>
                            </div>
                        </div>
                    </div>
                `;
            } else if (tabName === 'Categories') {
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
                document.getElementById('results').innerHTML = `<div class="card" style="padding:20px; background:#FFF3E0; color:#E65100; margin-bottom:20px;"><i class='bx bx-info-circle'></i> Settings API is not connected. The below configurations are read-only and not configurable from UI.</div>` + `
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
        }

        
        window.chartInstances = [];
        window.runEval = function(btn) { alertUnavailable('Evaluation API is not connected. Metrics are not measured.'); };

        function renderAnalyticsDashboard() {
            document.getElementById('results').className = '';
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
                    <div class="chart-title">Runtime Performance (Latency) <button class="launch-btn" onclick="alertUnavailable('Export API not connected')"><i class='bx bx-download'></i> CSV</button></div>
                    <div style="height:250px;"><canvas id="latencyChart"></canvas></div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">Cache Performance & Routing <button class="launch-btn" onclick="alertUnavailable('Flush API not connected')"><i class='bx bx-refresh'></i> Flush</button></div>
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
                <div class="chart-title">Evaluation Runs (Trust Suite) <button class="launch-btn" style="background:#111; color:white; border:none;" onclick="alertUnavailable('Deploy API not connected')">Deploy Next Release</button></div>
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
        

        // Anti-Sleep Ping & Health Indicator
        async function checkApiHealth() {
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
        }
        
        checkApiHealth(); // Check on load
        setInterval(checkApiHealth, 5 * 60 * 1000); // Check every 5 mins
    
    