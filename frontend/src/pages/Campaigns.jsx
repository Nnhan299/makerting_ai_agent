import React, { useState } from 'react';
import { 
  Plus, 
  Search, 
  FolderKanban, 
  DollarSign, 
  Sparkles, 
  ArrowUpRight,
  TrendingUp,
  ShieldCheck,
  CheckCircle2,
  Trash2,
  Edit2,
  Calendar,
  ExternalLink,
  Layers,
  Clock,
  Video,
  Camera,
  Play,
  X
} from 'lucide-react';

export default function Campaigns({ campaigns, setCampaigns, onSelectCampaign, onNavigateToStudio, onNavigateToCalendar, onApiCreate, onApiDelete, onApiUpdate }) {
  const [filter, setFilter] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingCamp, setEditingCamp] = useState(null);
  const [selectedCampId, setSelectedCampId] = useState(null);
  const [toast, setToast] = useState(null);

  // Form state for creating new campaign
  const [newCamp, setNewCamp] = useState({
    name: '',
    sku: '',
    product_name: '',
    target_audience: '',
    budget: '$15,000 USD',
    channels: ['TikTok', 'Facebook', 'Instagram']
  });

  const showToast = (msg, type = 'success') => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newCamp.name.trim()) return;

    const created = {
      id: Date.now(),
      name: newCamp.name,
      sku: newCamp.sku || `CAM-2026-${Date.now().toString().slice(-4)}`,
      product_name: newCamp.product_name || newCamp.name,
      target_audience: newCamp.target_audience || 'Khách hàng tiềm năng mục tiêu',
      budget: newCamp.budget,
      status: 'In-Progress',
      compliance_rate: 96.5,
      posts_count: 12,
      channels: newCamp.channels,
      start_date: new Date().toISOString().slice(0, 10),
      end_date: '2026-12-31'
    };

    if (onApiCreate) {
      await onApiCreate(created);
    } else {
      setCampaigns([created, ...campaigns]);
    }
    setShowCreateModal(false);
    setNewCamp({ name: '', sku: '', product_name: '', target_audience: '', budget: '$15,000 USD', channels: ['TikTok', 'Facebook', 'Instagram'] });
    showToast('Chiến dịch mới đã được tạo thành công!');
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Bạn có chắc muốn xóa chiến dịch này không? Thao tác này không thể hoàn tác.')) return;
    if (onApiDelete) {
      await onApiDelete(id);
    } else {
      setCampaigns(campaigns.filter(c => c.id !== id));
    }
    if (selectedCampId === id) setSelectedCampId(null);
    showToast('Đã xóa chiến dịch thành công.', 'error');
  };

  const handleEditOpen = (camp, e) => {
    if (e) e.stopPropagation();
    setEditingCamp({ ...camp });
    setShowEditModal(true);
  };

  const handleEditSave = async (e) => {
    e.preventDefault();
    if (!editingCamp) return;
    const updateData = {
      name: editingCamp.name,
      product_name: editingCamp.product_name,
      target_audience: editingCamp.target_audience,
      budget: editingCamp.budget,
      channels: Array.isArray(editingCamp.channels) ? editingCamp.channels.join(', ') : editingCamp.channels
    };
    if (onApiUpdate) {
      await onApiUpdate(editingCamp.id, updateData);
    } else {
      setCampaigns(campaigns.map(c => c.id === editingCamp.id ? { ...c, ...editingCamp } : c));
    }
    setShowEditModal(false);
    setEditingCamp(null);
    showToast('Brief chiến dịch đã được cập nhật!');
  };

  // ── Filter + Search ──────────────────────────────────────────
  const filteredCampaigns = campaigns.filter(c => {
    const matchesFilter = filter === 'All' || c.status === filter;
    const matchesSearch = c.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          c.sku.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  // ── Dynamic "featured" respects the active filter tab ──
  const activeCampaign = filteredCampaigns.find(c => c.id === selectedCampId)
    || filteredCampaigns[0]
    || null;

  // Status badge styling helper
  const statusStyle = (status) => {
    switch (status) {
      case 'In-Progress': return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Approved': return 'bg-indigo-50 text-indigo-700 border-indigo-200';
      case 'Completed': return 'bg-slate-100 text-slate-600 border-slate-200';
      case 'Draft': return 'bg-amber-50 text-amber-700 border-amber-200';
      default: return 'bg-slate-50 text-slate-600 border-slate-200';
    }
  };

  const statusBadge = (status) => {
    switch (status) {
      case 'In-Progress': return (
        <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-mono font-bold border border-emerald-300 flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse" />
          IN-PROGRESS (AI RUNNING)
        </span>
      );
      case 'Approved': return (
        <span className="px-3 py-1 rounded-full bg-indigo-100 text-indigo-800 text-xs font-mono font-bold border border-indigo-300 flex items-center gap-1.5">
          <CheckCircle2 className="w-3.5 h-3.5" /> APPROVED
        </span>
      );
      case 'Completed': return (
        <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-mono font-bold border border-slate-300 flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5" /> COMPLETED
        </span>
      );
      case 'Draft': return (
        <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-800 text-xs font-mono font-bold border border-amber-300 flex items-center gap-1.5">
          <Edit2 className="w-3 h-3" /> DRAFT
        </span>
      );
      default: return null;
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Toast Notification */}
      {toast && (
        <div className={`fixed top-5 right-5 z-[100] px-4 py-3 rounded-xl shadow-lg font-semibold text-sm flex items-center gap-2 transition-all ${
          toast.type === 'error' ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
        }`}>
          {toast.type === 'error' ? <X className="w-4 h-4" /> : <CheckCircle2 className="w-4 h-4" />}
          {toast.msg}
        </div>
      )}

      {/* ------------------------------------------------------------ */}
      {/* TOP UTILITY & ORCHESTRATION CONTROL BAR                     */}
      {/* ------------------------------------------------------------ */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3 border-b border-slate-200/80">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">
            Quản lý Chiến dịch Tiếp thị
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Lập kế hoạch phân bổ ngân sách, cấu hình đối tượng mục tiêu và điều phối nội dung đa kênh.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Tìm kiếm chiến dịch, SKU..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:bg-white transition w-56 font-sans"
            />
          </div>

          <button 
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white px-3.5 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition active:scale-95 cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Tạo Chiến dịch mới</span>
          </button>
        </div>
      </div>

      {/* ------------------------------------------------------------ */}
      {/* FILTER TABS & QUICK METRICS RIBBON                           */}
      {/* ------------------------------------------------------------ */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3 bg-white p-2.5 rounded-xl border border-slate-200/80 shadow-2xs">
        {/* Filter Pills */}
        <div className="flex items-center gap-1 bg-[#F2F3FF] p-1 rounded-lg">
          {[
            { id: 'All', label: 'Tất cả', count: campaigns.length },
            { id: 'Draft', label: 'Draft', count: campaigns.filter(c => c.status === 'Draft').length },
            { id: 'In-Progress', label: 'In-Progress', count: campaigns.filter(c => c.status === 'In-Progress').length, dot: 'bg-emerald-600' },
            { id: 'Approved', label: 'Approved', count: campaigns.filter(c => c.status === 'Approved').length },
            { id: 'Completed', label: 'Completed', count: campaigns.filter(c => c.status === 'Completed').length },
          ].map(tab => {
            const isActive = filter === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setFilter(tab.id);
                  setSelectedCampId(null); // Reset selection khi đổi tab
                }}
                className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs font-semibold transition ${
                  isActive 
                    ? 'bg-white text-[#3525CD] shadow-xs' 
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {tab.dot && <span className={`w-2 h-2 rounded-full ${tab.dot}`} />}
                <span>{tab.label}</span>
                <span className={`px-1.5 py-0.2 rounded-full text-[10px] font-mono ${
                  isActive ? 'bg-[#E2E7FF] text-[#3525CD] font-bold' : 'bg-slate-200/70 text-slate-600'
                }`}>
                  {tab.count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Quick Metrics Ribbon */}
        <div className="flex items-center gap-5 text-xs px-2 font-sans">
          <div className="flex items-center gap-1.5">
            <span className="text-slate-400 font-bold uppercase text-[10px] tracking-wider">Q4 AD SPEND:</span>
            <span className="font-mono font-bold text-slate-800">$42,800 USD</span>
          </div>
          <span className="w-1 h-1 rounded-full bg-slate-300" />
          <div className="flex items-center gap-1.5">
            <span className="text-slate-400 font-bold uppercase text-[10px] tracking-wider">COMPLIANCE RATE:</span>
            <span className="font-mono font-bold text-emerald-600">98.4%</span>
          </div>
        </div>
      </div>

      {/* ------------------------------------------------------------ */}
      {/* PRIMARY FEATURED CAMPAIGN BENTO BOX (dynamic)                */}
      {/* ------------------------------------------------------------ */}
      {activeCampaign ? (
        <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 space-y-5 relative overflow-hidden">
          
          {/* Top Status Ribbon */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2.5 flex-wrap">
              {statusBadge(activeCampaign.status)}
              <span className="text-xs font-mono text-slate-500 font-medium">ID: {activeCampaign.sku}</span>
              <span className="w-1 h-1 rounded-full bg-slate-300" />
              <span className="text-xs font-medium text-indigo-600 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5" /> Neural Engine v4.8 Active
              </span>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2">
              <button 
                onClick={(e) => handleEditOpen(activeCampaign, e)}
                className="px-3 py-1.5 rounded-lg bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs flex items-center gap-1.5 border border-slate-200 transition cursor-pointer"
              >
                <Edit2 className="w-3 h-3 text-slate-500" /> Sửa Brief
              </button>
              <button 
                onClick={() => onNavigateToCalendar()}
                className="px-3 py-1.5 rounded-lg bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs flex items-center gap-1.5 border border-slate-200 transition cursor-pointer"
              >
                <Calendar className="w-3 h-3 text-slate-500" /> Lịch phát sóng
              </button>
              <button 
                onClick={() => {
                  onSelectCampaign(activeCampaign);
                  onNavigateToStudio();
                }}
                className="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs flex items-center gap-1.5 shadow-xs transition cursor-pointer"
              >
                <Sparkles className="w-3 h-3" /> Mở AI Studio
              </button>
              <button 
                onClick={(e) => handleDelete(activeCampaign.id, e)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition cursor-pointer"
                title="Xóa chiến dịch"
              >
                <Trash2 className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Bento Grid: Left Details & Right Previews */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            
            {/* Left 7 Cols: Brief, Parameters & Progress */}
            <div className="lg:col-span-7 space-y-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-[10px] font-mono font-bold text-indigo-700 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded-md uppercase">
                    {activeCampaign.product_name || 'Sản phẩm mục tiêu'}
                  </span>
                </div>
                <h2 className="text-xl font-bold text-slate-900 tracking-tight">
                  {activeCampaign.name}
                </h2>
                <p className="text-xs text-slate-600 leading-relaxed mt-1 max-w-xl">
                  {activeCampaign.target_audience || 'Chiến dịch marketing đa kênh, tối ưu hóa chuyển đổi với AI.'}
                </p>
              </div>

              {/* Key Parameters Matrix */}
              <div className="grid grid-cols-3 gap-3 p-3.5 rounded-xl bg-slate-50/80 border border-slate-200/80 text-xs">
                <div>
                  <span className="text-[10px] font-bold text-slate-400 font-mono uppercase block">ĐỐI TƯỢNG</span>
                  <div className="font-bold text-slate-800 text-xs mt-0.5">{activeCampaign.target_audience?.split('•')[0]?.trim() || 'Khách hàng mục tiêu'}</div>
                  <div className="text-[10px] font-mono text-slate-500 mt-0.5">{activeCampaign.target_audience?.split('•')[1]?.trim() || ''}</div>
                </div>
                <div>
                  <span className="text-[10px] font-bold text-slate-400 font-mono uppercase block">NGÂN SÁCH</span>
                  <div className="font-bold text-indigo-700 text-xs mt-0.5">{activeCampaign.budget}</div>
                  <div className="text-[10px] font-mono text-emerald-600 mt-0.5">Đã phân bổ</div>
                </div>
                <div>
                  <span className="text-[10px] font-bold text-slate-400 font-mono uppercase block">THỜI GIAN</span>
                  <div className="font-bold text-slate-800 text-xs mt-0.5">
                    {activeCampaign.start_date && activeCampaign.end_date
                      ? Math.ceil((new Date(activeCampaign.end_date) - new Date(activeCampaign.start_date)) / 86400000) + ' Ngày'
                      : '—'}
                  </div>
                  <div className="text-[10px] font-mono text-slate-500 mt-0.5">
                    {activeCampaign.start_date} — {activeCampaign.end_date}
                  </div>
                </div>
              </div>

              {/* Channel Allocation & Post Progress Bar */}
              <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-2xs space-y-2.5">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-900 uppercase text-[11px] tracking-wider">TIẾN ĐỘ SÁNG TẠO NỘI DUNG</span>
                    <span className="px-2 py-0.5 rounded-full bg-[#E2DFFF] text-[#0F0069] text-[10px] font-mono font-bold">
                      {activeCampaign.posts_count || 12} / {activeCampaign.posts_count || 12} Posts Generated
                    </span>
                  </div>
                  <span className="font-mono text-[11px] font-bold text-emerald-600">100% Pipeline Synthesis</span>
                </div>

                {/* Tri-colored Progress Bar */}
                <div className="h-2.5 w-full bg-[#E2E7FF] rounded-full overflow-hidden flex">
                  <div className="bg-[#006C49] h-full" style={{ width: '55%' }} />
                  <div className="bg-[#3525CD] h-full" style={{ width: '30%' }} />
                  <div className="bg-[#4CD7F6] h-full" style={{ width: '15%' }} />
                </div>

                <div className="flex items-center justify-between text-[11px] pt-1 text-slate-600 font-mono">
                  <div className="flex items-center gap-3">
                    {(activeCampaign.channels || ['TikTok', 'Instagram', 'Facebook']).slice(0, 3).map((ch, i) => (
                      <span key={ch} className="flex items-center gap-1">
                        <span className={`w-2 h-2 rounded-full ${i === 0 ? 'bg-[#006C49]' : i === 1 ? 'bg-[#3525CD]' : 'bg-[#4CD7F6]'}`} />
                        {ch}
                      </span>
                    ))}
                  </div>
                  <button 
                    onClick={() => onNavigateToCalendar()}
                    className="text-[#3525CD] font-bold hover:underline flex items-center gap-1"
                  >
                    Xem trong Calendar <ArrowUpRight className="w-3 h-3" />
                  </button>
                </div>
              </div>
            </div>

            {/* Right 5 Cols: Creative Visual Matrix Preview */}
            <div className="lg:col-span-5 grid grid-cols-2 gap-3.5">
              
              {/* Asset Card 1 */}
              <div className="rounded-xl overflow-hidden bg-slate-900 border border-slate-200 relative group aspect-3/4 flex flex-col justify-end p-3.5 text-white shadow-xs">
                <img 
                  src="https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&auto=format&fit=crop&q=80" 
                  alt="TikTok Creative"
                  className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition duration-500 opacity-80" 
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-900/40 to-transparent" />
                <div className="relative z-10 space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="px-2 py-0.5 rounded-full bg-white/80 backdrop-blur-md text-slate-900 text-[10px] font-mono font-bold">
                      {(activeCampaign.channels || ['TikTok'])[0]} #01
                    </span>
                    <span className="text-[10px] font-mono text-emerald-400 font-bold">✔ Approved</span>
                  </div>
                  <div className="text-xs font-bold leading-tight line-clamp-2">
                    7s Hook: Da ẩm mọng như pha lê chỉ sau 1 đêm
                  </div>
                  <div className="text-[10px] font-mono text-cyan-300">
                    ROAS Dự phóng: 3.4x
                  </div>
                </div>
              </div>

              {/* Asset Card 2 */}
              <div className="rounded-xl overflow-hidden bg-slate-900 border border-slate-200 relative group aspect-3/4 flex flex-col justify-end p-3.5 text-white shadow-xs">
                <img 
                  src="https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600&auto=format&fit=crop&q=80" 
                  alt="Reels Creative"
                  className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition duration-500 opacity-80" 
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-900/40 to-transparent" />
                <div className="relative z-10 space-y-1">
                  <div className="flex items-center justify-between">
                    <span className="px-2 py-0.5 rounded-full bg-white/80 backdrop-blur-md text-slate-900 text-[10px] font-mono font-bold">
                      {(activeCampaign.channels || ['TikTok', 'Instagram'])[1] || 'Instagram'} #02
                    </span>
                    <span className="text-[10px] font-mono text-emerald-400 font-bold">✔ Approved</span>
                  </div>
                  <div className="text-xs font-bold leading-tight line-clamp-2">
                    Carousel: 4 Bước phục hồi màng ẩm chuyên sâu
                  </div>
                  <div className="text-[10px] font-mono text-indigo-300">
                    Compliance: {activeCampaign.compliance_rate || 98}/100
                  </div>
                </div>
              </div>

            </div>

          </div>

        </div>
      ) : (
        /* Empty state khi filter không có campaign nào */
        <div className="bg-white rounded-2xl border border-dashed border-slate-300 p-12 flex flex-col items-center justify-center text-center gap-3">
          <FolderKanban className="w-10 h-10 text-slate-300" />
          <h3 className="font-bold text-slate-500">Không có chiến dịch nào ở trạng thái "{filter}"</h3>
          <p className="text-xs text-slate-400">Chọn tab khác hoặc tạo chiến dịch mới</p>
          <button 
            onClick={() => setShowCreateModal(true)}
            className="mt-2 inline-flex items-center gap-1.5 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-4 py-2 rounded-lg font-semibold text-xs shadow-xs transition"
          >
            <Plus className="w-3.5 h-3.5" /> Tạo chiến dịch mới
          </button>
        </div>
      )}

      {/* ------------------------------------------------------------ */}
      {/* OTHER CAMPAIGNS GRID SECTION                                 */}
      {/* ------------------------------------------------------------ */}
      {filteredCampaigns.length > 1 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-extrabold text-slate-900 uppercase font-mono tracking-wider">
              CÁC CHIẾN DỊCH KHÁC ({filteredCampaigns.length - 1})
            </h3>
            <span className="text-xs text-slate-400 font-mono">Bấm vào thẻ để hiển thị ở trên</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredCampaigns.filter(c => c.id !== activeCampaign?.id).map((camp) => (
              <div 
                key={camp.id}
                onClick={() => setSelectedCampId(camp.id)}
                className="bg-white rounded-2xl border border-slate-200/90 shadow-2xs hover:shadow-md hover:border-indigo-300 transition-all flex flex-col justify-between overflow-hidden group cursor-pointer"
              >
                <div className="p-4 space-y-2.5">
                  <div className="flex items-start justify-between gap-2">
                    <span className="font-mono text-[10px] text-slate-400 font-bold bg-slate-100 px-2 py-0.5 rounded">
                      {camp.sku}
                    </span>
                    <span className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded-full border ${statusStyle(camp.status)}`}>
                      ● {camp.status}
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-[#4F46E5] transition leading-snug">
                    {camp.name}
                  </h4>

                  <p className="text-xs text-slate-500 line-clamp-2">
                    <span className="font-semibold text-slate-700">Mục tiêu:</span> {camp.target_audience}
                  </p>

                  {/* Progress and compliance */}
                  <div className="space-y-1 pt-1">
                    <div className="flex justify-between text-xs font-mono">
                      <span className="text-slate-500 text-[11px]">Brand Compliance</span>
                      <span className="font-bold text-emerald-600">{camp.compliance_rate}%</span>
                    </div>
                    <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                      <div 
                        className="bg-emerald-500 h-1.5 rounded-full transition-all"
                        style={{ width: `${camp.compliance_rate}%` }}
                      />
                    </div>
                  </div>

                  {/* Meta tags */}
                  <div className="pt-1 flex flex-wrap gap-1 text-[10px]">
                    {camp.channels.map(ch => (
                      <span key={ch} className="px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-medium">
                        #{ch}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Card Footer Actions */}
                <div className="p-3 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-xs">
                  <div>
                    <span className="text-slate-400 block text-[9px] font-mono uppercase">Ngân sách</span>
                    <span className="font-bold text-slate-800 text-xs">{camp.budget}</span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <button
                      type="button"
                      onClick={(e) => handleEditOpen(camp, e)}
                      className="p-1.5 text-slate-400 hover:text-indigo-600 rounded-lg hover:bg-white transition"
                      title="Sửa Brief"
                    >
                      <Edit2 className="w-3.5 h-3.5" />
                    </button>
                    <button
                      type="button"
                      onClick={(e) => handleDelete(camp.id, e)}
                      className="p-1.5 text-slate-400 hover:text-red-500 rounded-lg hover:bg-white transition"
                      title="Xóa chiến dịch"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectCampaign(camp);
                        onNavigateToStudio();
                      }}
                      className="inline-flex items-center gap-1 bg-[#4F46E5] hover:bg-[#4338CA] text-white font-bold px-2.5 py-1 rounded-lg shadow-xs transition active:scale-95 text-xs"
                    >
                      <Sparkles className="w-3 h-3" />
                      Mở Studio
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Show single card section when only 1 result */}
      {filteredCampaigns.length === 1 && (
        <div className="text-xs text-center text-slate-400 font-mono py-2">
          Chỉ có 1 chiến dịch trong bộ lọc này — hiển thị ở trên
        </div>
      )}

      {/* ------------------------------------------------------------ */}
      {/* EDIT BRIEF MODAL                                             */}
      {/* ------------------------------------------------------------ */}
      {showEditModal && editingCamp && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-slate-100">
            <div className="flex justify-between items-center pb-2 border-b">
              <div>
                <h3 className="font-bold text-base text-slate-900">Sửa Brief Chiến Dịch</h3>
                <span className="text-xs font-mono text-slate-400">{editingCamp.sku}</span>
              </div>
              <button onClick={() => setShowEditModal(false)} className="text-slate-400 hover:text-slate-600 p-1">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <form onSubmit={handleEditSave} className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Tên chiến dịch *</label>
                <input 
                  type="text" 
                  required
                  value={editingCamp.name}
                  onChange={(e) => setEditingCamp({ ...editingCamp, name: e.target.value })}
                  className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500 font-semibold text-sm" 
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Sản phẩm trọng tâm</label>
                <input 
                  type="text"
                  value={editingCamp.product_name || ''}
                  onChange={(e) => setEditingCamp({ ...editingCamp, product_name: e.target.value })}
                  className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500" 
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Chân dung đối tượng (Target Persona)</label>
                <textarea 
                  rows="2"
                  value={editingCamp.target_audience || ''}
                  onChange={(e) => setEditingCamp({ ...editingCamp, target_audience: e.target.value })}
                  className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Ngân sách</label>
                  <input 
                    type="text"
                    value={editingCamp.budget || ''}
                    onChange={(e) => setEditingCamp({ ...editingCamp, budget: e.target.value })}
                    className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500 font-bold" 
                  />
                </div>
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Kênh phân phối</label>
                  <input 
                    type="text"
                    value={Array.isArray(editingCamp.channels) ? editingCamp.channels.join(', ') : editingCamp.channels || ''}
                    onChange={(e) => setEditingCamp({ ...editingCamp, channels: e.target.value.split(',').map(s => s.trim()) })}
                    placeholder="TikTok, Instagram, Facebook"
                    className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500" 
                  />
                </div>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <button type="button" onClick={() => setShowEditModal(false)} className="px-4 py-2 border border-slate-200 rounded-xl text-slate-600 font-bold hover:bg-slate-50">Hủy</button>
                <button type="submit" className="px-4 py-2 bg-[#4F46E5] text-white rounded-xl font-bold shadow-md shadow-indigo-500/20 hover:bg-indigo-700">
                  Lưu thay đổi
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ------------------------------------------------------------ */}
      {/* CREATE CAMPAIGN MODAL                                        */}
      {/* ------------------------------------------------------------ */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-slate-100">
            <div className="flex justify-between items-center pb-2 border-b">
              <h3 className="font-bold text-base text-slate-900">Khởi tạo Chiến dịch Mới</h3>
              <button onClick={() => setShowCreateModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <form onSubmit={handleCreate} className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Tên chiến dịch *</label>
                <input 
                  type="text" 
                  required
                  placeholder="Ví dụ: Chiến dịch Ra mắt Kem Chống Nắng Ultra Shield" 
                  value={newCamp.name}
                  onChange={(e) => setNewCamp({ ...newCamp, name: e.target.value })}
                  className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500" 
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Mã SKU</label>
                  <input 
                    type="text" 
                    placeholder="VD: SKU-SUN-2026" 
                    value={newCamp.sku}
                    onChange={(e) => setNewCamp({ ...newCamp, sku: e.target.value })}
                    className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500 font-mono" 
                  />
                </div>
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Ngân sách dự kiến</label>
                  <input 
                    type="text" 
                    value={newCamp.budget}
                    onChange={(e) => setNewCamp({ ...newCamp, budget: e.target.value })}
                    className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500 font-bold" 
                  />
                </div>
              </div>

              <div>
                <label className="font-bold text-slate-700 block mb-1">Chân dung đối tượng (Target Persona)</label>
                <textarea 
                  rows="2" 
                  placeholder="Độ tuổi, giới tính, vấn đề da cần giải quyết..." 
                  value={newCamp.target_audience}
                  onChange={(e) => setNewCamp({ ...newCamp, target_audience: e.target.value })}
                  className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <button type="button" onClick={() => setShowCreateModal(false)} className="px-4 py-2 border border-slate-200 rounded-xl text-slate-600 font-bold">Hủy</button>
                <button type="submit" className="px-4 py-2 bg-[#4F46E5] text-white rounded-xl font-bold shadow-md shadow-indigo-500/20">Khởi tạo ngay</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
