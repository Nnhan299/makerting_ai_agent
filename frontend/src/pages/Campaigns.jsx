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
  Play
} from 'lucide-react';

export default function Campaigns({ campaigns, setCampaigns, onSelectCampaign, onNavigateToStudio, onNavigateToCalendar }) {
  const [filter, setFilter] = useState('All');
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Form state for creating new campaign
  const [newCamp, setNewCamp] = useState({
    name: '',
    sku: '',
    product_name: '',
    target_audience: '',
    budget: '$15,000 USD',
    channels: ['TikTok', 'Facebook', 'Instagram']
  });

  const handleCreate = (e) => {
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

    setCampaigns([created, ...campaigns]);
    setShowCreateModal(false);
    setNewCamp({
      name: '',
      sku: '',
      product_name: '',
      target_audience: '',
      budget: '$15,000 USD',
      channels: ['TikTok', 'Facebook', 'Instagram']
    });
  };

  const handleDelete = (id, e) => {
    e.stopPropagation();
    setCampaigns(campaigns.filter(c => c.id !== id));
  };

  const filteredCampaigns = campaigns.filter(c => {
    const matchesFilter = filter === 'All' || c.status.toLowerCase() === filter.toLowerCase();
    const matchesSearch = c.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          c.sku.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  // Featured Primary Campaign (PureGlow 2026)
  const featured = campaigns.find(c => c.sku.includes('PG01') || c.name.includes('PureGlow')) || campaigns[0];

  return (
    <div className="space-y-6">
      
      {/* ------------------------------------------------------------ */}
      {/* TOP UTILITY & ORCHESTRATION CONTROL BAR                     */}
      {/* ------------------------------------------------------------ */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3 border-b border-slate-200/80">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-[#3525CD] font-bold uppercase tracking-wider mb-1">
            <span>SRS 3.1 • CREATIVE ARCHITECTURE</span>
            <span className="w-1.5 h-1.5 rounded-full bg-slate-300" />
            <span className="text-slate-500 font-normal">Module CAM-01..05</span>
          </div>
          <div className="flex items-baseline gap-3">
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
              Chiến Dịch Tiếp Thị Số
            </h1>
            <span className="text-xs font-mono text-slate-500">
              {campaigns.length} Active • 1 Queued
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Tìm kiếm chiến dịch, SKU..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8 pr-3 py-1.5 bg-[#F2F3FF] border border-transparent rounded-lg text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-400 focus:bg-white transition w-56 font-sans"
            />
          </div>

          <button 
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center gap-1.5 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-3.5 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition active:scale-95"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>+ Tạo Chiến dịch mới</span>
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
            { id: 'Completed', label: 'Completed', count: 6 }
          ].map(tab => {
            const isActive = filter === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setFilter(tab.id)}
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
      {/* PRIMARY FEATURED CAMPAIGN BENTO BOX (Serum PureGlow 2026)    */}
      {/* ------------------------------------------------------------ */}
      {featured && (
        <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 space-y-5 relative overflow-hidden">
          
          {/* Top Status Ribbon */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2.5 flex-wrap">
              <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-mono font-bold border border-emerald-300 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse" />
                IN-PROGRESS (AI RUNNING)
              </span>
              <span className="text-xs font-mono text-slate-500 font-medium">ID: {featured.sku}</span>
              <span className="w-1 h-1 rounded-full bg-slate-300" />
              <span className="text-xs font-medium text-indigo-600 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5" /> Neural Engine v4.8 Active
              </span>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2">
              <button 
                onClick={() => {
                  onSelectCampaign(featured);
                  onNavigateToStudio();
                }}
                className="px-3 py-1.5 rounded-lg bg-[#3525CD] hover:bg-indigo-800 text-white font-semibold text-xs flex items-center gap-1.5 shadow-xs transition"
              >
                <Sparkles className="w-3 h-3" /> Chạy lại AI Pipeline
              </button>
              <button 
                onClick={() => onNavigateToCalendar()}
                className="px-3 py-1.5 rounded-lg bg-[#F2F3FF] hover:bg-indigo-100 text-slate-800 font-semibold text-xs flex items-center gap-1.5 border border-slate-200/70 transition"
              >
                <Calendar className="w-3 h-3 text-indigo-600" /> Xem Lịch Phát Sóng
              </button>
            </div>
          </div>

          {/* Bento Grid: Left Details & Right Previews */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            
            {/* Left 7 Cols: Brief, Parameters & Progress */}
            <div className="lg:col-span-7 space-y-4">
              <div>
                <div className="text-[11px] font-mono font-bold text-[#3525CD] tracking-widest uppercase">
                  SẢN PHẨM TRỌNG TÂM / <span className="text-slate-500 font-normal">{featured.product_name || 'Serum Niacinamide + Zinc Duo'}</span>
                </div>
                <h2 className="text-2xl font-black text-slate-900 mt-1 tracking-tight">
                  {featured.name}
                </h2>
                <p className="text-xs text-slate-600 leading-relaxed mt-2 max-w-xl">
                  Chiến dịch thúc đẩy nhận diện và chuyển đổi mùa tựu trường, tôn vinh làn da mộc tự nhiên với công nghệ màng sinh học nano dưỡng sáng và phục hồi hàng rào ẩm.
                </p>
              </div>

              {/* Key Parameters Matrix */}
              <div className="grid grid-cols-3 gap-3 p-3.5 rounded-xl bg-[#F2F3FF]/70 border border-indigo-100 text-xs">
                <div>
                  <span className="text-[10px] font-bold text-slate-400 font-mono uppercase block">TARGET AUDIENCE</span>
                  <div className="font-bold text-slate-800 text-sm mt-0.5">Gen Z Skincare</div>
                  <div className="text-[11px] font-mono text-slate-500 mt-0.5">Độ tuổi: 18 - 25</div>
                </div>
                <div>
                  <span className="text-[10px] font-bold text-slate-400 font-mono uppercase block">NGÂN SÁCH PHÂN BỔ</span>
                  <div className="font-bold text-[#3525CD] text-sm mt-0.5">{featured.budget}</div>
                  <div className="text-[11px] font-mono text-emerald-600 mt-0.5">$12,410 đã cam kết</div>
                </div>
                <div>
                  <span className="text-[10px] font-bold text-slate-400 font-mono uppercase block">THỜI GIAN</span>
                  <div className="font-bold text-slate-800 text-sm mt-0.5">31 Ngày</div>
                  <div className="text-[11px] font-mono text-slate-500 mt-0.5">10/10 - 10/11/2026</div>
                </div>
              </div>

              {/* Channel Allocation & Post Progress Bar */}
              <div className="p-3.5 rounded-xl bg-white border border-slate-200/80 shadow-2xs space-y-2.5">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-slate-900 uppercase text-[11px] tracking-wider">TIẾN ĐỘ SÁNG TẠO NỘI DUNG</span>
                    <span className="px-2 py-0.5 rounded-full bg-[#E2DFFF] text-[#0F0069] text-[10px] font-mono font-bold">
                      12 / 12 Posts Generated
                    </span>
                  </div>
                  <span className="font-mono text-[11px] font-bold text-emerald-600">100% Pipeline Synthesis</span>
                </div>

                {/* Tri-colored Progress Bar */}
                <div className="h-2.5 w-full bg-[#E2E7FF] rounded-full overflow-hidden flex">
                  <div className="bg-[#006C49] h-full" style={{ width: '55%' }} title="TikTok: 55%" />
                  <div className="bg-[#3525CD] h-full" style={{ width: '30%' }} title="Instagram: 30%" />
                  <div className="bg-[#4CD7F6] h-full" style={{ width: '15%' }} title="Facebook: 15%" />
                </div>

                <div className="flex items-center justify-between text-[11px] pt-1 text-slate-600 font-mono">
                  <div className="flex items-center gap-3">
                    <span className="flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-[#006C49]" /> TikTok: 6 Videos (3 Hooks each)
                    </span>
                    <span className="flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-[#3525CD]" /> Instagram: 4 Carousels
                    </span>
                    <span className="flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-[#4CD7F6]" /> Facebook: 2 Posts
                    </span>
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
              
              {/* Asset Card 1: TikTok #01 */}
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
                      TikTok #01
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

              {/* Asset Card 2: Reels #03 */}
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
                      Instagram #02
                    </span>
                    <span className="text-[10px] font-mono text-emerald-400 font-bold">✔ Approved</span>
                  </div>
                  <div className="text-xs font-bold leading-tight line-clamp-2">
                    Carousel: 4 Bước phục hồi màng ẩm chuyên sâu
                  </div>
                  <div className="text-[10px] font-mono text-indigo-300">
                    Compliance: 98/100
                  </div>
                </div>
              </div>

            </div>

          </div>

        </div>
      )}

      {/* ------------------------------------------------------------ */}
      {/* OTHER CAMPAIGNS GRID SECTION                                 */}
      {/* ------------------------------------------------------------ */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-extrabold text-slate-900 uppercase font-mono tracking-wider">
            CÁC CHIẾN DỊCH KHÁC ({filteredCampaigns.length})
          </h3>
          <span className="text-xs text-slate-400 font-mono">Bấm vào thẻ để chọn và mở Studio</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredCampaigns.map((camp) => (
            <div 
              key={camp.id}
              onClick={() => {
                onSelectCampaign(camp);
                onNavigateToStudio();
              }}
              className="bg-white rounded-2xl border border-slate-200/90 shadow-2xs hover:shadow-md hover:border-indigo-300 transition-all flex flex-col justify-between overflow-hidden group cursor-pointer"
            >
              <div className="p-4 space-y-2.5">
                <div className="flex items-start justify-between gap-2">
                  <span className="font-mono text-[10px] text-slate-400 font-bold bg-slate-100 px-2 py-0.5 rounded">
                    {camp.sku}
                  </span>
                  <span className={`text-[10px] font-bold font-mono px-2 py-0.5 rounded-full border ${
                    camp.status === 'Approved' 
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200' 
                      : camp.status === 'In-Progress'
                      ? 'bg-indigo-50 text-indigo-700 border-indigo-200'
                      : 'bg-amber-50 text-amber-700 border-amber-200'
                  }`}>
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

      {/* ------------------------------------------------------------ */}
      {/* CREATE CAMPAIGN MODAL                                        */}
      {/* ------------------------------------------------------------ */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-slate-100 animate-in fade-in zoom-in-95">
            <div className="flex justify-between items-center pb-2 border-b">
              <h3 className="font-bold text-base text-slate-900">Khởi tạo Chiến dịch Mới</h3>
              <button onClick={() => setShowCreateModal(false)} className="text-slate-400 hover:text-slate-600 font-bold">✕</button>
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
                  className="w-full p-2.5 border rounded-xl focus:outline-none focus:border-indigo-500" 
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
                    className="w-full p-2.5 border rounded-xl focus:outline-none focus:border-indigo-500 font-mono" 
                  />
                </div>
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Ngân sách dự kiến</label>
                  <input 
                    type="text" 
                    value={newCamp.budget}
                    onChange={(e) => setNewCamp({ ...newCamp, budget: e.target.value })}
                    className="w-full p-2.5 border rounded-xl focus:outline-none focus:border-indigo-500 font-bold" 
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
                  className="w-full p-2.5 border rounded-xl focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t">
                <button type="button" onClick={() => setShowCreateModal(false)} className="px-4 py-2 border rounded-xl text-slate-600 font-bold">Hủy</button>
                <button type="submit" className="px-4 py-2 bg-[#4F46E5] text-white rounded-xl font-bold shadow-md shadow-indigo-500/20">Khởi tạo ngay</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
