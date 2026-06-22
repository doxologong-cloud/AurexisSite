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
    const authSocialWrap = document.getElementById('auth-social-wrap');
    
    // Switch between Login and Register tabs
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            if (tab.classList.contains('active')) return;
            
            authTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Reset forms and errors
            document.querySelectorAll('.auth-error').forEach(el => el.textContent = '');
            verifyForm.style.display = 'none';

            if (tab.dataset.tab === 'login') {
                loginForm.style.display = 'flex';
                registerForm.style.display = 'none';
            } else {
                loginForm.style.display = 'none';
                registerForm.style.display = 'flex';
            }
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
                authSocialWrap.style.display = 'none';
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
        authSocialWrap.style.display = 'block';
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
            authSocialWrap.style.display = 'none';
            forgotForm.style.display = 'flex';
        });

        // Back to login
        backToLoginBtn.addEventListener('click', () => {
            forgotForm.style.display = 'none';
            document.querySelector('.auth-tabs').style.display = 'flex';
            loginForm.style.display = 'flex';
            authSocialWrap.style.display = 'block';
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
                    authSocialWrap.style.display = 'block';
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
    };

    // Logout
    document.getElementById('logout-btn').addEventListener('click', async () => {
        try {
            await fetch('/api/logout', { method: 'POST' });
        } catch(e) {}

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
    const editError = document.getElementById('edit-profile-error');

    if(editBtn && cancelEditBtn && saveProfileBtn) {
        editBtn.addEventListener('click', () => {
            profileDisplay.style.display = 'none';
            profileEditForm.style.display = 'block';
            editNickInput.value = document.getElementById('acc-nickname').textContent;
            editUserInput.value = document.getElementById('acc-username').textContent;
            editError.textContent = '';
        });

        cancelEditBtn.addEventListener('click', () => {
            profileDisplay.style.display = 'flex';
            profileEditForm.style.display = 'none';
        });

        saveProfileBtn.addEventListener('click', async () => {
            const newNick = editNickInput.value.trim();
            const newUser = editUserInput.value.trim();
            if(!newNick || !newUser) {
                editError.textContent = 'Заполните все поля!';
                return;
            }

            saveProfileBtn.disabled = true;
            saveProfileBtn.textContent = 'Сохранение...';
            
            try {
                const res = await fetch('/api/update-profile', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nickname: newNick, username: newUser })
                });
                const data = await res.json();
                if(data.success) {
                    if(window.loginUser) window.loginUser(data.user);
                    profileDisplay.style.display = 'flex';
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
            avatarUploadInput.click();
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

    loadReviews();
    loadBotStatus();
});
