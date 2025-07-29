import { Modal, Input, message, Divider, Select, Tabs, Form } from "antd";
import { setLocalStorage, getLocalStorage } from "./utils";
import { appContext } from "../hooks/provider";
import * as React from "react";
import { Button } from "./common/Button";

type SignInModalProps = {
  isVisible: boolean;
  onClose: () => void;
};

const SignInModal = ({ isVisible, onClose }: SignInModalProps) => {
  const { user, setUser } = React.useContext(appContext);
  const [email, setEmail] = React.useState(user?.email || "default");
  const [language, setLanguage] = React.useState(() => {
    return getLocalStorage("user_language", false) || "en";
  });

  // 从认证token获取真实用户信息
  const [authUser, setAuthUser] = React.useState<any>(null);

  React.useEffect(() => {
    if (!isVisible) return; // 只在模态框可见时执行

    // 首先检查URL参数中是否有token（从登录页面跳转过来）
    const urlParams = new URLSearchParams(window.location.search);
    const urlToken = urlParams.get("token");
    const urlUser = urlParams.get("user");

    let token = localStorage.getItem("access_token");
    let storedUser = localStorage.getItem("user");

    console.log("=== SignIn Modal Debug ===");
    console.log("URL Token:", urlToken);
    console.log("URL User:", urlUser);
    console.log("LocalStorage Token:", token);
    console.log("LocalStorage User:", storedUser);

    // 如果URL中有token，优先使用URL中的token并保存到localStorage
    if (urlToken && urlUser) {
      console.log("Found token in URL, saving to localStorage...");
      localStorage.setItem("access_token", urlToken);
      localStorage.setItem("user", urlUser);
      token = urlToken;
      storedUser = urlUser;

      // 清除URL参数，避免token暴露在URL中
      const newUrl = window.location.pathname;
      window.history.replaceState({}, document.title, newUrl);
    }

    if (token && storedUser) {
      try {
        const userData = JSON.parse(storedUser);
        console.log("Using user data:", userData);
        setAuthUser(userData);
        setEmail(userData.username || userData.email || "default");
      } catch (error) {
        console.error("Error parsing user data:", error);
        // 如果解析失败，重新获取
        fetchUserInfo(token);
      }
    } else if (token) {
      // 如果有 token 但没有用户信息，从 API 获取
      console.log("No stored user, fetching from API...");
      fetchUserInfo(token);
    } else {
      console.log("No token found");
    }
  }, [isVisible]);

  const fetchUserInfo = React.useCallback(async (token: string) => {
    try {
      console.log("Fetching user info with token:", token);
      const response = await fetch("http://127.0.0.1:8000/api/auth/me", {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      console.log("API response status:", response.status);

      if (response.ok) {
        const userData = await response.json();
        console.log("Fetched user data from API:", userData);
        localStorage.setItem("user", JSON.stringify(userData));
        setAuthUser(userData);
        setEmail(userData.username || userData.email || "default");
      } else {
        console.error("API response not ok:", response.status, response.statusText);
        const errorText = await response.text();
        console.error("Error response:", errorText);
      }
    } catch (error) {
      console.error("Error fetching user info:", error);
    }
  }, []);

  const isAlreadySignedIn = !!user?.email || !!authUser;

  // Language options
  const languageOptions = [
    { value: "en", label: "🇺🇸 English" },
    { value: "zh", label: "🇨🇳 中文" },
    { value: "ja", label: "🇯🇵 日本語" },
  ];

  // 多语言文本配置
  const translations = {
    en: {
      userManagement: "User Management",
      signIn: "Sign In",
      chooseLoginMethod: "Choose Login Method",
      quickLogin: "Quick Login (Demo Mode)",
      enterUsername: "Enter a username",
      quickSignIn: "Quick Sign In",
      fullAuth: "Full Authentication System",
      loginWithAuth: "🔐 Login with Authentication",
      currentUser: "Current User",
      logout: "🚪 Logout",
      profile: "👤 Profile",
      password: "🔒 Password",
      settings: "⚙️ Settings",
      username: "Username (Read Only)",
      usernameCannotChange: "Username cannot be changed",
      email: "Email (Read Only)",
      emailCannotChange: "Email cannot be changed",
      fullName: "Full Name",
      enterFullName: "Enter your full name",
      updateProfile: "Update Profile",
      currentPassword: "Current Password",
      enterCurrentPassword: "Enter current password",
      newPassword: "New Password",
      enterNewPassword: "Enter new password",
      confirmNewPassword: "Confirm New Password",
      confirmNewPasswordPlaceholder: "Confirm new password",
      changePassword: "Change Password",
      language: "🌍 Language",
      selectLanguage: "Select language",
      profileUpdated: "Profile updated successfully",
      passwordChanged: "Password changed successfully",
      languageChanged: "Language changed to",
      loggedOut: "Logged out successfully",
      pleaseLoginFirst: "Please login first",
      passwordsNotMatch: "Passwords do not match",
      pleaseEnterCurrentPassword: "Please enter current password",
      pleaseEnterNewPassword: "Please enter new password",
      pleaseConfirmNewPassword: "Please confirm new password"
    },
    zh: {
      userManagement: "用户管理",
      signIn: "登录",
      chooseLoginMethod: "选择登录方式",
      quickLogin: "快速登录（演示模式）",
      enterUsername: "输入用户名",
      quickSignIn: "快速登录",
      fullAuth: "完整认证系统",
      loginWithAuth: "🔐 使用认证系统登录",
      currentUser: "当前用户",
      logout: "🚪 退出登录",
      profile: "👤 个人资料",
      password: "🔒 密码",
      settings: "⚙️ 设置",
      username: "用户名（只读）",
      usernameCannotChange: "用户名无法更改",
      email: "邮箱（只读）",
      emailCannotChange: "邮箱无法更改",
      fullName: "全名",
      enterFullName: "输入您的全名",
      updateProfile: "更新资料",
      currentPassword: "当前密码",
      enterCurrentPassword: "输入当前密码",
      newPassword: "新密码",
      enterNewPassword: "输入新密码",
      confirmNewPassword: "确认新密码",
      confirmNewPasswordPlaceholder: "确认新密码",
      changePassword: "修改密码",
      language: "🌍 语言",
      selectLanguage: "选择语言",
      profileUpdated: "资料更新成功",
      passwordChanged: "密码修改成功",
      languageChanged: "语言已切换至",
      loggedOut: "退出登录成功",
      pleaseLoginFirst: "请先登录",
      passwordsNotMatch: "密码不匹配",
      pleaseEnterCurrentPassword: "请输入当前密码",
      pleaseEnterNewPassword: "请输入新密码",
      pleaseConfirmNewPassword: "请确认新密码"
    },
    ja: {
      userManagement: "ユーザー管理",
      signIn: "サインイン",
      chooseLoginMethod: "ログイン方法を選択",
      quickLogin: "クイックログイン（デモモード）",
      enterUsername: "ユーザー名を入力",
      quickSignIn: "クイックサインイン",
      fullAuth: "完全認証システム",
      loginWithAuth: "🔐 認証システムでログイン",
      currentUser: "現在のユーザー",
      logout: "🚪 ログアウト",
      profile: "👤 プロフィール",
      password: "🔒 パスワード",
      settings: "⚙️ 設定",
      username: "ユーザー名（読み取り専用）",
      usernameCannotChange: "ユーザー名は変更できません",
      email: "メール（読み取り専用）",
      emailCannotChange: "メールは変更できません",
      fullName: "フルネーム",
      enterFullName: "フルネームを入力",
      updateProfile: "プロフィール更新",
      currentPassword: "現在のパスワード",
      enterCurrentPassword: "現在のパスワードを入力",
      newPassword: "新しいパスワード",
      enterNewPassword: "新しいパスワードを入力",
      confirmNewPassword: "新しいパスワードの確認",
      confirmNewPasswordPlaceholder: "新しいパスワードを確認",
      changePassword: "パスワード変更",
      language: "🌍 言語",
      selectLanguage: "言語を選択",
      profileUpdated: "プロフィールが正常に更新されました",
      passwordChanged: "パスワードが正常に変更されました",
      languageChanged: "言語が変更されました：",
      loggedOut: "正常にログアウトしました",
      pleaseLoginFirst: "まずログインしてください",
      passwordsNotMatch: "パスワードが一致しません",
      pleaseEnterCurrentPassword: "現在のパスワードを入力してください",
      pleaseEnterNewPassword: "新しいパスワードを入力してください",
      pleaseConfirmNewPassword: "新しいパスワードを確認してください"
    }
  };

  const t = translations[language as keyof typeof translations] || translations.en;

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(e.target.value);
  };

  const handleSignIn = () => {
    const trimmedEmail = email.trim();
    if (!trimmedEmail) {
      message.error("Username cannot be empty");
      return;
    }
    setUser({ ...user, email: trimmedEmail, name: trimmedEmail });
    setLocalStorage("user_email", trimmedEmail);
    onClose();
  };

  const handleLanguageChange = (value: string) => {
    setLanguage(value);
    setLocalStorage("user_language", value, false);
    const selectedLang = languageOptions.find(opt => opt.value === value);
    const newTranslations = translations[value as keyof typeof translations] || translations.en;
    message.success(`${newTranslations.languageChanged} ${selectedLang?.label}`);
  };

  const handleGoToAuth = () => {
    // 跳转到认证系统登录页面
    window.location.href = "http://localhost:8000/login";
  };

  // 更新用户信息的处理函数
  const handleUpdateProfile = async (values: any) => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        message.error(t.pleaseLoginFirst);
        return;
      }

      // 只发送可修改的字段（full_name）
      const updateData = {
        full_name: values.full_name || null
      };

      console.log("🔄 Updating user profile:", updateData);

      const response = await fetch("http://127.0.0.1:8000/api/auth/me", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(updateData),
      });

      console.log("📡 API Response status:", response.status);

      if (response.ok) {
        const updatedUser = await response.json();
        console.log("✅ Profile updated:", updatedUser);

        // 更新localStorage和状态
        localStorage.setItem("user", JSON.stringify(updatedUser));
        setAuthUser(updatedUser);

        // 同时更新 appContext 中的 user 状态，这样头像会立即更新
        setUser({
          email: updatedUser.username || updatedUser.email,
          name: updatedUser.full_name || updatedUser.username || updatedUser.email
        });

        message.success(t.profileUpdated);

      } else {
        const error = await response.json();
        console.error("❌ API Error:", error);
        message.error(error.detail || "Failed to update profile");
      }
    } catch (error) {
      console.error("❌ Network Error:", error);
      message.error("Network error occurred");
    }
  };

  // 修改密码的处理函数
  const handleChangePassword = async (values: any) => {
    try {
      const token = localStorage.getItem("access_token");
      if (!token) {
        message.error(t.pleaseLoginFirst);
        return;
      }

      const response = await fetch("http://127.0.0.1:8000/api/auth/change-password", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({
          current_password: values.currentPassword,
          new_password: values.newPassword,
        }),
      });

      if (response.ok) {
        message.success(t.passwordChanged);
      } else {
        const error = await response.json();
        message.error(error.detail || "Failed to change password");
      }
    } catch (error) {
      console.error("Change password error:", error);
      message.error("Network error, please try again");
    }
  };

  const handleLogout = () => {
    console.log("=== Logout Process Started ===");

    // 清除所有用户状态
    setUser({ email: "", name: "" });
    setAuthUser(null);
    setEmail("default");

    // 清除所有本地存储
    console.log("Clearing localStorage...");
    setLocalStorage("user_email", "");
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    localStorage.removeItem("user_language");
    localStorage.removeItem("remember_me_enabled");
    localStorage.removeItem("remember_me_timestamp");

    // 🎯 跨端口logout解决方案 - 通过URL参数传递清除指令
    console.log("🚪 LOGOUT - Cross-port logout initiated...");

    try {
      // 1. 清除当前端口(8081)的所有数据
      console.log("🗑️ Clearing current port (8081) data...");
      localStorage.clear();
      sessionStorage.clear();

      // 2. 清除cookies
      document.cookie.split(";").forEach(function(c) {
        document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
      });

      console.log("✅ Current port data cleared");
      console.log("🔄 Redirecting to login with clear instruction...");

    } catch (error) {
      console.error("❌ Error clearing current port data:", error);
    }
    message.success(t.loggedOut);

    // 立即关闭模态框
    onClose();

    // 🎯 跳转到登录页面并传递清除指令
    const loginUrl = "http://127.0.0.1:8000/login?clear_remember_me=true&logout_time=" + Date.now();
    console.log("🔗 Redirecting to:", loginUrl);
    window.location.replace(loginUrl);
  };



  return (
    <Modal
      open={isVisible}
      footer={null}
      closable={isAlreadySignedIn}
      maskClosable={isAlreadySignedIn}
      onCancel={isAlreadySignedIn ? onClose : undefined}
      title={isAlreadySignedIn ? t.userManagement : t.signIn}
      width={600}
    >
      {!isAlreadySignedIn ? (
        // 未登录时显示登录选项
        <div className="mb-6">
          <span className="text-lg block mb-3">{t.chooseLoginMethod}</span>

          <div className="space-y-3">
            <div>
              <span className="text-sm text-gray-600 block mb-2">
                {t.quickLogin}
              </span>
              <Input
                type="text"
                placeholder={t.enterUsername}
                value={email}
                onChange={handleEmailChange}
                className="shadow-sm mb-2"
              />
              <Button
                variant="primary"
                onClick={handleSignIn}
                size="sm"
                className="w-full"
              >
                {t.quickSignIn}
              </Button>
            </div>

            <div className="text-center">
              <span className="text-sm text-gray-500">or</span>
            </div>

            <div>
              <span className="text-sm text-gray-600 block mb-2">
                {t.fullAuth}
              </span>
              <Button
                variant="secondary"
                onClick={handleGoToAuth}
                size="sm"
                className="w-full"
              >
                {t.loginWithAuth}
              </Button>
            </div>
          </div>
        </div>
      ) : (
        // 已登录时显示完整的用户管理界面
        <Tabs
          defaultActiveKey="profile"
          items={[
            {
              key: "profile",
              label: t.profile,
              children: (
                <div>
                  <div className="mb-4">
                    <span className="text-sm text-gray-600 block mb-2">{t.currentUser}</span>
                    <div className="text-lg font-medium">
                      {authUser?.username || authUser?.email || user?.name || user?.email || email}
                    </div>
                    {/* 调试信息 */}
                    {process.env.NODE_ENV === 'development' && (
                      <div className="text-xs text-gray-500 mt-2">
                        Debug: {JSON.stringify({
                          authUser: authUser ? {
                            username: authUser.username,
                            email: authUser.email,
                            full_name: authUser.full_name
                          } : null,
                          user: user
                        }, null, 2)}
                      </div>
                    )}
                  </div>

                  <Form
                    onFinish={handleUpdateProfile}
                    layout="vertical"
                    initialValues={{
                      username: authUser?.username || '',
                      email: authUser?.email || '',
                      full_name: authUser?.full_name || ''
                    }}
                    key={authUser?.id || 'default'} // 强制重新渲染当用户数据变化时
                  >
                    <Form.Item
                      label={t.username}
                      name="username"
                    >
                      <Input disabled placeholder={t.usernameCannotChange} />
                    </Form.Item>

                    <Form.Item
                      label={t.email}
                      name="email"
                    >
                      <Input disabled placeholder={t.emailCannotChange} />
                    </Form.Item>

                    <Form.Item
                      label={t.fullName}
                      name="full_name"
                    >
                      <Input placeholder={t.enterFullName} />
                    </Form.Item>

                    <Form.Item>
                      <button type="submit" className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm">
                        {t.updateProfile}
                      </button>
                    </Form.Item>
                  </Form>
                </div>
              ),
            },
            {
              key: "password",
              label: t.password,
              children: (
                <Form onFinish={handleChangePassword} layout="vertical">
                  <Form.Item
                    label={t.currentPassword}
                    name="currentPassword"
                    rules={[{ required: true, message: t.pleaseEnterCurrentPassword }]}
                  >
                    <Input.Password placeholder={t.enterCurrentPassword} />
                  </Form.Item>

                  <Form.Item
                    label={t.newPassword}
                    name="newPassword"
                    rules={[{ required: true, message: t.pleaseEnterNewPassword }]}
                  >
                    <Input.Password placeholder={t.enterNewPassword} />
                  </Form.Item>

                  <Form.Item
                    label={t.confirmNewPassword}
                    name="confirmPassword"
                    dependencies={["newPassword"]}
                    rules={[
                      { required: true, message: t.pleaseConfirmNewPassword },
                      ({ getFieldValue }) => ({
                        validator(_, value) {
                          if (!value || getFieldValue("newPassword") === value) {
                            return Promise.resolve();
                          }
                          return Promise.reject(new Error(t.passwordsNotMatch));
                        },
                      }),
                    ]}
                  >
                    <Input.Password placeholder={t.confirmNewPasswordPlaceholder} />
                  </Form.Item>

                  <Form.Item>
                    <button type="submit" className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded text-sm">
                      {t.changePassword}
                    </button>
                  </Form.Item>
                </Form>
              ),
            },
            {
              key: "settings",
              label: t.settings,
              children: (
                <div>
                  <div className="mb-6">
                    <div className="mb-3">
                      <span className="text-base font-medium">{t.language}</span>
                    </div>
                    <Select
                      value={language}
                      onChange={handleLanguageChange}
                      options={languageOptions}
                      className="w-full"
                      placeholder={t.selectLanguage}
                    />
                  </div>

                  <Divider />

                  <div className="mb-4">
                    <Button
                      variant="secondary"
                      onClick={handleLogout}
                      className="w-full flex items-center justify-center"
                    >
                      {t.logout}
                    </Button>
                  </div>
                </div>
              ),
            },
          ]}
        />
      )}
    </Modal>
  );
};

export default SignInModal;
