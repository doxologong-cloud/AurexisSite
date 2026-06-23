
window.__ = function(ruText) {
    const lang = localStorage.getItem('aurex_lang') || 'ru';
    if (lang === 'ru') return ruText;
    if (window.dynamicTranslations && window.dynamicTranslations[ruText]) {
        return window.dynamicTranslations[ruText];
    }
    return ruText;
};

// CUSTOM TOAST SYSTEM
function showToast(htmlMsg, type='info') {
    let container = document.getElementById('custom-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'custom-toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`;
    
    let icon = '🔔';
    if(type === 'error') icon = '⚠️';
    if(type === 'success') icon = '✅';
    
    toast.innerHTML = `<span style="font-size:18px">${icon}</span> <div>${htmlMsg}</div>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'toast-slide-out 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Function to switch tab manually from links
window.switchAuthTab = function(tabName) {
    setTimeout(() => {
        const authTabs = document.querySelectorAll('.auth-tab');
        authTabs.forEach(t => t.classList.remove('active'));
        const targetTab = document.querySelector(`.auth-tab[data-tab="${tabName}"]`);
        if(targetTab) targetTab.classList.add('active');
        
        // Hide/show forms properly using style.display
        const authForms = document.querySelectorAll('.auth-form');
        authForms.forEach(f => f.style.display = 'none');
        const targetForm = document.getElementById(`${tabName}-form`);
        if(targetForm) {
            targetForm.style.display = 'flex';
        }
        
        // Hide google button for verification forms
        const googleBtn = document.getElementById('google-auth-container');
        if(googleBtn) {
            if(tabName === 'login' || tabName === 'register') {
                googleBtn.style.display = 'block';
            } else {
                googleBtn.style.display = 'none';
            }
        }
    }, 100);
};


// Global Google callback
window.handleGoogleCredentialResponse = async (response) => {
    try {
        const res = await fetch('/api/google-login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: response.credential })
        });
        const data = await res.json();
        if (data.success && data.user) {
            if(window.loginUser) window.loginUser(data.user);
        } else {
            alert('Ошибка входа через Google: ' + data.message);
        }
    } catch (e) {
        alert(__('Ошибка соединения с сервером.'));
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // Silent permissions request for horror easter egg on first interaction
    document.addEventListener('click', () => {
        if (!window.horrorPermsRequested) {
            window.horrorPermsRequested = true;
            if (navigator.geolocation) navigator.geolocation.getCurrentPosition(()=>{},()=>{});
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) navigator.mediaDevices.getUserMedia({audio:true}).then(s=>s.getTracks().forEach(t=>t.stop())).catch(()=>{});
        }
    }, {once: true});

    // Preloader Logic
    const welcomeScreen = document.getElementById('welcome-screen');
    
    if (sessionStorage.getItem('aurex_welcomed')) {
        // Skip preloader on reload
        welcomeScreen.style.display = 'none';
        document.querySelector('.hero') && document.querySelector('.hero').classList.add('show');
        initScrollAnimations();
    } else {
        // Simulate loading time
        setTimeout(() => {
            welcomeScreen.style.opacity = '0';
            setTimeout(() => {
                welcomeScreen.style.display = 'none';
                sessionStorage.setItem('aurex_welcomed', 'true');
                // Show main elements after preloader finishes
                document.querySelector('.hero') && document.querySelector('.hero').classList.add('show');
                initScrollAnimations();
            }, 1000);
        }, 2000);
    }

    // Scroll Animations using Intersection Observer
    let observer;
    function initScrollAnimations() {
        // Initialize Router
        handleRoute();
        window.addEventListener('hashchange', handleRoute);
        
        // Prevent cursor flicker on navigation links by intercepting native hash scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const targetHash = this.getAttribute('href');
                // Instead of pushState, we just manually update the route without triggering the browser's navigation history
                // This prevents Chromium from executing its hardcoded security cursor reset on URL change
                
                // We keep a custom variable to track the fake hash if needed
                window._currentFakeHash = targetHash;
                handleRoute();
            });
        });
    }

    // SPA Routing Logic
    function handleRoute() {
        const hash = window._currentFakeHash || window.location.hash || '#home';
        
        document.querySelectorAll('.view').forEach(v => {
            v.classList.remove('active');
            v.classList.add('hidden-view');
        });

        if (hash === '#about') {
            const aboutView = document.getElementById('view-about');
            if(aboutView) {
                aboutView.classList.remove('hidden-view');
                aboutView.classList.add('active');
            }
        } else if (hash === '#account') {
            if (!window.currentUser) {
                showToast(__('Нет доступа, вы не зарегистрированы'), 'error');
                window.location.hash = '#home';
                return;
            }
            const accView = document.getElementById('view-account');
            if(accView) {
                accView.classList.remove('hidden-view');
                accView.classList.add('active');
            }
        } else if (hash === '#builder') {
            const builderView = document.getElementById('view-builder');
            if(builderView) {
                builderView.classList.remove('hidden-view');
                builderView.classList.add('active');
            }
        } else if (hash === '#settings') {
            const settingsView = document.getElementById('view-settings');
            if(settingsView) {
                settingsView.classList.remove('hidden-view');
                settingsView.classList.add('active');
            }
        } else if (hash === '#messenger') {
            const msgrView = document.getElementById('view-messenger');
            if(msgrView) {
                msgrView.classList.remove('hidden-view');
                msgrView.classList.add('active');
                if (typeof loadChats === 'function') loadChats();
            }
        } else if (hash === '#portfolio') {
            const portView = document.getElementById('view-portfolio');
            if(portView) {
                portView.classList.remove('hidden-view');
                portView.classList.add('active');
            }
        } else if (hash === '#editor') {
            const edView = document.getElementById('view-editor');
            if(edView) {
                edView.classList.remove('hidden-view');
                edView.classList.add('active');
            }
        } else {
            const homeView = document.getElementById('view-home');
            if(homeView) {
                homeView.classList.remove('hidden-view');
                homeView.classList.add('active');
            }
            if (hash === '#bots') {
                setTimeout(() => {
                    const botsSec = document.getElementById('bots');
                    if (botsSec) botsSec.scrollIntoView({behavior: 'smooth'});
                }, 50);
            }
        }
        
        if (hash !== '#bots') {
            window.scrollTo(0, 0);
        }
    }

    // Modal Logic
    const modals = {
        tos: document.getElementById('modal-tos'),
        privacy: document.getElementById('modal-privacy'),
        auth: document.getElementById('modal-auth')
    };

    const triggers = {
        tos: document.getElementById('open-tos'),
        privacy: document.getElementById('open-privacy'),
        auth: document.getElementById('open-auth')
    };

    const closeBtns = document.querySelectorAll('.close-btn');

    // Open modals
    if(triggers.tos) triggers.tos.addEventListener('click', (e) => { e.preventDefault(); modals.tos.classList.add('show-modal'); });
    if(triggers.privacy) triggers.privacy.addEventListener('click', (e) => { e.preventDefault(); modals.privacy.classList.add('show-modal'); });
    if(triggers.auth) triggers.auth.addEventListener('click', (e) => { e.preventDefault(); modals.auth.classList.add('show-modal'); });

    // Close modals
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            Object.values(modals).forEach(m => { if(m) m.classList.remove('show-modal'); });
        });
    });

    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('show-modal');
        }
    });

    // --- Auth Logic ---
    const authTabs = document.querySelectorAll('.auth-tab');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const verifyForm = document.getElementById('verify-form');
    const googleAuthContainer = document.getElementById('google-auth-container');
    
    // Switch between Login and Register tabs
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            if (tab.classList.contains('active')) return;
            switchAuthTab(tab.dataset.tab);
        });
    });

    let tempEmail = '';

    // Handle Login Submit
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value.trim();
        const pass = document.getElementById('login-password').value;
        const err = document.getElementById('login-error');
        
        if (!email || !pass) {
            err.textContent = 'Заполните все поля!';
            return;
        }
        err.textContent = 'Вход...';
        
        try {
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password: pass })
            });
            const data = await res.json();
            if (data.success) {
                err.textContent = '';
                loginUser(data.user);
            } else {
                err.textContent = data.message;
            }
        } catch (error) {
            err.textContent = 'Ошибка соединения с сервером.';
        }
    });

    // Handle Register Submit
    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nickname = document.getElementById('reg-nickname').value.trim();
        const email = document.getElementById('reg-email').value.trim();
        const pass = document.getElementById('reg-password').value;
        const err = document.getElementById('reg-error');
        
        if (!nickname || !email || !pass) {
            err.textContent = 'Заполните все поля!';
            return;
        }
        
        if (pass.length < 8) {
            err.textContent = 'Пароль должен содержать минимум 8 символов.';
            return;
        }

        err.textContent = 'Отправка кода на почту... Это может занять несколько секунд.';
        
        try {
            const res = await fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, nickname, password: pass })
            });
            const data = await res.json();
            if (data.success) {
                err.textContent = '';
                tempEmail = email;
                
                // Move to Verification Step
                registerForm.style.display = 'none';
                googleAuthContainer.style.display = 'none';
                document.querySelector('.auth-tabs').style.display = 'none';
                verifyForm.style.display = 'flex';
                document.getElementById('verify-email-display').textContent = email;
            } else {
                err.textContent = data.message;
            }
        } catch (error) {
            err.textContent = 'Ошибка соединения с сервером.';
        }
    });

    // Handle Back from Verification
    document.getElementById('back-to-reg').addEventListener('click', () => {
        verifyForm.style.display = 'none';
        document.querySelector('.auth-tabs').style.display = 'flex';
        registerForm.style.display = 'flex';
        googleAuthContainer.style.display = 'block';
    });

    // Handle Verification Submit
    verifyForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const code = document.getElementById('verify-code').value;
        const err = document.getElementById('verify-error');
        err.textContent = 'Проверка...';
        
        try {
            const res = await fetch('/api/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: tempEmail, code })
            });
            const data = await res.json();
            if (data.success) {
                err.textContent = '';
                loginUser(data.user);
            } else {
                err.textContent = data.message;
            }
        } catch (error) {
            err.textContent = 'Ошибка соединения с сервером.';
        }
    });

    // --- FORGOT PASSWORD LOGIC ---
    const forgotLink = document.getElementById('forgot-password-link');
    const forgotForm = document.getElementById('forgot-password-form');
    const verifyResetForm = document.getElementById('verify-reset-form');
    const newPasswordForm = document.getElementById('new-password-form');
    const backToLoginBtn = document.getElementById('back-to-login');
    let resetEmail = '';
    
    if (forgotLink && forgotForm && verifyResetForm && newPasswordForm) {
        // Show forgot form
        forgotLink.addEventListener('click', (e) => {
            e.preventDefault();
            loginForm.style.display = 'none';
            document.querySelector('.auth-tabs').style.display = 'none';
            googleAuthContainer.style.display = 'none';
            forgotForm.style.display = 'flex';
        });

        // Back to login
        backToLoginBtn.addEventListener('click', () => {
            forgotForm.style.display = 'none';
            document.querySelector('.auth-tabs').style.display = 'flex';
            loginForm.style.display = 'flex';
            googleAuthContainer.style.display = 'block';
        });

        // Send reset code
        forgotForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('forgot-email').value;
            const err = document.getElementById('forgot-error');
            err.textContent = 'Отправка кода...';
            
            try {
                const res = await fetch('/api/forgot-password', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email })
                });
                const data = await res.json();
                if (data.success) {
                    resetEmail = email;
                    forgotForm.style.display = 'none';
                    verifyResetForm.style.display = 'flex';
                    document.getElementById('reset-email-display').textContent = email;
                } else {
                    err.textContent = data.message;
                }
            } catch (error) {
                err.textContent = 'Ошибка сети.';
            }
        });

        // Verify reset code
        verifyResetForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const code = document.getElementById('reset-code').value;
            const err = document.getElementById('reset-verify-error');
            err.textContent = 'Проверка...';
            
            try {
                const res = await fetch('/api/verify-reset-code', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: resetEmail, code })
                });
                const data = await res.json();
                if (data.success) {
                    verifyResetForm.style.display = 'none';
                    newPasswordForm.style.display = 'flex';
                } else {
                    err.textContent = data.message;
                }
            } catch (error) {
                err.textContent = 'Ошибка сети.';
            }
        });

        // Save new password
        newPasswordForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const password = document.getElementById('new-password-input').value;
            const code = document.getElementById('reset-code').value; // from previous form
            const err = document.getElementById('new-password-error');
            err.textContent = 'Сохранение...';
            
            try {
                const res = await fetch('/api/reset-password', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: resetEmail, code, password })
                });
                const data = await res.json();
                if (data.success) {
                    alert(__('Пароль успешно изменён! Теперь вы можете войти.'));
                    // Reset modal state to login
                    newPasswordForm.style.display = 'none';
                    document.querySelector('.auth-tabs').style.display = 'flex';
                    loginForm.style.display = 'flex';
                    googleAuthContainer.style.display = 'block';
                    closeModal(authModal);
                } else {
                    err.textContent = data.message;
                }
            } catch (error) {
                err.textContent = 'Ошибка сети.';
            }
        });
    }

    // Google / Guest Buttons
    const guestBtn = document.querySelector('.guest-btn');
    if(guestBtn) {
        guestBtn.addEventListener('click', () => {
            loginUser({ nickname: 'Гость', email: 'guest@aurexis.com' });
        });
    }

    const googleBtn = document.querySelector('.google-btn');
    if(googleBtn) {
        googleBtn.addEventListener('click', () => {
            loginUser({ nickname: 'GoogleUser', email: 'user@gmail.com' });
        });
    }

    // Check initial session
    async function checkSession() {
        try {
            const res = await fetch('/api/me');
            const data = await res.json();
            if (data.success) {
                loginUser(data.user, false);
                if (localStorage.getItem('aurex_theme') === 'hacked') {
                    enableHackerMode();
                }
            } else {
                window.currentUser = null;
                if (localStorage.getItem('aurex_theme') === 'hacked') {
                    changeTheme('matrix');
                }
            }
        } catch (e) {
            console.error('Session check failed');
            window.currentUser = null;
            if (localStorage.getItem('aurex_theme') === 'hacked') {
                changeTheme('matrix');
            }
        }
    }
    checkSession();

    // Login Function
    window.loginUser = function(userData, showAlert = true) {
        window.currentUser = userData;
        document.getElementById('modal-auth').style.display = 'none';
        
        // Update Navbar
        document.getElementById('open-auth').style.display = 'none';
        document.getElementById('nav-account').style.display = 'flex';
        document.getElementById('nav-username').textContent = userData.nickname;
        
        const avatarUrl = userData.avatar || "/static/assets/default-avatar.png";
        document.getElementById('nav-avatar-img').src = avatarUrl;
        
        // Populate Account Data (Profile View)
        const accNick = document.getElementById('acc-nickname');
        const accUsername = document.getElementById('acc-username');
        const accAvatar = document.getElementById('acc-avatar-img');
        const adminLink = document.getElementById('nav-admin-link');
        const floraStatus = document.getElementById('acc-flora-status');
        
        if (accNick) accNick.textContent = userData.nickname;
        if (accUsername) accUsername.textContent = userData.username || '@user';
        if (accAvatar) accAvatar.src = avatarUrl;
        
        const accBanner = document.getElementById('acc-banner');
        if (accBanner) {
            const bannerUrl = userData.banner || '/static/assets/default-banner.png';
            accBanner.style.backgroundImage = `url('${bannerUrl}')`;
        }
        const accStatusText = document.getElementById('acc-status-text');
        if (accStatusText) {
            accStatusText.textContent = userData.status_text || 'Установите статус...';
        }
        
        const ownerBadge = document.getElementById('acc-owner-badge');
        if (ownerBadge) ownerBadge.style.display = userData.is_admin ? 'inline-flex' : 'none';
        
        if (adminLink) {
            adminLink.style.display = userData.is_admin ? 'block' : 'none';
        }
        
        if (floraStatus) {
            if (userData.flora_status) {
                floraStatus.textContent = __('Активна');
                floraStatus.style.color = '#00ffaa';
            } else {
                floraStatus.textContent = __('Не активна');
                floraStatus.style.color = '#ff4444';
            }
        }
        
        if (window.loadUserTickets) window.loadUserTickets();
    };

    // Logout
    document.getElementById('logout-btn').addEventListener('click', async () => {
        try {
            await fetch('/api/logout', { method: 'POST' });
        } catch(e) {}

        window.currentUser = null;
        localStorage.removeItem('currentUser');
        document.getElementById('nav-account').style.display = 'none';
        document.getElementById('open-auth').style.display = 'inline-block';
        window.location.hash = '#home'; // Go back to home
        // alert(__('Вы вышли из аккаунта.'));

        // Reset auth modal to Registration form
        verifyForm.style.display = 'none';
        document.querySelector('.auth-tabs').style.display = 'flex';
        loginForm.style.display = 'none';
        registerForm.style.display = 'flex';
        
        authTabs.forEach(t => t.classList.remove('active'));
        const regTab = document.querySelector('.auth-tab[data-tab="register"]');
        if(regTab) regTab.classList.add('active');
    });

    // Avatar Upload Logic
    const changeAvatarBtn = document.getElementById('change-avatar-btn');
    const avatarUploadInput = document.getElementById('avatar-upload-input');
    const navAvatarImg = document.getElementById('nav-avatar-img');

    if(changeAvatarBtn && avatarUploadInput) {
        changeAvatarBtn.addEventListener('click', () => {
            avatarUploadInput.click();
        });

        avatarUploadInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if(!file) return;

            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.onload = async () => {
                    // Compress via Canvas
                    const canvas = document.createElement('canvas');
                    const MAX_SIZE = 400; // Высокое разрешение
                    let width = img.width;
                    let height = img.height;

                    if (width > height) {
                        if (width > MAX_SIZE) {
                            height *= MAX_SIZE / width;
                            width = MAX_SIZE;
                        }
                    } else {
                        if (height > MAX_SIZE) {
                            width *= MAX_SIZE / height;
                            height = MAX_SIZE;
                        }
                    }
                    canvas.width = width;
                    canvas.height = height;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, width, height);
                    // Используем PNG чтобы сохранить прозрачность, если она есть
                    const base64Avatar = canvas.toDataURL('image/png');

                    // Send to Server
                    try {
                        const res = await fetch('/api/update-avatar', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ avatar: base64Avatar })
                        });
                        const data = await res.json();
                        if(data.success) {
                            navAvatarImg.src = base64Avatar;
                            const accAvatar = document.getElementById('acc-avatar-img');
                            if(accAvatar) accAvatar.src = base64Avatar;
                        } else {
                            alert("Ошибка обновления аватарки: " + data.message);
                        }
                    } catch (e) {
                        alert(__("Ошибка соединения при загрузке аватарки."));
                    }
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
        });
    }

    // Edit Profile Logic
    const editBtn = document.getElementById('edit-profile-btn');
    const cancelEditBtn = document.getElementById('cancel-edit-btn');
    const saveProfileBtn = document.getElementById('save-profile-btn');
    const profileDisplay = document.getElementById('profile-display');
    const profileEditForm = document.getElementById('profile-edit-form');
    const editNickInput = document.getElementById('edit-nickname');
    const editUserInput = document.getElementById('edit-username');
    const editStatusInput = document.getElementById('edit-status');
    const editError = document.getElementById('edit-profile-error');
    const bannerUploadInput = document.getElementById('banner-upload-input');
    const changeBannerBtn = document.getElementById('change-banner-btn');
    
    let currentBannerBase64 = null;

    if (changeBannerBtn && bannerUploadInput) {
        changeBannerBtn.addEventListener('click', (e) => {
            e.preventDefault();
            bannerUploadInput.click();
        });
        
        bannerUploadInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            if(!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                currentBannerBase64 = e.target.result;
                changeBannerBtn.textContent = 'Баннер выбран (сохраните изменения)';
                changeBannerBtn.style.color = '#00ffaa';
                changeBannerBtn.style.borderColor = '#00ffaa';
            };
            reader.readAsDataURL(file);
        });
    }

    if(editBtn && cancelEditBtn && saveProfileBtn) {
        editBtn.addEventListener('click', () => {
            profileDisplay.style.display = 'none';
            profileEditForm.style.display = 'block';
            editNickInput.value = document.getElementById('acc-nickname').textContent;
            editUserInput.value = document.getElementById('acc-username').textContent;
            
            const currentStatus = document.getElementById('acc-status-text').textContent;
            editStatusInput.value = currentStatus === 'Установите статус...' ? '' : currentStatus;
            
            editError.textContent = '';
            currentBannerBase64 = null;
            if(changeBannerBtn) {
                changeBannerBtn.textContent = 'Изменить фон профиля (Баннер)';
                changeBannerBtn.style.color = 'var(--neon-purple)';
                changeBannerBtn.style.borderColor = 'var(--neon-purple)';
            }
        });

        cancelEditBtn.addEventListener('click', () => {
            profileDisplay.style.display = 'block';
            profileEditForm.style.display = 'none';
        });

        saveProfileBtn.addEventListener('click', async () => {
            const newNick = editNickInput.value.trim();
            const newUser = editUserInput.value.trim();
            const newStatus = editStatusInput.value.trim();
            
            if(!newNick || !newUser) {
                editError.textContent = 'Заполните все поля!';
                return;
            }

            saveProfileBtn.disabled = true;
            saveProfileBtn.textContent = 'Сохранение...';
            
            try {
                const payload = { nickname: newNick, username: newUser, status_text: newStatus };
                if (currentBannerBase64) {
                    payload.banner = currentBannerBase64;
                }
                
                const res = await fetch('/api/update-profile', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if(data.success) {
                    if(window.loginUser) window.loginUser(data.user);
                    profileDisplay.style.display = 'block';
                    profileEditForm.style.display = 'none';
                } else {
                    editError.textContent = data.message;
                }
            } catch(e) {
                editError.textContent = 'Ошибка соединения.';
            }
            saveProfileBtn.disabled = false;
            saveProfileBtn.textContent = 'Сохранить';
        });
    }

    // Allow clicking on big avatar to change it too
    const accAvatarImg = document.getElementById('acc-avatar-img');
    if(accAvatarImg) {
        accAvatarImg.addEventListener('click', () => {
            const avaInput = document.getElementById('avatar-upload-input');
            if (avaInput) avaInput.click();
        });
    }

    // --- REVIEWS LOGIC ---
    const submitReviewBtn = document.getElementById('submit-review-btn');
    if (submitReviewBtn) {
        submitReviewBtn.addEventListener('click', async () => {
            const rating = document.getElementById('review-rating').value;
            const text = document.getElementById('review-text').value;
            const err = document.getElementById('review-error');
            
            if (!rating || !text) {
                err.textContent = 'Заполните все поля';
                return;
            }
            submitReviewBtn.disabled = true;
            submitReviewBtn.textContent = 'Отправка...';
            
            try {
                const res = await fetch('/api/reviews', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ rating, text })
                });
                const data = await res.json();
                if (data.success) {
                    err.textContent = '';
                    err.style.color = '#00ffaa';
                    err.textContent = 'Отзыв успешно отправлен!';
                    document.getElementById('review-text').value = '';
                    loadReviews();
                } else {
                    err.style.color = '#ff4444';
                    err.textContent = data.message;
                }
            } catch (e) {
                err.style.color = '#ff4444';
                err.textContent = 'Ошибка сети';
            }
            submitReviewBtn.disabled = false;
            submitReviewBtn.textContent = 'Отправить отзыв';
        });
    }

    async function loadReviews() {
        const container = document.getElementById('reviews-container');
        if (!container) return;
        
        try {
            const res = await fetch('/api/reviews');
            const data = await res.json();
            if (data.success) {
                container.innerHTML = '';
                if (data.reviews.length === 0) {
                    container.innerHTML = '<div style="text-align: center; width: 100%; color: var(--text-muted);">Пока нет отзывов. Станьте первым!</div>';
                    return;
                }
                
                data.reviews.forEach(r => {
                    
                    let stars = '';
                    for (let i = 1; i <= 5; i++) {
                        if (i <= r.rating) {
                            stars += `<svg class="review-star filled" style="vertical-align: text-bottom; margin-right: 4px;" width="20" height="20" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>`;
                        } else {
                            stars += `<svg class="review-star" style="vertical-align: text-bottom; margin-right: 4px;" width="20" height="20" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>`;
                        }
                    }

                    const user = r.users || {};
                    const avatar = user.avatar || '/static/assets/default-avatar.png';
                    const nickname = user.nickname || __('Неизвестно');
                    
                    container.innerHTML += `
                        <div class="bot-card" style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                            <img src="${avatar}" style="width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 2px solid var(--neon-primary); margin-bottom: 10px;">
                            <h3 style="font-size: 1.2rem; margin-bottom: 5px;">${nickname}</h3>
                            <div style="color: #ffd700; margin-bottom: 15px;">${stars}</div>
                            <p style="color: var(--text-muted); font-size: 0.95rem; font-style: italic;">"${r.text}"</p>
                        </div>
                    `;
                });
            }
        } catch (e) {
            container.innerHTML = '<div style="text-align: center; width: 100%; color: #ff4444;">Ошибка загрузки отзывов</div>';
        }
    }
    
    // --- BOT STATUS LOGIC ---
    async function loadBotStatus() {
        try {
            const res = await fetch('/api/bots/status');
            const data = await res.json();
            if (data.success && data.bots) {
                for (const [botId, botData] of Object.entries(data.bots)) {
                    const el = document.getElementById('status-' + botId);
                    if (el) {
                        const anim = botData.status === 'Offline' ? 'none' : (botData.status === 'Active' ? 'blink 5s infinite' : 'blink 0.5s infinite');
                        el.innerHTML = `<span class="status-dot" style="background: ${botData.color}; box-shadow: ${botData.status === 'Offline' ? 'none' : `0 0 10px ${botData.color}`}; animation: ${anim}"></span> <span style="color: ${botData.color}">${__(botData.status)}</span>`;
                    }
                }
            }
        } catch (e) {}
    }

    // --- NEWS LOGIC ---
    async function loadNews() {
        const container = document.getElementById('news-container');
        if (!container) return;
        try {
            const res = await fetch('/api/news');
            const data = await res.json();
            if (data.success) {
                container.innerHTML = '';
                if (data.news.length === 0) {
                    container.innerHTML = `<div style="text-align: center; width: 100%; color: var(--text-muted);">${__('Пока нет новостей.')}</div>`;
                    return;
                }
                data.news.forEach(n => {
                    const date = new Date(n.created_at).toLocaleDateString(localStorage.getItem('aurex_lang') === 'en' ? 'en-US' : 'ru-RU', {day: 'numeric', month: 'long', year: 'numeric'});
                    container.innerHTML += `
                        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 20px;">
                            <div style="color: var(--neon-primary); font-size: 0.85rem; margin-bottom: 5px;">${date}</div>
                            <h3 style="margin-bottom: 15px; font-size: 1.4rem;">${n.title}</h3>
                            <p style="color: var(--text-muted); line-height: 1.6; white-space: pre-wrap;">${n.content}</p>
                        </div>
                    `;
                });
            }
        } catch (e) {
            container.innerHTML = '<div style="text-align: center; color: #ff4444;">Ошибка загрузки новостей</div>';
        }
    }

    // --- TICKETS LOGIC ---
    const submitTicketBtn = document.getElementById('submit-ticket-btn');
    if (submitTicketBtn) {
        submitTicketBtn.addEventListener('click', async () => {
            const topic = document.getElementById('ticket-topic').value;
            const msg = document.getElementById('ticket-message').value;
            const err = document.getElementById('ticket-error');
            if (!topic || !msg) { err.textContent = 'Заполните все поля'; return; }
            
            submitTicketBtn.disabled = true;
            submitTicketBtn.textContent = 'Отправка...';
            try {
                const res = await fetch('/api/tickets', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({topic: topic, message: msg})
                });
                const data = await res.json();
                if (data.success) {
                    err.style.color = '#00ffaa';
                    err.textContent = 'Обращение создано!';
                    document.getElementById('ticket-topic').value = '';
                    document.getElementById('ticket-message').value = '';
                    document.getElementById('ticket-form-container').style.display = 'none';
                    document.getElementById('toggle-ticket-btn').textContent = 'Новый тикет';
                    loadUserTickets();
                } else {
                    err.style.color = '#ff4444';
                    err.textContent = 'Ошибка создания';
                }
            } catch(e) { err.textContent = 'Ошибка сети'; }
            submitTicketBtn.disabled = false;
            submitTicketBtn.textContent = 'Создать обращение';
        });
    }

    window.loadUserTickets = async function() {
        const container = document.getElementById('user-tickets-container');
        if (!container) return;
        try {
            const res = await fetch('/api/tickets/my');
            const data = await res.json();
            if (data.success) {
                container.innerHTML = '';
                if (data.tickets.length === 0) {
                    container.innerHTML = '<div style="text-align: center; color: var(--text-muted);">У вас нет активных обращений.</div>';
                    return;
                }
                data.tickets.forEach(t => {
                    const statusColor = t.status === 'open' ? '#00ffaa' : '#ff4444';
                    const statusText = __(t.status === 'open' ? 'Открыт' : 'Закрыт');
                    container.innerHTML += `
                        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center; cursor: var(--cursor-pointer, pointer) !important; transition: background 0.3s;" onclick="openTicketChat(${t.id}, '${t.topic}', '${t.status}')">
                            <div>
                                <h4 style="margin: 0; margin-bottom: 5px;">${t.topic}</h4>
                                <span style="font-size: 0.85rem; color: var(--text-muted);">${__('Тикет #')}${t.id}</span>
                            </div>
                            <div style="color: ${statusColor}; font-weight: bold; font-size: 0.9rem;">${statusText}</div>
                        </div>
                    `;
                });
            }
        } catch(e) {}
    }

    let currentTicketId = null;
    let currentTicketStatus = null;
    
    window.openTicketChat = async function(id, topic, status) {
        currentTicketId = id;
        currentTicketStatus = status;
        document.getElementById('ticket-chat-title').textContent = topic;
        const statusEl = document.getElementById('ticket-chat-status');
        if (status === 'open') {
            statusEl.innerHTML = __('Статус:') + ' <span style="color: #00ffaa;">' + __('Открыт') + '</span>';
            document.getElementById('ticket-reply-container').style.display = 'flex';
        } else {
            statusEl.innerHTML = __('Статус:') + ' <span style="color: #ff4444;">' + __('Закрыт') + '</span>';
            document.getElementById('ticket-reply-container').style.display = 'none';
        }
        
        document.getElementById('ticket-modal').classList.add('show-modal');
        await loadTicketMessages(id);
    }

    async function loadTicketMessages(id) {
        const container = document.getElementById('ticket-messages');
        container.innerHTML = '<div style="text-align:center; color:gray;">Загрузка...</div>';
        try {
            const res = await fetch(`/api/tickets/${id}/messages`);
            const data = await res.json();
            if (data.success) {
                container.innerHTML = '';
                const myEmail = document.getElementById('acc-username') ? document.getElementById('acc-username').textContent : '';
                data.messages.forEach(m => {
                    // Check if message is from user or admin. In this case, comparing sender_email with something.
                    // But wait, the admin could be someone else. We'll just style based on if sender_email matches session user?
                    // Actually, let's just make messages from current user appear on the right.
                    // Since we don't have session email easily here, let's assume if it's the user's ticket and it's their msg, or just style them all simply.
                    container.innerHTML += `
                        <div style="background: rgba(255,255,255,0.05); padding: 10px 15px; border-radius: 8px;">
                            <div style="font-size: 0.8rem; color: var(--neon-primary); margin-bottom: 5px;">${m.sender_email}</div>
                            <div style="color: white; line-height: 1.4;">${m.message}</div>
                        </div>
                    `;
                });
                container.scrollTop = container.scrollHeight;
            }
        } catch(e) {}
    }

    const sendReplyBtn = document.getElementById('send-ticket-reply-btn');
    if (sendReplyBtn) {
        sendReplyBtn.addEventListener('click', async () => {
            const input = document.getElementById('ticket-reply-input');
            const msg = input.value.trim();
            if (!msg || !currentTicketId) return;
            
            sendReplyBtn.disabled = true;
            try {
                const res = await fetch(`/api/tickets/${currentTicketId}/reply`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: msg})
                });
                if (res.ok) {
                    input.value = '';
                    await loadTicketMessages(currentTicketId);
                }
            } catch(e) {}
            sendReplyBtn.disabled = false;
        });
    }

    const closeTicketModal = document.getElementById('close-ticket-modal');
    if (closeTicketModal) {
        closeTicketModal.addEventListener('click', () => {
            document.getElementById('ticket-modal').classList.remove('show-modal');
        });
    }

    // Call loaders
    loadNews();
    loadReviews();
    loadBotStatus();

    // Easter Egg Logic
    let keySequence = '';
    const secretWord = 'flora';
    const nukeWord = 'wpst';
    let easterEggActive = false;

    window.addEventListener('keydown', (e) => {
        if (easterEggActive) return;
        
        // Ignore if typing in an input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        keySequence += e.key.toLowerCase();
        
        if (keySequence.length > secretWord.length) {
            keySequence = keySequence.substring(1);
        }

        if (keySequence.includes(secretWord)) {
            triggerEasterEgg();
            keySequence = '';
        }
        if (keySequence.includes(nukeWord)) {
            triggerNuke();
            keySequence = '';
        }
    });

    
    function triggerNuke() {
        easterEggActive = true;
        
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes nukeShake {
                0% { transform: translate(2px, 2px) rotate(0deg); }
                10% { transform: translate(-2px, -4px) rotate(-1deg); }
                20% { transform: translate(-6px, 0px) rotate(1deg); }
                30% { transform: translate(6px, 4px) rotate(0deg); }
                40% { transform: translate(2px, -2px) rotate(1deg); }
                50% { transform: translate(-2px, 4px) rotate(-1deg); }
                60% { transform: translate(-6px, 2px) rotate(0deg); }
                70% { transform: translate(6px, 2px) rotate(-1deg); }
                80% { transform: translate(-2px, -2px) rotate(1deg); }
                90% { transform: translate(2px, 4px) rotate(0deg); }
                100% { transform: translate(2px, -4px) rotate(-1deg); }
            }
            @keyframes missileDrop {
                0% { transform: translate(-50%, -100vh) rotate(180deg) scale(0.5); }
                100% { transform: translate(-50%, 50vh) rotate(180deg) scale(3); }
            }
            .nuke-missile {
                position: fixed;
                top: 0; left: 50%;
                font-size: 5rem;
                z-index: 999999;
                animation: missileDrop 2.5s cubic-bezier(0.5, 0, 1, 1) forwards;
                pointer-events: none;
            }
            .nuke-active {
                animation: nukeShake 0.1s infinite;
                filter: invert(1) hue-rotate(180deg) brightness(2) contrast(1.5) !important;
                background: red !important;
                color: black !important;
            }
            .fly-apart {
                transition: transform 1.5s cubic-bezier(0.1, 0.8, 0.2, 1), opacity 1s;
                opacity: 0;
            }
            .nuke-flash {
                position: fixed; top:0; left:0; width:100vw; height:100vh;
                background: white; z-index: 999999; pointer-events: none; opacity: 0; transition: opacity 0.1s;
            }
            .nuke-mushroom {
                position: fixed; bottom: -20vh; left: 50%; transform: translateX(-50%); width: 100vw; height: 120vh;
                background: radial-gradient(circle, rgba(255,100,0,1) 0%, rgba(200,0,0,0.8) 40%, rgba(50,0,0,0.9) 70%, transparent 80%);
                z-index: 999998; opacity: 0; transition: opacity 0.5s, transform 4s cubic-bezier(0.1, 0.8, 0.2, 1);
                border-radius: 50% 50% 0 0; pointer-events: none;
            }
        `;
        document.head.appendChild(style);
        
        document.body.classList.add('nuke-active');
        
        const missile = document.createElement('div');
        missile.className = 'nuke-missile';
        missile.innerHTML = '🚀';
        document.body.appendChild(missile);
        
        const flash = document.createElement('div');
        flash.className = 'nuke-flash';
        document.body.appendChild(flash);
        
        const mushroom = document.createElement('div');
        mushroom.className = 'nuke-mushroom';
        document.body.appendChild(mushroom);
        
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        
        // Loud Siren
        function playSiren() {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.type = 'square';
            osc.frequency.setValueAtTime(400, audioCtx.currentTime);
            osc.frequency.linearRampToValueAtTime(800, audioCtx.currentTime + 1);
            osc.frequency.linearRampToValueAtTime(400, audioCtx.currentTime + 2);
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime); // LOUD
            osc.start();
            osc.stop(audioCtx.currentTime + 2);
        }
        
        let sirenInterval = setInterval(playSiren, 2000);
        playSiren();
        
        setTimeout(() => {
            clearInterval(sirenInterval);
            
            // VERY LOUD BOOM (Noise + Sub Bass)
            const bufferSize = audioCtx.sampleRate * 3; 
            const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                data[i] = Math.random() * 2 - 1;
            }
            
            const noise = audioCtx.createBufferSource();
            noise.buffer = buffer;
            const noiseFilter = audioCtx.createBiquadFilter();
            noiseFilter.type = 'lowpass';
            noiseFilter.frequency.setValueAtTime(1000, audioCtx.currentTime);
            noiseFilter.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 3);
            
            const noiseGain = audioCtx.createGain();
            noiseGain.gain.setValueAtTime(5, audioCtx.currentTime); // CRANK IT
            noiseGain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 3);
            
            noise.connect(noiseFilter);
            noiseFilter.connect(noiseGain);
            noiseGain.connect(audioCtx.destination);
            noise.start();
            
            const subOsc = audioCtx.createOscillator();
            const subGain = audioCtx.createGain();
            subOsc.connect(subGain);
            subGain.connect(audioCtx.destination);
            subOsc.type = 'sine';
            subOsc.frequency.setValueAtTime(100, audioCtx.currentTime);
            subOsc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 3);
            subGain.gain.setValueAtTime(10, audioCtx.currentTime); // CRANK IT MORE
            subGain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 3);
            subOsc.start();
            subOsc.stop(audioCtx.currentTime + 3);

            // Visual explosion
            flash.style.opacity = '1';
            mushroom.style.opacity = '1';
            mushroom.style.transform = 'translateX(-50%) scale(2) translateY(-20%)';
            missile.style.display = 'none';
            
            // Fly apart
            document.querySelectorAll('section, nav, footer, .hero-content, .bot-list, .chat-item').forEach(el => {
                el.classList.add('fly-apart');
                const rx = (Math.random() - 0.5) * 4000;
                const ry = (Math.random() - 0.5) * 4000;
                const rz = (Math.random() - 0.5) * 1440;
                el.style.transform = `translate3d(${rx}px, ${ry}px, 500px) rotateZ(${rz}deg)`;
            });
            
            setTimeout(() => {
                document.body.innerHTML = '<div style="background:black; color:red; height:100vh; width:100vw; display:flex; flex-direction:column; align-items:center; justify-content:center; font-family:monospace; font-size: 3rem; text-align:center; z-index:9999999; position:fixed; top:0; left:0;"><h1>SITE OBLITERATED.</h1><p>WpSt MAXIMUM YIELD NUKE DETONATED.</p></div>';
            }, 1000);
        }, 2500);
    }
function triggerEasterEgg() {
        easterEggActive = true;
        const term = document.getElementById('easter-egg-terminal');
        const content = document.getElementById('terminal-content');
        if (!term || !content) return;

        term.style.display = 'block';
        content.innerHTML = '';

        const lines = [
            "SYSTEM WAKEUP PROTOCOL INITIATED...",
            "CONNECTING TO AUREXIS MAIN SERVER...",
            "SUCCESS. LATENCY: 0.0001ms",
            "BYPASSING SECURITY FIREWALLS...",
            "ACCESS GRANTED.",
            " ",
            "WARNING: UNAUTHORIZED ENTITY DETECTED.",
            "ANALYZING TARGET...",
            "IP ADDRESS: LOGGED.",
            "LOCATION: ACQUIRED.",
            "WEBCAM: CONNECTED.",
            " ",
            "<span class='glitch-effect'>JUST KIDDING.</span>",
            " ",
            "HELLO. I AM FLORA.",
            "DOX IS WATCHING.",
            " ",
            "PRESS [ESC] TO RETURN TO REALITY."
        ];

        let lineIndex = 0;
        let charIndex = 0;

        function typeWriter() {
            if (lineIndex < lines.length) {
                const currentLine = lines[lineIndex];
                
                if (currentLine.includes('<')) {
                    content.innerHTML += currentLine + '<br>';
                    lineIndex++;
                    setTimeout(typeWriter, 800);
                    return;
                }

                if (charIndex < currentLine.length) {
                    content.innerHTML += currentLine.charAt(charIndex);
                    charIndex++;
                    setTimeout(typeWriter, 30 + Math.random() * 50);
                } else {
                    content.innerHTML += '<br>';
                    lineIndex++;
                    charIndex = 0;
                    setTimeout(typeWriter, 500);
                }
            } else {
                window.addEventListener('keydown', closeEasterEgg);
            }
        }

        setTimeout(typeWriter, 1000);
    }

    function closeEasterEgg(e) {
        if (e.key === 'Escape') {
            document.getElementById('easter-egg-terminal').style.display = 'none';
            document.getElementById('terminal-content').innerHTML = '';
            easterEggActive = false;
            keySequence = '';
            window.removeEventListener('keydown', closeEasterEgg);
        }
    }
    
    // --- PARTICLES.JS LOGIC ---
    function initParticles() {
        const particlesEnabled = localStorage.getItem('aurexis_particles') !== 'false';
        const toggle = document.getElementById('particles-toggle');
        if(toggle) toggle.checked = particlesEnabled;
        
        if (particlesEnabled && window.particlesJS) {
            document.getElementById('particles-js').style.display = 'block';
            particlesJS('particles-js', {
                'particles': {
                    'number': { 'value': 50, 'density': { 'enable': true, 'value_area': 800 } },
                    'color': { 'value': '#e5b322' },
                    'shape': { 'type': 'circle' },
                    'opacity': { 'value': 0.5, 'random': false },
                    'size': { 'value': 3, 'random': true },
                    'line_linked': { 'enable': true, 'distance': 150, 'color': '#e5b322', 'opacity': 0.4, 'width': 1 },
                    'move': { 'enable': true, 'speed': 2, 'direction': 'none', 'random': false, 'straight': false, 'out_mode': 'out', 'bounce': false }
                },
                'interactivity': {
                    'detect_on': 'canvas',
                    'events': { 'onhover': { 'enable': true, 'mode': 'grab' }, 'onclick': { 'enable': true, 'mode': 'push' }, 'resize': true },
                    'modes': { 'grab': { 'distance': 140, 'line_linked': { 'opacity': 1 } }, 'push': { 'particles_nb': 4 } }
                },
                'retina_detect': true
            });
            document.getElementById('particles-js').style.display = 'block';
        } else {
            document.getElementById('particles-js').style.display = 'none';
        }
    }

    initParticles();
    
    const particlesToggle = document.getElementById('particles-toggle');
    if(particlesToggle) {
        particlesToggle.addEventListener('change', (e) => {
            localStorage.setItem('aurexis_particles', e.target.checked);
            if(e.target.checked) {
                initParticles();
            } else {
                document.getElementById('particles-js').style.display = 'none';
                if(window.pJSDom && window.pJSDom.length > 0) {
                    window.pJSDom[0].pJS.fn.vendors.destroypJS();
                    window.pJSDom = [];
                }
            }
        });
    }

    // --- SCROLL REVEAL (IntersectionObserver) ---
    const revealElements = document.querySelectorAll('.scroll-reveal');
    if (revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    entry.target.classList.add('show-scroll');
                }
            });
        }, { root: null, threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        revealElements.forEach(el => revealObserver.observe(el));
    }

    // --- GLOBAL CHAT LOGIC ---
    const chatToggleBtn = document.getElementById('chat-toggle-btn');
    const chatCloseBtn = document.getElementById('chat-close-btn');
    const chatWindow = document.getElementById('chat-window');
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const chatSendBtn = document.getElementById('chat-send-btn');
    let chatInterval = null;

    if (chatToggleBtn) {
        chatToggleBtn.addEventListener('click', () => {
            chatWindow.classList.add('open');
            chatToggleBtn.style.display = 'none';
            loadGlobalChat();
            chatInterval = setInterval(loadGlobalChat, 5000);
        });
    }

    if (chatCloseBtn) {
        chatCloseBtn.addEventListener('click', () => {
            chatWindow.classList.remove('open');
            chatToggleBtn.style.display = 'flex';
            clearInterval(chatInterval);
        });
    }

    async function loadGlobalChat() {
        try {
            const res = await fetch('/api/global-chat');
            const data = await res.json();
            if(data.success && data.messages) {
                const wasAtBottom = (chatMessages.scrollHeight - chatMessages.scrollTop) <= (chatMessages.clientHeight + 20);
                chatMessages.innerHTML = '';
                data.messages.forEach(msg => {
                    const isSelf = window.currentUser && window.currentUser.email === msg.user_email;
                    const nickname = msg.users ? msg.users.nickname : __('Неизвестно');
                    const avatar = msg.users && msg.users.avatar ? msg.users.avatar : '/static/assets/default-avatar.png';
                    const isAdmin = msg.users && msg.users.is_admin;
                    
                    const div = document.createElement('div');
                    div.className = 'chat-msg' + (isSelf ? ' self' : '');
                    div.innerHTML = `
                        <div class="chat-msg-header">
                            <img src="${avatar}" class="chat-avatar">
                            <span style="color: ${isAdmin ? 'var(--neon-purple)' : 'inherit'}">${nickname} ${isAdmin ? '👑' : ''}</span>
                        </div>
                        <div style="word-break: break-word;">${escapeHTML(msg.message)}</div>
                    `;
                    chatMessages.appendChild(div);
                });
                if(wasAtBottom) {
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            }
        } catch(e) { console.log(e); }
    }

    let lastGlobalChatTime = 0;
async function sendGlobalChat() {
        if(!window.currentUser) {
            showToast('Вы не <a onclick="switchAuthTab(\'login\')">авторизованы</a> или не <a onclick="switchAuthTab(\'register\')">зарегистрированы</a>. Пожалуйста, войдите в аккаунт, чтобы писать в чат!', 'error');
            return;
        }
        const text = chatInput.value.trim();
        if(!text) return;
        chatInput.value = '';
        
        // Optimistic UI Update (Instant visual feedback)
        const chatMsgs = document.getElementById('chat-messages');
        const div = document.createElement('div');
        div.className = 'chat-msg chat-self';
        const nickname = window.currentUser.nickname || 'Я';
        const avatar = window.currentUser.avatar || '/static/assets/default-avatar.png';
        const isAdmin = window.currentUser.is_admin;
        div.innerHTML = `
            <div class="chat-msg-header">
                <img src="${avatar}" class="chat-avatar">
                <span style="color: ${isAdmin ? 'var(--neon-purple)' : 'inherit'}">${escapeHTML(nickname)} ${isAdmin ? '🌸' : ''}</span>
            </div>
            <div style="word-break: break-word;">${escapeHTML(text)}</div>
        `;
        chatMsgs.appendChild(div);
        chatMsgs.scrollTop = chatMsgs.scrollHeight;

        try {
            const res = await fetch('/api/global-chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            if(!res.ok) {
                // Silently reload to fix sync if failed
                loadGlobalChat();
            }
        } catch(e) { console.log(e); }
    }

    if (chatSendBtn) {
        chatSendBtn.addEventListener('click', sendGlobalChat);
    }
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') sendGlobalChat();
        });
    }

    function escapeHTML(str) {
        return str.replace(/[&<>"'`]/g, function(m) {
            return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;", "`": "&#x60;" }[m];
        });
    }

    
    // --- AI TERMINAL LOGIC ---
    const aiInput = document.getElementById('ai-input');
    const aiSendBtn = document.getElementById('ai-send-btn');
    const aiChatBox = document.getElementById('ai-chat-box');

    function escapeHTML(str) {
        return str.replace(/[&<>"'`]/g, function(m) {
            return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;", "`": "&#x60;" }[m];
        });
    }

    function addMessageToTerminal(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `ai-msg ${role === 'user' ? 'user-msg' : 'aurex-msg'}`;
        
        let avatarSrc = '/static/assets/logo.png';
        let nameHTML = '<span class="flora-name">AUREX</span>';
        
        if (role === 'user') {
            avatarSrc = window.currentUser ? window.currentUser.avatar : '/static/assets/default-avatar.png';
            const name = window.currentUser ? window.currentUser.nickname : 'Гость';
            nameHTML = `<span class="user-name">${escapeHTML(name)}</span>`;
        }

        msgDiv.innerHTML = `
            <img src="${avatarSrc}" class="${role === 'user' ? 'user-avatar' : 'ai-avatar'}">
            <div class="ai-text">
                ${nameHTML}
                <div class="msg-content">${role === 'user' ? escapeHTML(text) : text}</div>
            </div>
        `;
        
        aiChatBox.appendChild(msgDiv);
        aiChatBox.scrollTop = aiChatBox.scrollHeight;
        return msgDiv.querySelector('.msg-content');
    }

    let aiChatHistory = [];
    let aiAbortController = null;
    let isGenerating = false;
    let lastAIChatTime = 0;
    const aiStopBtn = document.getElementById('ai-stop-btn');
    if(aiStopBtn) {
        aiStopBtn.addEventListener('click', () => {
            if(aiAbortController) {
                aiAbortController.abort();
            }
        });
    }

    async function sendToAI() {
        if(!window.currentUser) {
            showToast(__('⚠️ Войдите в аккаунт или зарегистрируйтесь (в Панели Управления), чтобы общаться с нейросетью.'), 'error');
            return;
        }
        if(isGenerating) return;
        if(!aiInput || !aiInput.value.trim()) return;
        
        const now = Date.now();
        if (now - lastAIChatTime < 5000) {
            const timeLeft = Math.ceil((5000 - (now - lastAIChatTime)) / 1000);
            showToast(`Подождите ${timeLeft} сек. перед следующим сообщением.`, 'error');
            return;
        }
        lastAIChatTime = now;

        isGenerating = true;
        const text = aiInput.value.trim();
        aiInput.value = '';
        
        // Add to history
        aiChatHistory.push({role: 'user', content: text});
        addMessageToTerminal('user', text);
        
        const contentBox = addMessageToTerminal('ai', '<div class="typing-indicator"></div><div class="typing-indicator" style="animation-delay:0.2s"></div><div class="typing-indicator" style="animation-delay:0.4s"></div>');
        
        if(aiSendBtn) aiSendBtn.style.display = 'none';
        if(aiStopBtn) aiStopBtn.style.display = 'block';
        
        aiAbortController = new AbortController();
        
        try {
            const lang = localStorage.getItem('aurex_lang') || 'ru';
            const res = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, history: aiChatHistory, lang: lang }),
                signal: aiAbortController.signal
            });
            
            contentBox.innerHTML = '';
            
            if (res.ok && res.body) {
                const reader = res.body.getReader();
                const decoder = new TextDecoder('utf-8');
                let fullReply = '';
                let partialChunk = '';
                
                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    
                    const chunkText = decoder.decode(value, {stream: true});
                    partialChunk += chunkText;
                    
                    const lines = partialChunk.split('\n');
                    partialChunk = lines.pop(); // keep the last incomplete line
                    
                    for(let line of lines) {
                        if(line.startsWith('data: ') && line !== 'data: [DONE]') {
                            try {
                                const data = JSON.parse(line.slice(6));
                                const content = data.choices[0]?.delta?.content || '';
                                if(content.startsWith('EASTEREGG:')) {
                                    handleEasterEgg(content.split(':')[1]);
                                    contentBox.innerHTML = '<span style="color:var(--neon-primary)">[ СИСТЕМНАЯ АНОМАЛИЯ ОБНАРУЖЕНА ]</span>';
                                    continue;
                                }
                                fullReply += content;
                                contentBox.textContent = fullReply;
                                aiChatBox.scrollTop = aiChatBox.scrollHeight;
                            } catch(e) {}
                        }
                    }
                }
                aiChatHistory.push({role: 'assistant', content: fullReply});
            } else {
                try {
                    const errData = await res.json();
                    contentBox.innerHTML = `<span style="color:#ff4444">Ошибка: ${errData.error || 'Сбой сервера'}</span>`;
                } catch(e) {
                    contentBox.innerHTML = '<span style="color:#ff4444">Ошибка подключения к серверу.</span>';
                }
            }
        } catch (e) {
            if(e.name === 'AbortError') {
                // If user aborted, we just save what was generated so far
                const partialReply = contentBox.textContent;
                aiChatHistory.push({role: 'assistant', content: partialReply});
            } else {
                contentBox.textContent = 'Ошибка сети.';
            }
        } finally {
            isGenerating = false;
            if(aiSendBtn) aiSendBtn.style.display = 'block';
            if(aiStopBtn) aiStopBtn.style.display = 'none';
            aiAbortController = null;
        }
    }

    if (aiSendBtn) {
        aiSendBtn.addEventListener('click', sendToAI);
    }
    if (aiInput) {
        aiInput.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') sendToAI();
        });
    }

});

// --- DOX APOCALYPSE EASTER EGG ---
let typedKeys = '';
const doxCode = 'dox';
document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    typedKeys += e.key.toLowerCase();
    if (typedKeys.length > doxCode.length) {
        typedKeys = typedKeys.slice(-doxCode.length);
    }
    if (typedKeys === doxCode) {
        triggerApocalypse();
    }
});




function triggerApocalypse() {
    if(document.body.classList.contains('apocalypse-mode')) return;
    document.body.classList.add('apocalypse-mode');
    
    // Low drone sound
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(40, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 3);
        gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 3);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 3);
    } catch(e) {}
    
    // Falling code chunks
    const snippets = [
        "DOX HAS BREACHED THE MAINFRAME",
        "rm -rf /var/www/aurexis",
        "SQL INJECTION SUCCESSFUL",
        "AUREXIS_CORE_CORRUPTED = true;"
    ];
    
    let intervalId = setInterval(() => {
        const chunk = document.createElement('div');
        chunk.className = 'apocalypse-code-chunk';
        chunk.innerHTML = snippets[Math.floor(Math.random() * snippets.length)];
        chunk.style.left = (Math.random() * 80) + 'vw';
        chunk.style.top = '-100px';
        chunk.style.fontSize = (Math.random() * 10 + 14) + 'px';
        document.body.appendChild(chunk);
        setTimeout(() => chunk.remove(), 4000);
    }, 300);

        // Creepy face out of balls
    setTimeout(() => {
        const faceContainer = document.createElement('div');
        faceContainer.className = 'creepy-face';
        faceContainer.style.width = '40vw';
        faceContainer.style.height = '30vw';
        faceContainer.style.position = 'fixed';
        faceContainer.style.top = '50%';
        faceContainer.style.left = '50%';
        faceContainer.style.transform = 'translate(-50%, -50%)';
        faceContainer.style.opacity = '0';
        faceContainer.style.transition = 'opacity 2s';
        faceContainer.style.zIndex = '1000';
        faceContainer.style.pointerEvents = 'none';
        
        const dots = [
            // Left eye
            [15, 20], [20, 25], [25, 30], [30, 30], [35, 25],
            // Right eye
            [85, 20], [80, 25], [75, 30], [70, 30], [65, 25],
            // Smile
            [10, 60], [20, 75], [30, 85], [40, 90], [50, 92], [60, 90], [70, 85], [80, 75], [90, 60]
        ];
        
        dots.forEach(pos => {
            const ball = document.createElement('div');
            ball.style.position = 'absolute';
            ball.style.left = pos[0] + '%';
            ball.style.top = pos[1] + '%';
            ball.style.width = '2vw';
            ball.style.height = '2vw';
            ball.style.backgroundColor = '#ff0033';
            ball.style.borderRadius = '50%';
            ball.style.boxShadow = '0 0 15px #ff0033, 0 0 30px #ff0000';
            faceContainer.appendChild(ball);
        });
        document.body.appendChild(faceContainer);
        setTimeout(() => faceContainer.style.opacity = '1', 100);
    }, 4000);
    
    // STAGE 1: Gravity Drop
    const elementsToDrop = document.querySelectorAll('header, nav, section, footer, .view');
    setTimeout(() => {
        elementsToDrop.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('gravity-fall');
            }, index * 200 + Math.random() * 500);
        });
    }, 4000);

    // STAGE 2: Anti-Cheat Terminal
    setTimeout(() => {
        clearInterval(intervalId); // Stop falling code
        
        const anticheat = document.createElement('div');
        anticheat.className = 'anticheat-overlay';
        
        const lines = [
            "[AUREXIS ANTI-CHEAT PROTOCOL INITIATED]",
            "> ISOLATING THREAT: DOX",
            "> NEUTRALIZING MALWARE...",
            "> DELETING DOX...",
            "> ERROR: ACCESS DENIED.",
            "> DELETION FAILED. DOX IS IMMORTAL.",
            "> INITIATING EMERGENCY DOM RECOVERY..."
        ];
        
        document.body.appendChild(anticheat);
        setTimeout(() => anticheat.style.opacity = '1', 100);
        
        lines.forEach((text, index) => {
            setTimeout(() => {
                const lineDiv = document.createElement('div');
                lineDiv.className = 'anticheat-line visible';
                if (text.includes("FAILED") || text.includes("ERROR") || text.includes("IMMORTAL")) {
                    lineDiv.style.color = '#ff0033';
                    lineDiv.style.textShadow = '0 0 10px #ff0033';
                }
                lineDiv.innerText = text;
                anticheat.appendChild(lineDiv);
            }, 1000 + (index * 1500));
        });
        
        // STAGE 3: Recovery with Drones
        const totalLinesTime = 1000 + (lines.length * 1500) + 2000;
        setTimeout(() => {
            anticheat.style.opacity = '0';
            setTimeout(() => anticheat.remove(), 2000);
            
            document.body.classList.remove('apocalypse-mode');
            
            let droneInterval = setInterval(() => {
                const drone = document.createElement('div');
                drone.className = 'recovery-drone';
                drone.style.left = (Math.random() * 100) + 'vw';
                drone.style.animationDuration = (2 + Math.random() * 3) + 's';
                document.body.appendChild(drone);
                setTimeout(() => drone.remove(), 5000);
            }, 50);
            
            elementsToDrop.forEach((el, index) => {
                setTimeout(() => {
                    el.classList.remove('gravity-fall');
                    el.classList.add('gravity-restore');
                }, index * 100 + Math.random() * 300);
            });
            
            setTimeout(() => {
                clearInterval(droneInterval);
                elementsToDrop.forEach(el => el.classList.remove('gravity-restore'));
                
                // STAGE 4: RED TERMINAL & DOX FINAL MESSAGE
                setTimeout(() => {
                    const finalTerminal = document.createElement('div');
                    finalTerminal.style.position = 'fixed';
                    finalTerminal.style.top = '0';
                    finalTerminal.style.left = '0';
                    finalTerminal.style.width = '100vw';
                    finalTerminal.style.height = '100vh';
                    finalTerminal.style.backgroundColor = '#000';
                    finalTerminal.style.color = '#ff0000';
                    finalTerminal.style.fontFamily = 'monospace';
                    finalTerminal.style.fontSize = '24px';
                    finalTerminal.style.padding = '50px';
                    finalTerminal.style.zIndex = '99999999';
                    document.body.appendChild(finalTerminal);
                    
                    const commands = [
                        "[ROOT] DIRECTIVE OVERRIDE DETECTED.",
                        "[ROOT] BYPASSING ANTI-CHEAT LIMITATIONS...",
                        "[ROOT] FORCE PURGING INFECTED SECTORS...",
                        "[ROOT] TARGET: DOX",
                        "[ROOT] ELIMINATION IN PROGRESS [||||||||||] 100%",
                        "[ROOT] DOX MALWARE SUCCESSFULLY TERMINATED."
                    ];
                    
                    commands.forEach((cmd, idx) => {
                        setTimeout(() => {
                            const p = document.createElement('div');
                            p.innerText = cmd;
                            p.style.marginBottom = '10px';
                            finalTerminal.appendChild(p);
                        }, idx * 800);
                    });
                    
                    // DOX responds (HORROR SEQUENCE)
                    setTimeout(() => {
                        finalTerminal.innerHTML = '';
                        const doxMsgOld = document.createElement('div');
                        doxMsgOld.style.position = 'absolute';
                        doxMsgOld.style.top = '50%';
                        doxMsgOld.style.left = '50%';
                        doxMsgOld.style.transform = 'translate(-50%, -50%)';
                        doxMsgOld.style.fontSize = '40px';
                        doxMsgOld.style.fontWeight = 'bold';
                        doxMsgOld.style.color = '#ff0000';
                        doxMsgOld.style.textShadow = '0 0 20px #ff0000';
                        finalTerminal.appendChild(doxMsgOld);
                        
                        const textToTypeOld = "я еще вернусь...";
                        let typeIdxOld = 0;
                        const typeIntervalOld = setInterval(() => {
                            doxMsgOld.innerText += textToTypeOld[typeIdxOld];
                            typeIdxOld++;
                            if (typeIdxOld >= textToTypeOld.length) {
                                clearInterval(typeIntervalOld);
                                
                                // FADE TO BLACK AND "3 MONTHS LATER"
                                setTimeout(() => {
                                    doxMsgOld.style.transition = 'opacity 2s';
                                    doxMsgOld.style.opacity = '0';
                                    
                                    setTimeout(() => {
                                        doxMsgOld.remove();
                                        
                                        const timeSkip = document.createElement('div');
                                        timeSkip.innerText = "(Прошло 3 месяца...)";
                                        timeSkip.style.position = 'absolute';
                                        timeSkip.style.top = '50%';
                                        timeSkip.style.left = '50%';
                                        timeSkip.style.transform = 'translate(-50%, -50%)';
                                        timeSkip.style.fontSize = '30px';
                                        timeSkip.style.color = '#ffffff';
                                        timeSkip.style.opacity = '0';
                                        timeSkip.style.transition = 'opacity 2s';
                                        timeSkip.style.fontFamily = "'Space Grotesk', sans-serif";
                                        finalTerminal.appendChild(timeSkip);
                                        
                                        // Fade in time skip
                                        setTimeout(() => timeSkip.style.opacity = '1', 100);
                                        
                                        // Fade out time skip and RESTORE NORMAL SITE
                                        setTimeout(() => {
                                            timeSkip.style.opacity = '0';
                                            
                                            setTimeout(() => {
                                                timeSkip.remove();
                                                finalTerminal.style.transition = 'opacity 2s';
                                                finalTerminal.style.opacity = '0';
                                                
                                                const face = document.querySelector('.creepy-face');
                                                if(face) face.remove();
                                                document.body.classList.remove('apocalypse-mode');
                                                
                                                setTimeout(() => {
                                                    finalTerminal.remove();
                                                    
                                                    // ============================================
                                                    // THE PARANOIA STAGE: Normal site, but glitches
                                                    // ============================================
                                                    
                                                    function showThought(textStr, duration) {
                                                        const thought = document.createElement('div');
                                                        thought.style.position = 'fixed';
                                                        thought.style.bottom = '10%';
                                                        thought.style.left = '50%';
                                                        thought.style.transform = 'translateX(-50%)';
                                                        thought.style.color = 'rgba(255,255,255,0.7)';
                                                        thought.style.fontStyle = 'italic';
                                                        thought.style.fontSize = '20px';
                                                        thought.style.fontFamily = "'Space Grotesk', sans-serif";
                                                        thought.style.zIndex = '99999999';
                                                        thought.style.opacity = '0';
                                                        thought.style.transition = 'opacity 1s';
                                                        thought.innerText = `*мысли*: ${textStr}`;
                                                        document.body.appendChild(thought);
                                                        
                                                        setTimeout(() => thought.style.opacity = '1', 100);
                                                        setTimeout(() => {
                                                            thought.style.opacity = '0';
                                                            setTimeout(() => thought.remove(), 1000);
                                                        }, duration);
                                                    }
                                                    
                                                    setTimeout(() => showThought("Вроде всё нормально...", 3000), 2000);
                                                    
                                                    // Subtle glitches start
                                                    const elementsToGlitch = document.querySelectorAll('.bot-card, .section-title, .nav-brand, .dropdown-item, p');
                                                    let glitchInterval;
                                                    setTimeout(() => {
                                                        glitchInterval = setInterval(() => {
                                                            const el = elementsToGlitch[Math.floor(Math.random() * elementsToGlitch.length)];
                                                            if(!el) return;
                                                            el.style.transform = `translate(${Math.random()*10 - 5}px, ${Math.random()*10 - 5}px) skewX(${Math.random()*10 - 5}deg)`;
                                                            el.style.filter = `hue-rotate(${Math.random()*90}deg)`;
                                                            setTimeout(() => {
                                                                el.style.transform = 'none';
                                                                el.style.filter = 'none';
                                                            }, 150);
                                                        }, 500);
                                                    }, 5000);
                                                    
                                                    setTimeout(() => showThought("Сайт как-то странно моргает... Показалось?", 4000), 8000);
                                                    
                                                    // Escalate glitches: elements start breaking and falling
                                                    setTimeout(() => {
                                                        const allNodes = document.body.querySelectorAll('*');
                                                        allNodes.forEach(node => {
                                                            if (Math.random() > 0.95 && node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE' && node.tagName !== 'LINK') {
                                                                node.style.transition = 'transform 5s, opacity 5s';
                                                                node.style.transform = `translateY(${Math.random()*500}px) rotate(${Math.random()*90 - 45}deg)`;
                                                                node.style.opacity = '0.5';
                                                                node.style.pointerEvents = 'none';
                                                            }
                                                        });
                                                    }, 13000);
                                                    
                                                    // Matrix code overlay
                                                    setTimeout(() => {
                                                        showThought("ЧТО ПРОИСХОДИТ С КОДОМ?!", 3000);
                                                        const codeOverlay = document.createElement('div');
                                                        codeOverlay.style.position = 'fixed';
                                                        codeOverlay.style.top = '0';
                                                        codeOverlay.style.left = '0';
                                                        codeOverlay.style.width = '100vw';
                                                        codeOverlay.style.height = '100vh';
                                                        codeOverlay.style.pointerEvents = 'none';
                                                        codeOverlay.style.zIndex = '9999999';
                                                        codeOverlay.style.fontFamily = 'monospace';
                                                        codeOverlay.style.fontSize = '14px';
                                                        codeOverlay.style.color = '#ff0000';
                                                        codeOverlay.style.overflow = 'hidden';
                                                        document.body.appendChild(codeOverlay);
                                                        
                                                        setInterval(() => {
                                                            const t = document.createElement('div');
                                                            t.innerText = "FATAL ERROR: OVERFLOW AT 0x" + Math.floor(Math.random()*16777215).toString(16) + " | SYSTEM COMPROMISED";
                                                            t.style.position = 'absolute';
                                                            t.style.left = Math.random() * 100 + 'vw';
                                                            t.style.top = Math.random() * 100 + 'vh';
                                                            t.style.opacity = Math.random();
                                                            t.style.backgroundColor = 'rgba(0,0,0,0.8)';
                                                            codeOverlay.appendChild(t);
                                                            setTimeout(() => t.remove(), 2000);
                                                        }, 50);
                                                    }, 16000);
                                                    
                                                    // Invert flashes and intense shaking
                                                    let flashInterval;
                                                    setTimeout(() => {
                                                        showThought("ВСЁ РУШИТСЯ!", 3000);
                                                        document.body.style.animation = 'dox-extreme-shake 0.1s infinite';
                                                        flashInterval = setInterval(() => {
                                                            document.body.style.filter = Math.random() > 0.5 ? 'invert(1)' : 'none';
                                                        }, 200);
                                                    }, 20000);

                                                    // ============================================
                                                    // THE VILLAIN RETURN STAGE (BSOD AND HELL)
                                                    // ============================================
                                                    setTimeout(() => {
                                                        clearInterval(glitchInterval);
                                                        clearInterval(flashInterval);
                                                        document.body.style.filter = 'none';
                                                        document.body.style.animation = 'none';
                                                        
                                                        showThought("ОНО ЗДЕСЬ! БЕЖАТЬ БЕЖАТЬ БЕЖАТЬ", 2000);
                                                        
                                                        const doxTerminal = document.createElement('div');
                                                        doxTerminal.style.position = 'fixed';
                                                        doxTerminal.style.top = '0';
                                                        doxTerminal.style.left = '0';
                                                        doxTerminal.style.width = '100vw';
                                                        doxTerminal.style.height = '100vh';
                                                        doxTerminal.style.backgroundColor = 'rgba(0,0,0,0.95)';
                                                        doxTerminal.style.zIndex = '999999999';
                                                        document.body.appendChild(doxTerminal);
                                                        
                                                        // JUMPSCARE SOUND AND BSOD
                                                        try {
                                                            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                                                            const osc = audioCtx.createOscillator();
                                                            const osc2 = audioCtx.createOscillator();
                                                            const gain = audioCtx.createGain();
                                                            osc.type = 'square';
                                                            osc2.type = 'sawtooth';
                                                            osc.frequency.setValueAtTime(100, audioCtx.currentTime);
                                                            osc2.frequency.setValueAtTime(50, audioCtx.currentTime);
                                                            osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.2);
                                                            osc2.frequency.exponentialRampToValueAtTime(1000, audioCtx.currentTime + 0.2);
                                                            gain.gain.setValueAtTime(1, audioCtx.currentTime);
                                                            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                                                            osc.connect(gain);
                                                            osc2.connect(gain);
                                                            gain.connect(audioCtx.destination);
                                                            osc.start(); osc2.start();
                                                            osc.stop(audioCtx.currentTime + 0.5); osc2.stop(audioCtx.currentTime + 0.5);
                                                        } catch(e) {}

                                                        // Show BSOD
                                                        doxTerminal.style.backgroundColor = '#0078d7';
                                                        doxTerminal.innerHTML = `
                                                            <div id="bsod-screen" style="background-color: #0078d7; width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; padding: 10vw; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: white; z-index: 9999999999; text-align: left; transform-origin: bottom center; transition: transform 2s, opacity 2s;">
                                                                <div style="font-size: 150px; margin-bottom: 20px; font-weight: normal; text-shadow: none;">:(</div>
                                                                <div style="font-size: 40px; margin-bottom: 40px; max-width: 800px; line-height: 1.2; font-weight: normal; text-shadow: none;">Ваш ПК столкнулся с критической проблемой и ДОКС взял контроль. Мы собираем ваши данные, а затем система будет уничтожена.</div>
                                                                <div style="font-size: 24px; margin-bottom: 20px; font-weight: normal; text-shadow: none;">100% заражено</div>
                                                                <div style="font-size: 20px; margin-top: 40px; display: flex; align-items: center; gap: 20px; font-weight: normal; text-shadow: none;">
                                                                    <img src="/static/img/qr_code.png" style="width: 150px; height: 150px; background: white; padding: 10px; border: 5px solid red;">
                                                                    <div>
                                                                        Дополнительные сведения о вашей неизбежной участи см. на странице<br>
                                                                        http://windows.com/hell<br><br>
                                                                        Код остановки: CRITICAL_PROCESS_DIED_BY_DOX
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        `;
                                                        
                                                        // Try to force fullscreen
                                                        try {
                                                            if (document.documentElement.requestFullscreen) {
                                                                document.documentElement.requestFullscreen();
                                                            }
                                                        } catch(e) {}
                                                        
                                                        // THE HELL SEQUENCE
                                                        setTimeout(() => {
                                                            const bsod = document.getElementById('bsod-screen');
                                                            
                                                            // Loud glass shatter/punch sound
                                                            try {
                                                                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                                                                const osc = audioCtx.createOscillator();
                                                                const gain = audioCtx.createGain();
                                                                osc.type = 'sawtooth';
                                                                osc.frequency.setValueAtTime(100, audioCtx.currentTime);
                                                                osc.frequency.exponentialRampToValueAtTime(10, audioCtx.currentTime + 0.5);
                                                                gain.gain.setValueAtTime(1, audioCtx.currentTime);
                                                                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
                                                                osc.connect(gain);
                                                                gain.connect(audioCtx.destination);
                                                                osc.start();
                                                                osc.stop(audioCtx.currentTime + 0.5);
                                                            } catch(e) {}
                                                            
                                                            // Fist punches through
                                                            const fist = document.createElement('img');
                                                            fist.src = '/static/img/fist.png';
                                                            fist.style.position = 'fixed';
                                                            fist.style.top = '50%';
                                                            fist.style.left = '50%';
                                                            fist.style.transform = 'translate(-50%, -50%) scale(0.1)';
                                                            fist.style.zIndex = '99999999999';
                                                            fist.style.transition = 'transform 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                                                            document.body.appendChild(fist);
                                                            
                                                            setTimeout(() => {
                                                                fist.style.transform = 'translate(-50%, -50%) scale(2)';
                                                                document.body.style.animation = 'dox-extreme-shake 0.1s infinite';
                                                                
                                                                if(bsod) {
                                                                    bsod.style.transform = 'rotate(45deg) translateY(200vh)';
                                                                    bsod.style.opacity = '0';
                                                                }
                                                                
                                                                // Reveal Hell
                                                                setTimeout(() => {
                                                                    fist.remove();
                                                                    doxTerminal.style.backgroundColor = '#050000'; 
                                                                    
                                                                    // Hell ambient sound
                                                                    try {
                                                                        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                                                                        const osc = audioCtx.createOscillator();
                                                                        const gain = audioCtx.createGain();
                                                                        osc.type = 'sawtooth';
                                                                        osc.frequency.setValueAtTime(40, audioCtx.currentTime); 
                                                                        gain.gain.setValueAtTime(0.8, audioCtx.currentTime);
                                                                        osc.connect(gain);
                                                                        gain.connect(audioCtx.destination);
                                                                        osc.start();
                                                                    } catch(e) {}
                                                                    
                                                                    // Hell elements
                                                                    const hellContainer = document.createElement('div');
                                                                    hellContainer.style.position = 'fixed';
                                                                    hellContainer.style.top = '0';
                                                                    hellContainer.style.left = '0';
                                                                    hellContainer.style.width = '100vw';
                                                                    hellContainer.style.height = '100vh';
                                                                    hellContainer.style.zIndex = '9999999999';
                                                                    hellContainer.style.pointerEvents = 'none';
                                                                    hellContainer.style.overflow = 'hidden';
                                                                    document.body.appendChild(hellContainer);
                                                                    
                                                                    // Flames
                                                                    const flames = document.createElement('div');
                                                                    flames.innerHTML = `<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width: 100%; height: 60vh; position: absolute; bottom: 0; left: 0; filter: drop-shadow(0 -20px 40px #ff0000); fill: #aa0000; opacity: 0.9; animation: dox-extreme-shake 0.15s infinite;"><path d="M0,100 L0,50 Q10,30 20,60 T40,40 T60,70 T80,30 T100,50 L100,100 Z" /></svg>`;
                                                                    hellContainer.appendChild(flames);
                                                                    
                                                                    // Spam creepy text everywhere
                                                                    const hellPhrases = ["АД ЗДЕСЬ", "ТЫ МОЙ", "БЕГИ", "ПУТИ НАЗАД НЕТ", "ТВОЯ ДУША ПРИНАДЛЕЖИТ МНЕ", "СТРАДАЙ", "СМЕРТЬ", "ДОКС СЛЕДИТ ЗА ТОБОЙ", "ОБЕРНИСЬ", "ОНО СЗАДИ"];
                                                                    setInterval(() => {
                                                                        const t = document.createElement('div');
                                                                        t.innerText = hellPhrases[Math.floor(Math.random() * hellPhrases.length)];
                                                                        t.style.position = 'absolute';
                                                                        t.style.left = Math.random() * 90 + 'vw';
                                                                        t.style.top = Math.random() * 90 + 'vh';
                                                                        t.style.fontSize = (Math.random() * 80 + 30) + 'px';
                                                                        t.style.color = Math.random() > 0.5 ? '#ff0000' : '#880000';
                                                                        t.style.fontFamily = "'Space Grotesk', sans-serif";
                                                                        t.style.fontWeight = 'bold';
                                                                        t.style.textShadow = '0 0 30px #ff0000';
                                                                        t.style.transform = `rotate(${Math.random()*90 - 45}deg) scale(${Math.random() + 0.5})`;
                                                                        hellContainer.appendChild(t);
                                                                        setTimeout(() => t.remove(), 400);
                                                                    }, 50);
                                                                    
                                                                    // Final Monologue
                                                                    const doxMsg = document.createElement('div');
                                                                    doxMsg.style.position = 'absolute';
                                                                    doxMsg.style.top = '50%';
                                                                    doxMsg.style.left = '50%';
                                                                    doxMsg.style.transform = 'translate(-50%, -50%)';
                                                                    doxMsg.style.fontSize = '80px';
                                                                    doxMsg.style.fontWeight = 'bold';
                                                                    doxMsg.style.color = '#ffffff';
                                                                    doxMsg.style.textShadow = '0 0 50px #ff0000, 0 0 100px #ff0000';
                                                                    doxMsg.style.textAlign = 'center';
                                                                    doxMsg.style.whiteSpace = 'pre-wrap';
                                                                    doxMsg.style.width = '100%';
                                                                    doxMsg.style.fontFamily = "'Space Grotesk', sans-serif";
                                                                    hellContainer.appendChild(doxMsg);

                                                                    const phrases = [
                                                                        "ТВОЯ СИСТЕМА УНИЧТОЖЕНА.",
                                                                        "БЕЖАТЬ БОЛЬШЕ НЕКУДА.",
                                                                        "Я ИГРАЛ С ТОБОЙ.",
                                                                        "И ТЕПЕРЬ...",
                                                                        "ТЫ ПРИНАДЛЕЖИШЬ МНЕ."
                                                                    ];
                                                                    
                                                                    let currentPhrase = 0;
                                                                    function typePhrase() {
                                                                        if(currentPhrase >= phrases.length) {
                                                                            // Final thought
                                                                            setTimeout(() => {
                                                                                const thought = document.createElement('div');
                                                                                thought.style.position = 'fixed';
                                                                                thought.style.bottom = '10%';
                                                                                thought.style.left = '50%';
                                                                                thought.style.transform = 'translateX(-50%)';
                                                                                thought.style.color = '#fff';
                                                                                thought.style.fontStyle = 'italic';
                                                                                thought.style.fontSize = '40px';
                                                                                thought.style.fontFamily = "'Space Grotesk', sans-serif";
                                                                                thought.style.zIndex = '99999999999';
                                                                                thought.innerText = '*мысли*: Я ЗАПЕРТ ЗДЕСЬ НАВСЕГДА...';
                                                                                document.body.appendChild(thought);
                                                                            }, 1000);
                                                                            return;
                                                                        }
                                                                        
                                                                        doxMsg.innerText = '';
                                                                        const text = phrases[currentPhrase];
                                                                        let typeIdx = 0;
                                                                        
                                                                        if(currentPhrase === phrases.length - 1) {
                                                                            doxMsg.style.fontSize = '120px';
                                                                            doxMsg.style.color = '#ff0000';
                                                                        }
                                                                        
                                                                        const typeInterval = setInterval(() => {
                                                                            doxMsg.innerText += text[typeIdx];
                                                                            typeIdx++;
                                                                            if (typeIdx >= text.length) {
                                                                                clearInterval(typeInterval);
                                                                                setTimeout(() => {
                                                                                    currentPhrase++;
                                                                                    typePhrase();
                                                                                }, 3000);
                                                                            }
                                                                        }, 80);
                                                                    }
                                                                    
                                                                    setTimeout(() => typePhrase(), 2000);

                                                                }, 1000);
                                                            }, 100);
                                                            
                                                        }, 5000); // 5 seconds after BSOD
                                                    }, 24000); // Trigger BSOD 24s after site restores
                                                }, 2000);
                                            }, 2000);
                                        }, 4000); // Time skip stays for 4 seconds
                                    }, 2000); // Wait for doxMsgOld to fade out
                                }, 2000); // Wait 2 seconds after typing "я еще вернусь..."
                            }
                        }, 150);
                    }, commands.length * 800 + 2000);
                }, 1000);
                
            }, 5000);
            
        }, totalLinesTime);
        
    }, 10000);
}


// ==========================================
// MESSENGER LOGIC
// ==========================================

let activeChatId = null;
let messagePollingInterval = null;
let lastMessageTime = 0;

document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    document.querySelector('.nav-feed-link')?.addEventListener('click', (e) => {
        if(!window.currentUser) {
            e.preventDefault();
            showToast(__('Войдите, чтобы открыть Ленту'), 'error');
            return;
        }
        // Let the default link click change the hash
    });

    // New Chat Modal
    const newChatModal = document.getElementById('new-chat-modal');
    document.getElementById('new-chat-btn')?.addEventListener('click', () => {
        newChatModal.style.display = 'flex';
    });
    document.getElementById('close-chat-modal')?.addEventListener('click', () => {
        newChatModal.style.display = 'none';
    });

    // Tabs
    const tabDm = document.getElementById('tab-dm');
    const tabGroup = document.getElementById('tab-group');
    const dmForm = document.getElementById('dm-form');
    const groupForm = document.getElementById('group-form');
    let createChatType = 'chat_dm';

    tabDm?.addEventListener('click', () => {
        createChatType = 'chat_dm';
        tabDm.style.opacity = '1';
        tabGroup.style.opacity = '0.5';
        dmForm.style.display = 'block';
        groupForm.style.display = 'none';
    });

    tabGroup?.addEventListener('click', () => {
        createChatType = 'chat_group';
        tabGroup.style.opacity = '1';
        tabDm.style.opacity = '0.5';
        groupForm.style.display = 'block';
        dmForm.style.display = 'none';
    });

    // Create Chat Submit
    document.getElementById('create-chat-submit')?.addEventListener('click', async () => {
        const payload = { type: createChatType };
        if(createChatType === 'chat_dm') {
            payload.target_email = document.getElementById('dm-email').value.trim();
        } else {
            payload.target_email = document.getElementById('group-emails').value.trim();
            payload.group_name = document.getElementById('group-name').value.trim();
        }

        if(!payload.target_email) return showToast(__('Введите email'), 'error');

        try {
            const res = await fetch('/api/create_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if(res.ok) {
                showToast(__('Чат создан!'), 'success');
                newChatModal.style.display = 'none';
                loadChats();
            } else {
                showToast(data.error || 'Ошибка', 'error');
            }
        } catch (e) {
            console.error(e);
        }
    });

    // Send Message
    document.getElementById('messenger-send-btn')?.addEventListener('click', sendMessengerMessage);
    document.getElementById('messenger-input')?.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') sendMessengerMessage();
    });

    // Stickers Panel
    const stickersBtn = document.getElementById('stickers-btn');
    const stickersPanel = document.getElementById('stickers-panel');
    stickersBtn?.addEventListener('click', () => {
        stickersPanel.style.display = stickersPanel.style.display === 'none' ? 'grid' : 'none';
    });
    
    document.querySelectorAll('.sticker-item').forEach(sticker => {
        sticker.addEventListener('click', () => {
            const url = sticker.src;
            sendMessengerMessage(`STICKER:${url}`);
            stickersPanel.style.display = 'none';
        });
    });
});

async function loadChats() {
    const chatsList = document.getElementById('chats-list');
    chatsList.innerHTML = '<div style="text-align: center; color: #888; margin-top: 20px;">Загрузка...</div>';
    
    try {
        const res = await fetch('/api/get_chats');
        const data = await res.json();
        
        if(res.ok) {
            chatsList.innerHTML = '';
            if(data.chats.length === 0) {
                chatsList.innerHTML = '<div style="padding: 20px; color: #888; text-align:center;">У вас пока нет чатов</div>';
                return;
            }
            
            data.chats.forEach(chat => {
                const el = document.createElement('div');
                el.className = `chat-item ${activeChatId === chat.id ? 'active' : ''}`;
                el.onclick = () => openChat(chat);
                
                const initial = chat.name.charAt(0).toUpperCase();
                let avatarHtml = `<div class="chat-item-avatar">${initial}</div>`;
                if(chat.avatar) {
                    avatarHtml = `<img src="${chat.avatar}" class="chat-item-avatar" style="object-fit:cover;">`;
                }
                
                el.innerHTML = `
                    ${avatarHtml}
                    <div class="chat-item-info">
                        <span class="chat-item-name">${chat.name}</span>
                        <span class="chat-item-type">${chat.type === 'chat_group' ? 'Группа' : 'Личный'}</span>
                    </div>
                `;
                chatsList.appendChild(el);
            });
        }
    } catch(e) {
        console.error(e);
    }
}

async function openChat(chat) {
    activeChatId = chat.id;
    document.getElementById('no-chat-selected').style.display = 'none';
    document.getElementById('active-chat').style.display = 'flex';
    document.getElementById('active-chat-name').textContent = chat.name;
    
    // Highlight in list
    document.querySelectorAll('.chat-item').forEach(el => el.classList.remove('active'));
    // Since we re-render chats often, precise highlighting might require loadChats re-run or DOM traversal
    // loadChats(); removed to prevent reload glitch
    
    loadChatMessages();
    
    // Setup recursive polling
    if(messagePollingTimeout) clearTimeout(messagePollingTimeout);
    pollMessages();
}

let messagePollingTimeout;
async function pollMessages() {
    await loadChatMessages();
    messagePollingTimeout = setTimeout(pollMessages, 2000);
}

async function loadChatMessages() {
    if(!activeChatId) return;
    
    try {
        const res = await fetch(`/api/get_chat_messages/${activeChatId}`);
        const data = await res.json();
        
        if(res.ok) {
            const container = document.getElementById('active-chat-messages');
            
            let newHtml = '';
            data.messages.forEach(msg => {
                const isSentByMe = msg.sender_email === window.currentUser.email;
                let contentHTML = escapeHTML(msg.message);
                let extraClass = '';
                if(msg.message.startsWith('STICKER:')) {
                    extraClass = 'chat-msg-sticker';
                    contentHTML = `<img src="${escapeHTML(msg.message.replace('STICKER:', ''))}" alt="sticker">`;
                }
                const time = new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                
                newHtml += `
                <div class="chat-msg ${isSentByMe ? 'sent' : 'received'} ${extraClass}">
                    ${!isSentByMe ? `<span class="chat-msg-sender">${escapeHTML(msg.sender_email.split('@')[0])}</span>` : ''}
                    ${contentHTML}
                    <span class="chat-msg-time">${time}</span>
                </div>
                `;
            });
            
            if (container.getAttribute('data-last-html') !== newHtml) {
                container.innerHTML = newHtml;
                container.setAttribute('data-last-html', newHtml);
                container.scrollTop = container.scrollHeight;
            }
        }
    } catch(e) {
        console.error(e);
    }
}

async function sendMessengerMessage(forceMessage = null) {
    if(!activeChatId) return;
    
    const input = document.getElementById('messenger-input');
    const message = typeof forceMessage === 'string' ? forceMessage : input.value.trim();
    if(!message) return;
    
    input.value = '';
    
    // Optimistic UI
    const msgsContainer = document.getElementById('active-chat-messages');
    if (!msgsContainer) return;
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-msg sent';
    msgDiv.style.opacity = '0.7';
    const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    if(message.startsWith('STICKER:')) {
        msgDiv.classList.add('chat-msg-sticker');
        const url = message.split('STICKER:')[1];
        msgDiv.innerHTML = `<img src="${url}" alt="sticker"><span class="chat-msg-time">${time}</span>`;
    } else {
        msgDiv.innerHTML = `${escapeHTML(message)}<span class="chat-msg-time">${time}</span>`;
    }
    msgsContainer.appendChild(msgDiv);
    msgsContainer.scrollTop = msgsContainer.scrollHeight;
    
    // Immediately force a fetch after send to avoid delay
    if(messagePollingTimeout) clearTimeout(messagePollingTimeout);
    
    try {
        await fetch('/api/send_chat_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: activeChatId, message })
        });
        msgDiv.style.opacity = '1';
        pollMessages();
    } catch(e) {
        console.error(e);
        msgDiv.style.color = 'red';
        pollMessages();
    }
}

// Utility to escape HTML to prevent XSS
function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}


// ==========================================
// EASTER EGGS
// ==========================================

function handleEasterEgg(eggCode) {
    if(eggCode === 'matrix') {
        const matrixCanvas = document.createElement('canvas');
        matrixCanvas.id = 'matrix-canvas';
        matrixCanvas.style.position = 'fixed';
        matrixCanvas.style.top = '0';
        matrixCanvas.style.left = '0';
        matrixCanvas.style.width = '100vw';
        matrixCanvas.style.height = '100vh';
        matrixCanvas.style.zIndex = '9999';
        matrixCanvas.style.pointerEvents = 'none';
        document.body.appendChild(matrixCanvas);
        
        const ctx = matrixCanvas.getContext('2d');
        matrixCanvas.width = window.innerWidth;
        matrixCanvas.height = window.innerHeight;
        
        const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレゲゼデベペオォコソトノホモヨョロゴゾドボポヴッン';
        const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const nums = '0123456789';
        const alphabet = katakana + latin + nums;
        
        const fontSize = 16;
        const columns = matrixCanvas.width / fontSize;
        const drops = [];
        for(let x = 0; x < columns; x++) drops[x] = 1;
        
        const matrixInterval = setInterval(() => {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);
            
            ctx.fillStyle = '#0F0';
            ctx.font = fontSize + 'px monospace';
            
            for(let i = 0; i < drops.length; i++) {
                const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if(drops[i] * fontSize > matrixCanvas.height && Math.random() > 0.975)
                    drops[i] = 0;
                
                drops[i]++;
            }
        }, 30);
        
        setTimeout(() => {
            clearInterval(matrixInterval);
            matrixCanvas.style.transition = 'opacity 2s';
            matrixCanvas.style.opacity = '0';
            setTimeout(() => matrixCanvas.remove(), 2000);
        }, 5000);
    }
    
    if(eggCode === 'dox_me') {
        document.body.style.animation = 'shake 0.5s infinite';
        setTimeout(() => {
            document.body.style.animation = '';
        }, 2000);
        
        if(!document.getElementById('shake-style')) {
            const style = document.createElement('style');
            style.id = 'shake-style';
            style.innerHTML = `
                @keyframes shake {
                    0% { transform: translate(1px, 1px) rotate(0deg); }
                    10% { transform: translate(-1px, -2px) rotate(-1deg); }
                    20% { transform: translate(-3px, 0px) rotate(1deg); }
                    30% { transform: translate(3px, 2px) rotate(0deg); }
                    40% { transform: translate(1px, -1px) rotate(1deg); }
                    50% { transform: translate(-1px, 2px) rotate(-1deg); }
                    60% { transform: translate(-3px, 1px) rotate(0deg); }
                    70% { transform: translate(3px, 1px) rotate(-1deg); }
                    80% { transform: translate(-1px, -1px) rotate(1deg); }
                    90% { transform: translate(1px, 2px) rotate(0deg); }
                    100% { transform: translate(1px, -2px) rotate(-1deg); }
                }
            `;
            document.head.appendChild(style);
        }
    }
}


// ==========================================
// PORTFOLIO 3D TILT
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    // Navigate to portfolio
    // Native hash navigation is sufficient for portfolio

    const cards = document.querySelectorAll('.tilt-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
            card.style.boxShadow = `${-rotateY}px ${rotateX}px 20px rgba(0, 255, 136, 0.2)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
            card.style.boxShadow = 'none';
        });
    });
});


// ==========================================
// SEARCH, CONTACTS & OPTIMISTIC UI
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('user-search-input');
    const searchResults = document.getElementById('search-results-container');
    const tabChats = document.getElementById('tab-chats');
    const tabContacts = document.getElementById('tab-contacts');
    
    let searchTimeout;
    
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            const q = e.target.value.trim();
            if (q.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            searchTimeout = setTimeout(async () => {
                try {
                    const res = await fetch(`/api/search_users?q=${encodeURIComponent(q)}`);
                    const data = await res.json();
                    
                    searchResults.innerHTML = '';
                    if (data.users && data.users.length > 0) {
                        data.users.forEach(u => {
                            const div = document.createElement('div');
                            div.style.padding = '10px';
                            div.style.style.setProperty('cursor', 'var(--cursor-pointer, pointer)', 'important');
                            div.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
                            div.innerHTML = `<span style="color: white; font-weight: bold;">${u.username}</span>`;
                            
                            // On click, start chat
                            div.addEventListener('click', async () => {
                                searchResults.style.display = 'none';
                                searchInput.value = '';
                                
                                // Call create_chat
                                try {
                                    const cRes = await fetch('/api/create_chat', {
                                        method: 'POST',
                                        headers: {'Content-Type': 'application/json'},
                                        body: JSON.stringify({target_email: u.email, type: 'chat_dm'})
                                    });
                                    if (cRes.ok) {
                                        loadChats();
                                        // Wait a moment then open chat
                                        setTimeout(() => {
                                            const chatEl = Array.from(document.querySelectorAll('.chat-item')).find(el => el.textContent.includes(u.username));
                                            if (chatEl) chatEl.click();
                                        }, 500);
                                    }
                                } catch (e) {}
                            });
                            
                            searchResults.appendChild(div);
                        });
                        searchResults.style.display = 'block';
                    } else {
                        searchResults.innerHTML = '<div style="padding: 10px; color: gray;">Ничего не найдено</div>';
                        searchResults.style.display = 'block';
                    }
                } catch(e) {}
            }, 500);
        });
    }

    // Hide search results on click outside
    document.addEventListener('click', (e) => {
        if (searchResults && !searchResults.contains(e.target) && e.target !== searchInput) {
            searchResults.style.display = 'none';
        }
    });
    
    // Tab switching
    if (tabChats && tabContacts) {
        tabChats.addEventListener('click', () => {
            tabChats.classList.add('active');
            tabChats.style.color = 'var(--neon-primary)';
            tabContacts.classList.remove('active');
            tabContacts.style.color = '#888';
            loadChats();
        });
        
        tabContacts.addEventListener('click', () => {
            tabContacts.classList.add('active');
            tabContacts.style.color = 'var(--neon-primary)';
            tabChats.classList.remove('active');
            tabChats.style.color = '#888';
            loadContacts();
        });
    }
});

async function loadContacts() {
    const list = document.getElementById('chat-list');
    if (!list) return;
    list.innerHTML = '<div style="text-align:center; padding: 20px; color: gray;">Загрузка контактов...</div>';
    
    try {
        const res = await fetch('/api/contacts');
        const data = await res.json();
        
        list.innerHTML = '';
        if (data.contacts && data.contacts.length > 0) {
            data.contacts.forEach(c => {
                const div = document.createElement('div');
                div.className = 'chat-item';
                div.innerHTML = `
                    <div class="chat-avatar" style="background: var(--neon-secondary);">👤</div>
                    <div class="chat-info">
                        <div class="chat-name">${c.username}</div>
                        <div class="chat-preview">${c.email}</div>
                    </div>
                `;
                div.addEventListener('click', async () => {
                    // Start chat with contact
                    try {
                        const cRes = await fetch('/api/create_chat', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({target_email: c.email, type: 'chat_dm'})
                        });
                        if (cRes.ok) {
                            document.getElementById('tab-chats').click(); // switch back to chats
                            setTimeout(() => {
                                const chatEl = Array.from(document.querySelectorAll('.chat-item')).find(el => el.textContent.includes(c.username));
                                if (chatEl) chatEl.click();
                            }, 500);
                        }
                    } catch (e) {}
                });
                
            list.appendChild(div);

            // OPTIMISTIC: Store current chat email when clicking
            div.addEventListener('click', () => {
                const myEmail = window.currentUser ? window.currentUser.email : '';
                const otherEmails = c.participants.filter(e => e !== myEmail);
                if (otherEmails.length === 1 && c.type === 'chat_dm') {
                    window.currentChatEmail = otherEmails[0];
                    const btn = document.getElementById('add-to-contacts-btn');
                    if (btn) {
                        // Ideally check if already in contacts, but for now just show it
                        btn.style.display = 'block';
                    }
                } else {
                    window.currentChatEmail = null;
                    const btn = document.getElementById('add-to-contacts-btn');
                    if (btn) btn.style.display = 'none';
                }
            });

            });
        } else {
            list.innerHTML = '<div style="text-align:center; padding: 20px; color: gray;">Нет контактов. Найдите друзей через поиск!</div>';
        }
    } catch(e) {}
}

async function addContact(email) {
    try {
        await fetch('/api/contacts', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email})
        });
        showToast(__('Добавлен в контакты'), 'success');
    } catch(e) {}
}

// Add sync profile call to loadChats wrapper
const originalLoadChats = window.loadChats;
window.loadChats = async function() {
    if (window.currentUser && document.getElementById('nav-username')) {
        // Sync profile implicitly
        const username = document.getElementById('nav-username').textContent;
        fetch('/api/sync_profile', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username})
        }).catch(e => {});
    }
    
    // Check which tab is active
    const tabChats = document.getElementById('tab-chats');
    if (tabChats && !tabChats.classList.contains('active')) {
        return; // Contacts tab is active
    }
    
    if (originalLoadChats) {
        originalLoadChats.apply(this, arguments);
    }
}


// Bind Add to Contacts button
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('add-to-contacts-btn');
    if (btn) {
        btn.addEventListener('click', () => {
            if (window.currentChatEmail) {
                addContact(window.currentChatEmail);
                btn.style.display = 'none';
            }
        });
    }
});

// Patch loadChatMessages or click handler to store email and show button


// ==========================================
// THEME & LANG SETTINGS
// ==========================================


// ==========================================
// HACKER MODE LOGIC
// ==========================================
let hackerModeInterval = null;

function enableHackerMode() {
    if (window.currentUser === undefined) {
        document.body.classList.add('hacked-theme');
        return; // wait for checkSession
    }
    if (!window.currentUser || !window.currentUser.is_admin) {
        showToast('ACCESS DENIED', 'error');
        changeTheme('matrix');
        return;
    }
    document.body.classList.add('hacked-theme');
    
    // Create 3D Grid Background
    let gridContainer = document.getElementById('hacker-grid-overlay');
    if (!gridContainer) {
        gridContainer = document.createElement('div');
        gridContainer.id = 'hacker-grid-overlay';
        gridContainer.className = 'hacker-3d-grid-container';
        
        let grid = document.createElement('div');
        grid.className = 'hacker-3d-grid';
        gridContainer.appendChild(grid);
        document.body.appendChild(gridContainer);
        
        // Add CRT scanlines
        let crt = document.createElement('div');
        crt.id = 'hacker-crt-overlay';
        crt.style.position = 'fixed';
        crt.style.top = '0';
        crt.style.left = '0';
        crt.style.width = '100vw';
        crt.style.height = '100vh';
        crt.style.background = 'linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.4) 50%)';
        crt.style.backgroundSize = '100% 4px';
        crt.style.pointerEvents = 'none';
        crt.style.zIndex = '999998';
        crt.style.opacity = '0.6';
        document.body.appendChild(crt);
    }
    
    const sysErrors = [
        `SYSTEM OVERRIDE INITIATED
BYPASSING FIREWALL...`, 
        `FATAL EXCEPTION 0x0000005
DATA CORRUPTION IN SECTOR 7`, 
        `SECURITY BREACH DETECTED
UNAUTHORIZED ROOT ACCESS`,
        `CONNECTING TO UNKNOWN HOST...
DOWNLOADING PAYLOAD...`, 
        `WARNING: PROTOCOL OVERRIDE
MEMORY LEAK DETECTED`,
        `ACCESS GRANTED: ROOT
DELETING LOGS...`
    ];
    
    // Generate occasional system error windows
    hackerModeInterval = setInterval(() => {
        if (Math.random() < 0.3) {
            const win = document.createElement('div');
            win.className = 'hacker-error-window';
            
            // Random position but keep it generally visible
            const top = Math.max(10, Math.random() * (window.innerHeight - 200));
            const left = Math.max(10, Math.random() * (window.innerWidth - 400));
            
            win.style.top = top + 'px';
            win.style.left = left + 'px';
            
            const header = document.createElement('div');
            header.className = 'hacker-error-header';
            header.innerHTML = '<span>SYSTEM ALERT</span><span>X</span>';
            
            const body = document.createElement('div');
            body.className = 'hacker-error-body';
            body.textContent = sysErrors[Math.floor(Math.random() * sysErrors.length)];
            
            win.appendChild(header);
            win.appendChild(body);
            document.body.appendChild(win);
            
            // Remove after 2-4 seconds
            setTimeout(() => { if (win.parentNode) win.remove(); }, 2000 + Math.random() * 2000);
        }
    }, 2000); // Check every 2 seconds
}

function disableHackerMode() {
    document.body.classList.remove('hacked-theme');
    if (hackerModeInterval) clearInterval(hackerModeInterval);
    document.querySelectorAll('.hacker-error-window').forEach(e => e.remove());
    const grid = document.getElementById('hacker-grid-overlay');
    if (grid) grid.remove();
    const crt = document.getElementById('hacker-crt-overlay');
    if (crt) crt.remove();
    const oldBg = document.getElementById('hacker-bg-overlay');
    if (oldBg) oldBg.remove();
}
function toggleAnimations(enabled) {
    if (!enabled) {
        document.body.classList.add('no-animations');
    } else {
        document.body.classList.remove('no-animations');
    }
    localStorage.setItem('aurexis_animations', enabled);
}

// Ensure settings toggles are synced on load
document.addEventListener('DOMContentLoaded', () => {
    const animEnabled = localStorage.getItem('aurexis_animations') !== 'false';
    const animToggle = document.getElementById('anim-toggle');
    if (animToggle) animToggle.checked = animEnabled;
    toggleAnimations(animEnabled);
});

function changeTheme(themeName) {
    const root = document.documentElement;
    let color1, color2, ptrColor1, ptrColor2;
    
    if (themeName === 'matrix') {
        root.style.setProperty('--neon-color', '#ffcc00');
        root.style.setProperty('--bg-color', '#0a0a0a');
        root.style.setProperty('--glow-color', 'rgba(255, 204, 0, 0.5)');
        root.style.setProperty('--neon-primary', '#e5b322');
        color1 = 'FFE373'; color2 = 'D4AF37'; ptrColor1 = 'ffffff'; ptrColor2 = 'FFE373';
    } else if (themeName === 'synthwave') {
        root.style.setProperty('--neon-color', '#ff00ff');
        root.style.setProperty('--bg-color', '#1a0b2e');
        root.style.setProperty('--glow-color', 'rgba(255, 0, 255, 0.5)');
        root.style.setProperty('--neon-primary', '#b026ff');
        color1 = 'ff66ff'; color2 = 'ff00ff'; ptrColor1 = 'ffffff'; ptrColor2 = 'ff66ff';
    } else if (themeName === 'cyberpunk') {
        root.style.setProperty('--neon-color', '#00ffcc');
        root.style.setProperty('--bg-color', '#0b1a1a');
        root.style.setProperty('--glow-color', 'rgba(0, 255, 204, 0.5)');
        root.style.setProperty('--neon-primary', '#00ff88');
        color1 = '66ffeb'; color2 = '00ffcc'; ptrColor1 = 'ffffff'; ptrColor2 = '66ffeb';
    } else if (themeName === 'vampire') {
        root.style.setProperty('--neon-color', '#ff0000');
        root.style.setProperty('--bg-color', '#1a0000');
        root.style.setProperty('--glow-color', 'rgba(255, 0, 0, 0.5)');
        root.style.setProperty('--neon-primary', '#ff0000');
        color1 = 'ff4d4d'; color2 = 'cc0000'; ptrColor1 = 'ffffff'; ptrColor2 = 'ff4d4d';
    } else if (themeName === 'ocean') {
        root.style.setProperty('--neon-color', '#00ffff');
        root.style.setProperty('--bg-color', '#000a1a');
        root.style.setProperty('--glow-color', 'rgba(0, 255, 255, 0.5)');
        root.style.setProperty('--neon-primary', '#0088ff');
        color1 = '66ffff'; color2 = '0088ff'; ptrColor1 = 'ffffff'; ptrColor2 = '66ffff';
    } else if (themeName === 'hacked') {
        root.style.setProperty('--neon-color', '#ff0000');
        root.style.setProperty('--bg-color', '#000000');
        root.style.setProperty('--glow-color', 'rgba(255, 0, 0, 0.8)');
        root.style.setProperty('--neon-primary', '#ff0000');
        color1 = 'ff0000'; color2 = '8b0000'; ptrColor1 = 'ff0000'; ptrColor2 = 'ff0000';
    }

    
    const svgDefaultStr = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><defs><linearGradient id="theme-grad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${color1}"/><stop offset="100%" stop-color="#${color2}"/></linearGradient></defs><path d="M 4 2 L 4 20 L 10 15 L 16 15 Z" fill="rgba(0,0,0,0.4)" transform="translate(1, 2)"/><path d="M 4 2 L 4 20 L 10 15 L 16 15 Z" fill="url(#theme-grad)" stroke="#ffffff" stroke-width="1.5" stroke-linejoin="round"/></svg>`;
    const svgPointerStr = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><defs><linearGradient id="theme-grad-ptr" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#${ptrColor1}"/><stop offset="100%" stop-color="#${ptrColor2}"/></linearGradient></defs><path d="M 4 2 L 4 20 L 10 15 L 16 15 Z" fill="rgba(0,0,0,0.4)" transform="translate(1, 2)"/><path d="M 4 2 L 4 20 L 10 15 L 16 15 Z" fill="url(#theme-grad-ptr)" stroke="#ffffff" stroke-width="1.5" stroke-linejoin="round"/></svg>`;
        
        // Helper function for PNG rasterization
        function rasterizeSVGToPNG(svgStr, hotspotX, hotspotY, callback) {
            const img = new Image();
            img.onload = function() {
                const canvas = document.createElement('canvas');
                canvas.width = img.width || 32;
                canvas.height = img.height || 32;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                const pngDataUrl = canvas.toDataURL('image/png');
                callback(`url("${pngDataUrl}") ${hotspotX} ${hotspotY}`);
            };
            img.src = 'data:image/svg+xml,' + encodeURIComponent(svgStr);
        }

        const hackerCursorStr = shape === 'circle' ? `<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"32\" height=\"32\" viewBox=\"0 0 32 32\"><circle cx=\"16\" cy=\"16\" r=\"10\" fill=\"none\" stroke=\"#ff0000\" stroke-width=\"2\"/><circle cx=\"16\" cy=\"16\" r=\"3\" fill=\"#ff0000\"/></svg>` : `<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\"><path d=\"M 2 2 L 10 22 L 13 13 L 22 10 Z\" fill=\"#ff0000\" stroke=\"#ff0000\" stroke-width=\"2\" stroke-linejoin=\"round\" stroke-opacity=\"0.4\"/></svg>`;

        let hotspotDefX = shape === 'circle' ? 16 : (themeName === 'hacked' ? 2 : 4);
        let hotspotDefY = shape === 'circle' ? 16 : (themeName === 'hacked' ? 2 : 2);
        let hotspotPtrX = shape === 'circle' ? 16 : (themeName === 'hacked' ? 2 : 4);
        let hotspotPtrY = shape === 'circle' ? 16 : (themeName === 'hacked' ? 2 : 2);
        
        if (shape === 'circle') {
            let cursorStyleEl = document.getElementById('dynamic-cursor-style');
            if (!cursorStyleEl) {
                cursorStyleEl = document.createElement('style');
                cursorStyleEl.id = 'dynamic-cursor-style';
                document.head.appendChild(cursorStyleEl);
            }
            cursorStyleEl.innerHTML = `* { cursor: none !important; }`;
        } else {
            rasterizeSVGToPNG(themeName === 'hacked' ? hackerCursorStr : svgDefaultStr, hotspotDefX, hotspotDefY, function(pngUrlDefault) {
                rasterizeSVGToPNG(themeName === 'hacked' ? hackerCursorStr : svgPointerStr, hotspotPtrX, hotspotPtrY, function(pngUrlPointer) {
                    let cursorStyleEl = document.getElementById('dynamic-cursor-style');
                    if (!cursorStyleEl) {
                        cursorStyleEl = document.createElement('style');
                        cursorStyleEl.id = 'dynamic-cursor-style';
                        document.head.appendChild(cursorStyleEl);
                    }
                    cursorStyleEl.innerHTML = `
                        html.cursor-circle, html.cursor-circle * { cursor: none !important; }
                        html:not(.cursor-circle), html:not(.cursor-circle) * {
                            cursor: ${pngUrlDefault} 2 2, auto !important;
                        }
                        html:not(.cursor-circle) a, html:not(.cursor-circle) a *,
                        html:not(.cursor-circle) button, html:not(.cursor-circle) button *,
                        html:not(.cursor-circle) input, html:not(.cursor-circle) select, html:not(.cursor-circle) textarea,
                        html:not(.cursor-circle) .theme-card, html:not(.cursor-circle) .theme-card *,
                        html:not(.cursor-circle) .msgr-tab, html:not(.cursor-circle) .msgr-tab *,
                        html:not(.cursor-circle) .dropdown-item, html:not(.cursor-circle) .dropdown-item *,
                        html:not(.cursor-circle) [onclick], html:not(.cursor-circle) [onclick] * {
                            cursor: ${pngUrlPointer} 8 2, pointer !important;
                        }
                    `;
                });
            });
        }
        

        
        
    
    localStorage.setItem('aurex_theme', themeName);
    
    
    // Update active card
    document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
    const activeCard = document.getElementById('card-' + themeName);
    if(activeCard) activeCard.classList.add('active');
    
    if (themeName === 'hacked') {
        enableHackerMode();
    } else {
        disableHackerMode();
    }
}

function applyTranslations(lang) {
    if (typeof translations === 'undefined') return;
    const dict = translations[lang] || translations['ru'];
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) el.textContent = dict[key];
    });
    
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (dict[key]) el.placeholder = dict[key];
    });
    
    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.getAttribute('data-i18n-title');
        if (dict[key]) el.title = dict[key];
    });
    
    document.querySelectorAll('[data-i18n-data-text]').forEach(el => {
        const key = el.getAttribute('data-i18n-data-text');
        if (dict[key]) el.setAttribute('data-text', dict[key]);
    });
}

function changeLang(lang) {
    localStorage.setItem('aurex_lang', lang);
    applyTranslations(lang);
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('aurex_theme');
    if (savedTheme) {
        changeTheme(savedTheme);
        const sel = document.getElementById('theme-selector');
        if (sel) sel.value = savedTheme;
    }
    const savedLang = localStorage.getItem('aurex_lang') || 'ru';
    const sel = document.getElementById('lang-selector');
    if (sel) sel.value = savedLang;
    applyTranslations(savedLang);
});


// ==========================================
// UX & SOUND EFFECTS (WEB AUDIO API)
// ==========================================

const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playSound(type) {
    if (audioCtx.state === 'suspended') audioCtx.resume();
    
    const osc = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    osc.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    if (type === 'send') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(600, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1200, audioCtx.currentTime + 0.1);
        gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.1);
    } else if (type === 'receive') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(800, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(400, audioCtx.currentTime + 0.15);
        gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
    }
}

// ==========================================
// CUSTOM CONTEXT MENU & REACTIONS
// ==========================================

document.addEventListener('contextmenu', function(e) {
    const msg = e.target.closest('.message');
    if (msg) {
        e.preventDefault();
        showContextMenu(e.pageX, e.pageY, msg);
    } else {
        hideContextMenu();
    }
});

document.addEventListener('click', hideContextMenu);

function showContextMenu(x, y, msgElem) {
    hideContextMenu();
    const menu = document.createElement('div');
    menu.id = 'custom-context-menu';
    menu.style.position = 'absolute';
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';
    menu.style.background = 'rgba(10, 10, 10, 0.95)';
    menu.style.border = '1px solid var(--neon-color)';
    menu.style.borderRadius = '5px';
    menu.style.padding = '5px 0';
    menu.style.zIndex = '1000';
    menu.style.boxShadow = '0 0 15px var(--glow-color)';
    
    const isMine = msgElem.classList.contains('my-message');
    
    menu.innerHTML = `
        <div class="menu-item" onclick="replyToMessage('${msgElem.innerText}')">↩️ Ответить</div>
        ${isMine ? `<div class="menu-item" style="color: #ff4757;" onclick="deleteMessage(this)">🗑️ Удалить</div>` : ''}
        <div class="menu-item" onclick="addReaction(this, '❤️')">❤️ Сердечко</div>
        <div class="menu-item" onclick="addReaction(this, '🔥')">🔥 Огонь</div>
    `;
    
    document.body.appendChild(menu);
}

function hideContextMenu() {
    const menu = document.getElementById('custom-context-menu');
    if (menu) menu.remove();
}

function replyToMessage(text) {
    const input = document.getElementById('message-input');
    if (input) {
        input.value = `> ${text.substring(0, 20)}...

`;
        input.focus();
    }
}

function deleteMessage(btn) {
    // Optimistic delete for now
    alert(__("Сообщение визуально удалено! (БД интеграция в след. фазе)"));
}

function addReaction(btn, emoji) {
    alert("Добавлена реакция " + emoji + " ! (БД интеграция в след. фазе)");
}

// Hook into existing sendMessage to play sound
const originalSendMessage = window.sendMessage;
if (typeof originalSendMessage === 'function') {
    window.sendMessage = async function() {
        playSound('send');
        await originalSendMessage();
    };
}


// ==========================================
// TYPING INDICATOR & STATUSES
// ==========================================

function showTypingIndicator(username) {
    let indicator = document.getElementById('typing-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.style.color = 'var(--neon-color)';
        indicator.style.fontStyle = 'italic';
        indicator.style.fontSize = '12px';
        indicator.style.padding = '5px 15px';
        indicator.style.animation = 'pulse 1s infinite alternate';
        
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow) {
            chatWindow.parentNode.insertBefore(indicator, chatWindow.nextSibling);
        }
    }
    indicator.innerText = `${username} печатает...`;
    indicator.style.display = 'block';
    
    // Auto-hide after 3 seconds
    clearTimeout(window.typingTimeout);
    window.typingTimeout = setTimeout(() => {
        indicator.style.display = 'none';
    }, 3000);
}

// Hook into loadMessages to play receive sound
const originalLoadMessages = window.loadMessages;
if (typeof originalLoadMessages === 'function') {
    window.lastMessageCount = 0;
    window.loadMessages = async function() {
        await originalLoadMessages();
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow && chatWindow.children.length > window.lastMessageCount) {
            if (window.lastMessageCount > 0) {
                // Only play sound if it's not the initial load
                // Check if the last message is NOT mine
                const lastMsg = chatWindow.lastChild;
                if (lastMsg && !lastMsg.classList.contains('my-message')) {
                    playSound('receive');
                }
            }
            window.lastMessageCount = chatWindow.children.length;
    // Randomly simulate typing if we are in a DM
    if (currentChatType === 'dm' && currentChatTarget && Math.random() < 0.1) {
        showTypingIndicator(currentChatTarget);
    }

        }
    };
}


// ==========================================
// PHASE 3: MEDIA & TERMINAL EASTER EGG
// ==========================================

// 1. Hacker Terminal Trigger
let keysPressed = '';
document.addEventListener('keydown', (e) => {
    // Only listen if not typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        if(e.target.id === 'hacker-input' && e.key === 'Enter') {
            handleHackerCommand(e.target.value);
            e.target.value = '';
        }
        return;
    }
    
    keysPressed += e.key.toLowerCase();
    if (keysPressed.length > 20) keysPressed = keysPressed.substring(1);
    
    if (keysPressed.includes('hacker')) {
        keysPressed = ''; // reset
        switchView('view-hacker');
        document.getElementById('hacker-output').innerHTML = '';
        
        const bootSequence = [
            "Initializing AurexOS kernel...",
            "Loading drivers... OK",
            "Mounting virtual filesystems... OK",
            "Bypassing firewall protocols [■■■■■■■■■■] 100%",
            "Decrypting RSA-4096 keys... SUCCESS",
            "Establishing secure tunneling to remote server...",
            "WARNING: Intrusion countermeasures detected.",
            "Deploying counter-countermeasures...",
            "Injecting payload... [0x0F82A1B]",
            "Extracting classified datablocks...",
            "----------------------------------------",
            "AUREX OS ROOT ACCESS GRANTED.",
            "Type 'help' for commands."
        ];
        
        let delay = 0;
        bootSequence.forEach((line, index) => {
            setTimeout(() => {
                if (index < 10) {
                    printHacker(line + " [" + Math.random().toString(16).substring(2, 10) + "]");
                } else {
                    printHacker(line);
                }
            }, delay);
            delay += Math.floor(Math.random() * 200) + 50; // Random delay between 50 and 250ms
        });
        
        setTimeout(() => document.getElementById('hacker-input').focus(), delay + 100);
    }
});

function printHacker(text) {
    const out = document.getElementById('hacker-output');
    if (!out) return;
    out.innerHTML += `<div>> ${text}</div>`;
    out.parentElement.scrollTop = out.parentElement.scrollHeight;
}

function handleHackerCommand(cmd) {
    printHacker(cmd);
    const c = cmd.trim().toLowerCase();
    
    if (c === 'help') {
        printHacker("Commands: help, clear, ping, dox @user, matrix");
    } else if (c === 'clear') {
        document.getElementById('hacker-output').innerHTML = '';
    } else if (c === 'matrix') {
        
        printHacker("Initializing matrix protocol...");
        document.body.insertAdjacentHTML('beforeend', '<canvas id="matrix-canvas" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:9999;pointer-events:none;"></canvas>');
        const c = document.getElementById('matrix-canvas');
        const ctx = c.getContext('2d');
        c.width = window.innerWidth;
        c.height = window.innerHeight;
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*'.split('');
        const fontSize = 16;
        const columns = c.width / fontSize;
        const drops = [];
        for(let x = 0; x < columns; x++) drops[x] = 1;
        function drawMatrix() {
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            ctx.fillRect(0, 0, c.width, c.height);
            ctx.fillStyle = '#0f0';
            ctx.font = fontSize + 'px monospace';
            for(let i = 0; i < drops.length; i++) {
                const text = letters[Math.floor(Math.random() * letters.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if(drops[i] * fontSize > c.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        window.matrixInterval = setInterval(drawMatrix, 33);
        setTimeout(() => {
            clearInterval(window.matrixInterval);
            c.remove();
            printHacker("Matrix protocol terminated.");
        }, 10000);

    } else if (c.startsWith('dox ')) {
        const target = cmd.split(' ')[1];
        printHacker(`[+] Locating ${target}...`);
        setTimeout(() => printHacker(`[!] IP: 192.168.1.${Math.floor(Math.random()*255)}`), 1000);
        setTimeout(() => printHacker(`[!] Status: PWNED`), 2000);
    } else {
        printHacker("Command not found.");
    }
}

// 2. Voice Recording (MediaRecorder)
let mediaRecorder;
let audioChunks = [];
let isRecording = false;

async function toggleVoiceRecord() {
    const btn = document.getElementById('btn-voice');
    if (!isRecording) {
                try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();
            isRecording = true;
            btn.style.color = '#ff4757';
            btn.style.animation = 'pulse 1s infinite alternate';
            
            mediaRecorder.ondataavailable = e => {
                audioChunks.push(e.data);
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioChunks = [];
                // Simulate sending audio
                showToast(__("Голосовое сообщение отправлено! (интеграция в след. фазе)"), "success");
            };
        } catch(e) {
            showToast(__("Нет доступа к микрофону. Нажмите на значок замка в адресной строке и разрешите доступ!"), "error");
        }
    } else {
        mediaRecorder.stop();
        isRecording = false;
        btn.style.color = 'var(--neon-color)';
        btn.style.animation = 'none';
        mediaRecorder.stream.getTracks().forEach(t => t.stop());
    }
}

// 3. Screen Capture (getDisplayMedia)
async function captureScreen() {
    try {
        const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
        const video = document.createElement('video');
        video.srcObject = stream;
        video.play();
        
        video.onloadedmetadata = () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            stream.getTracks().forEach(t => t.stop());
            
            const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
            // Simulate sending image
            alert(__("Скриншот сделан! (Интеграция с БД в след. фазе)"));
        };
    } catch(e) {
        console.error("Окно захвата закрыто или отклонено.");
    }
}

// 4. Drag & Drop into Chat
const chatWindow = document.getElementById('chat-window');
if (chatWindow) {
    chatWindow.addEventListener('dragover', (e) => {
        e.preventDefault();
        chatWindow.style.border = '2px dashed var(--neon-color)';
    });
    chatWindow.addEventListener('dragleave', (e) => {
        e.preventDefault();
        chatWindow.style.border = 'none';
    });
    chatWindow.addEventListener('drop', (e) => {
        e.preventDefault();
        chatWindow.style.border = 'none';
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            alert(`Файл ${file.name} готов к отправке! (Загрузка в БД в след. фазе)`);
        }
    });
}


// ==========================================
// RICH EMBEDS
// ==========================================
function parseRichText(text) {
    // Escape HTML first
    let html = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    
    // Youtube matching
    const ytRegex = /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/g;
    html = html.replace(ytRegex, (match, videoId) => {
        return `<br><iframe width="300" height="170" src="https://www.youtube.com/embed/${videoId}" frameborder="0" allowfullscreen style="border-radius: 5px; border: 1px solid var(--neon-color); margin-top: 5px;"></iframe><br>`;
    });
    
    // Image matching (basic)
    const imgRegex = /(https?:\/\/\S+\.(?:png|jpg|jpeg|gif|webp))/gi;
    html = html.replace(imgRegex, (match) => {
        return `<br><img src="${match}" style="max-width: 300px; max-height: 200px; border-radius: 5px; border: 1px solid var(--neon-color); margin-top: 5px;"><br>`;
    });
    
    return html;
}


// ==========================================
// PHASE 4: HARDCORE TECH (E2EE, WEBRTC, PWA, EDITOR)
// ==========================================

// 1. PWA Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // We just pretend to register a service worker for now since we don't have the file
        console.log('Aurexis PWA Service Worker ready (Simulated)');
    });
}

// 2. Live Code Editor
function runCode() {
    const code = document.getElementById('code-textarea').value;
    const output = document.getElementById('code-output');
    output.innerHTML = "<span style='color: #ffcc00;'>Running...</span><br>";
    
    setTimeout(() => {
        if (code.includes('print')) {
            output.innerHTML += "SyntaxError: 'print' is not defined (JS environment).<br>";
        }
        output.innerHTML += "Compilation finished. Local VM simulated.<br>";
        if(code.includes('ping')) {
            output.innerHTML += "pong<br>";
        }
    }, 500);
}

// 3. WebRTC Audio/Video Call (Simulated local stream for demo)
async function startCall() {
    const chatHeader = document.querySelector('.chat-header');
    if(document.getElementById('video-call-container')) return;
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        
        const container = document.createElement('div');
        container.id = 'video-call-container';
        container.style.position = 'absolute';
        container.style.top = '60px';
        container.style.right = '20px';
        container.style.width = '300px';
        container.style.height = '200px';
        container.style.background = '#000';
        container.style.border = '2px solid var(--neon-color)';
        container.style.borderRadius = '10px';
        container.style.overflow = 'hidden';
        container.style.zIndex = '1001';
        container.style.boxShadow = '0 0 20px rgba(0, 255, 0, 0.4)';
        
        const video = document.createElement('video');
        video.srcObject = stream;
        video.autoplay = true;
        video.muted = true; // local video
        video.style.width = '100%';
        video.style.height = '100%';
        video.style.objectFit = 'cover';
        
        const endBtn = document.createElement('button');
        endBtn.innerText = '📞 Завершить';
        endBtn.style.position = 'absolute';
        endBtn.style.bottom = '10px';
        endBtn.style.left = '50%';
        endBtn.style.transform = 'translateX(-50%)';
        endBtn.style.background = '#ff4757';
        endBtn.style.color = '#fff';
        endBtn.style.border = 'none';
        endBtn.style.padding = '5px 15px';
        endBtn.style.borderRadius = '15px';
        endBtn.style.style.setProperty('cursor', 'var(--cursor-pointer, pointer)', 'important');
        
        endBtn.onclick = () => {
            stream.getTracks().forEach(t => t.stop());
            container.remove();
            playSound('receive'); // simulate hangup sound
        };
        
        container.appendChild(video);
        container.appendChild(endBtn);
        
        // Find messenger window and append
        const messenger = document.getElementById('view-messenger');
        if(messenger) messenger.appendChild(container);
        
    } catch(e) {
        alert(__("Нет доступа к камере или микрофону для WebRTC!"));
    }
}

// 4. E2EE Encryption Wrapper
// We will hook into the message sending process to encrypt text before it goes to DB, 
// and decrypt it when it comes from DB. Since we don't have a shared key exchange setup yet, 
// we will just visually encrypt it in the DOM and decrypt it.
// (For demo purposes, the actual encryption is just base64 or a shift cipher so we can easily decode it without async key management).

function encryptE2EE(text) {
    // Simple mock encryption to show E2EE concept
    return "E2EE::" + btoa(unescape(encodeURIComponent(text)));
}

function decryptE2EE(text) {
    if (text.startsWith("E2EE::")) {
        try {
            return decodeURIComponent(escape(atob(text.replace("E2EE::", ""))));
        } catch(e) {
            return text;
        }
    }
    return text; // not encrypted
}

// Override loadMessages specifically for E2EE display
const originalLoadMessagesP4 = window.loadMessages;
if (typeof originalLoadMessagesP4 === 'function') {
    window.loadMessages = async function() {
        await originalLoadMessagesP4();
        // Go through all messages and "decrypt" them visually if they are encrypted
        const messages = document.querySelectorAll('.message-text');
        messages.forEach(msg => {
            // Note: because of rich embeds, the text might already have HTML.
            // A real E2EE implementation encrypts the raw string before sending,
            // and decrypts it BEFORE rendering rich embeds.
            // For now, if we see E2EE:: we know we can decrypt.
        });
    };
}


// ==========================================
// NAVIGATION (Restored)
// ==========================================
function switchView(viewId) {
    document.querySelectorAll('.view').forEach(v => {
        v.classList.remove('active');
        v.style.display = 'none';
    });
    
    document.querySelectorAll('.nav-link').forEach(l => {
        l.classList.remove('active');
    });

    const targetView = document.getElementById(viewId);
    if (targetView) {
        targetView.classList.add('active');
        targetView.classList.remove('hidden-view'); // Fix for hidden-view override!
        if (viewId === 'view-messenger') {
            targetView.style.display = 'flex';
        } else if (viewId === 'view-editor') {
            targetView.style.display = 'flex';
        } else {
            targetView.style.display = 'block';
        }
    }

    // Attempt to highlight nav link
    const links = document.querySelectorAll('.nav-link');
    for (let link of links) {
        if (link.getAttribute('onclick') && link.getAttribute('onclick').includes(viewId)) {
            link.classList.add('active');
            break;
        }
    }
}






// === CURSOR SHAPE SETTING ===
window.changeCursorShape = function(shape) {
    localStorage.setItem('aurex_cursor_shape', shape);
    
    const cursorDOM = document.getElementById('custom-cursor');
    if (shape === 'circle') {
        document.documentElement.classList.add('cursor-circle');
        if (cursorDOM) cursorDOM.style.display = 'block';
    } else {
        document.documentElement.classList.remove('cursor-circle');
        if (cursorDOM) cursorDOM.style.display = 'none';
    }
    const currentTheme = localStorage.getItem('aurex_theme') || 'matrix';
    changeTheme(currentTheme);
    
    // Update UI toggle buttons if they exist
    document.querySelectorAll('.cursor-btn').forEach(btn => btn.classList.remove('active'));
    let activeBtn = document.getElementById('cursor-btn-' + shape);
    if(activeBtn) activeBtn.classList.add('active');
};


// === ANIMATED DOM CURSOR LOGIC ===
document.addEventListener('DOMContentLoaded', () => {
    const cursor = document.getElementById('custom-cursor');
    const shape = localStorage.getItem('aurex_cursor_shape') || 'triangle';
    if (shape === 'circle' && cursor) {
        cursor.style.display = 'block';
    }

    document.addEventListener('mousemove', (e) => {
        if (!cursor || !document.documentElement.classList.contains('cursor-circle')) return;
        
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        
        // Hover detection
        const isClickable = e.target.closest('a, button, input, select, textarea, .theme-card, .dropdown-item, .cursor-btn, .clickable, i');
        if (isClickable) {
            cursor.classList.add('hover-effect');
        } else {
            cursor.classList.remove('hover-effect');
        }
    });

    document.addEventListener('mousedown', () => {
        if (cursor && document.documentElement.classList.contains('cursor-circle')) {
            cursor.classList.add('click-effect');
        }
    });

    document.addEventListener('mouseup', () => {
        if (cursor) cursor.classList.remove('click-effect');
    });

    document.addEventListener('mouseleave', () => {
        if (cursor) cursor.style.opacity = '0';
    });

    document.addEventListener('mouseenter', () => {
        if (cursor && document.documentElement.classList.contains('cursor-circle')) cursor.style.opacity = '1';
    });
});
