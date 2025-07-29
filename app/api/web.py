#!/usr/bin/env python3
"""
Web页面路由
提供登录、注册等HTML页面
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(tags=["web"])

# 设置模板目录
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """登录页面"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """注册页面"""
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """首页 - 重定向到登录页面"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/user-management.js")
async def user_management_script():
    """用户管理JavaScript脚本"""
    script_content = """
// 用户管理和语言切换集成脚本
const translations = {
    en: {
        user_menu: "User Menu",
        profile: "Profile",
        edit_profile: "Edit Profile",
        username: "Username",
        email: "Email",
        full_name: "Full Name",
        save_changes: "Save Changes",
        cancel: "Cancel",
        sign_out: "Sign Out",
        language: "Language",
        english: "English",
        chinese: "中文",
        japanese: "日本語",
        update_success: "Profile updated successfully",
        update_error: "Failed to update profile",
        logout_confirm: "Are you sure you want to sign out?",
        network_error: "Network error, please try again"
    },
    zh: {
        user_menu: "用户菜单",
        profile: "个人资料",
        edit_profile: "编辑资料",
        username: "用户名",
        email: "邮箱",
        full_name: "姓名",
        save_changes: "保存更改",
        cancel: "取消",
        sign_out: "退出登录",
        language: "语言",
        english: "English",
        chinese: "中文",
        japanese: "日本語",
        update_success: "资料更新成功",
        update_error: "资料更新失败",
        logout_confirm: "确定要退出登录吗？",
        network_error: "网络错误，请重试"
    },
    ja: {
        user_menu: "ユーザーメニュー",
        profile: "プロフィール",
        edit_profile: "プロフィール編集",
        username: "ユーザー名",
        email: "メールアドレス",
        full_name: "氏名",
        save_changes: "変更を保存",
        cancel: "キャンセル",
        sign_out: "サインアウト",
        language: "言語",
        english: "English",
        chinese: "中文",
        japanese: "日本語",
        update_success: "プロフィールが正常に更新されました",
        update_error: "プロフィールの更新に失敗しました",
        logout_confirm: "サインアウトしてもよろしいですか？",
        network_error: "ネットワークエラーが発生しました。再試行してください"
    }
};

let currentLang = localStorage.getItem('preferred_language') || 'en';
let currentUser = null;

function t(key) {
    return translations[currentLang][key] || key;
}

function switchLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('preferred_language', lang);
    updateLanguageUI();
}

function updateLanguageUI() {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[currentLang][key]) {
            element.textContent = translations[currentLang][key];
        }
    });

    document.querySelectorAll('.language-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-lang') === currentLang) {
            btn.classList.add('active');
        }
    });
}

async function getCurrentUser() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            throw new Error('No access token');
        }

        const response = await fetch('http://localhost:8000/api/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            currentUser = await response.json();
            updateUserDisplay();
            return currentUser;
        } else {
            throw new Error('Failed to get user info');
        }
    } catch (error) {
        console.error('Error getting user info:', error);
        window.location.href = 'http://localhost:8000/login';
    }
}

function updateUserDisplay() {
    if (!currentUser) return;

    const userCircle = document.querySelector('.user-circle, [data-user-circle]');
    if (userCircle) {
        userCircle.textContent = currentUser.username ? currentUser.username[0].toUpperCase() : 'U';
        userCircle.title = currentUser.username || 'User';
    }

    const usernameDisplay = document.querySelector('#user-username');
    const emailDisplay = document.querySelector('#user-email');
    const fullNameDisplay = document.querySelector('#user-fullname');

    if (usernameDisplay) usernameDisplay.textContent = currentUser.username || '';
    if (emailDisplay) emailDisplay.textContent = currentUser.email || '';
    if (fullNameDisplay) fullNameDisplay.textContent = currentUser.full_name || '';
}

async function updateUserProfile(userData) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch('http://localhost:8000/api/auth/me', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            currentUser = await response.json();
            updateUserDisplay();
            showMessage(t('update_success'), 'success');
            return true;
        } else {
            const error = await response.json();
            showMessage(error.detail || t('update_error'), 'error');
            return false;
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        showMessage(t('network_error'), 'error');
        return false;
    }
}

async function signOut() {
    if (confirm(t('logout_confirm'))) {
        try {
            const token = localStorage.getItem('access_token');
            await fetch('http://localhost:8000/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            window.location.href = 'http://localhost:8000/login';
        }
    }
}

function showMessage(message, type = 'info') {
    console.log(`${type.toUpperCase()}: ${message}`);

    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 6px;
        color: white;
        z-index: 10000;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
    `;

    document.body.appendChild(messageDiv);

    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

function initUserManagement() {
    getCurrentUser();
    updateLanguageUI();
}

window.UserManagement = {
    init: initUserManagement,
    getCurrentUser,
    updateUserProfile,
    signOut,
    switchLanguage,
    t,
    currentUser: () => currentUser
};

// 自动初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUserManagement);
} else {
    initUserManagement();
}
"""
    return Response(content=script_content, media_type="application/javascript")

@router.get("/ui", response_class=HTMLResponse)
async def magentic_ui_with_user_management(request: Request):
    """带用户管理的Magentic-UI界面"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magentic-UI with User Management</title>
    <style>
        body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }

        /* 隐藏Magentic-UI原生按钮的尝试 */
        iframe {
            width: 100%;
            height: 100vh;
            border: none;
        }

        /* 尝试通过CSS选择器隐藏原生用户按钮 */
        iframe::after {
            content: '';
            position: fixed;
            top: 20px;
            right: 75px;
            width: 32px;
            height: 32px;
            background: var(--color-bg-primary, white);
            border-radius: 50%;
            z-index: 9999;
            pointer-events: none;
        }

        .user-management-overlay {
            position: fixed;
            top: 16px;
            right: 102px; /* 向上移动1px */
            z-index: 10000;
            display: flex;
            align-items: center;
        }

        /* 用户管理容器 - 覆盖在原生用户按钮上 */
        .user-menu-container {
            position: relative;
        }

        /* 语言选择菜单项样式 */
        .language-menu-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 20px;
            color: var(--color-text-primary, #374151);
            cursor: pointer;
            border: none;
            background: none;
            width: 100%;
            text-align: left;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .language-menu-item:hover {
            background: var(--color-bg-secondary, #f9fafb);
            color: var(--color-magenta-800, #a21caf);
        }

        .language-menu-item.active {
            background: var(--color-magenta-50, #fdf4ff);
            color: var(--color-magenta-800, #a21caf);
        }

        .language-flag {
            font-size: 16px;
            margin-right: 8px;
        }

        .language-check {
            color: var(--color-magenta-800, #a21caf);
            font-weight: 600;
        }

        /* 用户圆形按钮样式 - 仿原生UI */
        .user-circle {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--color-magenta-800, #a21caf); /* 保持紫色背景 */
            color: rgba(255, 255, 255, 0.6); /* 默认灰色文字 */
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 14px;
            border: 1px solid var(--color-magenta-800, #a21caf);
            position: relative;
            z-index: 10001;
        }

        .user-circle:hover {
            background: var(--color-magenta-800, #a21caf); /* 背景保持不变 */
            color: white; /* 悬停时文字变白色高亮 */
            border-color: var(--color-magenta-800, #a21caf);
        }

        /* Tooltip样式 - 精确仿原生设计 */
        .user-circle::after {
            content: 'User';
            position: absolute;
            bottom: -40px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(55, 65, 81, 0.95); /* 灰黑色背景，类似截图 */
            color: rgba(255, 255, 255, 0.9);
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 500;
            white-space: nowrap;
            opacity: 0;
            visibility: hidden;
            transition: all 0.15s ease;
            pointer-events: none;
            z-index: 10002;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 45px;
            text-align: center;
        }

        .user-circle:hover::after {
            opacity: 1;
            visibility: visible;
            bottom: -38px;
        }

        .user-circle:hover {
            background: var(--color-magenta-900, #86198f);
            border-color: var(--color-magenta-900, #86198f);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(162, 28, 175, 0.3);
        }
        /* 与登录界面一致的下拉菜单样式 */
        .user-dropdown {
            position: absolute;
            top: 100%;
            right: 0;
            margin-top: 12px;
            background: var(--color-bg-primary, white);
            border: 1px solid var(--color-border-primary, #e5e7eb);
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            min-width: 320px;
            max-width: 320px;
            z-index: 10001;
            opacity: 0;
            visibility: hidden;
            transform: translateY(-10px);
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }

        .user-dropdown.show {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }

        .user-dropdown-header {
            padding: 20px;
            border-bottom: 1px solid var(--color-border-secondary, #f3f4f6);
            background: linear-gradient(135deg, var(--color-magenta-50, #fdf4ff) 0%, var(--color-blue-50, #eff6ff) 100%);
            border-radius: 12px 12px 0 0;
        }

        .user-name {
            font-weight: 600;
            color: var(--color-text-primary, #111827);
            margin-bottom: 6px;
            font-size: 16px;
        }

        .user-email {
            color: var(--color-text-secondary, #6b7280);
            font-size: 14px;
        }

        .user-dropdown-menu {
            padding: 12px 0;
        }

        .menu-item {
            display: flex;
            align-items: center;
            padding: 14px 20px;
            color: var(--color-text-primary, #374151);
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
            background: none;
            width: 100%;
            text-align: left;
            font-size: 14px;
            font-weight: 500;
        }

        .menu-item:hover {
            background: var(--color-bg-secondary, #f9fafb);
            color: var(--color-magenta-800, #a21caf);
        }

        .menu-item.danger {
            color: var(--color-error-primary, #dc2626);
        }

        .menu-item.danger:hover {
            background: var(--color-error-light, #fef2f2);
            color: var(--color-error-primary, #dc2626);
        }

        .menu-icon {
            width: 18px;
            height: 18px;
            margin-right: 14px;
        }

        /* 与登录界面一致的表单样式 */
        .edit-form {
            padding: 20px;
            border-top: 1px solid var(--color-border-secondary, #f3f4f6);
            background: var(--color-bg-primary, white);
            border-radius: 0 0 12px 12px;
        }

        .form-group {
            margin-bottom: 16px;
        }

        .form-label {
            display: block;
            margin-bottom: 6px;
            font-weight: 500;
            color: var(--color-text-primary, #374151);
            font-size: 14px;
        }

        .form-input {
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
            padding: 12px 16px;
            border: 1px solid var(--color-border-primary, #d1d5db);
            border-radius: 8px;
            font-size: 14px;
            transition: all 0.2s ease;
            background: var(--color-bg-primary, white);
            color: var(--color-text-primary, #111827);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--color-magenta-800, #a21caf);
            box-shadow: 0 0 0 3px rgba(162, 28, 175, 0.1);
        }

        .form-actions {
            display: flex;
            gap: 12px;
            justify-content: flex-end;
            margin-top: 20px;
        }

        .btn {
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            transition: all 0.2s ease;
        }

        .btn-primary {
            background: var(--color-magenta-800, #a21caf);
            color: white;
        }

        .btn-primary:hover {
            background: var(--color-magenta-900, #86198f);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(162, 28, 175, 0.3);
        }

        .btn-secondary {
            background: var(--color-bg-secondary, #f3f4f6);
            color: var(--color-text-primary, #374151);
        }

        .btn-secondary:hover {
            background: var(--color-bg-tertiary, #e5e7eb);
        }

        .hidden {
            display: none;
        }

        /* 语言分隔线 */
        .language-divider {
            height: 1px;
            background: var(--color-border-secondary, #f3f4f6);
            margin: 8px 0;
        }

        /* 响应式设计 */
        @media (max-width: 480px) {
            .user-management-overlay {
                top: 10px;
                right: 10px;
            }

            .user-circle {
                width: 28px;
                height: 28px;
                font-size: 12px;
            }

            .user-circle::after {
                font-size: 11px;
                padding: 6px 10px;
                border-radius: 6px;
                min-width: 40px;
            }

            .user-dropdown {
                min-width: 300px;
                max-width: 300px;
                margin-top: 8px;
            }
        }
    </style>
</head>
<body>
    <div class="user-management-overlay">
        <div class="user-menu-container">
            <div class="user-circle" id="user-circle">U</div>
            <div class="user-dropdown" id="user-dropdown">
                <div class="user-dropdown-header">
                    <div class="user-name" id="user-username">Username</div>
                    <div class="user-email" id="user-email">user@example.com</div>
                </div>
                <div class="user-dropdown-menu" id="user-menu">
                    <button class="menu-item" id="edit-profile-btn">
                        <svg class="menu-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                        </svg>
                        <span data-i18n="edit_profile">Edit Profile</span>
                    </button>

                    <div class="language-divider"></div>

                    <!-- 语言选择选项 -->
                    <button class="language-menu-item active" data-lang="en">
                        <div>
                            <span class="language-flag">🇺🇸</span>
                            <span data-i18n="english">English</span>
                        </div>
                        <span class="language-check">✓</span>
                    </button>
                    <button class="language-menu-item" data-lang="zh">
                        <div>
                            <span class="language-flag">🇨🇳</span>
                            <span data-i18n="chinese">中文</span>
                        </div>
                        <span class="language-check" style="opacity: 0;">✓</span>
                    </button>
                    <button class="language-menu-item" data-lang="ja">
                        <div>
                            <span class="language-flag">🇯🇵</span>
                            <span data-i18n="japanese">日本語</span>
                        </div>
                        <span class="language-check" style="opacity: 0;">✓</span>
                    </button>

                    <div class="language-divider"></div>

                    <button class="menu-item danger" id="sign-out-btn">
                        <svg class="menu-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
                        </svg>
                        <span data-i18n="sign_out">Sign Out</span>
                    </button>
                </div>
                <div class="edit-form hidden" id="edit-form">
                    <div class="form-group">
                        <label class="form-label" data-i18n="username">Username</label>
                        <input type="text" class="form-input" id="edit-username" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" data-i18n="email">Email</label>
                        <input type="email" class="form-input" id="edit-email">
                    </div>
                    <div class="form-group">
                        <label class="form-label" data-i18n="full_name">Full Name</label>
                        <input type="text" class="form-input" id="edit-fullname">
                    </div>
                    <div class="form-actions">
                        <button class="btn btn-secondary" id="cancel-edit-btn" data-i18n="cancel">Cancel</button>
                        <button class="btn btn-primary" id="save-changes-btn" data-i18n="save_changes">Save</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <iframe id="magentic-ui-frame" src="http://localhost:8081" style="width: 100%; height: 100vh; border: none;" onload="positionUserButton()"></iframe>
    <script src="http://localhost:8000/user-management.js"></script>
    <script>
        // 用户按钮初始化 - 位置通过CSS固定
        function positionUserButton() {
            // 按钮位置已通过CSS固定设置
        }

        // 初始化语言菜单
        function initLanguageMenu() {
            const currentLang = localStorage.getItem('preferred_language') || 'en';
            updateLanguageMenu(currentLang);
        }

        // 更新语言菜单显示
        function updateLanguageMenu(selectedLang) {
            document.querySelectorAll('.language-menu-item').forEach(item => {
                const lang = item.getAttribute('data-lang');
                const checkMark = item.querySelector('.language-check');

                if (lang === selectedLang) {
                    item.classList.add('active');
                    checkMark.style.opacity = '1';
                } else {
                    item.classList.remove('active');
                    checkMark.style.opacity = '0';
                }
            });
        }

        const userCircle = document.getElementById('user-circle');
        const userDropdown = document.getElementById('user-dropdown');
        const editProfileBtn = document.getElementById('edit-profile-btn');
        const signOutBtn = document.getElementById('sign-out-btn');
        const editForm = document.getElementById('edit-form');
        const userMenu = document.getElementById('user-menu');
        const cancelEditBtn = document.getElementById('cancel-edit-btn');
        const saveChangesBtn = document.getElementById('save-changes-btn');

        userCircle.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('show');
        });

        document.addEventListener('click', function() {
            userDropdown.classList.remove('show');
        });

        userDropdown.addEventListener('click', function(e) {
            e.stopPropagation();
        });

        editProfileBtn.addEventListener('click', function() {
            if (window.UserManagement && window.UserManagement.currentUser()) {
                const user = window.UserManagement.currentUser();
                document.getElementById('edit-username').value = user.username || '';
                document.getElementById('edit-email').value = user.email || '';
                document.getElementById('edit-fullname').value = user.full_name || '';
                userMenu.classList.add('hidden');
                editForm.classList.remove('hidden');
            }
        });

        cancelEditBtn.addEventListener('click', function() {
            editForm.classList.add('hidden');
            userMenu.classList.remove('hidden');
        });

        saveChangesBtn.addEventListener('click', async function() {
            const userData = {
                username: document.getElementById('edit-username').value,
                email: document.getElementById('edit-email').value || null,
                full_name: document.getElementById('edit-fullname').value || null
            };

            if (window.UserManagement) {
                const success = await window.UserManagement.updateUserProfile(userData);
                if (success) {
                    editForm.classList.add('hidden');
                    userMenu.classList.remove('hidden');
                    userDropdown.classList.remove('show');
                }
            }
        });

        signOutBtn.addEventListener('click', function() {
            if (window.UserManagement) {
                window.UserManagement.signOut();
            }
        });

        // 语言菜单项点击事件
        document.querySelectorAll('.language-menu-item').forEach(item => {
            item.addEventListener('click', function() {
                const lang = this.getAttribute('data-lang');
                if (window.UserManagement) {
                    window.UserManagement.switchLanguage(lang);
                    updateLanguageMenu(lang);
                    // 关闭下拉菜单
                    userDropdown.classList.remove('show');
                }
            });
        });

        // 初始化语言菜单
        initLanguageMenu();

        // 智能定位用户按钮
        positionUserButton();
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)
