import React, { useState } from 'react';
import { 
  Sparkles, 
  ShieldCheck, 
  Radio, 
  BrainCircuit, 
  Scale, 
  Mail, 
  Lock, 
  Eye, 
  EyeOff, 
  LogIn, 
  CheckCircle2 
} from 'lucide-react';

export default function Login({ onLoginSuccess }) {
  const [lang, setLang] = useState('VI');
  const [showPassword, setShowPassword] = useState(false);
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [rememberMe, setRememberMe] = useState(true);

  const handleLogin = (e) => {
    e.preventDefault();
    if (onLoginSuccess) {
      onLoginSuccess({
        username,
        name: username === 'admin' ? 'Nguyễn Nhật Minh (Admin)' : 'Trần Thu Hà (Lead)',
        role: username === 'admin' ? 'System Admin' : 'Marketing Lead'
      });
    }
  };

  const handleQuickLogin = (role) => {
    if (onLoginSuccess) {
      if (role === 'admin') {
        onLoginSuccess({ username: 'admin', name: 'Quản trị viên Hệ thống', role: 'System Admin' });
      } else if (role === 'lead') {
        onLoginSuccess({ username: 'lead', name: 'Trần Nhật Minh', role: 'Marketing Lead' });
      } else {
        onLoginSuccess({ username: 'creator', name: 'Lê Hoàng Nam', role: 'Content Creator' });
      }
    }
  };

  return (
    <div className="min-h-screen w-full bg-[#FAF8FF] flex items-center justify-center p-4 lg:p-12 relative overflow-hidden font-sans">
      {/* Ambient Backdrop Aura Orbs */}
      <div className="absolute -top-16 -left-16 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -bottom-20 -right-20 w-[420px] h-[420px] bg-emerald-400/15 rounded-full blur-3xl pointer-events-none" />

      {/* Main Dual Split Card Structure */}
      <div className="w-full max-w-6xl bg-white rounded-2xl shadow-2xl overflow-hidden grid grid-cols-1 lg:grid-cols-12 border border-slate-100 relative z-10">
        
        {/* ============================================================ */}
        {/* LEFT PANEL: Brand Showcase & Autonomous 3-Agent Matrix (7 Cols) */}
        {/* ============================================================ */}
        <div className="lg:col-span-7 bg-[#283044] p-8 lg:p-12 flex flex-col justify-between relative overflow-hidden text-white">
          <div className="flex items-center justify-between relative z-10">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-[#4F46E5] flex items-center justify-center shadow-md shadow-indigo-500/20">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold tracking-tight text-[#FAF8FF] leading-none">AuraAI</h1>
                <span className="text-[10px] font-mono tracking-widest text-[#D2D9F4] uppercase font-medium">ENTERPRISE OS</span>
              </div>
            </div>

            <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 border border-white/5 shadow-sm">
              <ShieldCheck className="w-4 h-4 text-[#6FFBBE]" />
              <span className="text-xs font-mono font-medium text-[#6FFBBE]">Enterprise Grade Security</span>
            </div>
          </div>

          <div className="my-8 relative z-10 space-y-5">
            <div className="text-xs font-semibold tracking-wider text-[#C3C0FF] uppercase">
              NEXT-GEN CREATIVE OPS
            </div>
            
            <h2 className="text-3xl lg:text-4xl font-extrabold text-[#FAF8FF] tracking-tight leading-tight">
              Autonomous Marketing <br />Intelligence 2026
            </h2>

            <p className="text-sm text-[#D2D9F4] leading-relaxed max-w-lg">
              Điều phối tự động chiến dịch đa kênh với ma trận 3 AI Agents chuyên trách, tuân chuẩn quy chuẩn thương hiệu và bảo mật phân quyền đa lớp.
            </p>

            <div className="pt-4 space-y-3">
              <div className="flex items-center justify-between text-xs font-semibold">
                <span className="text-[#D2D9F4] tracking-wider uppercase">HỆ THỐNG TỰ HÀNH ĐA AGENT</span>
                <span className="font-mono text-[#4EDEA3] tracking-widest">PIPELINES LIVE</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                <div className="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-white/10 transition-colors">
                  <div className="flex items-center justify-between mb-2">
                    <div className="w-7 h-7 rounded-md bg-cyan-900/40 flex items-center justify-center text-[#ACEDFF]">
                      <Radio className="w-4 h-4" />
                    </div>
                    <span className="text-[10px] font-mono text-[#ACEDFF]">Ag-01</span>
                  </div>
                  <div className="text-xs font-bold text-white mb-1">Market Intel</div>
                  <p className="text-[11px] text-[#D2D9F4] leading-snug line-clamp-2">
                    Phân tích hành vi đối thủ & dự báo xu hướng tiêu dùng 24/7.
                  </p>
                  <div className="flex items-center gap-1.5 mt-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#6FFBBE]" />
                    <span className="text-[10px] font-mono text-[#6FFBBE]">99.4% Tốc độ cao</span>
                  </div>
                </div>

                <div className="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-white/10 transition-colors">
                  <div className="flex items-center justify-between mb-2">
                    <div className="w-7 h-7 rounded-md bg-indigo-900/50 flex items-center justify-center text-[#E2DFFF]">
                      <BrainCircuit className="w-4 h-4" />
                    </div>
                    <span className="text-[10px] font-mono text-[#E2DFFF]">Ag-02</span>
                  </div>
                  <div className="text-xs font-bold text-white mb-1">Copywriter</div>
                  <p className="text-[11px] text-[#D2D9F4] leading-snug line-clamp-2">
                    Sinh trưởng thông điệp quảng cáo cá nhân hóa đa ngữ điệu.
                  </p>
                  <div className="flex items-center gap-1.5 mt-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#E2DFFF]" />
                    <span className="text-[10px] font-mono text-[#E2DFFF]">Gemini 3.8 Flash</span>
                  </div>
                </div>

                <div className="bg-white/5 border border-white/10 rounded-lg p-3 hover:bg-white/10 transition-colors">
                  <div className="flex items-center justify-between mb-2">
                    <div className="w-7 h-7 rounded-md bg-emerald-900/40 flex items-center justify-center text-[#6FFBBE]">
                      <Scale className="w-4 h-4" />
                    </div>
                    <span className="text-[10px] font-mono text-[#6FFBBE]">Ag-03</span>
                  </div>
                  <div className="text-xs font-bold text-white mb-1">Compliance</div>
                  <p className="text-[11px] text-[#D2D9F4] leading-snug line-clamp-2">
                    Kiểm soát rủi ro pháp lý & bảo vệ nhận diện thương hiệu.
                  </p>
                  <div className="flex items-center gap-1.5 mt-2.5">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#6FFBBE]" />
                    <span className="text-[10px] font-mono text-[#6FFBBE]">100% Brand Safe</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-white/10 flex items-center justify-between text-xs relative z-10">
            <div>
              <div className="font-mono text-white font-semibold">Đồng bộ hơn 1.400+ Ads Groups</div>
              <div className="text-[#D2D9F4] text-[11px]">Meta Ads, TikTok for Business, Google Marketing</div>
            </div>
            <div className="text-[#D2D9F4] font-mono text-[11px] flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5 text-[#6FFBBE]" />
              FR-ADM Verified
            </div>
          </div>
        </div>

        {/* ============================================================ */}
        {/* RIGHT PANEL: Authentication & SSO Workspace Card (5 Cols)   */}
        {/* ============================================================ */}
        <div className="lg:col-span-5 p-8 lg:p-12 flex flex-col justify-between bg-white">
          <div className="flex items-center justify-between pb-4">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#006C49] animate-pulse" />
              <span className="font-mono text-xs text-[#464555] font-medium">SSO Gateway Online</span>
            </div>

            <div className="flex bg-[#EAEDFF] p-0.5 rounded-lg border border-indigo-100">
              <button 
                type="button"
                onClick={() => setLang('VI')}
                className={`px-2.5 py-1 text-xs font-bold rounded ${lang === 'VI' ? 'bg-white text-[#3525CD] shadow-sm' : 'text-[#464555]'}`}
              >
                VI
              </button>
              <button 
                type="button"
                onClick={() => setLang('EN')}
                className={`px-2.5 py-1 text-xs font-bold rounded ${lang === 'EN' ? 'bg-white text-[#3525CD] shadow-sm' : 'text-[#464555]'}`}
              >
                EN
              </button>
            </div>
          </div>

          <div className="my-auto space-y-5">
            <div>
              <h2 className="text-2xl font-bold text-[#131B2E] tracking-tight">Đăng nhập AuraAI</h2>
              <p className="text-xs text-[#464555] mt-1">
                Hệ thống xác thực quản trị viên & nhóm chiến dịch tập trung
              </p>
            </div>

            <form onSubmit={handleLogin} className="space-y-3.5">
              <div className="space-y-1">
                <label className="block text-xs font-semibold text-[#131B2E]">
                  Email công việc / Username <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="admin hoặc lead"
                    required
                    className="w-full bg-[#F2F3FF] border border-transparent focus:border-[#4F46E5] focus:bg-white rounded-lg pl-10 pr-4 py-2.5 text-sm text-[#131B2E] placeholder-slate-400 outline-none transition"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between items-center">
                  <label className="block text-xs font-semibold text-[#131B2E]">
                    Mật khẩu <span className="text-red-500">*</span>
                  </label>
                  <a href="#forgot" className="text-xs font-semibold text-[#3525CD] hover:underline">
                    Quên mật khẩu?
                  </a>
                </div>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    required
                    className="w-full bg-[#F2F3FF] border border-transparent focus:border-[#4F46E5] focus:bg-white rounded-lg pl-10 pr-10 py-2.5 text-sm text-[#131B2E] placeholder-slate-400 outline-none transition"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <div className="flex items-center justify-between text-xs pt-1">
                <label className="flex items-center gap-2 text-[#464555] cursor-pointer">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="w-4 h-4 rounded text-[#4F46E5] focus:ring-0"
                  />
                  Ghi nhớ đăng nhập
                </label>
                <span className="font-mono text-[#006C49] font-medium text-[11px]">SRS FR-ADM</span>
              </div>

              <button
                type="submit"
                className="w-full bg-[#4F46E5] hover:bg-[#4338CA] text-white py-3 px-4 rounded-lg font-semibold text-sm flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/25 transition active:scale-[0.99]"
              >
                <LogIn className="w-4 h-4" />
                Đăng nhập Workspace
              </button>
            </form>

            {/* Quick Demo 1-Click for Professors & Evaluators */}
            <div className="pt-2">
              <div className="text-[10px] font-mono uppercase text-center font-bold text-slate-400 mb-2">
                ⚡ Đăng nhập nhanh để Demo (1-Click)
              </div>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => handleQuickLogin('admin')}
                  className="py-1.5 px-2 bg-purple-50 hover:bg-purple-100 text-purple-700 text-xs font-bold rounded-lg border border-purple-200 transition"
                >
                  👑 Admin
                </button>
                <button
                  type="button"
                  onClick={() => handleQuickLogin('lead')}
                  className="py-1.5 px-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 text-xs font-bold rounded-lg border border-emerald-200 transition"
                >
                  🎯 Lead
                </button>
                <button
                  type="button"
                  onClick={() => handleQuickLogin('creator')}
                  className="py-1.5 px-2 bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-bold rounded-lg border border-blue-200 transition"
                >
                  ✍️ Creator
                </button>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-100 space-y-1">
            <div className="flex items-center justify-between text-[11px] font-mono text-[#464555]">
              <span className="flex items-center gap-1">
                <Lock className="w-3 h-3 text-[#006C49]" />
                AES-256 Encrypted & RBAC v2.4
              </span>
              <span>SRS Sec 6.0</span>
            </div>
            <p className="text-[10px] text-slate-400 leading-tight">
              Truy cập được bảo vệ theo phân vùng vai trò: Super Admin, Creative Lead, Analyst, Client Viewer.
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}

