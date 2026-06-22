
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
            showToast('Войдите, чтобы открыть Ленту', 'error');
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

        if(!payload.target_email) return showToast('Введите email', 'error');

        try {
            const res = await fetch('/api/create_chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if(res.ok) {
                showToast('Чат создан!', 'success');
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
                
                el.innerHTML = `
                    <div class="chat-item-avatar">${initial}</div>
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
    loadChats();
    
    loadChatMessages();
    
    // Setup polling
    if(messagePollingInterval) clearInterval(messagePollingInterval);
    messagePollingInterval = setInterval(loadChatMessages, 3000);
}

async function loadChatMessages() {
    if(!activeChatId) return;
    
    try {
        const res = await fetch(`/api/get_chat_messages/${activeChatId}`);
        const data = await res.json();
        
        if(res.ok) {
            const container = document.getElementById('active-chat-messages');
            container.innerHTML = '';
            
            data.messages.forEach(msg => {
                const isSentByMe = msg.sender_email === window.currentUser.email;
                const el = document.createElement('div');
                el.className = `chat-msg ${isSentByMe ? 'sent' : 'received'}`;
                
                let contentHTML = escapeHTML(msg.message);
                if(msg.message.startsWith('STICKER:')) {
                    el.classList.add('chat-msg-sticker');
                    contentHTML = `<img src="${escapeHTML(msg.message.replace('STICKER:', ''))}" alt="sticker">`;
                }
                
                const time = new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                
                el.innerHTML = `
                    ${!isSentByMe ? `<span class="chat-msg-sender">${escapeHTML(msg.sender_email.split('@')[0])}</span>` : ''}
                    ${contentHTML}
                    <span class="chat-msg-time">${time}</span>
                `;
                container.appendChild(el);
            });
            
            container.scrollTop = container.scrollHeight;
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
    
    // Optimistic UI could be added here, but simple fetch is fine
    try {
        await fetch('/api/send_chat_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: activeChatId, message })
        });
        loadChatMessages();
    } catch(e) {
        console.error(e);
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
                            div.style.cursor = 'pointer';
                            div.style.borderBottom = '1px solid rgba(255,255,255,0.05)';
                            div.innerHTML = `<span style="color: white; font-weight: bold;">${u.username}</span> <br><span style="color: gray; font-size: 0.8rem;">${u.email}</span>`;
                            
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
        showToast('Добавлен в контакты', 'success');
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
// WEB-OS WINDOW MANAGER
// ==========================================
let zIndexCounter = 100;
let draggedWindow = null;
let offsetX = 0;
let offsetY = 0;

function bringToFront(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        zIndexCounter++;
        win.style.zIndex = zIndexCounter;
    }
}

function startDrag(e, windowId) {
    if (e.target.closest('.window-controls')) return; // Don't drag if clicking buttons
    
    draggedWindow = document.getElementById(windowId);
    if (!draggedWindow) return;
    
    bringToFront(windowId);
    
    const rect = draggedWindow.getBoundingClientRect();
    offsetX = e.clientX - rect.left;
    offsetY = e.clientY - rect.top;
    
    document.addEventListener('mousemove', dragWindow);
    document.addEventListener('mouseup', stopDrag);
}

function dragWindow(e) {
    if (!draggedWindow) return;
    
    // Convert to top/left positioning instead of transform translate for easier dragging
    draggedWindow.style.transform = 'none';
    draggedWindow.style.left = (e.clientX - offsetX) + 'px';
    draggedWindow.style.top = (e.clientY - offsetY) + 'px';
}

function stopDrag() {
    draggedWindow = null;
    document.removeEventListener('mousemove', dragWindow);
    document.removeEventListener('mouseup', stopDrag);
}

function closeWindow(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        win.classList.remove('active');
        // If it's messenger, clean up intervals if needed
    }
}

function minimizeWindow(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        const content = win.querySelector('.window-content');
        if (content.style.display === 'none') {
            content.style.display = '';
            win.style.minHeight = '200px';
        } else {
            content.style.display = 'none';
            win.style.minHeight = '40px';
            win.style.height = '40px';
        }
    }
}

function maximizeWindow(windowId) {
    const win = document.getElementById(windowId);
    if (win) {
        if (win.classList.contains('maximized')) {
            win.classList.remove('maximized');
            win.style.width = win.dataset.oldWidth || '';
            win.style.height = win.dataset.oldHeight || '';
            win.style.left = win.dataset.oldLeft || '50%';
            win.style.top = win.dataset.oldTop || '50%';
            if(win.dataset.oldLeft === undefined) {
                win.style.transform = 'translate(-50%, -50%)';
            }
        } else {
            win.dataset.oldWidth = win.style.width;
            win.dataset.oldHeight = win.style.height;
            win.dataset.oldLeft = win.style.left;
            win.dataset.oldTop = win.style.top;
            
            win.classList.add('maximized');
            win.style.transform = 'none';
            win.style.left = '0';
            win.style.top = '70px'; // Below navbar
            win.style.width = '100vw';
            win.style.height = 'calc(100vh - 70px)';
        }
    }
}

// Override switchView to open windows instead of hiding others
window.switchView = function(viewId) {
    const targetView = document.getElementById(viewId);
    if (targetView) {
        targetView.classList.add('active');
        bringToFront(viewId);
    }
};

// Make windows focusable by clicking anywhere on them
document.addEventListener('mousedown', (e) => {
    const win = e.target.closest('.window');
    if (win) {
        bringToFront(win.id);
    }
});


// ==========================================
// THEME & LANG SETTINGS
// ==========================================

function changeTheme(themeName) {
    const root = document.documentElement;
    if (themeName === 'matrix') {
        root.style.setProperty('--neon-color', '#ffcc00');
        root.style.setProperty('--bg-color', '#0a0a0a');
        root.style.setProperty('--glow-color', 'rgba(255, 204, 0, 0.5)');
    } else if (themeName === 'synthwave') {
        root.style.setProperty('--neon-color', '#ff00ff');
        root.style.setProperty('--bg-color', '#1a0b2e');
        root.style.setProperty('--glow-color', 'rgba(255, 0, 255, 0.5)');
    } else if (themeName === 'cyberpunk') {
        root.style.setProperty('--neon-color', '#00ffcc');
        root.style.setProperty('--bg-color', '#0b1a1a');
        root.style.setProperty('--glow-color', 'rgba(0, 255, 204, 0.5)');
    }
    localStorage.setItem('aurex_theme', themeName);
}

function changeLang(lang) {
    // Simple alert for now, full localization requires mapping
    alert('Язык изменен на: ' + lang + '. (Локализация будет добавлена в следующих фазах)');
    localStorage.setItem('aurex_lang', lang);
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('aurex_theme');
    if (savedTheme) {
        changeTheme(savedTheme);
        const sel = document.getElementById('theme-selector');
        if (sel) sel.value = savedTheme;
    }
    const savedLang = localStorage.getItem('aurex_lang');
    if (savedLang) {
        const sel = document.getElementById('lang-selector');
        if (sel) sel.value = savedLang;
    }
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
    alert("Сообщение визуально удалено! (БД интеграция в след. фазе)");
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
        printHacker("AUREX OS ROOT ACCESS GRANTED.");
        printHacker("Type 'help' for commands.");
        setTimeout(() => document.getElementById('hacker-input').focus(), 100);
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
        switchView('view-home');
        document.body.style.animation = 'glitch 0.2s infinite';
        setTimeout(() => document.body.style.animation = 'none', 2000);
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
                alert("Голосовое сообщение записано! (Интеграция с БД в след. фазе)");
                // Usually we'd upload to Supabase Storage and send the URL
            };
        } catch(e) {
            alert("Нет доступа к микрофону!");
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
            alert("Скриншот сделан! (Интеграция с БД в след. фазе)");
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
        endBtn.style.cursor = 'pointer';
        
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
        alert("Нет доступа к камере или микрофону для WebRTC!");
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
