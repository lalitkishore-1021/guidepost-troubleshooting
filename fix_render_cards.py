import re

def main():
    with open('web/index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # The block inside renderCards:
    old_block = r'''            ctx\.actions\.forEach\(action => \{
                const cat = action\.category \|\| "auto";
                html \+= `<div class="card">
                    <div class="card-header">
                        <span class="tag \$\{cat\}">\$\{cat\}</span>
                        <i class='bx bx-dots-horizontal-rounded' style="color:#CCC; cursor:pointer;" onclick="alert\('Options Menu clicked'\)"></i>
                    </div>
                    <div class="card-title">\$\{action\.actionName\}</div>
                    <div class="card-desc">\$\{action\.description\}</div>
                `;
                if \(action\.stepGroups && action\.stepGroups\.length > 0\) \{
                    html \+= `<div class="card-steps"><ul>`;
                    action\.stepGroups\[0\]\.steps\.forEach\(step => html \+= `<li>\$\{step\}</li>`\);
                    html \+= `</ul></div>`;
                    
                    html \+= `<div class="card-footer" style="justify-content: space-between; align-items: center;">
                        <div style="display:flex; gap:10px; color:#888;">
                            <span style="font-size:12px; font-weight:500;">Did this help\?</span>
                            <i class='bx bx-like' style="cursor:pointer;" onclick="this\.style\.color='#DCEE77'"></i>
                            <i class='bx bx-dislike' style="cursor:pointer;" onclick="this\.style\.color='#FFB3B3'"></i>
                        </div>
                        \$\{\(action\.stepGroups\[0\]\.actionableDeepLink && cat !== "manual"\) \? `<button class="launch-btn" onclick="alert\('Launching Device Settings'\)">Launch Settings</button>` : ''\}
                    </div>`;
                \}
                html \+= `</div>`;
            \}\);'''

    new_block = r'''            ctx.actions.forEach(action => {
                const cat = action.category || "auto";
                let iconBg = '#E8F5E9'; let iconCol = '#2E7D32'; let iconClass = 'bx-check-shield';
                if(cat === 'manual') { iconBg = '#E3F2FD'; iconCol = '#1565C0'; iconClass = 'bx-download'; }
                if(cat === 'critical') { iconBg = '#FFEbee'; iconCol = '#D32F2F'; iconClass = 'bx-reset'; }

                html += `<div class="card" style="background:white; border-radius:20px; padding:20px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
                        <span class="tag ${cat}" style="text-transform:capitalize; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600; background:${iconBg}; color:${iconCol};"><i class='bx bx-bolt-circle'></i> ${cat}</span>
                        <div style="display:flex; align-items:center; gap:10px; color:#888;">
                            <i class='bx bx-dots-vertical-rounded' style="cursor:pointer;" onclick="alert('Options Menu clicked')"></i>
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
                        ${(action.stepGroups[0].actionableDeepLink && cat !== "manual") ? `<button class="launch-btn" style="background:#1E1F22; color:white; border:none; padding:8px 16px; border-radius:15px;" onclick="alert('Launching Device Settings')">Launch Settings</button>` : ''}
                    </div>`;
                }
                html += `</div>`;
            });'''

    content = re.sub(old_block, new_block, content)

    # I also need to hide the heroSection when switching out of Home or when rendering search results.
    # In switchTab, `tabName === 'Home'` should `document.getElementById('heroSection').style.display = 'flex';`
    # Other tabs should `document.getElementById('heroSection').style.display = 'none';`
    content = content.replace("document.getElementById('topUI').style.display = 'block';", "document.getElementById('topUI').style.display = 'block'; document.getElementById('heroSection').style.display = 'flex';")
    content = content.replace("document.getElementById('topUI').style.display = 'none';", "document.getElementById('topUI').style.display = 'none'; document.getElementById('heroSection').style.display = 'none';")

    # In `renderCards`, hide heroSection too
    content = content.replace("topUI.innerHTML = \"\";", "topUI.innerHTML = \"\"; document.getElementById('heroSection').style.display = 'none';")

    with open('web/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated renderCards layout and hero display logic.")

if __name__ == '__main__':
    main()
