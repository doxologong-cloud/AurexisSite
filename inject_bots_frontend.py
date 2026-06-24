import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace Tab Bots HTML
new_bots_html = """            <!-- Bots Tab -->
            <div id="tab-bots" class="vault-tab" style="display: none; width: 100%; max-width: 900px; background: rgba(20,28,36,0.9); border: 1px solid #2b3a4a; border-radius: 12px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); backdrop-filter: blur(10px);">
                <h2 style="margin-top: 0; color: #fff; border-bottom: 1px solid #2b3a4a; padding-bottom: 15px; display: flex; justify-content: space-between;">
                    <span><i class="fa-solid fa-robot"></i> УПРАВЛЕНИЕ БОТАМИ</span>
                    <button style="background: transparent; border: 1px dashed #7f91a4; color: #7f91a4; cursor: pointer; padding: 5px 15px; border-radius: 4px;">+ ДОБАВИТЬ</button>
                </h2>
                <div id="bots-container" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                    <div style="color: #7f91a4;">Синхронизация с сервером...</div>
                </div>
            </div>"""

text = re.sub(r'<!-- Bots Tab -->.*?</div>\s*</div>\s*<!-- Panel \(Console\) Tab -->', new_bots_html + '\n\n            <!-- Panel (Console) Tab -->', text, flags=re.DOTALL)

# Inject Bots JS Logic
bots_js = """
    // --- BOTS MANAGEMENT LOGIC ---
    let botsUpdateInterval;

    function renderBots(bots) {
        const container = document.getElementById('bots-container');
        if(container.innerHTML.includes('Синхронизация') && bots.length === 0) return;
        
        let html = '';
        bots.forEach(bot => {
            const isOnline = bot.status === 'ONLINE';
            const statusColor = isOnline ? '#4caf50' : '#ff4444';
            const btnColor = isOnline ? '#ff4444' : '#8774e1';
            const btnHover = isOnline ? '#cc0000' : '#7b68c9';
            const btnText = isOnline ? 'ОТКЛЮЧИТЬ' : 'ЗАПУСТИТЬ';
            const action = isOnline ? `stopBot('${bot.id}')` : `startBot('${bot.id}')`;
            
            // Checking if loading
            const btnId = `btn-${bot.id}`;
            const btnState = window[`state_${btnId}`] || btnText;
            const disabled = btnState.includes('...') ? 'disabled' : '';
            const finalBtnColor = btnState.includes('...') ? '#ffbb33' : btnColor;
            
            html += `
                <div style="background: #1c242d; border: 1px solid #232e3c; border-radius: 8px; padding: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <div style="font-weight: bold; font-size: 1.1rem; color: #fff;">${bot.name}</div>
                        <div style="color: ${statusColor}; font-size: 0.8rem; border: 1px solid ${statusColor}; padding: 2px 8px; border-radius: 10px;">${bot.status}</div>
                    </div>
                    <p style="color: #7f91a4; font-size: 0.9rem; margin-bottom: 20px;">${bot.desc}</p>
                    <div style="display: flex; gap: 10px;">
                        <button id="${btnId}" ${disabled} onclick="${action}" style="flex: 1; background: ${finalBtnColor}; color: #fff; border: none; padding: 8px; border-radius: 4px; cursor: pointer; transition: 0.2s;" onmouseover="if(!this.disabled) this.style.background='${btnHover}'" onmouseout="if(!this.disabled) this.style.background='${finalBtnColor}'">${btnState}</button>
                        <button style="background: #2b3a4a; color: #fff; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer;"><i class="fa-solid fa-gear"></i></button>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    }

    function fetchBots() {
        fetch('/api/bots')
            .then(res => res.json())
            .then(data => {
                if(data.success) renderBots(data.bots);
            })
            .catch(err => console.error("Error fetching bots:", err));
    }

    function startBot(id) {
        window[`state_btn-${id}`] = "Загрузка...";
        fetchBots(); // Re-render to show loading
        
        fetch(`/api/bots/${id}/start`, { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                window[`state_btn-${id}`] = null;
                fetchBots();
            });
    }

    function stopBot(id) {
        window[`state_btn-${id}`] = "Отключение...";
        fetchBots();
        
        fetch(`/api/bots/${id}/stop`, { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                window[`state_btn-${id}`] = null;
                fetchBots();
            });
    }

    // Start polling when tab is opened
    const originalOpenTab = window.openTab;
    window.openTab = function(tabId) {
        originalOpenTab(tabId);
        if(tabId === 'bots') {
            fetchBots();
            if(!botsUpdateInterval) botsUpdateInterval = setInterval(fetchBots, 3000);
        } else {
            if(botsUpdateInterval) { clearInterval(botsUpdateInterval); botsUpdateInterval = null; }
        }
    };
"""

text = text.replace('// --- CONSOLE LOGIC ---', bots_js + '\n\n    // --- CONSOLE LOGIC ---')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Frontend bots logic injected.")
