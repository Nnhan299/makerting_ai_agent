import React, { useState } from 'react';
import { 
  Download, 
  Send, 
  CheckCircle, 
  Clock, 
  ExternalLink, 
  Sparkles, 
  Share2, 
  Calendar as CalendarIcon, 
  Check, 
  ChevronLeft, 
  ChevronRight,
  Filter,
  Eye,
  AlertTriangle,
  FileSpreadsheet,
  ShieldCheck,
  Edit3
} from 'lucide-react';

import { publishPostApi, updatePostApi } from '../api';

export default function CalendarReview({ posts, setPosts, onNavigateToStudio }) {
  const [viewMode, setViewMode] = useState('calendar'); // 'calendar' | 'list'
  const [channelFilter, setChannelFilter] = useState('all');
  const [stageFilter, setStageFilter] = useState('all');
  const [selectedPostId, setSelectedPostId] = useState(1);
  const [publishedPosts, setPublishedPosts] = useState({});

  // Initial posts list if not passed
  const allPosts = posts || [
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
  ];

  const selectedPost = allPosts.find(p => p.id === selectedPostId) || allPosts[0];

  const handlePublishNow = async (id) => {
    const postUrl = `https://facebook.com/PureGlowVN/posts/fb_${Date.now()}`;
    await publishPostApi(id, postUrl);
    setPublishedPosts(prev => ({
      ...prev,
      [id]: {
        published_at: new Date().toLocaleTimeString(),
        post_url: postUrl
      }
    }));
    if (setPosts) {
      setPosts(prev => prev.map(p => p.id === id ? { ...p, status: 'Published' } : p));
    }
  };

  const handleApprove = async (id) => {
    await updatePostApi(id, { status: 'Approved' });
    if (setPosts) {
      setPosts(prev => prev.map(p => p.id === id ? { ...p, status: 'Approved' } : p));
    }
  };

  const handleExportExcel = () => {
    const headers = 'ID,Tiêu đề,Giai đoạn,Kênh,Ngày đăng,Điểm tuân thủ,Trạng thái\n';
    const rows = allPosts.map(p => `"${p.id}","${p.title}","${p.stage}","${p.channel}","${p.date_str}","${p.compliance_score}","${p.status}"`).join('\n');
    const blob = new Blob([headers + rows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AuraAI_Marketing_Calendar_PureGlow_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
  };

  const filteredPosts = allPosts.filter(p => {
    const matchChannel = channelFilter === 'all' || p.channel.toLowerCase() === channelFilter.toLowerCase();
    const matchStage = stageFilter === 'all' || p.stage.toLowerCase() === stageFilter.toLowerCase();
    return matchChannel && matchStage;
  });

  return (
    <div className="space-y-5">
      
      {/* ------------------------------------------------------------ */}
      {/* HEADER CONTROL BAR: VIEW SWITCHER, FILTERS & ACTIONS         */}
      {/* ------------------------------------------------------------ */}
      <div className="bg-white p-3.5 rounded-2xl border border-slate-200/90 shadow-2xs flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
        
        <div className="flex items-center gap-3 flex-wrap">
          {/* View Toggle */}
          <div className="flex items-center bg-[#F2F3FF] p-1 rounded-lg">
            <button
              onClick={() => setViewMode('calendar')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition ${
                viewMode === 'calendar' ? 'bg-white text-[#3525CD] shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <CalendarIcon className="w-3.5 h-3.5" />
              <span>Lịch tháng</span>
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition ${
                viewMode === 'list' ? 'bg-white text-[#3525CD] shadow-xs' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Filter className="w-3.5 h-3.5" />
              <span>Timeline / Danh sách</span>
            </button>
          </div>

          {/* Month Navigation Marker */}
          <div className="flex items-center gap-2 bg-[#F2F3FF] px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-800">
            <button className="text-slate-500 hover:text-slate-800"><ChevronLeft className="w-3.5 h-3.5" /></button>
            <span>Tháng 10, 2026</span>
            <button className="text-slate-500 hover:text-slate-800"><ChevronRight className="w-3.5 h-3.5" /></button>
            <span className="text-[#3525CD] font-mono font-bold pl-1 border-l border-slate-300">48 BÀI ĐĂNG</span>
          </div>
        </div>

        {/* Channel & Funnel Filters */}
        <div className="flex items-center gap-3 flex-wrap w-full lg:w-auto justify-between lg:justify-end">
          {/* Channel Filter */}
          <div className="flex items-center gap-1">
            <span className="text-[10px] font-mono font-bold text-slate-400 uppercase mr-1">KÊNH:</span>
            {['all', 'tiktok', 'facebook', 'instagram'].map(ch => (
              <button
                key={ch}
                onClick={() => setChannelFilter(ch)}
                className={`px-2.5 py-1 rounded-full text-xs font-semibold capitalize transition ${
                  channelFilter === ch 
                    ? 'bg-[#4F46E5] text-white shadow-xs' 
                    : 'bg-[#F2F3FF] text-slate-600 hover:bg-slate-200'
                }`}
              >
                {ch === 'all' ? 'Tất cả' : ch}
              </button>
            ))}
          </div>

          {/* Export Excel Button */}
          <button 
            onClick={handleExportExcel}
            className="inline-flex items-center gap-1.5 bg-[#006C49] hover:bg-[#005236] text-white px-3.5 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition active:scale-95"
          >
            <FileSpreadsheet className="w-3.5 h-3.5" />
            <span>Xuất Excel (3 Sheets)</span>
          </button>
        </div>

      </div>

      {/* ------------------------------------------------------------ */}
      {/* VIEW MODE 1: CALENDAR SPLIT BOARD (LEFT 8 COLS, RIGHT 4 COLS)*/}
      {/* ------------------------------------------------------------ */}
      {viewMode === 'calendar' ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
          
          {/* Left 8 Cols: Calendar Board */}
          <div className="lg:col-span-8 bg-white rounded-2xl border border-slate-200/90 p-5 shadow-2xs space-y-4">
            
            {/* Sub-header info & legend */}
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <h3 className="font-bold text-sm text-slate-900">
                  Kế hoạch phát hành đa kênh Serum PureGlow
                </h3>
                <span className="text-[10px] font-mono bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded font-bold border border-indigo-200">
                  v4.8-synced
                </span>
              </div>

              <div className="flex items-center gap-3 text-xs font-mono">
                <span className="flex items-center gap-1.5 text-slate-600">
                  <span className="w-2 h-2 rounded-full bg-[#006C49]" />
                  Approved (39)
                </span>
                <span className="flex items-center gap-1.5 text-slate-600">
                  <span className="w-2 h-2 rounded-full bg-[#BA1A1A]" />
                  Pending Review (9)
                </span>
              </div>
            </div>

            {/* Days of Week Header */}
            <div className="grid grid-cols-7 gap-1.5 text-center font-mono text-[11px] font-bold text-slate-500 py-1 bg-[#F2F3FF] rounded-lg">
              <div>T2 / THỨ HAI</div>
              <div>T3 / THỨ BA</div>
              <div>T4 / THỨ TƯ</div>
              <div>T5 / THỨ NĂM</div>
              <div>T6 / THỨ SÁU</div>
              <div className="text-[#3525CD]">T7 / THỨ BẢY</div>
              <div className="text-[#3525CD]">CN / CHỦ NHẬT</div>
            </div>

            {/* Calendar Month Grid (Week segment) */}
            <div className="grid grid-cols-7 gap-1.5 min-h-[360px]">
              
              {/* Mon 12: Empty */}
              <div className="bg-[#F2F3FF]/40 rounded-xl p-2 min-h-[140px] flex flex-col justify-between border border-transparent">
                <span className="font-mono text-xs text-slate-400 font-bold">12</span>
                <span className="text-center font-mono text-[10px] text-slate-400 my-auto">Trống</span>
              </div>

              {/* Tue 13: TikTok #01 */}
              <div 
                onClick={() => setSelectedPostId(1)}
                className={`rounded-xl p-2 min-h-[140px] flex flex-col justify-between transition cursor-pointer border ${
                  selectedPostId === 1 
                    ? 'bg-indigo-50/70 border-indigo-500 ring-2 ring-indigo-200 shadow-sm' 
                    : 'bg-white border-slate-200/90 hover:border-indigo-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-slate-800">13</span>
                  <span className="text-[10px] font-mono text-[#3525CD] font-bold">Teaser</span>
                </div>
                <div className="p-2 rounded-lg bg-white border border-slate-200/80 shadow-2xs space-y-1 my-1">
                  <div className="flex items-center justify-between">
                    <span className="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-cyan-100 text-cyan-900">
                      TIKTOK
                    </span>
                    <CheckCircle className="w-3 h-3 text-emerald-600" />
                  </div>
                  <div className="text-[10px] font-bold text-slate-900 line-clamp-2 leading-tight">
                    #SecretDrop: 3 giọt tinh chất
                  </div>
                </div>
                <span className="text-[9px] font-mono text-slate-400">19:30</span>
              </div>

              {/* Wed 14: Facebook Post */}
              <div 
                onClick={() => setSelectedPostId(2)}
                className={`rounded-xl p-2 min-h-[140px] flex flex-col justify-between transition cursor-pointer border ${
                  selectedPostId === 2 
                    ? 'bg-indigo-50/70 border-indigo-500 ring-2 ring-indigo-200 shadow-sm' 
                    : 'bg-white border-slate-200/90 hover:border-indigo-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-slate-800">14</span>
                  <span className="text-[10px] font-mono text-[#3525CD] font-bold">Teaser</span>
                </div>
                <div className="p-2 rounded-lg bg-white border border-slate-200/80 shadow-2xs space-y-1 my-1">
                  <div className="flex items-center justify-between">
                    <span className="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-indigo-100 text-indigo-900">
                      FACEBOOK
                    </span>
                    <CheckCircle className="w-3 h-3 text-emerald-600" />
                  </div>
                  <div className="text-[10px] font-bold text-slate-900 line-clamp-2 leading-tight">
                    Hé lộ thành phần Niacinamide
                  </div>
                </div>
                <span className="text-[9px] font-mono text-slate-400">20:00</span>
              </div>

              {/* Thu 15: TikTok Pending */}
              <div 
                onClick={() => setSelectedPostId(3)}
                className={`rounded-xl p-2 min-h-[140px] flex flex-col justify-between transition cursor-pointer border ${
                  selectedPostId === 3 
                    ? 'bg-indigo-50/70 border-indigo-500 ring-2 ring-indigo-200 shadow-sm' 
                    : 'bg-white border-slate-200/90 hover:border-indigo-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-slate-800">15</span>
                  <span className="w-2 h-2 rounded-full bg-red-500" />
                </div>
                <div className="p-2 rounded-lg bg-white border border-red-200 shadow-2xs space-y-1 my-1">
                  <div className="flex items-center justify-between">
                    <span className="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-cyan-100 text-cyan-900">
                      TIKTOK
                    </span>
                    <AlertTriangle className="w-3 h-3 text-red-500" />
                  </div>
                  <div className="text-[10px] font-bold text-slate-900 line-clamp-2 leading-tight">
                    Serum Glow & Kháng Viêm
                  </div>
                  <div className="text-[9px] font-mono text-red-600 font-bold">92/100 • 1 Cảnh báo</div>
                </div>
                <span className="text-[9px] font-mono text-slate-400">18:45</span>
              </div>

              {/* Fri 16: Instagram Carousel */}
              <div 
                onClick={() => setSelectedPostId(4)}
                className={`rounded-xl p-2 min-h-[140px] flex flex-col justify-between transition cursor-pointer border ${
                  selectedPostId === 4 
                    ? 'bg-indigo-50/70 border-indigo-500 ring-2 ring-indigo-200 shadow-sm' 
                    : 'bg-white border-slate-200/90 hover:border-indigo-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-slate-800">16</span>
                  <span className="text-[10px] font-mono text-[#006C49] font-bold">Launch</span>
                </div>
                <div className="p-2 rounded-lg bg-white border border-slate-200/80 shadow-2xs space-y-1 my-1">
                  <div className="flex items-center justify-between">
                    <span className="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-purple-100 text-purple-900">
                      INSTAGRAM
                    </span>
                    <CheckCircle className="w-3 h-3 text-emerald-600" />
                  </div>
                  <div className="text-[10px] font-bold text-slate-900 line-clamp-2 leading-tight">
                    Carousel: Routine 7 ngày
                  </div>
                </div>
                <span className="text-[9px] font-mono text-slate-400">12:00</span>
              </div>

              {/* Sat 17: Mega Launch */}
              <div 
                onClick={() => setSelectedPostId(5)}
                className={`rounded-xl p-2 min-h-[140px] flex flex-col justify-between transition cursor-pointer border ${
                  selectedPostId === 5 
                    ? 'bg-indigo-50/70 border-indigo-500 ring-2 ring-indigo-200 shadow-sm' 
                    : 'bg-white border-slate-200/90 hover:border-indigo-300'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs font-bold text-slate-800">17</span>
                  <span className="text-[10px] font-mono text-emerald-700 font-bold bg-emerald-100 px-1 rounded">Mega</span>
                </div>
                <div className="p-2 rounded-lg bg-white border border-slate-200/80 shadow-2xs space-y-1 my-1">
                  <div className="flex items-center justify-between">
                    <span className="text-[9px] font-mono font-bold px-1.5 py-0.2 rounded bg-cyan-100 text-cyan-900">
                      TIKTOK
                    </span>
                    <CheckCircle className="w-3 h-3 text-emerald-600" />
                  </div>
                  <div className="text-[10px] font-bold text-slate-900 line-clamp-2 leading-tight">
                    KOC Unboxing Box Quà
                  </div>
                </div>
                <span className="text-[9px] font-mono text-slate-400">20:15</span>
              </div>

              {/* Sun 18: Rest */}
              <div className="bg-[#F2F3FF]/40 rounded-xl p-2 min-h-[140px] flex flex-col justify-between border border-transparent">
                <span className="font-mono text-xs text-slate-400 font-bold">18</span>
                <span className="text-center font-mono text-[10px] text-slate-400 my-auto">Chờ duyệt</span>
              </div>

            </div>

          </div>

          {/* Right 4 Cols: Selected Post Inspector Panel */}
          <div className="lg:col-span-4 bg-white rounded-2xl border border-slate-200/90 p-5 shadow-2xs space-y-4">
            
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <h4 className="font-bold text-sm text-slate-900">
                Chi tiết bài đăng #{selectedPost.id}
              </h4>
              <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full ${
                selectedPost.status === 'Approved' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-700'
              }`}>
                ● {selectedPost.status}
              </span>
            </div>

            {/* Media thumbnail */}
            <div className="rounded-xl overflow-hidden aspect-video bg-slate-100 relative">
              <img 
                src={selectedPost.media_url} 
                alt="Post asset preview" 
                className="w-full h-full object-cover"
              />
              <span className="absolute bottom-2 left-2 bg-slate-900/80 backdrop-blur-md text-white text-[10px] font-mono px-2 py-0.5 rounded">
                {selectedPost.channel} • {selectedPost.scheduled_time}
              </span>
            </div>

            {/* Title & Copy */}
            <div className="space-y-1.5 text-xs">
              <div className="font-mono text-[10px] text-slate-400">{selectedPost.date_str}</div>
              <h4 className="font-bold text-slate-900 text-sm leading-snug">
                {selectedPost.title}
              </h4>
              <p className="text-slate-600 line-clamp-3 leading-relaxed text-[11px] pt-1">
                {selectedPost.copy}
              </p>
            </div>

            {/* Compliance Guard score dial */}
            <div className="p-3 rounded-xl bg-[#F2F3FF] flex items-center justify-between text-xs">
              <div>
                <span className="text-slate-500 text-[10px] font-mono block">Điểm tuân thủ quy chế</span>
                <span className="text-xl font-bold font-mono text-slate-900">
                  {selectedPost.compliance_score}<span className="text-xs text-slate-400">/100</span>
                </span>
              </div>
              <span className={`px-2 py-1 rounded-lg text-xs font-bold font-mono ${
                selectedPost.compliance_score >= 95 ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
              }`}>
                {selectedPost.compliance_score >= 95 ? 'Brand Safe' : 'Cần chú ý'}
              </span>
            </div>

            {/* Action buttons */}
            <div className="space-y-2 pt-2 border-t border-slate-100">
              {publishedPosts[selectedPost.id] ? (
                <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs space-y-1 text-emerald-800 font-medium">
                  <div className="flex items-center gap-1.5 font-bold">
                    <CheckCircle className="w-4 h-4 text-emerald-600" />
                    <span>Đã phát sóng lúc {publishedPosts[selectedPost.id].published_at}</span>
                  </div>
                  <a 
                    href={publishedPosts[selectedPost.id].post_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-indigo-600 hover:underline flex items-center gap-1 text-[11px]"
                  >
                    <ExternalLink className="w-3 h-3" /> Xem bài đăng trực tiếp
                  </a>
                </div>
              ) : (
                <>
                  <button
                    onClick={() => handlePublishNow(selectedPost.id)}
                    className="w-full py-2.5 px-4 rounded-xl bg-[#059669] hover:bg-[#047857] text-white font-bold text-xs flex items-center justify-center gap-2 shadow-xs transition active:scale-95"
                  >
                    <Send className="w-3.5 h-3.5" />
                    <span>⚡ Phát sóng tức thì (Publish Now)</span>
                  </button>

                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <button
                      onClick={() => handleApprove(selectedPost.id)}
                      className="py-2 px-3 rounded-xl border border-slate-200 hover:bg-slate-50 font-bold text-slate-700 flex items-center justify-center gap-1 transition"
                    >
                      <Check className="w-3.5 h-3.5 text-emerald-600" />
                      <span>Duyệt bài</span>
                    </button>
                    <button
                      onClick={onNavigateToStudio}
                      className="py-2 px-3 rounded-xl bg-indigo-50 hover:bg-indigo-100 text-[#3525CD] font-bold flex items-center justify-center gap-1 transition border border-indigo-200"
                    >
                      <Edit3 className="w-3.5 h-3.5" />
                      <span>Mở Studio</span>
                    </button>
                  </div>
                </>
              )}
            </div>

          </div>

        </div>
      ) : (
        /* VIEW MODE 2: TIMELINE / LIST VIEW */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredPosts.map(post => {
            const isPublished = !!publishedPosts[post.id];
            return (
              <div 
                key={post.id}
                className="bg-white rounded-2xl border border-slate-200/90 shadow-2xs hover:shadow-md transition-all p-5 flex flex-col justify-between space-y-3"
              >
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <div className="flex items-center gap-2">
                      <span className="bg-indigo-50 text-indigo-700 font-bold px-2 py-0.5 rounded text-[10px]">
                        {post.stage}
                      </span>
                      <span className="text-slate-400 font-medium">#{post.channel}</span>
                    </div>
                    <span className="text-slate-500 font-semibold">{post.date_str}</span>
                  </div>

                  <div className="flex gap-3 items-start">
                    <img 
                      src={post.media_url} 
                      alt="Thumbnail" 
                      className="w-16 h-16 rounded-xl object-cover shrink-0 border border-slate-200" 
                    />
                    <div>
                      <h4 className="font-bold text-sm text-slate-900 leading-snug">{post.title}</h4>
                      <p className="text-xs text-slate-500 line-clamp-2 mt-1">{post.copy}</p>
                    </div>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-1.5 font-mono">
                    <span className="text-slate-400">Score:</span>
                    <span className="font-bold text-emerald-600">{post.compliance_score}/100</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <button 
                      onClick={onNavigateToStudio}
                      className="text-xs font-bold text-indigo-600 hover:underline"
                    >
                      Mở Studio
                    </button>
                    <button
                      onClick={() => handlePublishNow(post.id)}
                      className="bg-[#4F46E5] hover:bg-[#4338CA] text-white font-bold text-xs px-3 py-1.5 rounded-lg shadow-xs transition"
                    >
                      ⚡ Đăng ngay
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

    </div>
  );
}
