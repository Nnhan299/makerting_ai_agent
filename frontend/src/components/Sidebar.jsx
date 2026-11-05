import React from 'react';
import { 
  Sparkles, 
  FolderKanban, 
  ShieldCheck, 
  SplitSquareVertical, 
  CalendarClock, 
  Settings2, 
  LogOut, 
  Database, 
  Activity,
  Layers
} from 'lucide-react';

export default function Sidebar({ activePage, setActivePage, currentUser, onLogout }) {
  const navItems = [
    { id: 'campaigns', label: 'Quản lý Chiến dịch', icon: FolderKanban, badge: 'CAM-01' },
    { id: 'brand_rules', label: 'Quy tắc Thương hiệu', icon: ShieldCheck, badge: 'BRD-02' },
    { id: 'studio_canvas', label: 'Studio Split-Canvas', icon: SplitSquareVertical, badge: 'LIVE AI' },
    { id: 'calendar', label: 'Lịch Phát sóng & Duyệt', icon: CalendarClock, badge: '48 Posts' },
    { id: 'admin', label: 'Admin Quản trị Hệ thống', icon: Settings2, badge: 'v4.1' },
  ];

  return (
    <aside className="w-72 bg-[#283044] text-white h-screen flex flex-col justify-between shrink-0 border-r border-slate-700/50 shadow-xl select-none">
      {/* Brand Top Header */}
      <div>
        <div className="p-6 border-b border-white/10 flex items-center justify-between">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActivePage('campaigns')}>
            <div className="w-10 h-10 rounded-xl bg-[#4F46E5] flex items-center justify-center shadow-lg shadow-indigo-500/30">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-base font-extrabold tracking-tight text-white leading-none">AuraAI</h1>
              <span className="text-[10px] font-mono tracking-widest text-[#D2D9F4] uppercase font-semibold">ENTERPRISE OS</span>
            </div>
          </div>
          <span className="px-2 py-0.5 rounded-full bg-[#6FFBBE]/15 text-[#6FFBBE] text-[10px] font-mono font-bold border border-[#6FFBBE]/30">
            PRO
          </span>
        </div>

        {/* User Card */}
        <div className="p-4 mx-3 my-4 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center font-bold text-white text-sm shadow-md">
              {currentUser?.name ? currentUser.name[0].toUpperCase() : 'A'}
            </div>
            <div>
              <div className="text-xs font-bold text-white leading-tight">{currentUser?.name || 'Nguyễn Nhật Minh'}</div>
              <div className="text-[10px] text-[#6FFBBE] font-mono font-semibold flex items-center gap-1 mt-0.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#6FFBBE]" />
                {currentUser?.role || 'System Admin'}
              </div>
            </div>
          </div>
          <button 
            onClick={onLogout}
            title="Đăng xuất"
            className="p-1.5 text-slate-400 hover:text-white hover:bg-white/10 rounded-lg transition"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>

        {/* Navigation Section */}
        <div className="px-3 space-y-1">
          <div className="px-3 pb-2 text-[10px] font-mono font-bold tracking-wider text-slate-400 uppercase">
            WORKSPACE NAVIGATION
          </div>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive 
                    ? 'bg-[#4F46E5] text-white shadow-lg shadow-indigo-600/30 font-bold' 
                    : 'text-slate-300 hover:bg-white/5 hover:text-white'
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </div>
                <span className={`text-[10px] font-mono px-2 py-0.5 rounded-md ${
                  isActive ? 'bg-white/20 text-white' : 'bg-black/20 text-slate-400'
                }`}>
                  {item.badge}
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* System Status Footer */}
      <div className="p-4 m-3 rounded-xl bg-black/20 border border-white/5 text-[11px] font-mono space-y-2">
        <div className="flex items-center justify-between text-slate-300">
          <span className="flex items-center gap-1.5">
            <Database className="w-3.5 h-3.5 text-indigo-400" />
            PostgreSQL 18
          </span>
          <span className="text-[#6FFBBE] font-bold">READY</span>
        </div>
        <div className="flex items-center justify-between text-slate-300">
          <span className="flex items-center gap-1.5">
            <Activity className="w-3.5 h-3.5 text-emerald-400" />
            3-Agent Matrix
          </span>
          <span className="text-indigo-300 font-bold">ONLINE</span>
        </div>
        <div className="pt-2 border-t border-white/10 text-[10px] text-slate-400 text-center">
          AuraAI Engine v4.8 • Enterprise
        </div>
      </div>
    </aside>
  );
}

