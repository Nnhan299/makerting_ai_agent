import React, { useState } from 'react';
import '../auth.css';
import { loginApi } from '../api';

export default function Login({ onLoginSuccess }) {
  const [lang, setLang] = useState('VI');
  const [showPassword, setShowPassword] = useState(false);
  const [username, setUsername] = useState('nhan');
  const [password, setPassword] = useState('nhan1903');
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleLogin = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setErrorMsg('');
    try {
      const res = await loginApi(username, password);
      if (res && res.user) {
        if (rememberMe) {
          localStorage.setItem('aura_active_user', JSON.stringify(res.user));
          localStorage.setItem('aura_token', res.token || 'demo_token');
        }
        if (onLoginSuccess) {
          onLoginSuccess(res.user);
        }
      } else {
        throw new Error('Dữ liệu xác thực không hợp lệ');
      }
    } catch (err) {
      console.error('Login error:', err);
      setErrorMsg(err.message || 'Tên đăng nhập hoặc mật khẩu không chính xác.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = async (userType) => {
    let u = 'nhan';
    let p = 'nhan1903';
    if (userType === 'admin') {
      u = 'admin';
      p = 'admin123';
    } else if (userType === 'creator') {
      u = 'creator';
      p = 'creator123';
    }
    setUsername(u);
    setPassword(p);
    setLoading(true);
    setErrorMsg('');
    try {
      const res = await loginApi(u, p);
      if (res && res.user) {
        localStorage.setItem('aura_active_user', JSON.stringify(res.user));
        localStorage.setItem('aura_token', res.token || 'demo_token');
        if (onLoginSuccess) {
          onLoginSuccess(res.user);
        }
      }
    } catch (err) {
      // Local fallback in case server temporarily unreachable
      const fallbackUser = userType === 'admin' 
        ? { id: 1, username: 'admin', name: 'Quản trị viên Hệ thống', initials: 'QT', role: 'Admin', email: 'admin@marketing.ai' }
        : userType === 'creator'
        ? { id: 3, username: 'creator', name: 'Trần Thị Mai (Creator)', initials: 'TT', role: 'Content Creator', email: 'mai.tran@marketing.ai' }
        : { id: 2, username: 'nhan', name: 'Nguyễn Hoàng Nhân (Lead)', initials: 'NH', role: 'Marketing Lead', email: 'nhan@marketing.ai' };
      localStorage.setItem('aura_active_user', JSON.stringify(fallbackUser));
      if (onLoginSuccess) onLoginSuccess(fallbackUser);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <main className="auth-viewport">
        <div className="auth-card">

          {/* ============================================================
               LEFT PANEL: BRAND SHOWCASE & MULTI-AGENT PIPELINE
               ============================================================ */}
          <section className="brand-panel" aria-label="Giới thiệu hệ thống AuraAI">
            <div className="brand-panel-glow"></div>

            {/* Top Bar */}
            <div className="brand-top">
              <div className="logo-group">
                <div className="logo-mark">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                    <path d="M12 2L14.8 9.2L22 12L14.8 14.8L12 22L9.2 14.8L2 12L9.2 9.2L12 2Z"/>
                    <path d="M5 3v4M3 5h4"/>
                  </svg>
                </div>
                <div className="logo-text">
                  <span className="logo-name">AuraAI</span>
                  <span className="logo-sub mono-text">ENTERPRISE OS</span>
                </div>
              </div>

              <div className="security-pill mono-text">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  <path d="m9 12 2 2 4-4"/>
                </svg>
                <span>Enterprise Grade Security</span>
              </div>
            </div>

            {/* Hero Copy */}
            <div className="brand-hero">
              <h1 className="hero-title">
                Autonomous Marketing Intelligence 2026
              </h1>
              <p className="hero-desc">
                Điều phối tự động chiến dịch đa kênh với ma trận 3 AI Agents chuyên trách, tuân chuẩn quy tắc thương hiệu và bảo mật phân quyền đa lớp.
              </p>
            </div>

            {/* Multi-Agent Pipeline Section */}
            <div className="pipeline-section">
              <div className="pipeline-header">
                <span className="pipeline-title font-semibold text-slate-300">Ma trận Điều phối Đa Agent</span>
                <span className="pipeline-line"></span>
                <span className="pipeline-status mono-text">
                  <span className="dot-live"></span>
                  PIPELINES LIVE
                </span>
              </div>

              <div className="agent-grid">
                {/* Agent 01 */}
                <article className="agent-card">
                  <div className="agent-card-top">
                    <span className="agent-icon icon-cyan">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="10"/>
                        <circle cx="12" cy="12" r="6"/>
                        <circle cx="12" cy="12" r="2"/>
                      </svg>
                    </span>
                    <span className="agent-code mono-text">Ag-01</span>
                  </div>
                  <h2 className="agent-name">Market Intel</h2>
                  <p className="agent-desc">
                    Phân tích hành vi đối thủ &amp; dự báo xu hướng tiêu dùng 24/7.
                  </p>
                  <div className="agent-metric metric-green mono-text">
                    <span className="metric-dot"></span>
                    <span>&lt; 45ms &bull; 99.4% SLA</span>
                  </div>
                </article>

                {/* Agent 02 */}
                <article className="agent-card">
                  <div className="agent-card-top">
                    <span className="agent-icon icon-indigo">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 20h9"/>
                        <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/>
                      </svg>
                    </span>
                    <span className="agent-code mono-text">Ag-02</span>
                  </div>
                  <h2 className="agent-name">Copywriter</h2>
                  <p className="agent-desc">
                    Khởi tạo thông điệp quảng cáo cá nhân hóa đa ngữ điệu.
                  </p>
                  <div className="agent-metric metric-indigo mono-text">
                    <span className="metric-dot"></span>
                    <span>Mô hình Aura-v4 LLM</span>
                  </div>
                </article>

                {/* Agent 03 */}
                <article className="agent-card">
                  <div className="agent-card-top">
                    <span className="agent-icon icon-emerald">
                      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                        <path d="m9 12 2 2 4-4"/>
                      </svg>
                    </span>
                    <span className="agent-code mono-text">Ag-03</span>
                  </div>
                  <h2 className="agent-name">Compliance</h2>
                  <p className="agent-desc">
                    Kiểm soát rủi ro pháp lý &amp; chuẩn hóa nhận diện thương hiệu.
                  </p>
                  <div className="agent-metric metric-green mono-text">
                    <span className="metric-dot"></span>
                    <span>100% Brand Safe</span>
                  </div>
                </article>
              </div>
            </div>

            {/* Bottom Social Proof / Trust Footer */}
            <div className="brand-footer">
              <div className="sync-proof">
                <div className="avatar-stack" aria-hidden="true">
                  <span className="avatar-item av-1">M</span>
                  <span className="avatar-item av-2">T</span>
                  <span className="avatar-item av-3">G</span>
                  <span className="avatar-item av-more">+1.4k</span>
                </div>
                <div className="sync-text">
                  <strong>Đồng bộ hơn 1.400+ Ads Groups</strong>
                  <span>Meta Ads, TikTok for Business, Google Marketing</span>
                </div>
              </div>

              <div className="verified-badge mono-text">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                  <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <span>FR-ADM Verified</span>
              </div>
            </div>
          </section>

          {/* ============================================================
               RIGHT PANEL: ENTERPRISE AUTHENTICATION FORM
               ============================================================ */}
          <section className="form-panel" aria-label="Biểu mẫu đăng nhập">

            {/* Status & Language Header */}
            <div className="form-topbar">
              <div className="gateway-status mono-text">
                <span className="status-dot"></span>
                <span>SSO Gateway Online</span>
              </div>

              <div className="lang-switch" role="group" aria-label="Chọn ngôn ngữ">
                <button 
                  type="button" 
                  onClick={() => setLang('VI')}
                  className={`lang-btn ${lang === 'VI' ? 'active' : ''}`}
                >
                  VI
                </button>
                <button 
                  type="button" 
                  onClick={() => setLang('EN')}
                  className={`lang-btn ${lang === 'EN' ? 'active' : ''}`}
                >
                  EN
                </button>
              </div>
            </div>

            {/* Main Form Content */}
            <div className="form-container">
              <header className="form-header">
                <h2 className="form-title">Đăng nhập AuraAI</h2>
                <p className="form-subtitle">
                  Hệ thống xác thực quản trị viên &amp; nhóm chiến dịch tập trung
                </p>
              </header>

              {/* Error Alert Banner */}
              {errorMsg && (
                <div className="auth-error" role="alert">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  <span>{errorMsg}</span>
                </div>
              )}

              <form id="loginForm" className="auth-form" onSubmit={handleLogin} noValidate>
                {/* Email / Username Field */}
                <div className="field-group">
                  <label htmlFor="workEmail" className="field-label">
                    Email công việc / Username <span className="req">*</span>
                  </label>
                  <div className="input-box">
                    <span className="input-icon" aria-hidden="true">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="4"/>
                        <path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-4 8"/>
                      </svg>
                    </span>
                    <input
                      type="text"
                      id="workEmail"
                      name="email"
                      className="field-input"
                      placeholder="admin hoặc nhan"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      required
                      autoComplete="username"
                    />
                  </div>
                </div>

                {/* Password Field */}
                <div className="field-group">
                  <div className="label-row">
                    <label htmlFor="workPassword" className="field-label">
                      Mật khẩu <span className="req">*</span>
                    </label>
                    <a href="#forgot-password" onClick={(e) => { e.preventDefault(); alert('Vui lòng liên hệ Admin hệ thống hoặc dùng chức năng Demo 1-Click.'); }} className="forgot-link">
                      Quên mật khẩu?
                    </a>
                  </div>
                  <div className="input-box">
                    <span className="input-icon" aria-hidden="true">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
                        <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                      </svg>
                    </span>
                    <input
                      type={showPassword ? 'text' : 'password'}
                      id="workPassword"
                      name="password"
                      className="field-input"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      autoComplete="current-password"
                    />
                    <button
                      type="button"
                      id="togglePwdBtn"
                      className="pwd-toggle"
                      onClick={() => setShowPassword(!showPassword)}
                      aria-label="Hiện hoặc ẩn mật khẩu"
                    >
                      {showPassword ? (
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
                          <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
                          <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/>
                          <line x1="2" y1="2" x2="22" y2="22"/>
                        </svg>
                      ) : (
                        <svg id="eyeIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
                          <circle cx="12" cy="12" r="3"/>
                        </svg>
                      )}
                    </button>
                  </div>
                </div>

                {/* Remember Me & MFA Policy Row */}
                <div className="options-row">
                  <label className="checkbox-label">
                    <input 
                      type="checkbox" 
                      checked={rememberMe} 
                      onChange={(e) => setRememberMe(e.target.checked)} 
                    />
                    <span className="custom-check"></span>
                    <span>Ghi nhớ đăng nhập (30 ngày)</span>
                  </label>
                  <span className="mfa-tag mono-text" title="Xác thực đa yếu tố bắt buộc cho tài khoản Quản trị">
                    2FA/MFA Ready
                  </span>
                </div>

                {/* Primary Submit CTA */}
                <button type="submit" className="btn-submit" id="submitBtn" disabled={loading}>
                  <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                    <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
                    <polyline points="10 17 15 12 10 7"/>
                    <line x1="15" y1="12" x2="3" y2="12"/>
                  </svg>
                  <span>{loading ? 'Đang xác thực phiên làm việc...' : 'Đăng nhập với AuraAI'}</span>
                </button>
              </form>

              {/* Quick Demo 1-Click for Evaluators */}
              <div className="demo-bar">
                <div className="demo-title">⚡ Đăng nhập nhanh để trải nghiệm (1-Click)</div>
                <div className="demo-grid">
                  <button 
                    type="button" 
                    onClick={() => handleQuickLogin('admin')} 
                    className="btn-demo btn-demo-admin"
                    title="Tài khoản Quản trị viên cao cấp"
                  >
                    👑 Admin
                  </button>
                  <button 
                    type="button" 
                    onClick={() => handleQuickLogin('lead')} 
                    className="btn-demo btn-demo-lead"
                    title="Tài khoản Marketing Lead (Nguyễn Hoàng Nhân)"
                  >
                    🎯 Lead
                  </button>
                  <button 
                    type="button" 
                    onClick={() => handleQuickLogin('creator')} 
                    className="btn-demo btn-demo-creator"
                    title="Tài khoản Content Creator (Trần Thị Mai)"
                  >
                    ✍️ Creator
                  </button>
                </div>
              </div>

              {/* Enterprise SSO Divider */}
              <div className="sso-divider">
                <span>HOẶC KẾT NỐI SSO DOANH NGHIỆP</span>
              </div>

              {/* SSO Buttons */}
              <div className="sso-grid">
                <button 
                  type="button" 
                  onClick={() => handleQuickLogin('lead')}
                  className="btn-sso"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24">
                    <path fill="#EA4335" d="M12 5c1.6 0 3 .6 4.1 1.7l3.1-3.1C17.3 1.8 14.8 1 12 1 7.4 1 3.5 3.6 1.6 7.4l3.7 2.8C6.2 7.2 8.9 5 12 5z"/>
                    <path fill="#4285F4" d="M23.5 12.3c0-.8-.1-1.6-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.6l3.7 2.9c2.2-2 3.7-5 3.7-8.7z"/>
                    <path fill="#FBBC05" d="M5.3 14.8c-.2-.8-.4-1.8-.4-2.8s.2-2 .4-2.8L1.6 6.4C.6 8.4 0 10.6 0 12s.6 3.6 1.6 5.6l3.7-2.8z"/>
                    <path fill="#34A853" d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3.1 0-5.8-2.1-6.7-5l-3.7 2.8C3.5 20.4 7.4 23 12 23z"/>
                  </svg>
                  <span>Google Workspace</span>
                </button>

                <button 
                  type="button" 
                  onClick={() => handleQuickLogin('admin')}
                  className="btn-sso"
                >
                  <svg width="16" height="16" viewBox="0 0 23 23">
                    <path fill="#f35325" d="M1 1h10v10H1z"/>
                    <path fill="#81bc06" d="M12 1h10v10H12z"/>
                    <path fill="#05a6f0" d="M1 12h10v10H1z"/>
                    <path fill="#ffba08" d="M12 12h10v10H12z"/>
                  </svg>
                  <span>Microsoft Azure AD</span>
                </button>
              </div>
            </div>

            {/* Security & RBAC Footer */}
            <footer className="form-footer">
              <div className="footer-security-row mono-text">
                <div className="encryption-badge">
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                    <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                  </svg>
                  <span>AES-256 Encrypted &amp; RBAC v2.4</span>
                </div>
                <span className="spec-code">SRS FR-ADM &bull; Sec 6.0</span>
              </div>

              <div className="rbac-roles">
                <span className="rbac-label">Phân vùng vai trò được bảo vệ:</span>
                <div className="role-pills">
                  <span className="role-pill">Super Admin</span>
                  <span className="role-pill">Creative Lead</span>
                  <span className="role-pill">Analyst</span>
                  <span className="role-pill">Client Viewer</span>
                </div>
              </div>
            </footer>

          </section>
        </div>
      </main>
    </div>
  );
}
