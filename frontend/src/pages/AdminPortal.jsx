import React, { useState } from 'react';
import { 
  Settings, 
  Key, 
  Users, 
  Database, 
  Activity, 
  Cpu, 
  RefreshCw, 
  Save, 
  Lock,
  Plus,
  Trash2,
  Check,
  Search,
  ShieldCheck,
  FileSpreadsheet,
  AlertCircle,
  ExternalLink,
  Sliders,
  CheckCircle2
} from 'lucide-react';

export default function AdminPortal() {
  const [activeTab, setActiveTab] = useState('users');
  const [apiKeySaved, setApiKeySaved] = useState(false);
  const [cacheCleared, setCacheCleared] = useState(false);
  const [showAddUserModal, setShowAddUserModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // Form states
  const [geminiKey, setGeminiKey] = useState('AIzaSyD_MOCK_GEMINI_API_KEY_SECURE_MASKED');
  const [fbPageId, setFbPageId] = useState('104829104812345');
  const [fbToken, setFbToken] = useState('EAAGm0PX4ZB9...long_lived_token_meta_2026');
  const [tiktokSecret, setTiktokSecret] = useState('tt_sec_89f029410adfe81923');

  const [users, setUsers] = useState([
    { id: 1, initials: 'NM', username: 'admin', name: 'Nguyễn Nhật Minh', role: 'System Admin', email: 'minh.admin@aura.ai', status: 'Active', last_login: '14:20 Hôm nay', two_fa: true },
    { id: 2, initials: 'NH', username: 'nhan', name: 'Nhan Tran', role: 'Marketing Lead', email: 'nhan_2251220268@dau.edu.vn', status: 'Active', last_login: '14:28 Hôm nay', two_fa: true },
    { id: 3, initials: 'LN', username: 'nam.creator', name: 'Lê Hoàng Nam', role: 'Content Creator', email: 'nam.creator@aura.ai', status: 'Active', last_login: 'Hôm qua', two_fa: true },
    { id: 4, initials: 'TA', username: 'anh.reviewer', name: 'Trần Quỳnh Anh', role: 'Compliance Auditor', email: 'anh.auditor@aura.ai', status: 'Active', last_login: '3 ngày trước', two_fa: false }
  ]);

  const [newUser, setNewUser] = useState({
    username: '',
    name: '',
    email: '',
    role: 'Content Creator'
  });

  const handleSaveKeys = (e) => {
    e.preventDefault();
    setApiKeySaved(true);
    setTimeout(() => setApiKeySaved(false), 3000);
  };

  const handleClearCache = () => {
    setCacheCleared(true);
    setTimeout(() => setCacheCleared(false), 2500);
  };

  const handleAddUser = (e) => {
    e.preventDefault();
    if (!newUser.username.trim() || !newUser.name.trim()) return;

    const initials = newUser.name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() || 'US';

    setUsers([
      ...users,
      {
        id: Date.now(),
        initials,
        username: newUser.username,
        name: newUser.name,
        email: newUser.email || `${newUser.username}@aura.ai`,
        role: newUser.role,
        status: 'Active',
        last_login: 'Vừa tạo',
        two_fa: true
      }
    ]);
    setShowAddUserModal(false);
    setNewUser({ username: '', name: '', email: '', role: 'Content Creator' });
  };

  const handleDeleteUser = (id) => {
    setUsers(users.filter(u => u.id !== id));
  };

  const filteredUsers = users.filter(u => 
    u.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.role.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      
      {/* ------------------------------------------------------------ */}
      {/* SCREEN HEADER WITH METADATA & GLOBAL TRIGGERS                */}
      {/* ------------------------------------------------------------ */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3 border-b border-slate-200/80">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-[#3525CD] font-bold uppercase tracking-wider mb-1">
            <span>SRS-FR-ADM · v4.1</span>
            <span className="w-1.5 h-1.5 rounded-full bg-slate-300" />
            <span className="text-slate-500 font-normal">HLD: ui/pages/6_admin.py</span>
          </div>
          <div className="flex items-baseline gap-3">
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
              Hệ Thống Quản Trị & System Governance
            </h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Giám sát tài nguyên suy luận LLM, bảo mật phân quyền RBAC đa cấp, và quản lý chuỗi kết nối lưu trữ tập trung.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button 
            onClick={handleClearCache}
            className="inline-flex items-center gap-1.5 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 px-3.5 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-slate-500 ${cacheCleared ? 'animate-spin' : ''}`} />
            <span>{cacheCleared ? 'Đã xóa Cache thành công ✓' : 'Xóa Bộ Nhớ Cache'}</span>
          </button>

          <button 
            onClick={() => {
              const headers = 'ID,Tên,Username,Vai trò,Email,Trạng thái,2FA\n';
              const rows = users.map(u => `"${u.id}","${u.name}","${u.username}","${u.role}","${u.email}","${u.status}","${u.two_fa ? 'Bật' : 'Tắt'}"`).join('\n');
              const blob = new Blob([headers + rows], { type: 'text/csv;charset=utf-8;' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = `AuraAI_System_Audit_${new Date().toISOString().slice(0, 10)}.csv`;
              a.click();
            }}
            className="inline-flex items-center gap-1.5 bg-[#3525CD] hover:bg-indigo-800 text-white px-3.5 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition active:scale-95"
          >
            <FileSpreadsheet className="w-3.5 h-3.5" />
            <span>Export System Audit (.xlsx)</span>
          </button>
        </div>
      </div>

      {/* ------------------------------------------------------------ */}
      {/* TOP KPI STATS (4 CARDS)                                      */}
      {/* ------------------------------------------------------------ */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Stat 1: System Health */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-2xs space-y-2">
          <div className="flex items-center justify-between text-xs font-mono font-bold text-slate-400 uppercase">
            <span>SYSTEM HEALTH SLA</span>
            <span className="w-6 h-6 rounded-md bg-emerald-100 text-emerald-700 flex items-center justify-center">
              <Activity className="w-3.5 h-3.5" />
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-slate-900 tracking-tight">99.98%</span>
            <span className="text-xs font-mono font-bold text-emerald-600">Operational</span>
          </div>
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-1 border-t border-slate-100">
            <span className="flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> All 14 Microservices UP
            </span>
            <span className="text-emerald-700 font-bold">0 Outages</span>
          </div>
        </div>

        {/* Stat 2: LLM Tokens */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-2xs space-y-2">
          <div className="flex items-center justify-between text-xs font-mono font-bold text-slate-400 uppercase">
            <span>TOTAL LLM TOKENS USED</span>
            <span className="w-6 h-6 rounded-md bg-indigo-100 text-[#3525CD] flex items-center justify-center">
              <Cpu className="w-3.5 h-3.5" />
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-slate-900 tracking-tight">4.82M</span>
            <span className="text-xs font-mono font-bold text-[#3525CD]">($142.80)</span>
          </div>
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-1 border-t border-slate-100">
            <span>Budget Cap: $500.00</span>
            <span className="text-indigo-600 font-bold">28.5% quota</span>
          </div>
        </div>

        {/* Stat 3: Active Users */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-2xs space-y-2">
          <div className="flex items-center justify-between text-xs font-mono font-bold text-slate-400 uppercase">
            <span>ACTIVE USERS (LIVE)</span>
            <span className="w-6 h-6 rounded-md bg-cyan-100 text-cyan-800 flex items-center justify-center">
              <Users className="w-3.5 h-3.5" />
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-black text-slate-900 tracking-tight">18</span>
            <span className="text-xs font-mono text-slate-400 font-bold">/ 24 Seats</span>
          </div>
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-1 border-t border-slate-100">
            <span>Marketing Managers</span>
            <span className="text-emerald-700 font-bold">100% 2FA</span>
          </div>
        </div>

        {/* Stat 4: Connected DB */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-2xs space-y-2">
          <div className="flex items-center justify-between text-xs font-mono font-bold text-slate-400 uppercase">
            <span>CONNECTED DATABASE</span>
            <span className="w-6 h-6 rounded-md bg-purple-100 text-purple-700 flex items-center justify-center">
              <Database className="w-3.5 h-3.5" />
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-black text-slate-900 tracking-tight">PostgreSQL 16</span>
          </div>
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-1 border-t border-slate-100">
            <span className="flex items-center gap-1 text-emerald-600 font-bold">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> Connected
            </span>
            <span>Latency: 22ms</span>
          </div>
        </div>

      </div>

      {/* ------------------------------------------------------------ */}
      {/* SECTION TABS                                                 */}
      {/* ------------------------------------------------------------ */}
      <div className="bg-white p-1.5 rounded-xl border border-slate-200/90 shadow-2xs flex items-center gap-1.5 w-fit">
        <button
          onClick={() => setActiveTab('users')}
          className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition ${
            activeTab === 'users' ? 'bg-[#4F46E5] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Users className="w-3.5 h-3.5" />
          <span>Quản lý Tài Khoản & RBAC ({users.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('keys')}
          className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition ${
            activeTab === 'keys' ? 'bg-[#4F46E5] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Key className="w-3.5 h-3.5" />
          <span>Cấu hình API Keys & Kênh Mạng Xã Hội</span>
        </button>

        <button
          onClick={() => setActiveTab('db')}
          className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition ${
            activeTab === 'db' ? 'bg-[#4F46E5] text-white shadow-xs' : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          <Database className="w-3.5 h-3.5" />
          <span>Giám Sát Cơ Sở Dữ Liệu</span>
        </button>
      </div>

      {/* ------------------------------------------------------------ */}
      {/* TAB 1: USER MANAGEMENT (RBAC TABLE)                          */}
      {/* ------------------------------------------------------------ */}
      {activeTab === 'users' && (
        <div className="bg-white rounded-2xl border border-slate-200/90 shadow-2xs p-6 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div>
              <h3 className="font-bold text-base text-slate-900">
                1. Quản Lý Tài Khoản & Phân Quyền
              </h3>
              <p className="text-xs text-slate-500">
                Ma trận kiểm soát quyền truy cập RBAC (Marketing Manager, Admin, Content Creator) & phiên hoạt động.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <div className="relative">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Tìm theo tên, email hoặc vai trò..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-8 pr-3 py-1.5 bg-[#F2F3FF] border border-transparent rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-400 focus:bg-white transition w-60"
                />
              </div>

              <button 
                onClick={() => setShowAddUserModal(true)}
                className="inline-flex items-center gap-1.5 bg-[#3525CD] hover:bg-indigo-800 text-white px-3.5 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition active:scale-95"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>Thêm Thành Viên</span>
              </button>
            </div>
          </div>

          {/* User Table */}
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="bg-[#F2F3FF] text-[#464555] font-mono text-[11px] font-bold uppercase rounded-lg">
                  <th className="py-2.5 px-3 rounded-l-lg">NHÂN VIÊN / USER</th>
                  <th className="py-2.5 px-3">VAI TRÒ (ROLE)</th>
                  <th className="py-2.5 px-3">TRẠNG THÁI</th>
                  <th className="py-2.5 px-3">ĐĂNG NHẬP GẦN NHẤT</th>
                  <th className="py-2.5 px-3">BẢO MẬT 2FA</th>
                  <th className="py-2.5 px-3 text-right rounded-r-lg">THAO TÁC</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredUsers.map(u => (
                  <tr key={u.id} className="hover:bg-slate-50 transition font-medium">
                    <td className="py-3 px-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-xl bg-[#4F46E5] text-white flex items-center justify-center font-mono font-bold text-xs shadow-2xs">
                          {u.initials}
                        </div>
                        <div>
                          <div className="font-bold text-slate-900">{u.name}</div>
                          <div className="text-[11px] text-slate-400 font-mono">{u.email}</div>
                        </div>
                      </div>
                    </td>

                    <td className="py-3 px-3">
                      <span className={`px-2.5 py-1 rounded-md font-mono text-[10px] font-bold ${
                        u.role === 'System Admin' 
                          ? 'bg-purple-100 text-purple-800' 
                          : u.role === 'Marketing Lead'
                          ? 'bg-indigo-100 text-indigo-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}>
                        {u.role}
                      </span>
                    </td>

                    <td className="py-3 px-3">
                      <span className="text-emerald-700 font-bold flex items-center gap-1.5 text-xs">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                        {u.status}
                      </span>
                    </td>

                    <td className="py-3 px-3 text-slate-600 font-mono text-[11px]">
                      {u.last_login}
                    </td>

                    <td className="py-3 px-3 font-mono text-[11px]">
                      {u.two_fa ? (
                        <span className="text-emerald-700 font-bold flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Bật
                        </span>
                      ) : (
                        <span className="text-slate-400 flex items-center gap-1">
                          Chưa kích hoạt
                        </span>
                      )}
                    </td>

                    <td className="py-3 px-3 text-right">
                      {u.username !== 'admin' && (
                        <button 
                          onClick={() => handleDeleteUser(u.id)}
                          className="text-slate-400 hover:text-red-600 p-1.5 rounded-lg hover:bg-red-50 transition"
                          title="Xóa thành viên"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------ */}
      {/* TAB 2: API KEYS & CHANNELS CONFIGURATION                     */}
      {/* ------------------------------------------------------------ */}
      {activeTab === 'keys' && (
        <div className="bg-white rounded-2xl border border-slate-200/90 shadow-2xs p-6 space-y-5">
          <div>
            <h3 className="font-bold text-base text-slate-900">
              2. Quản Trị Khóa API & Kết Nối Kênh Phân Phối
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Các khóa kỹ thuật được mã hóa an toàn và tự động đồng bộ cùng hệ thống kiểm duyệt Compliance Guard.
            </p>
          </div>

          <form onSubmit={handleSaveKeys} className="space-y-4 max-w-2xl text-xs">
            
            {/* Gemini API Key */}
            <div className="space-y-1">
              <label className="font-bold text-slate-800 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-indigo-600" />
                <span>Google Gemini 1.5 Pro API Key (AuraOmni Neural Engine)</span>
              </label>
              <input 
                type="password"
                value={geminiKey}
                onChange={(e) => setGeminiKey(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl font-mono text-xs text-slate-900 focus:outline-none focus:border-indigo-500"
              />
              <span className="text-[10px] text-slate-400 font-mono">Tự động xoay khóa định kỳ 30 ngày một lần</span>
            </div>

            {/* Facebook Meta Page ID & Token */}
            <div className="grid grid-cols-2 gap-3">
              <div className="space-y-1">
                <label className="font-bold text-slate-800">Facebook Meta Page ID</label>
                <input 
                  type="text"
                  value={fbPageId}
                  onChange={(e) => setFbPageId(e.target.value)}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl font-mono text-xs text-slate-900 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="space-y-1">
                <label className="font-bold text-slate-800">TikTok Marketing API Secret</label>
                <input 
                  type="password"
                  value={tiktokSecret}
                  onChange={(e) => setTiktokSecret(e.target.value)}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl font-mono text-xs text-slate-900 focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="font-bold text-slate-800">Meta Graph API Long-Lived Token</label>
              <textarea 
                rows="2"
                value={fbToken}
                onChange={(e) => setFbToken(e.target.value)}
                className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl font-mono text-xs text-slate-900 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="pt-2 flex items-center justify-between">
              <button 
                type="submit"
                className="inline-flex items-center gap-1.5 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-5 py-2.5 rounded-xl font-bold text-xs shadow-md shadow-indigo-500/20 transition active:scale-95"
              >
                <Save className="w-3.5 h-3.5" />
                <span>Lưu & Kiểm Tra Kết Nối</span>
              </button>

              {apiKeySaved && (
                <div className="text-emerald-700 font-bold flex items-center gap-1 text-xs">
                  <Check className="w-4 h-4" /> Đã cập nhật thành công khóa API và xác thực token!
                </div>
              )}
            </div>

          </form>
        </div>
      )}

      {/* ------------------------------------------------------------ */}
      {/* TAB 3: DATABASE & CACHE MONITORING                           */}
      {/* ------------------------------------------------------------ */}
      {activeTab === 'db' && (
        <div className="bg-white rounded-2xl border border-slate-200/90 shadow-2xs p-6 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div>
              <h3 className="font-bold text-base text-slate-900">
                3. Trạng Thái Kết Nối Cơ Sở Dữ Liệu & Pool Tài Nguyên
              </h3>
              <p className="text-xs text-slate-500">Giám sát hiệu năng Postgres/SQLite và tình trạng bộ nhớ đệm redis.</p>
            </div>
            <span className="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 font-mono font-bold text-xs">
              Pool Healthy
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs font-mono">
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="text-slate-400 text-[10px] uppercase">URI KẾT NỐI CHÍNH</span>
              <div className="font-bold text-slate-800 truncate">postgresql://aura_admin:***@localhost:5432/aura_db</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="text-slate-400 text-[10px] uppercase">ACTIVE CONNECTIONS</span>
              <div className="font-bold text-emerald-600 text-base">15 / 100 Connections</div>
            </div>
            <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1">
              <span className="text-slate-400 text-[10px] uppercase">CACHE HIT RATIO</span>
              <div className="font-bold text-indigo-600 text-base">98.7% (Redis In-Memory)</div>
            </div>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------ */}
      {/* ADD USER MODAL                                               */}
      {/* ------------------------------------------------------------ */}
      {showAddUserModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl border border-slate-100">
            <div className="flex justify-between items-center pb-2 border-b">
              <h3 className="font-bold text-base text-slate-900">Thêm Thành Viên Mới</h3>
              <button onClick={() => setShowAddUserModal(false)} className="text-slate-400 hover:text-slate-600 font-bold">✕</button>
            </div>

            <form onSubmit={handleAddUser} className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Tên đầy đủ *</label>
                <input 
                  type="text" 
                  required
                  placeholder="Ví dụ: Hoàng Tuấn Anh" 
                  value={newUser.name}
                  onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                  className="w-full p-2.5 border rounded-xl focus:outline-none focus:border-indigo-500" 
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Tên đăng nhập (Username) *</label>
                <input 
                  type="text" 
                  required
                  placeholder="Ví dụ: anh.creator" 
                  value={newUser.username}
                  onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                  className="w-full p-2.5 border rounded-xl focus:outline-none focus:border-indigo-500 font-mono" 
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Email</label>
                <input 
                  type="email" 
                  placeholder="anh.creator@aura.ai" 
                  value={newUser.email}
                  onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                  className="w-full p-2.5 border rounded-xl focus:outline-none focus:border-indigo-500 font-mono" 
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Vai trò (Role)</label>
                <select 
                  value={newUser.role}
                  onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                  className="w-full p-2.5 border rounded-xl font-semibold text-slate-800 focus:outline-none focus:border-indigo-500"
                >
                  <option value="Content Creator">Content Creator</option>
                  <option value="Marketing Lead">Marketing Lead</option>
                  <option value="Compliance Auditor">Compliance Auditor</option>
                  <option value="System Admin">System Admin</option>
                </select>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <button type="button" onClick={() => setShowAddUserModal(false)} className="px-4 py-2 border rounded-xl text-slate-600 font-bold">Hủy</button>
                <button type="submit" className="px-4 py-2 bg-[#4F46E5] text-white rounded-xl font-bold shadow-md shadow-indigo-500/20">Thêm ngay</button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
