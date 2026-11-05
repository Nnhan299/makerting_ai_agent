import React, { useState, useEffect } from 'react';
import { 
  Sparkles, 
  ChevronDown, 
  User, 
  CheckCircle2, 
  Plus,
  ShieldCheck,
  Settings,
  Database
} from 'lucide-react';

import StudioCanvas from './pages/StudioCanvas';
import Campaigns from './pages/Campaigns';
import BrandRules from './pages/BrandRules';
import CalendarReview from './pages/CalendarReview';
import AdminPortal from './pages/AdminPortal';

import { 
  fetchHealth, 
  fetchCampaigns, 
  fetchPosts, 
  createCampaignApi, 
  deleteCampaignApi,
  updatePostApi 
} from './api';

export default function App() {
  const [activeNav, setActiveNav] = useState('AI Pipeline');
  const [isApproved, setIsApproved] = useState(false);
  const [projectDropdownOpen, setProjectDropdownOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const [dbInfo, setDbInfo] = useState({ engine: 'PostgreSQL 16', status: 'connected', latency_ms: 22 });

  // Global campaigns list (initially fallback, then populated from DB)
  const [campaigns, setCampaigns] = useState([
    {
      id: 1,
      sku: 'CAM-2026-PG01',
      name: 'Serum PureGlow 2026',
      product_name: 'Serum Niacinamide + Zinc Duo',
      target_audience: 'Gen Z Skincare • Độ tuổi: 18 - 25',
      budget: '$15,000 USD',
      status: 'In-Progress',
      compliance_rate: 98.4,
      posts_count: 12,
      channels: ['TikTok', 'Instagram', 'Facebook'],
      start_date: '2026-10-10',
      end_date: '2026-11-10'
    },
    {
      id: 2,
      sku: 'CAM-2026-RT02',
      name: 'Kem Dưỡng Retinol Phục Hồi 2026',
      product_name: 'Kem Dưỡng Retinol 0.5% + Peptide',
      target_audience: 'Phụ nữ 25 - 40 • Chống lão hóa & Nếp nhăn',
      budget: '$12,500 USD',
      status: 'Approved',
      compliance_rate: 99.1,
      posts_count: 8,
      channels: ['Facebook', 'Instagram'],
      start_date: '2026-11-01',
      end_date: '2026-12-01'
    },
    {
      id: 3,
      sku: 'CAM-2026-MC03',
      name: 'Tẩy Trang Dịu Nhẹ Micellar Pure',
      product_name: 'Nước Tẩy Trang Cúc La Mã',
      target_audience: 'Học sinh, sinh viên 16 - 24 • Da mụn nhạy cảm',
      budget: '$8,000 USD',
      status: 'Draft',
      compliance_rate: 94.0,
      posts_count: 6,
      channels: ['TikTok', 'Instagram'],
      start_date: '2026-11-15',
      end_date: '2026-12-15'
    }
  ]);

  const [currentCampaign, setCurrentCampaign] = useState(campaigns[0]);

  // Global posts list
  const [posts, setPosts] = useState([
    {
      id: 1,
      day: 13,
      date_str: 'Thứ Ba, 13/10/2026',
      title: 'Đánh thức làn da căng bóng chuẩn thủy tinh chỉ sau 14 ngày',
      hook: '#SecretDrop: 3 giọt tinh chất phục hồi màng ẩm',
      stage: 'Teaser',
      channel: 'TikTok',
      status: 'Approved',
      compliance_score: 98,
      scheduled_time: '19:30',
      media_url: 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&auto=format&fit=crop&q=80',
      copy: 'Đánh thức làn da căng bóng chuẩn thủy tinh chỉ sau 14 ngày cùng Siêu Tinh Chất Phục Hồi PureGlow Serum 2026! Công thức Niacinamide 10% kết hợp Ceramide tinh khiết giúp củng cố hàng rào ẩm tự nhiên.'
    },
    {
      id: 2,
      day: 14,
      date_str: 'Thứ Tư, 14/10/2026',
      title: 'Hé lộ thành phần Niacinamide 10% + Zinc Duo',
      hook: 'Khoa học làn da: Tại sao Ceramide là chìa khóa phục hồi?',
      stage: 'Teaser',
      channel: 'Facebook',
      status: 'Approved',
      compliance_score: 95,
      scheduled_time: '20:00',
      media_url: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600&auto=format&fit=crop&q=80',
      copy: 'Thời tiết giao mùa khiến da bạn khô ráp, mẩn đỏ và căng rát? Đừng bỏ qua những tín hiệu cảnh báo này. Cùng PureGlow khám phá công thức cấp ẩm đa tầng.'
    },
    {
      id: 3,
      day: 15,
      date_str: 'Thứ Năm, 15/10/2026',
      title: 'Serum Glow & Kháng Viêm Dịu Nhẹ Cho Da Nhạy Cảm',
      hook: 'Chất serum mỏng nhẹ thấm sâu không bết dính',
      stage: 'Teaser',
      channel: 'TikTok',
      status: 'Pending',
      compliance_score: 92,
      scheduled_time: '18:45',
      media_url: 'https://images.unsplash.com/photo-1512290900672-1f41e57c66d8?w=600&auto=format&fit=crop&q=80',
      copy: 'Da nhạy cảm cần sự chăm sóc đặc biệt. Trải nghiệm cảm giác nhẹ tênh ngay sau khi thoa với công nghệ Micro-Drop độc quyền.'
    },
    {
      id: 4,
      day: 16,
      date_str: 'Thứ Sáu, 16/10/2026',
      title: 'Carousel: Routine 7 ngày phục hồi màng ẩm chuyên sâu',
      hook: '4 Bước chuẩn y khoa từ chuyên gia da liễu',
      stage: 'Launch',
      channel: 'Instagram',
      status: 'Approved',
      compliance_score: 98,
      scheduled_time: '12:00',
      media_url: 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&auto=format&fit=crop&q=80',
      copy: 'Khám phá bí mật phức hợp B5 + HA Nano đa tầng. Serum PureGlow mang lại hiệu quả thẩm thấu sâu đến tầng trung bì.'
    },
    {
      id: 5,
      day: 17,
      date_str: 'Thứ Bảy, 17/10/2026',
      title: 'KOC Unboxing Box Quà Hạn Giờ 100 Suất Ra Mắt',
      hook: 'Ưu đãi đặc biệt mở bán tuần lễ vàng',
      stage: 'Launch',
      channel: 'TikTok',
      status: 'Approved',
      compliance_score: 96,
      scheduled_time: '20:15',
      media_url: 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600&auto=format&fit=crop&q=80',
      copy: 'Chỉ còn 48H: Nhận ngay quà tặng trải nghiệm giới hạn cho 100 đơn hàng đầu tiên trong tuần lễ ra mắt chính thức!'
    }
  ]);

  // Load live data from PostgreSQL / SQLite on mount
  useEffect(() => {
    async function loadData() {
      // 1. Health check
      const health = await fetchHealth();
      if (health) {
        setDbInfo({
          engine: health.engine || (health.is_postgres ? 'PostgreSQL 16' : 'SQLite 3 Fallback'),
          status: health.status || 'connected',
          latency_ms: health.latency_ms || 22
        });
      }

      // 2. Fetch live campaigns
      const remoteCamps = await fetchCampaigns();
      if (remoteCamps && remoteCamps.length > 0) {
        setCampaigns(remoteCamps);
        // Find PureGlow or first
        const pg = remoteCamps.find(c => c.name.includes('PureGlow')) || remoteCamps[0];
        setCurrentCampaign(pg);
      }

      // 3. Fetch live posts
      const remotePosts = await fetchPosts();
      if (remotePosts && remotePosts.length > 0) {
        setPosts(remotePosts.map((p, idx) => ({
          ...p,
          day: 13 + (idx % 6),
          date_str: `Ngày ${p.scheduled_date || '2026-10-15'}`
        })));
      }
    }

    loadData();
  }, []);

  const handleApprovePost = async () => {
    setIsApproved(true);
    // Sync approval to DB
    const firstPost = posts[0];
    if (firstPost && firstPost.id) {
      await updatePostApi(firstPost.id, { status: 'Approved' });
    }
    // Update local state
    setPosts(prev => prev.map((p, idx) => idx === 0 ? { ...p, status: 'Approved', compliance_score: 98 } : p));
  };

  const handleCreateCampaign = async (newCampData) => {
    const res = await createCampaignApi({
      name: newCampData.name,
      product_name: newCampData.product_name || newCampData.name,
      target_audience: newCampData.target_audience || '',
      budget: newCampData.budget || '$15,000 USD',
      channels: Array.isArray(newCampData.channels) ? newCampData.channels.join(', ') : newCampData.channels,
      start_date: newCampData.start_date,
      end_date: newCampData.end_date
    });

    // Refresh campaigns from DB
    const updated = await fetchCampaigns();
    if (updated && updated.length > 0) {
      setCampaigns(updated);
    }
    return res;
  };

  const handleDeleteCampaign = async (id) => {
    await deleteCampaignApi(id);
    const updated = await fetchCampaigns();
    if (updated) {
      setCampaigns(updated);
      if (currentCampaign.id === id && updated.length > 0) {
        setCurrentCampaign(updated[0]);
      }
    }
  };

  return (
    <div className="min-h-screen bg-[#F4F6FB] text-slate-800 font-sans flex flex-col justify-between selection:bg-indigo-500 selection:text-white">
      
      {/* ============================================================ */}
      {/* 1. TOP NAVIGATION STUDIO HEADER                              */}
      {/* ============================================================ */}
      <header className="bg-white border-b border-slate-200/80 px-5 py-2.5 flex items-center justify-between sticky top-0 z-40 shadow-xs">
        
        {/* Left: Brand Logo & Project Dropdown */}
        <div className="flex items-center gap-3">
          <div 
            onClick={() => setActiveNav('AI Pipeline')}
            className="flex items-center gap-2 bg-[#4F46E5] text-white px-3 py-1.5 rounded-xl font-extrabold text-sm shadow-sm shadow-indigo-500/20 cursor-pointer select-none"
          >
            <Sparkles className="w-4 h-4 fill-white" />
            <span>AuraAI</span>
          </div>

          {/* Project Switcher Dropdown */}
          <div className="relative">
            <button
              onClick={() => setProjectDropdownOpen(!projectDropdownOpen)}
              className="flex items-center gap-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-xl text-xs font-semibold text-slate-700 cursor-pointer transition select-none"
            >
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>{currentCampaign?.name || 'Serum PureGlow 2026'}</span>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
            </button>

            {/* Dropdown Menu */}
            {projectDropdownOpen && (
              <div className="absolute left-0 top-full mt-1.5 w-72 bg-white rounded-2xl shadow-xl border border-slate-200 p-2 z-50 animate-in fade-in zoom-in-95">
                <div className="text-[10px] font-mono text-slate-400 font-bold uppercase px-3 py-1 flex justify-between items-center">
                  <span>DỰ ÁN TỪ DATABASE</span>
                  <span className="text-emerald-600 font-bold">● {(dbInfo?.engine || 'PostgreSQL 16').split(' ')[0]}</span>
                </div>
                <div className="space-y-1">
                  {campaigns.map(camp => (
                    <button
                      key={camp.id}
                      onClick={() => {
                        setCurrentCampaign(camp);
                        setProjectDropdownOpen(false);
                      }}
                      className={`w-full text-left px-3 py-2 rounded-xl text-xs font-semibold flex items-center justify-between transition ${
                        currentCampaign?.id === camp.id 
                          ? 'bg-[#EBF2FF] text-[#2563EB]' 
                          : 'text-slate-700 hover:bg-slate-50'
                      }`}
                    >
                      <span className="truncate">{camp.name}</span>
                      <span className="text-[10px] font-mono text-slate-400">{camp.status}</span>
                    </button>
                  ))}
                </div>
                <div className="border-t border-slate-100 mt-1 pt-1">
                  <button
                    onClick={() => {
                      setProjectDropdownOpen(false);
                      setActiveNav('Campaigns');
                    }}
                    className="w-full text-left px-3 py-1.5 rounded-xl text-xs font-bold text-[#4F46E5] hover:bg-indigo-50 flex items-center gap-1.5 transition"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>Quản lý tất cả chiến dịch...</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Center: Module Navigation Tabs */}
        <nav className="flex items-center gap-1">
          {['Campaigns', 'Brand Rules', 'AI Pipeline', 'Calendar & Review', 'Admin & System'].map((tab) => {
            const isActive = activeNav === tab;
            return (
              <button
                key={tab}
                onClick={() => setActiveNav(tab)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition select-none ${
                  isActive 
                    ? 'bg-[#EBF2FF] text-[#2563EB]' 
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/70'
                }`}
              >
                {tab}
              </button>
            );
          })}
        </nav>

        {/* Right: Pipeline Active Status & User Profile Avatar */}
        <div className="flex items-center gap-3">
          {/* Real Database Sync Badge */}
          <div 
            className="flex items-center gap-1.5 bg-emerald-50 border border-emerald-200/80 px-3 py-1 rounded-full text-[11px] font-semibold text-emerald-700 select-none cursor-pointer"
            title={`Đang đồng bộ trực tiếp với ${dbInfo?.engine || 'PostgreSQL 16'} (Độ trễ: ${dbInfo?.latency_ms || 22}ms)`}
          >
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            <span>AI Pipeline Active • {(dbInfo?.engine || 'PostgreSQL 16').split(' ')[0]}</span>
          </div>

          <div className="relative">
            <button 
              onClick={() => setUserDropdownOpen(!userDropdownOpen)}
              className="w-8 h-8 rounded-full bg-[#4F46E5] flex items-center justify-center text-white shadow-sm cursor-pointer hover:ring-2 hover:ring-indigo-300 transition"
              title="Tài khoản Nhan Tran (nhan_2251220268@dau.edu.vn)"
            >
              <User className="w-4 h-4" />
            </button>

            {/* User Dropdown */}
            {userDropdownOpen && (
              <div className="absolute right-0 top-full mt-2 w-64 bg-white rounded-2xl shadow-xl border border-slate-200 p-3 z-50 text-xs animate-in fade-in zoom-in-95">
                <div className="pb-2 border-b border-slate-100">
                  <div className="font-bold text-slate-900">Nhan Tran</div>
                  <div className="text-[11px] text-slate-400 font-mono">nhan_2251220268@dau.edu.vn</div>
                  <span className="inline-block mt-1 px-2 py-0.5 rounded-md bg-indigo-50 text-indigo-700 font-mono font-bold text-[10px]">
                    Marketing Lead
                  </span>
                </div>
                <div className="py-1 space-y-1">
                  <div className="px-2 py-1.5 text-slate-600 font-mono text-[11px] flex items-center justify-between">
                    <span>Database:</span>
                    <strong className="text-emerald-700 font-bold">{dbInfo.engine}</strong>
                  </div>
                  <button 
                    onClick={() => {
                      setUserDropdownOpen(false);
                      setActiveNav('Admin & System');
                    }}
                    className="w-full text-left px-2 py-1.5 rounded-lg hover:bg-slate-50 flex items-center gap-2 text-slate-700"
                  >
                    <Settings className="w-3.5 h-3.5 text-slate-400" />
                    <span>Cấu hình hệ thống</span>
                  </button>
                  <button 
                    onClick={() => {
                      setUserDropdownOpen(false);
                      setActiveNav('Brand Rules');
                    }}
                    className="w-full text-left px-2 py-1.5 rounded-lg hover:bg-slate-50 flex items-center gap-2 text-slate-700"
                  >
                    <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
                    <span>Quy tắc thương hiệu</span>
                  </button>
                </div>
                <div className="pt-1 border-t border-slate-100">
                  <button 
                    onClick={() => setUserDropdownOpen(false)}
                    className="w-full text-left px-2 py-1.5 rounded-lg text-emerald-600 font-bold flex items-center gap-2"
                  >
                    <span className="w-2 h-2 rounded-full bg-emerald-500" />
                    <span>DB Connection: 22ms</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

      </header>

      {/* ============================================================ */}
      {/* 2. DYNAMIC WORKSPACE BODY BASED ON ACTIVE NAV TAB            */}
      {/* ============================================================ */}
      <main className="flex-1 p-4 lg:p-5 max-w-[1700px] w-full mx-auto">
        
        {activeNav === 'AI Pipeline' && (
          <StudioCanvas 
            currentCampaign={currentCampaign} 
            onApprovePost={handleApprovePost}
            isApproved={isApproved}
            setIsApproved={setIsApproved}
            onNavigateToCalendar={() => setActiveNav('Calendar & Review')}
          />
        )}

        {activeNav === 'Campaigns' && (
          <Campaigns 
            campaigns={campaigns}
            setCampaigns={setCampaigns}
            onSelectCampaign={(camp) => {
              setCurrentCampaign(camp);
            }}
            onNavigateToStudio={() => setActiveNav('AI Pipeline')}
            onNavigateToCalendar={() => setActiveNav('Calendar & Review')}
            onApiCreate={handleCreateCampaign}
            onApiDelete={handleDeleteCampaign}
          />
        )}

        {activeNav === 'Brand Rules' && (
          <BrandRules />
        )}

        {activeNav === 'Calendar & Review' && (
          <CalendarReview 
            posts={posts}
            setPosts={setPosts}
            onNavigateToStudio={() => setActiveNav('AI Pipeline')}
          />
        )}

        {activeNav === 'Admin & System' && (
          <AdminPortal />
        )}

      </main>

      {/* ============================================================ */}
      {/* 3. BOTTOM FOOTER BAR                                         */}
      {/* ============================================================ */}
      <footer className="bg-white border-t border-slate-200/80 px-5 py-2.5 flex items-center justify-between text-xs text-slate-500">
        <div className="flex items-center gap-2 font-mono text-[11px]">
          <span>Aura Marketing Engine v2.4</span>
          <span>•</span>
          <span className="text-emerald-600 font-bold">System Operational</span>
          <span>•</span>
          <span className="text-indigo-600 font-bold">DB Synced ({dbInfo?.engine || 'PostgreSQL 16'})</span>
        </div>
        <div className="text-[11px] text-slate-400">
          © 2026 Aura AI Inc. All rights reserved.
        </div>
      </footer>

    </div>
  );
}
