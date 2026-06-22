
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
    window.location.hash = '#account';
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
        alert('Ошибка соединения с сервером.');
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // Preloader Logic
    const welcomeScreen = document.getElementById('welcome-screen');
    
    // Simulate loading time (e.g. 2.5 seconds)
    setTimeout(() => {
        welcomeScreen.style.opacity = '0';
        setTimeout(() => {
            welcomeScreen.style.visibility = 'hidden';
            // Show main elements after preloader finishes
            document.querySelector('.hero').classList.add('show');
            initScrollAnimations();
        }, 1000); // Wait for fade out transition
    }, 2500);

    // Scroll Animations using Intersection Observer
    let observer;
    function initScrollAnimations() {
        // Initialize Router
        handleRoute();
        window.addEventListener('hashchange', handleRoute);
    }

    // SPA Routing Logic
    function handleRoute() {
        const hash = window.location.hash || '#home';
        
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
        const email = document.getElementById('login-email').value;
        const pass = document.getElementById('login-password').value;
        const err = document.getElementById('login-error');
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
        const nickname = document.getElementById('reg-nickname').value;
        const email = document.getElementById('reg-email').value;
        const pass = document.getElementById('reg-password').value;
        const err = document.getElementById('reg-error');
        
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
                    alert('Пароль успешно изменён! Теперь вы можете войти.');
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
            }
        } catch (e) {
            console.error('Session check failed');
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
                floraStatus.textContent = 'Активна';
                floraStatus.style.color = '#00ffaa';
            } else {
                floraStatus.textContent = 'Не активна';
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
        document.getElementById('nav-account').style.display = 'none';
        document.getElementById('open-auth').style.display = 'inline-block';
        window.location.hash = '#home'; // Go back to home
        // alert('Вы вышли из аккаунта.');

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
                        alert("Ошибка соединения при загрузке аватарки.");
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
                    const stars = '⭐'.repeat(r.rating);
                    const user = r.users || {};
                    const avatar = user.avatar || '/static/assets/default-avatar.png';
                    const nickname = user.nickname || 'Неизвестно';
                    
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
                        el.innerHTML = `<span class="status-dot" style="background: ${botData.color}; box-shadow: 0 0 10px ${botData.color}"></span> <span style="color: ${botData.color}">${botData.status}</span>`;
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
                    container.innerHTML = '<div style="text-align: center; width: 100%; color: var(--text-muted);">Пока нет новостей.</div>';
                    return;
                }
                data.news.forEach(n => {
                    const date = new Date(n.created_at).toLocaleDateString('ru-RU', {day: 'numeric', month: 'long', year: 'numeric'});
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
                    const statusText = t.status === 'open' ? 'Открыт' : 'Закрыт';
                    container.innerHTML += `
                        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 15px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: background 0.3s;" onclick="openTicketChat(${t.id}, '${t.topic}', '${t.status}')">
                            <div>
                                <h4 style="margin: 0; margin-bottom: 5px;">${t.topic}</h4>
                                <span style="font-size: 0.85rem; color: var(--text-muted);">Тикет #${t.id}</span>
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
            statusEl.innerHTML = 'Статус: <span style="color: #00ffaa;">Открыт</span>';
            document.getElementById('ticket-reply-container').style.display = 'flex';
        } else {
            statusEl.innerHTML = 'Статус: <span style="color: #ff4444;">Закрыт</span>';
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
    let easterEggActive = false;

    window.addEventListener('keydown', (e) => {
        if (easterEggActive) return;
        
        // Ignore if typing in an input
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        keySequence += e.key.toLowerCase();
        
        if (keySequence.length > secretWord.length) {
            keySequence = keySequence.substring(1);
        }

        if (keySequence === secretWord) {
            triggerEasterEgg();
        }
    });

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
                    const nickname = msg.users ? msg.users.nickname : 'Неизвестно';
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
    const aiStopBtn = document.getElementById('ai-stop-btn');
    if(aiStopBtn) {
        aiStopBtn.addEventListener('click', () => {
            if(aiAbortController) {
                aiAbortController.abort();
            }
        });
    }

    async function sendToAI() {
        if(!aiInput || !aiInput.value.trim()) return;
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
            const res = await fetch('/api/ai/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, history: aiChatHistory }),
                signal: aiAbortController.signal
            });
            
            contentBox.innerHTML = '';
            
            if (res.ok && res.body) {
                const reader = res.body.getReader();
                const decoder = new TextDecoder('utf-8');
                let fullReply = '';
                
                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    
                    const chunk = decoder.decode(value, {stream: true});
                    fullReply += chunk;
                    contentBox.textContent = fullReply;
                    aiChatBox.scrollTop = aiChatBox.scrollHeight;
                }
                aiChatHistory.push({role: 'assistant', content: fullReply});
            } else {
                contentBox.textContent = 'Ошибка подключения к серверу.';
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
                    
                    // DOX responds
                    setTimeout(() => {
                        finalTerminal.innerHTML = '';
                        const doxMsg = document.createElement('div');
                        doxMsg.style.position = 'absolute';
                        doxMsg.style.top = '50%';
                        doxMsg.style.left = '50%';
                        doxMsg.style.transform = 'translate(-50%, -50%)';
                        doxMsg.style.fontSize = '40px';
                        doxMsg.style.fontWeight = 'bold';
                        doxMsg.style.color = '#ff0000';
                        doxMsg.style.textShadow = '0 0 20px #ff0000';
                        finalTerminal.appendChild(doxMsg);
                        
                        const textToType = "я еще вернусь...";
                        let typeIdx = 0;
                        const typeInterval = setInterval(() => {
                            doxMsg.innerText += textToType[typeIdx];
                            typeIdx++;
                            if (typeIdx >= textToType.length) {
                                clearInterval(typeInterval);
                                // Fade out to normal site
                                                                setTimeout(() => {
                                    finalTerminal.style.transition = 'opacity 2s';
                                    finalTerminal.style.opacity = '0';
                                    const face = document.querySelector('.creepy-face');
                                    if(face) {
                                        face.style.transition = 'opacity 2s';
                                        face.style.opacity = '0';
                                    }
                                    setTimeout(() => {
                                        finalTerminal.remove();
                                        if(face) face.remove();
                                        document.body.classList.remove('apocalypse-mode'); // Clean up any remaining classes
                                    }, 2000);
                                }, 3000);
                            }
                        }, 150);
                    }, commands.length * 800 + 2000);
                    
                }, 1000);
                
            }, 5000);
            
        }, totalLinesTime);
        
    }, 10000);
}
