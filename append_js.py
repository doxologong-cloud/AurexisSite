import os

js_code = """
    // --- BOT BUILDER LOGIC ---
    const builderNameInput = document.getElementById('builder-bot-name');
    const builderColorInput = document.getElementById('builder-bot-color');
    const mockMessagesContainer = document.getElementById('discord-mock-messages');
    
    function updateMockBotIdentity() {
        const newName = builderNameInput ? builderNameInput.value || 'AUREXIS DEMO' : 'AUREXIS DEMO';
        const newColor = builderColorInput ? builderColorInput.value || '#e5b322' : '#e5b322';
        document.querySelectorAll('.discord-author').forEach(el => {
            el.textContent = newName;
            el.style.color = newColor;
        });
    }

    if (builderNameInput) builderNameInput.addEventListener('input', updateMockBotIdentity);
    if (builderColorInput) builderColorInput.addEventListener('input', updateMockBotIdentity);

    function addMockMessage(contentHTML) {
        const newName = builderNameInput ? builderNameInput.value || 'AUREXIS DEMO' : 'AUREXIS DEMO';
        const newColor = builderColorInput ? builderColorInput.value || '#e5b322' : '#e5b322';
        const msgDiv = document.createElement('div');
        msgDiv.className = 'discord-msg';
        msgDiv.innerHTML = `
            <img src="/static/assets/logo.png" class="discord-avatar">
            <div class="discord-msg-content">
                <div class="discord-msg-header">
                    <span class="discord-author" style="color: ${newColor};">${newName}</span>
                    <span class="discord-bot-tag">BOT</span>
                    <span class="discord-time">Только что</span>
                </div>
                <div class="discord-text">${contentHTML}</div>
            </div>
        `;
        if (mockMessagesContainer) {
            mockMessagesContainer.appendChild(msgDiv);
            mockMessagesContainer.scrollTop = mockMessagesContainer.scrollHeight;
        }
    }

    const modules = [
        { id: 'module-music', html: '<div class="discord-embed"><div class="discord-embed-title">🎵 Сейчас играет</div><div>Cyberpunk Mix 2026 - Synthwave Radio</div></div>' },
        { id: 'module-economy', html: '💰 <strong>@user</strong>, ваш баланс пополнен на 500 монет! Текущий баланс: 1500.' },
        { id: 'module-moderation', html: '🔨 <strong>@troll</strong> был предупрежден модератором <strong>@admin</strong>. Причина: Спам.' },
        { id: 'module-ai', html: '🧠 <em>Генерирую ответ...</em><br>Искусственный интеллект AUREXIS FLORA готов к работе. Задайте мне любой вопрос.' }
    ];

    modules.forEach(mod => {
        const toggle = document.getElementById(mod.id);
        if (toggle) {
            toggle.addEventListener('change', (e) => {
                if (e.target.checked) {
                    setTimeout(() => addMockMessage(mod.html), 300);
                }
            });
        }
    });

    const builderOrderBtn = document.getElementById('builder-order-btn');
    if (builderOrderBtn) {
        builderOrderBtn.addEventListener('click', () => {
            if (!window.currentUser) {
                alert('Пожалуйста, авторизуйтесь для заказа!');
                document.getElementById('open-auth').click();
                return;
            }
            const botName = builderNameInput ? builderNameInput.value || 'AUREXIS DEMO' : 'AUREXIS DEMO';
            const botColor = builderColorInput ? builderColorInput.value || '#e5b322' : '#e5b322';
            let activeModules = [];
            modules.forEach(mod => {
                const checkbox = document.getElementById(mod.id);
                if (checkbox && checkbox.checked) {
                    activeModules.push(mod.id.replace('module-', ''));
                }
            });
            
            const orderText = `ЗАКАЗ БОТА:\nИмя: ${botName}\nЦвет: ${botColor}\nМодули: ${activeModules.length > 0 ? activeModules.join(', ') : 'Базовый функционал'}`;

            // Open ticket modal and prefill
            const ticketModal = document.getElementById('modal-ticket');
            if(ticketModal) {
                ticketModal.style.display = 'flex';
                document.getElementById('ticket-topic').value = 'Заказ кастомного бота';
                document.getElementById('ticket-message').value = orderText;
            }
        });
    }
"""

filepath = 'static/script.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# remove trailing "});" and append new code
idx = content.rfind('});')
if idx != -1:
    content = content[:idx] + js_code + "\n});"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully appended JS code.')
else:
    print('Could not find closing brackets.')
