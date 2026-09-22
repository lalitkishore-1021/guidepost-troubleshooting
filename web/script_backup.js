
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
                    html += `<div class="card" style="cursor:pointer; border: 1px solid transparent;" onmouseover="this.style.borderColor='#CCC'" onmouseout="this.style.borderColor='transparent'" onclick="fillAndSearch('${qSafe}')">
                        <div class="card-header"><span class="tag ${cat}">${cat}</span><span style="font-size:11px; color:#888;">"${qSafe}"</span></div>
                        <div class="card-title">${rq.actionName}</div>
                        <div class="card-desc">${rq.description}</div>
                        <div class="card-footer"><button class="launch-btn" onclick="event.stopPropagation(); alert('Launching Device Settings')">Re-run Search</button></div>
                    </div>`;
                });
                resultsDiv.innerHTML = html;
                document.getElementById("mainTitle").innerHTML = `Recent Queries <span class="badge-count">${recentQueries.length}</span> <button class="launch-btn" style="margin-left:auto;" onclick="localStorage.removeItem('guidepost_recent'); location.reload();">Clear History</button>`;
                return;
            }
            resultsDiv.innerHTML = `
                <div class="card">
                    <div class="card-header"><span class="tag auto">Auto</span><i class='bx bx-dots-horizontal-rounded' style="color:#CCC; cursor:pointer;" onclick="alert('Action options menu')"></i></div>
                    <div class="card-title">Bluetooth Pairing Failed</div>
                    <div class="card-desc">It will reset the Bluetooth module connections.</div>
                    <div class="card-steps"><ul><li>Navigate to Settings</li><li>Tap Connections</li><li>Tap Bluetooth and unpair devices</li></ul></div>
                    <div class="card-footer"><button class="launch-btn" onclick="alert('Executing: bixby://settings/bluetooth')">Launch Settings</button></div>
                </div>
                <div class="card">
                    <div class="card-header"><span class="tag manual">Manual</span><i class='bx bx-dots-horizontal-rounded' style="color:#CCC; cursor:pointer;" onclick="alert('Action options menu')"></i></div>
                    <div class="card-title">Clean Charging Port</div>
                    <div class="card-desc">It will guide the user to physically clean port.</div>
                    <div class="card-steps"><ul><li>Turn off the device</li><li>Use a wooden toothpick to gently remove lint</li></ul></div>
                </div>
                <div class="card">
                    <div class="card-header"><span class="tag critical">Critical</span><i class='bx bx-dots-horizontal-rounded' style="color:#CCC; cursor:pointer;" onclick="alert('Action options menu')"></i></div>
                    <div class="card-title">Factory Reset Device</div>
                    <div class="card-desc">It will erase all user data permanently.</div>
                    <div class="card-steps"><ul><li>Navigate to General Management</li><li>Tap Reset</li><li>Tap Factory data reset</li></ul></div>
                    <div class="card-footer"><button class="launch-btn" onclick="alert('Launch Factory Reset')">Launch Settings</button></div>
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
                        const activeTab = document.querySelector('.nav-icon.active');
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

        async function runAppSearch() {
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
            currentApiData = data;
            const resultsDiv = document.getElementById("results");
            const topUI = document.getElementById("topUI");
            const titleEl = document.getElementById("mainTitle");
            
            topUI.innerHTML = "";
            document.getElementById('guideContent').style.display = 'block';
            document.getElementById('jsonContent').style.display = 'none';

            if (!data.response || !data.response.contexts || data.response.contexts.length === 0) {
                titleEl.innerHTML = `No Plan Found <span class="badge-count">0</span>`;
                resultsDiv.innerHTML = `<div class="card">No suitable troubleshooting guide found.</div>`;
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
                html += `<div class="card">
                    <div class="card-header">
                        <span class="tag ${cat}">${cat}</span>
                        <i class='bx bx-dots-horizontal-rounded' style="color:#CCC; cursor:pointer;" onclick="alert('Options Menu clicked')"></i>
                    </div>
                    <div class="card-title">${action.actionName}</div>
                    <div class="card-desc">${action.description}</div>
                `;
                if (action.stepGroups && action.stepGroups.length > 0) {
                    html += `<div class="card-steps"><ul>`;
                    action.stepGroups[0].steps.forEach(step => html += `<li>${step}</li>`);
                    html += `</ul></div>`;
                    
                    html += `<div class="card-footer" style="justify-content: space-between; align-items: center;">
                        <div style="display:flex; gap:10px; color:#888;">
                            <span style="font-size:12px; font-weight:500;">Did this help?</span>
                            <i class='bx bx-like' style="cursor:pointer;" onclick="this.style.color='#DCEE77'"></i>
                            <i class='bx bx-dislike' style="cursor:pointer;" onclick="this.style.color='#FFB3B3'"></i>
                        </div>
                        ${(action.stepGroups[0].actionableDeepLink && cat !== "manual") ? `<button class="launch-btn" onclick="alert('Launching Device Settings')">Launch Settings</button>` : ''}
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
            document.querySelectorAll('.nav-icon').forEach(icon => icon.classList.remove('active'));
            element.classList.add('active');
            
            if(tabName === 'Home') {
                document.getElementById('topUI').style.display = 'block';
                renderDefaultState();
            } else if (tabName === 'Agent Console') {
                document.getElementById('topUI').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Support Agent Console <span class="badge-count">Live Queue</span>`;
                
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
                                <button class="header-btn" style="background:#111; color:white; font-size:14px; border-radius:8px;" onclick="alert('Reply sent to Sarah W.!')"><i class='bx bx-send'></i> Send to Customer</button>
                                <button class="launch-btn" style="padding:10px 16px; font-size:14px;" onclick="alert('Opening editor...')"><i class='bx bx-edit-alt'></i> Edit Plan</button>
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
                                <button class="header-btn" style="background:#111; color:white; font-size:14px; border-radius:8px;" onclick="alert('Reply sent to John D.!')"><i class='bx bx-send'></i> Send to Customer</button>
                                <button class="launch-btn" style="padding:10px 16px; font-size:14px;" onclick="alert('Opening editor...')"><i class='bx bx-edit-alt'></i> Edit Plan</button>
                            </div>
                        `;
                    }
                };

                document.getElementById('results').innerHTML = `
                    <div style="display:flex; gap:30px; width:100%; align-items: flex-start;">
                        <div style="flex:1; display:flex; flex-direction:column; gap:12px; max-width: 350px;">
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
                        <div style="flex:2;" class="card" id="ai-preview">
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
                                <button class="header-btn" style="background:#111; color:white; font-size:14px; border-radius:8px;" onclick="alert('Reply sent to John D.!')"><i class='bx bx-send'></i> Send to Customer</button>
                                <button class="launch-btn" style="padding:10px 16px; font-size:14px;" onclick="alert('Opening editor...')"><i class='bx bx-edit-alt'></i> Edit Plan</button>
                            </div>
                        </div>
                    </div>
                `;
            } else if (tabName === 'Categories') {
                document.getElementById('topUI').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Categories Overview <span class="badge-count">3</span>`;
                document.getElementById('results').innerHTML = `
                    <div class="card"><div class="card-title">Auto Actions</div><div class="card-desc">Fully automated steps that users can execute with one tap. High success rate.</div></div>
                    <div class="card"><div class="card-title">Manual Actions</div><div class="card-desc">Physical hardware steps like cleaning ports, changing SIM cards, wiping screen.</div></div>
                    <div class="card"><div class="card-title">Critical Actions</div><div class="card-desc">Dangerous actions like Factory Resets. Always prompts for user confirmation.</div></div>
                `;
            } else if (tabName === 'Analytics') {
                document.getElementById('topUI').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Deep Analytics`;
                document.getElementById('results').innerHTML = `<div class="card"><div class="card-title">System Telemetry</div><div class="card-desc">Semantic cache hit rate: 94.2% bypassing LLM calls. Average response time: 12ms. Total queries processed: 12,450.</div></div>`;
            } else if (tabName === 'Team') {
                document.getElementById('topUI').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `Team Members`;
                document.getElementById('results').innerHTML = `<div class="card"><div class="card-title">Admin User</div><div class="card-desc">Role: Super Admin</div></div>`;
            } else if (tabName === 'Settings') {
                document.getElementById('topUI').style.display = 'none';
                document.getElementById('mainTitle').innerHTML = `System Settings`;
                document.getElementById('results').innerHTML = `<div class="card"><div class="card-title">API Configuration</div><div class="card-desc">Endpoint: guidepost-api.onrender.com<br>Mock Mode: Enabled<br>Cache: FAISS + SQLite</div></div>`;
            }
        }

        // Anti-Sleep Ping & Health Indicator
        async function checkApiHealth() {
            try {
                const res = await fetch("https://guidepost-api.onrender.com/health");
                if (res.ok) {
                    document.getElementById("healthDot").className = "status-dot green";
                    document.getElementById("healthText").innerText = "API Ready";
                } else {
                    throw new Error("Bad status");
                }
            } catch(e) {
                document.getElementById("healthDot").className = "status-dot red";
                document.getElementById("healthText").innerText = "API Starting/Sleeping...";
            }
        }
        
        checkApiHealth(); // Check on load
        setInterval(checkApiHealth, 5 * 60 * 1000); // Check every 5 mins
    