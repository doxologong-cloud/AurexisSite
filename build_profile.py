import re

index_path = r"C:\Users\user\Desktop\сайт\templates\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Sidebar Menu
sidebar_menu = """        <div class="sidebar-menu">
            <div class="sidebar-item"><img src="/static/assets/default-avatar.png" id="sidebar-avatar-mini" style="width: 24px; height: 24px; border-radius: 50%; object-fit: cover;"> <span id="sidebar-name-mini">ДомадOX</span></div>
            <div class="sidebar-divider"></div>
            
            <div class="sidebar-item" onclick="openProfile()"><i class="fa-regular fa-user"></i> Мой профиль</div>
            <div class="sidebar-item"><i class="fa-solid fa-robot"></i> БОТЫ</div>
            <div class="sidebar-item"><i class="fa-solid fa-folder-open"></i> Архив проектов</div>
            <div class="sidebar-item"><i class="fa-solid fa-book"></i> Журнал выживания</div>
            <div class="sidebar-divider"></div>
            <div class="sidebar-item" onclick="openSettings()"><i class="fa-solid fa-gear"></i> Настройки системы</div>
        </div>"""

text = re.sub(r'<div class="sidebar-menu">.*?</div>\s*</div>\s*</div>', sidebar_menu + '\n    </div>\n</div>', text, flags=re.DOTALL)

# 2. Add Modals HTML and CSS
modals_html = """
    <!-- MODALS OVERLAY -->
    <style>
        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(5px);
            z-index: 10000;
            display: flex; justify-content: center; align-items: center;
            opacity: 0; pointer-events: none;
            transition: opacity 0.3s ease;
        }
        .modal-overlay.active {
            opacity: 1; pointer-events: auto;
        }
        
        /* Telegram Profile Card */
        .profile-card {
            width: 360px;
            background: #1c242d;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transform: scale(0.9);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            font-family: 'Inter', sans-serif;
            color: #fff;
        }
        .modal-overlay.active .profile-card { transform: scale(1); }
        
        .profile-header {
            position: relative;
            text-align: center;
            padding-bottom: 20px;
        }
        .profile-banner {
            width: 100%; height: 120px;
            background: #2b3a4a;
            background-size: cover;
            background-position: center;
            transition: all 0.3s;
        }
        .profile-actions {
            position: absolute; top: 10px; right: 10px;
            display: flex; gap: 10px;
        }
        .icon-btn {
            background: rgba(0,0,0,0.3); border: none; color: #fff;
            width: 32px; height: 32px; border-radius: 50%;
            cursor: pointer; display: flex; justify-content: center; align-items: center;
            transition: background 0.2s;
        }
        .icon-btn:hover { background: rgba(0,0,0,0.6); }
        
        .profile-avatar-wrapper {
            position: relative;
            width: 100px; height: 100px;
            margin: -50px auto 10px auto;
            border-radius: 50%;
            border: 4px solid #1c242d;
            background: #1c242d;
        }
        .profile-avatar {
            width: 100%; height: 100%;
            border-radius: 50%; object-fit: cover;
        }
        .avatar-edit-overlay {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            border-radius: 50%; background: rgba(0,0,0,0.5);
            display: flex; justify-content: center; align-items: center;
            cursor: pointer; opacity: 0; transition: opacity 0.2s;
        }
        .profile-avatar-wrapper:hover .avatar-edit-overlay { opacity: 1; }
        
        .profile-name { font-size: 1.3rem; font-weight: 600; margin-bottom: 5px; }
        .profile-status { font-size: 0.9rem; color: #8774e1; }
        
        .profile-body { padding: 0 20px 20px 20px; text-align: left; }
        .info-block { padding: 15px 0; border-bottom: 1px solid #232e3c; }
        .info-block:last-child { border-bottom: none; }
        .info-value { font-size: 1rem; color: #fff; margin-bottom: 4px; word-wrap: break-word; }
        .info-label { font-size: 0.85rem; color: #7f91a4; }
        
        .edit-group { margin-bottom: 15px; }
        .edit-group label { display: block; font-size: 0.85rem; color: #7f91a4; margin-bottom: 5px; }
        .edit-group input, .edit-group textarea {
            width: 100%; background: #242f3d; border: 1px solid #2b3a4a;
            color: #fff; padding: 10px; border-radius: 6px; font-family: inherit;
            box-sizing: border-box; outline: none;
        }
        .edit-group textarea { resize: vertical; min-height: 60px; }
        .save-btn {
            width: 100%; background: #8774e1; color: #fff; border: none;
            padding: 12px; border-radius: 6px; font-weight: 600; cursor: pointer;
            transition: background 0.2s;
        }
        .save-btn:hover { background: #7b68c9; }

        /* Settings Card */
        .settings-card {
            width: 320px; background: #1c242d; border-radius: 12px;
            padding: 20px; color: #fff; font-family: 'Inter', sans-serif;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            transform: scale(0.9); transition: transform 0.3s;
        }
        .modal-overlay.active .settings-card { transform: scale(1); }
        .settings-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #232e3c; padding-bottom: 15px; margin-bottom: 15px; }
        .settings-header h3 { margin: 0; font-size: 1.1rem; }
    </style>

    <!-- Profile Modal -->
    <div id="profile-modal" class="modal-overlay">
        <div class="profile-card">
            <div class="profile-header">
                <div class="profile-banner" id="profile-banner-bg" onclick="changeBanner()" style="cursor: pointer;">
                    <div class="avatar-edit-overlay" id="banner-edit-overlay"><i class="fa-solid fa-camera"></i></div>
                </div>
                <div class="profile-actions">
                    <button class="icon-btn edit-btn" onclick="toggleProfileEdit()"><i class="fa-solid fa-pen"></i></button>
                    <button class="icon-btn close-btn" onclick="closeProfile()"><i class="fa-solid fa-xmark"></i></button>
                </div>
                <div class="profile-avatar-wrapper">
                    <img src="/static/assets/default-avatar.png" class="profile-avatar" id="profile-avatar-img-lrg">
                    <div class="avatar-edit-overlay" onclick="changeAvatar()"><i class="fa-solid fa-camera"></i></div>
                </div>
                <div class="profile-name" id="profile-name-text">ДомадOX</div>
                <div class="profile-status">в сети</div>
            </div>
            
            <div class="profile-body" id="profile-display-mode">
                <div class="info-block">
                    <div class="info-value" id="disp-phone">+7 983 323 7549</div>
                    <div class="info-label">Телефон</div>
                </div>
                <div class="info-block">
                    <div class="info-value" id="disp-bio">возвращенипе челика под названием doxчеловекglitchитд. заброший акк</div>
                    <div class="info-label">О себе</div>
                </div>
                <div class="info-block">
                    <div class="info-value" id="disp-username">@dxdplayersnow</div>
                    <div class="info-label">Имя пользователя</div>
                </div>
            </div>
            
            <div class="profile-body" id="profile-edit-mode" style="display: none;">
                <div class="edit-group">
                    <label>Имя</label>
                    <input type="text" id="edit-name" value="ДомадOX">
                </div>
                <div class="edit-group">
                    <label>Телефон</label>
                    <input type="text" id="edit-phone" value="+7 983 323 7549">
                </div>
                <div class="edit-group">
                    <label>О себе</label>
                    <textarea id="edit-bio">возвращенипе челика под названием doxчеловекglitchитд. заброший акк</textarea>
                </div>
                <div class="edit-group">
                    <label>Имя пользователя</label>
                    <input type="text" id="edit-username" value="@dxdplayersnow">
                </div>
                <button class="save-btn" onclick="saveProfile()">Сохранить</button>
            </div>
        </div>
    </div>
    
    <!-- Hidden file inputs -->
    <input type="file" id="avatar-upload" style="display: none;" accept="image/*">
    <input type="file" id="banner-upload" style="display: none;" accept="image/*">

    <!-- Settings Modal -->
    <div id="settings-modal" class="modal-overlay">
        <div class="settings-card">
            <div class="settings-header">
                <h3>Настройки системы</h3>
                <button class="icon-btn close-btn" onclick="closeSettings()"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="settings-body">
                <div class="edit-group">
                    <label>Визуализация фона</label>
                    <select id="bg-selector" style="width: 100%; background: #242f3d; color: #fff; border: 1px solid #2b3a4a; padding: 8px; border-radius: 6px;">
                        <option value="sparks">А: Пепел и Искры</option>
                        <option value="abyss">Б: Цифровая Бездна</option>
                        <option value="fluid">В: Живая Материя</option>
                    </select>
                </div>
                <div class="edit-group" style="display: flex; align-items: center; gap: 10px; margin-top: 20px;">
                    <input type="checkbox" id="audio-toggle" style="width: auto;">
                    <label style="margin: 0; color: #fff;">Дарк-Эмбиент (Звук)</label>
                </div>
            </div>
        </div>
    </div>
"""

# Inject modals after UI overlay
text = re.sub(r'<!-- Main Center Content Placeholder -->.*?</div>', '<!-- Main Center Content Placeholder -->\n        <div style="flex-grow: 1; display: flex; justify-content: center; align-items: center; pointer-events: auto;"></div>\n' + modals_html, text, flags=re.DOTALL)

# Remove old vault settings panel
text = re.sub(r'<!-- Bottom Bar / Settings -->.*?</div>\s*<!-- Settings Panel -->.*?</div>', '', text, flags=re.DOTALL)

# Add Modal JS
js_logic = """
    // --- MODALS & PROFILE LOGIC ---
    const profileModal = document.getElementById('profile-modal');
    const settingsModal = document.getElementById('settings-modal');
    const editMode = document.getElementById('profile-edit-mode');
    const displayMode = document.getElementById('profile-display-mode');
    
    function openProfile() { profileModal.classList.add('active'); sidebar.style.left = '-300px'; }
    function closeProfile() { profileModal.classList.remove('active'); editMode.style.display = 'none'; displayMode.style.display = 'block'; }
    
    function openSettings() { settingsModal.classList.add('active'); sidebar.style.left = '-300px'; }
    function closeSettings() { settingsModal.classList.remove('active'); }
    
    function toggleProfileEdit() {
        if(editMode.style.display === 'none') {
            editMode.style.display = 'block';
            displayMode.style.display = 'none';
        } else {
            editMode.style.display = 'none';
            displayMode.style.display = 'block';
        }
    }
    
    function saveProfile() {
        const name = document.getElementById('edit-name').value;
        const phone = document.getElementById('edit-phone').value;
        const bio = document.getElementById('edit-bio').value;
        const username = document.getElementById('edit-username').value;
        
        document.getElementById('profile-name-text').innerText = name;
        document.getElementById('disp-phone').innerText = phone;
        document.getElementById('disp-bio').innerText = bio;
        document.getElementById('disp-username').innerText = username;
        
        // Update sidebar
        document.querySelector('.sidebar-name').innerText = name;
        document.getElementById('sidebar-name-mini').innerText = name;
        
        toggleProfileEdit();
    }

    // Avatar/Banner upload logic (Local preview)
    const avatarUpload = document.getElementById('avatar-upload');
    const bannerUpload = document.getElementById('banner-upload');
    
    function changeAvatar() { avatarUpload.click(); }
    function changeBanner() { bannerUpload.click(); }
    
    avatarUpload.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('profile-avatar-img-lrg').src = e.target.result;
                document.getElementById('vault-avatar').src = e.target.result;
                document.getElementById('sidebar-avatar-mini').src = e.target.result;
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    bannerUpload.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('profile-banner-bg').style.backgroundImage = `url(${e.target.result})`;
            }
            reader.readAsDataURL(this.files[0]);
        }
    });
"""

# Inject JS before </script>
text = text.replace('</script>\n</body>', js_logic + '\n</script>\n</body>')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Profile and Settings modals added successfully.")
