import React, { useState } from 'react';
import { 
  Sparkles, 
  Check, 
  AlertTriangle, 
  Layers, 
  Wand2, 
  CheckCircle2, 
  RotateCcw, 
  ThumbsUp, 
  MessageCircle, 
  Share2, 
  ShieldCheck, 
  Eye, 
  Edit3, 
  XCircle,
  Video,
  Camera,
  Music,
  Bookmark,
  Heart,
  Send,
  Loader2,
  FileText,
  Users
} from 'lucide-react';

import { updatePostApi } from '../api';

// ── Local 3-layer compliance check (no API call needed for demo) ──
function runLocalComplianceCheck(content, postKind, disclosureLabel) {
  const findings = [];
  const text = (content || '').toLowerCase();

  // CORE-001: absolute commitment
  ['cam kết 100%', 'đảm bảo 100%', 'chắc chắn 100%'].forEach(kw => {
    if (text.includes(kw)) findings.push({
      rule_code: 'CORE-001', severity: 'critical', matched_text: kw,
      message: 'Cam kết tuyệt đối không có bằng chứng.',
      suggestion: 'Dùng: "có thể giúp cải thiện..."'
    });
  });

  // CORE-002: superlative language
  ['số 1', 'tốt nhất', 'duy nhất'].forEach(kw => {
    if (text.includes(kw)) findings.push({
      rule_code: 'CORE-002', severity: 'warning', matched_text: kw,
      message: 'Từ ngữ tuyệt đối yêu cầu bằng chứng.',
      suggestion: 'Thêm nguồn hoặc giải thích cụ thể.'
    });
  });

  // COS-001: medical treatment language
  ['chữa khỏi', 'trị dứt điểm', 'điều trị', 'thần dược'].forEach(kw => {
    if (text.includes(kw)) findings.push({
      rule_code: 'COS-001', severity: 'critical', matched_text: kw,
      message: 'Ngôn ngữ điều trị bệnh không được dùng cho mỹ phẩm.',
      suggestion: 'Dùng: "giúp làm dịu", "hỗ trợ cải thiện"'
    });
  });

  // CORE-003: missing disclosure label
  if ((postKind === 'paid_ad' || postKind === 'creator_partnership') && !disclosureLabel) {
    findings.push({
      rule_code: 'CORE-003', severity: 'critical', matched_text: '(thiếu nhãn)',
      message: 'Bài có quan hệ thương mại phải có nhãn quảng cáo.',
      suggestion: 'Thêm #QuảngCáo hoặc "Nội dung được tài trợ"'
    });
  }

  const nCritical = findings.filter(f => f.severity === 'critical').length;
  const nWarning  = findings.filter(f => f.severity === 'warning').length;
  const score     = Math.max(0, 100 - 40 * nCritical - 10 * nWarning);
  const riskLevel = nCritical > 0 ? 'critical' : nWarning > 0 ? 'warning' : 'low';

  return { score, riskLevel, findings, nCritical };
}

// ── Severity badge styling map ──
const FINDING_STYLES = {
  critical: { border: 'border-rose-200',   bg: 'bg-rose-50/80',     codeBg: 'bg-rose-100 text-rose-700',   label: 'Nghiêm trọng' },
  warning:  { border: 'border-amber-200', bg: 'bg-amber-50/80',   codeBg: 'bg-amber-100 text-amber-700', label: 'Cảnh báo' },
  info:     { border: 'border-indigo-200', bg: 'bg-indigo-50/80',  codeBg: 'bg-indigo-100 text-indigo-700', label: 'Lưu ý' },
};

const SCORE_STYLES = {
  critical: 'bg-red-600 text-white',
  warning:  'bg-amber-500 text-white',
  low:      'bg-emerald-600 text-white',
};

export default function StudioCanvas({ currentCampaign, onApprovePost, isApproved, setIsApproved }) {
  const [activeChannel, setActiveChannel] = useState('Facebook Feed');
  const [zoomLevel, setZoomLevel] = useState(100);
  const [hasAppliedFix, setHasAppliedFix] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [isRunningPipeline, setIsRunningPipeline] = useState(false);
  const [pipelineStep, setPipelineStep] = useState(0);
  const [complianceResult, setComplianceResult] = useState(null);
  const [postKind, setPostKind] = useState('organic');
  const [disclosureLabel, setDisclosureLabel] = useState('');

  // Editable post content state
  const [postContent, setPostContent] = useState({
    title: 'Giải Pháp Phục Hồi Làn Da Nhạy Cảm 2026',
    hook: 'Đánh thức làn da căng bóng chuẩn thủy tinh chỉ sau 14 ngày cùng Siêu Tinh Chất Phục Hồi PureGlow Serum 2026!',
    body: 'Công thức Niacinamide 10% kết hợp Ceramide tinh khiết giúp củng cố hàng rào ẩm tự nhiên.',
    forbiddenPart: 'cam kết 100%',
    safePart: 'đã được kiểm nghiệm hỗ trợ phục hồi rõ rệt',
    tail: 'phục hồi cấu trúc da chỉ sau liệu trình đầu tiên mà không gây kích ứng! ✨💧',
    hashtags: ['#PureGlowVN', '#SerumPureGlow', '#PhucHoiDa', '#KhoaHocLanDa', '#Chamsocda2026']
  });

  // Apply AI optimization fix and sync with DB
  const handleApplyFix = async () => {
    const nextFix = !hasAppliedFix;
    setHasAppliedFix(nextFix);
    try {
      await updatePostApi(74, {
        compliance_score: nextFix ? 98 : 88,
        content: nextFix
          ? `${postContent.hook}\n${postContent.body} ${postContent.safePart} ${postContent.tail}\n${postContent.hashtags.join(' ')}`
          : `${postContent.hook}\n${postContent.body} ${postContent.forbiddenPart} ${postContent.tail}\n${postContent.hashtags.join(' ')}`
      });
    } catch (e) {
      console.warn('Sync post fix error:', e);
    }
  };

  const handleSaveEdit = async () => {
    setShowEditModal(false);
    try {
      await updatePostApi(74, {
        content: `${postContent.hook}\n${postContent.body}\n${postContent.hashtags.join(' ')}`
      });
    } catch (e) {
      console.warn('Sync post edit error:', e);
    }
  };

  // Run Agent Suite Simulation
  const handleRunPipeline = () => {
    setIsRunningPipeline(true);
    setPipelineStep(1);
    setTimeout(() => setPipelineStep(2), 1200);
    setTimeout(() => setPipelineStep(3), 2400);
    setTimeout(() => {
      setIsRunningPipeline(false);
      setPipelineStep(0);
      setHasAppliedFix(false);
      setIsApproved(false);
    }, 3600);
  };

  return (
    <div className="space-y-4">
      {/* ============================================================ */}
      {/* 3-COLUMN WORKBENCH: EXACT MATCH TO USER'S FIGMA SCREENSHOT  */}
      {/* ============================================================ */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        
        {/* ------------------------------------------------------------ */}
        {/* COLUMN 1 (LEFT 3 COLS): PIPELINE AGENTS & BRIEF PARAMETERS   */}
        {/* ------------------------------------------------------------ */}
        <div className="lg:col-span-3 space-y-4">
          <div className="bg-white rounded-2xl border border-slate-200/90 p-4 shadow-2xs space-y-4">
            
            {/* Header: PureGlow 2026 */}
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-base font-bold text-slate-900 leading-tight">
                  {currentCampaign?.name ? currentCampaign.name.replace('Chiến dịch ', '').slice(0, 18) : 'PureGlow 2026'}
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">Điều phối 3 Agents & ngữ cảnh</p>
              </div>
              <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-[10px] font-bold font-mono border border-emerald-200 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                Active
              </span>
            </div>

            {/* Pipeline Agents Section */}
            <div className="space-y-2 pt-1 border-t border-slate-100">
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                <span>Ma trận điều phối Agent</span>
                <span className="text-[10px] font-mono text-slate-400">3 Nodes Live</span>
              </div>

              {/* Agent 1 Card */}
              <div className={`p-2.5 rounded-xl border transition ${
                pipelineStep === 1 
                  ? 'bg-emerald-50 border-emerald-400 ring-2 ring-emerald-200' 
                  : 'bg-slate-50/90 border-slate-200/70'
              } flex items-start gap-2.5`}>
                <div className="w-6 h-6 rounded-md bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0 mt-0.5">
                  {pipelineStep === 1 ? <Loader2 className="w-3.5 h-3.5 animate-spin text-emerald-600" /> : <Check className="w-3.5 h-3.5 stroke-[3]" />}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-900 truncate">Agent 1: Market Intel</span>
                    <span className="text-[10px] font-bold text-emerald-600 bg-emerald-50 px-1.5 py-0.2 rounded border border-emerald-200">
                      {pipelineStep === 1 ? 'Đang chạy' : 'Done'}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-400 font-mono block mt-0.5">Insight dataset v4.1</span>
                </div>
              </div>

              {/* Agent 2 Card */}
              <div className={`p-2.5 rounded-xl border transition ${
                pipelineStep === 2 
                  ? 'bg-indigo-50 border-indigo-400 ring-2 ring-indigo-200' 
                  : 'bg-slate-50/90 border-slate-200/70'
              } flex items-start gap-2.5`}>
                <div className="w-6 h-6 rounded-md bg-indigo-100 text-indigo-700 flex items-center justify-center shrink-0 mt-0.5">
                  {pipelineStep === 2 ? <Loader2 className="w-3.5 h-3.5 animate-spin text-indigo-600" /> : <Layers className="w-3.5 h-3.5" />}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-900 truncate">Agent 2: Copywriter</span>
                    <span className="text-[10px] font-bold text-indigo-600 font-mono">
                      {pipelineStep === 2 ? 'Đang sinh' : '12 Posts'}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-400 font-mono block mt-0.5">Omnichannel generated</span>
                </div>
              </div>

              {/* Agent 3 Card */}
              <div className={`p-2.5 rounded-xl border transition ${
                pipelineStep === 3
                  ? 'bg-amber-50 border-amber-400 ring-2 ring-amber-200'
                  : hasAppliedFix
                  ? 'bg-emerald-50/50 border-emerald-200'
                  : 'bg-rose-50/50 border-rose-200/80'
              } flex items-start gap-2.5`}>
                <div className={`w-6 h-6 rounded-md flex items-center justify-center shrink-0 mt-0.5 ${
                  hasAppliedFix ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-600'
                }`}>
                  {pipelineStep === 3 ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : hasAppliedFix ? (
                    <Check className="w-3.5 h-3.5 stroke-[3]" />
                  ) : (
                    <AlertTriangle className="w-3.5 h-3.5" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-slate-900 truncate">Agent 3: Compliance</span>
                    <span className={`text-[10px] font-bold px-1.5 py-0.2 rounded border ${
                      hasAppliedFix 
                        ? 'text-emerald-700 bg-emerald-100 border-emerald-200' 
                        : 'text-rose-600 bg-rose-100/80 border-rose-200'
                    }`}>
                      {hasAppliedFix ? '0 Cảnh báo' : '1 Cảnh báo'}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-500 font-mono block mt-0.5">
                    {hasAppliedFix ? 'Đạt chuẩn 100% Brand Safe' : 'Từ cấm y tế & cam kết'}
                  </span>
                </div>
              </div>
            </div>

            {/* Tham Số Brief Section */}
            <div className="space-y-3 pt-2 border-t border-slate-100 text-xs">
              <span className="text-xs font-semibold text-slate-700 block">
                Tham số Brief chiến dịch
              </span>

              {/* Giọng điệu */}
              <div className="space-y-1">
                <span className="text-slate-500 text-[11px]">Giọng điệu thương hiệu</span>
                <div className="flex items-center justify-between p-2 rounded-xl bg-slate-50 border border-slate-200 font-semibold text-slate-800">
                  <span className="flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-indigo-600" /> Chuyên gia & Thân thiện
                  </span>
                  <span className="text-slate-400 text-xs">⇅</span>
                </div>
              </div>

              {/* Đối tượng mục tiêu */}
              <div className="space-y-1">
                <span className="text-slate-500 text-[11px]">Đối tượng mục tiêu</span>
                <div className="flex items-center justify-between p-2 rounded-xl bg-slate-50 border border-slate-200 font-medium text-slate-800">
                  <span>Phụ nữ 25-35 • Da nhạy cảm</span>
                  <Users className="w-3.5 h-3.5 text-slate-400" />
                </div>
              </div>

              {/* Từ cấm theo dõi */}
              <div className="space-y-1.5">
                <div className="flex justify-between items-center text-[11px]">
                  <span className="text-slate-500">Từ cấm theo dõi</span>
                  <span className="text-rose-600 font-mono font-bold">14 từ cấm</span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  <span className="px-2 py-0.5 rounded-md bg-rose-50 text-rose-600 text-[11px] font-semibold border border-rose-200/80">
                    trị dứt điểm
                  </span>
                  <span className="px-2 py-0.5 rounded-md bg-rose-100 text-rose-700 text-[11px] font-bold border border-rose-300">
                    cam kết 100%
                  </span>
                  <span className="px-2 py-0.5 rounded-md bg-rose-50 text-rose-600 text-[11px] font-semibold border border-rose-200/80">
                    thần dược
                  </span>
                  <span className="text-slate-400 text-[11px] self-center ml-1">+11 khác</span>
                </div>
              </div>
            </div>

            {/* Run Button at Bottom */}
            <div className="pt-2">
              <button 
                onClick={handleRunPipeline}
                disabled={isRunningPipeline}
                className="w-full bg-[#4F46E5] hover:bg-[#4338CA] text-white py-2.5 px-4 rounded-xl font-bold text-xs flex items-center justify-center gap-2 shadow-md shadow-indigo-500/25 transition active:scale-[0.98] disabled:opacity-75"
              >
                {isRunningPipeline ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Đang điều phối 3 Agent...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-3.5 h-3.5 fill-white" />
                    <span>Chạy lại Agent Suite</span>
                  </>
                )}
              </button>
              <div className="text-center font-mono text-[10px] text-slate-400 mt-1.5">
                Model: AuraOmni-Flash-2026
              </div>
            </div>

          </div>
        </div>

        {/* ------------------------------------------------------------ */}
        {/* COLUMN 2 (CENTER 6 COLS): SOCIAL PREVIEW & MOCKUP CANVAS    */}
        {/* ------------------------------------------------------------ */}
        <div className="lg:col-span-6 space-y-3">
          
          {/* Top Channel Bar */}
          <div className="flex items-center justify-between bg-white px-3 py-1.5 rounded-xl border border-slate-200/80 shadow-2xs">
            <div className="flex items-center gap-1">
              {[
                { id: 'Facebook Feed', icon: FileText, label: 'Facebook Feed' },
                { id: 'TikTok Script Card', icon: Video, label: 'TikTok Script Card' },
                { id: 'Instagram Carousel', icon: Layers, label: 'Instagram Carousel' }
              ].map(ch => {
                const isSelected = activeChannel === ch.id;
                const IconComponent = ch.icon;
                return (
                  <button
                    key={ch.id}
                    onClick={() => setActiveChannel(ch.id)}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                      isSelected ? 'bg-indigo-50 text-indigo-700 font-bold' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                    }`}
                  >
                    <IconComponent className="w-3.5 h-3.5" />
                    <span>{ch.label}</span>
                  </button>
                );
              })}
            </div>

            {/* Zoom Controls */}
            <div className="flex items-center gap-1 text-slate-500 text-xs">
              <div className="flex items-center bg-slate-50 px-2 py-1 rounded-md border border-slate-200 font-mono text-[11px]">
                <button onClick={() => setZoomLevel(z => Math.max(70, z - 10))} className="px-1 hover:text-slate-900">-</button>
                <span className="px-1.5 font-bold text-slate-700">{zoomLevel}%</span>
                <button onClick={() => setZoomLevel(z => Math.min(130, z + 10))} className="px-1 hover:text-slate-900">+</button>
              </div>
              <button className="flex items-center gap-1 px-2 py-1 hover:bg-slate-100 rounded text-xs text-slate-600 font-medium">
                <Eye className="w-3.5 h-3.5" />
                <span>Trực quan</span>
              </button>
            </div>
          </div>

          {/* DYNAMIC CHANNEL PREVIEW */}
          {activeChannel === 'Facebook Feed' && (
            <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden">
              {/* Header row */}
              <div className="p-4 flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-9 h-9 rounded-md bg-[#2563EB] text-white flex items-center justify-center font-bold text-xs tracking-wider">
                    PG
                  </div>
                  <div>
                    <div className="flex items-center gap-1">
                      <span className="font-bold text-sm text-slate-900">PureGlow VN</span>
                      <span className="w-3.5 h-3.5 rounded-full bg-[#2563EB] text-white flex items-center justify-center text-[9px] font-bold">✓</span>
                    </div>
                    <div className="text-[11px] text-slate-400 flex items-center gap-1">
                      <span>Vừa xong</span>
                      <span>•</span>
                      <span>🌐</span>
                    </div>
                  </div>
                </div>
                <span className="text-slate-400 font-bold px-2 cursor-pointer">•••</span>
              </div>

              {/* Post Caption */}
              <div className="px-4 pb-3 text-xs leading-relaxed text-slate-800 space-y-2">
                <p>
                  ✨ {postContent.hook}
                </p>
                <p>
                  {postContent.body}{' '}
                  {hasAppliedFix ? (
                    <span className="bg-emerald-100 text-emerald-800 font-bold px-1 rounded border border-emerald-300">
                      {postContent.safePart}
                    </span>
                  ) : (
                    <span className="bg-red-100 text-red-600 font-bold px-1 rounded border border-red-300 underline decoration-red-500">
                      {postContent.forbiddenPart}
                    </span>
                  )}{' '}
                  {postContent.tail}
                </p>
                <div className="text-[#2563EB] font-medium flex flex-wrap gap-1 text-[11px]">
                  {postContent.hashtags.map(h => <span key={h}>{h}</span>)}
                </div>
              </div>

              {/* Product Image Preview with Overlays */}
              <div className="relative bg-slate-900 overflow-hidden flex items-center justify-center">
                <img 
                  src="/pureglow_serum.png" 
                  alt="PureGlow Luxury Facial Serum" 
                  className="w-full object-cover object-center"
                />
              </div>

              {/* Reactions Count */}
              <div className="px-4 py-2 border-b border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                <div className="flex items-center gap-1.5">
                  <div className="flex -space-x-1">
                    <span className="w-4 h-4 rounded-full bg-blue-500 text-white flex items-center justify-center text-[8px]">👍</span>
                    <span className="w-4 h-4 rounded-full bg-red-500 text-white flex items-center justify-center text-[8px]">❤️</span>
                  </div>
                  <span className="font-medium text-slate-700 ml-1">2.4k lượt thích</span>
                </div>
                <div className="flex items-center gap-3">
                  <span>318 bình luận</span>
                  <span>•</span>
                  <span>86 lượt chia sẻ</span>
                </div>
              </div>

              {/* Action Bar */}
              <div className="grid grid-cols-3 py-1 text-xs text-slate-600 font-semibold border-b border-slate-100 text-center">
                <button className="py-2 flex items-center justify-center gap-1.5 hover:bg-slate-50 transition">
                  <ThumbsUp className="w-4 h-4" /> Thích
                </button>
                <button className="py-2 flex items-center justify-center gap-1.5 hover:bg-slate-50 transition">
                  <MessageCircle className="w-4 h-4" /> Bình luận
                </button>
                <button className="py-2 flex items-center justify-center gap-1.5 hover:bg-slate-50 transition">
                  <Share2 className="w-4 h-4" /> Chia sẻ
                </button>
              </div>
            </div>
          )}

          {/* TIKTOK SCRIPT PREVIEW */}
          {activeChannel === 'TikTok Script Card' && (
            <div className="bg-slate-900 text-white rounded-2xl p-5 border border-slate-800 shadow-sm space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <Video className="w-4 h-4 text-pink-500" />
                  <span className="font-bold text-sm">Kịch bản Video TikTok (45s)</span>
                </div>
                <span className="text-[10px] font-mono bg-pink-500/20 text-pink-400 px-2 py-0.5 rounded border border-pink-500/30">
                  Hook Retention: 88%
                </span>
              </div>

              <div className="space-y-3 text-xs leading-relaxed">
                <div className="bg-white/5 p-3 rounded-xl border border-white/10 space-y-1">
                  <span className="text-[10px] font-mono text-cyan-400 font-bold">[00:00 - 00:05] HOOK GÂY TÒ MÒ:</span>
                  <p className="text-slate-300">"Da mẩn đỏ, căng rát mỗi khi giao mùa? Đừng vội mua kem dưỡng đắt tiền nếu chưa biết bí mật này!"</p>
                </div>

                <div className="bg-white/5 p-3 rounded-xl border border-white/10 space-y-1">
                  <span className="text-[10px] font-mono text-purple-400 font-bold">[00:05 - 00:30] BODY & DEMO:</span>
                  <p className="text-slate-300">Cận cảnh giọt Serum PureGlow thẩm thấu nhanh vào da. Thử nghiệm độ ẩm tăng từ 28% lên 76% ngay trên máy đo da liễu.</p>
                </div>

                <div className="bg-white/5 p-3 rounded-xl border border-white/10 space-y-1">
                  <span className="text-[10px] font-mono text-emerald-400 font-bold">[00:30 - 00:45] CALL TO ACTION:</span>
                  <p className="text-slate-300">"Bấm ngay vào giỏ hàng bên dưới để nhận voucher độc quyền 30% cho 50 người nhanh tay nhất hôm nay!"</p>
                </div>
              </div>

              <div className="flex items-center gap-2 pt-2 text-[11px] font-mono text-slate-400">
                <Music className="w-3.5 h-3.5 text-pink-400" />
                <span>Trending Sound: Lofi Skincare Chill Beat (120k videos)</span>
              </div>
            </div>
          )}

          {/* INSTAGRAM CAROUSEL PREVIEW */}
          {activeChannel === 'Instagram Carousel' && (
            <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm overflow-hidden p-4 space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <Camera className="w-4 h-4 text-purple-600" />
                  <span className="font-bold text-xs text-slate-900">Instagram Carousel (Slide 1/4)</span>
                </div>
                <div className="flex gap-1">
                  <span className="w-2 h-2 rounded-full bg-purple-600" />
                  <span className="w-2 h-2 rounded-full bg-slate-200" />
                  <span className="w-2 h-2 rounded-full bg-slate-200" />
                  <span className="w-2 h-2 rounded-full bg-slate-200" />
                </div>
              </div>

              <div className="aspect-square bg-slate-100 rounded-xl overflow-hidden relative">
                <img 
                  src="https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&auto=format&fit=crop&q=80" 
                  alt="Serum Botanical Texture" 
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent flex flex-col justify-end p-5 text-white">
                  <span className="text-[10px] font-mono uppercase tracking-widest text-emerald-300">CHĂM SÓC DA KHOA HỌC</span>
                  <h3 className="text-lg font-extrabold leading-snug">4 Bước Phục Hồi Hàng Rào Ẩm Chuẩn Y Khoa</h3>
                </div>
              </div>

              <div className="flex items-center justify-between pt-1 text-slate-700">
                <div className="flex items-center gap-4">
                  <Heart className="w-5 h-5 text-red-500 fill-red-500" />
                  <MessageCircle className="w-5 h-5" />
                  <Send className="w-5 h-5" />
                </div>
                <Bookmark className="w-5 h-5" />
              </div>
            </div>
          )}

          {/* Bottom Auto-Sync Status Bar */}
          <div className="flex items-center justify-center gap-2 text-[11px] font-mono text-slate-500 py-1">
            <span className="flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Auto-Sync FB & TikTok
            </span>
            <span>•</span>
            <span>Draft #12-Serum-PureGlow</span>
            <span>•</span>
            <span>Auto-saved 14:28:09</span>
          </div>

        </div>

        {/* ------------------------------------------------------------ */}
        {/* COLUMN 3 (RIGHT 3 COLS): COMPLIANCE GUARD INSPECTOR         */}
        {/* ------------------------------------------------------------ */}
        <div className="lg:col-span-3 space-y-4">
          <div className="bg-white rounded-2xl border border-slate-200/90 p-4 shadow-2xs space-y-4">
            
            {/* Header: Compliance Guard */}
            <div className="flex items-start justify-between pb-2 border-b border-slate-100">
              <div>
                <h3 className="text-base font-bold text-slate-900 leading-tight">
                  Kiểm định Tuân thủ
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">Sàng lọc từ cấm & an toàn thương hiệu</p>
              </div>
              <ShieldCheck className="w-5 h-5 text-indigo-600" />
            </div>

            {/* Compliance Score Dial */}
            <div className="space-y-1">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs text-slate-500 font-medium">Chỉ số tuân thủ</span>
                  <div className="text-3xl font-black text-slate-900 tracking-tight">
                    {hasAppliedFix ? '98' : '88'}<span className="text-sm font-bold text-slate-400">/100</span>
                  </div>
                </div>

                {/* Circular indicator */}
                <div className="relative w-14 h-14 flex items-center justify-center">
                  <svg className="w-14 h-14 -rotate-90" viewBox="0 0 36 36">
                    <path
                      className="text-slate-100"
                      strokeWidth="3.5"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      className={hasAppliedFix ? 'text-emerald-500' : 'text-indigo-600'}
                      strokeDasharray={`${hasAppliedFix ? 98 : 88}, 100`}
                      strokeWidth="3.5"
                      strokeLinecap="round"
                      stroke="currentColor"
                      fill="none"
                      d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center text-xs">
                    <Sparkles className="w-4 h-4 text-indigo-600" />
                  </div>
                </div>
              </div>
              
              <div className={`text-xs font-semibold flex items-center gap-1.5 ${
                hasAppliedFix ? 'text-emerald-700' : 'text-rose-600'
              }`}>
                {hasAppliedFix ? <CheckCircle2 className="w-3.5 h-3.5 shrink-0" /> : <AlertTriangle className="w-3.5 h-3.5 shrink-0" />}
                <span>{hasAppliedFix ? 'Đạt chuẩn an toàn thương hiệu 100%' : 'Phát hiện từ ngữ vi phạm'}</span>
              </div>
            </div>

            {/* Red Alert Card */}
            {!hasAppliedFix && (
              <div className="p-3 rounded-xl bg-rose-50/80 border border-rose-200 text-xs space-y-1">
                <div className="font-bold text-rose-700 flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                  <span>Phát hiện từ cấm tuyệt đối</span>
                </div>
                <p className="text-xs text-rose-600 leading-relaxed">
                  Cụm từ <strong>"cam kết 100%"</strong> vi phạm điều lệ quy chuẩn quảng cáo mỹ phẩm & bảo vệ người tiêu dùng.
                </p>
              </div>
            )}

            {/* AI Optimization Suggestion Card */}
            <div className="p-3 rounded-xl bg-indigo-50/70 border border-indigo-200/90 text-xs space-y-2">
              <div className="flex items-center justify-between font-bold">
                <span className="flex items-center gap-1.5 text-indigo-900">
                  <Wand2 className="w-3.5 h-3.5 text-indigo-600" />
                  Đề xuất AI Tối ưu an toàn
                </span>
                <span className="text-emerald-700 font-mono text-[10px] bg-emerald-100 px-1.5 py-0.2 rounded font-bold">
                  +10 Điểm
                </span>
              </div>

              <div className="space-y-1 text-xs">
                <div className="text-slate-500 font-mono text-[10px]">
                  BẢN GỐC (VI PHẠM):
                </div>
                <div className="text-rose-600 line-through font-medium">
                  "...cam kết 100% phục hồi..."
                </div>
                <div className="text-slate-500 font-mono text-[10px] pt-1">
                  ĐỀ XUẤT AN TOÀN:
                </div>
                <div className="text-emerald-700 font-semibold">
                  "...đã được kiểm nghiệm hỗ trợ phục hồi rõ rệt..."
                </div>
              </div>

              {/* Action Button: Áp dụng gợi ý ngay */}
              <button 
                onClick={handleApplyFix}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-3 rounded-xl font-semibold text-xs flex items-center justify-center gap-1.5 shadow-xs transition active:scale-[0.98] cursor-pointer"
              >
                <Wand2 className="w-3.5 h-3.5" />
                <span>{hasAppliedFix ? 'Khôi phục bản gốc ban đầu' : 'Áp dụng đề xuất an toàn'}</span>
              </button>
            </div>

            {/* Checklist: Hạng mục kiểm tra */}
            <div className="space-y-2 pt-1 border-t border-slate-100 text-xs">
              <div className="text-xs font-semibold text-slate-700">
                Hạng mục kiểm định tuân thủ
              </div>

              <div className="space-y-1.5">
                <div className="flex items-center justify-between text-[11px]">
                  <span className="flex items-center gap-1.5 text-slate-700">
                    <span className="text-emerald-600 font-bold">✔</span> Không chứa từ ngữ y tế cấm
                  </span>
                  <span className="text-emerald-600 font-bold font-mono">Đạt</span>
                </div>

                <div className="flex items-center justify-between text-[11px]">
                  <span className="flex items-center gap-1.5 text-slate-700">
                    <span className="text-emerald-600 font-bold">✔</span> Nhận diện thương hiệu & Logo
                  </span>
                  <span className="text-emerald-600 font-bold font-mono">Đạt</span>
                </div>

                <div className="flex items-center justify-between text-[11px]">
                  <span className="flex items-center gap-1.5 text-slate-700">
                    <span className="text-emerald-600 font-bold">✔</span> Đúng Tone 'Chuyên gia'
                  </span>
                  <span className="text-emerald-600 font-bold font-mono">94%</span>
                </div>

                <div className="flex items-center justify-between text-[11px]">
                  <span className="flex items-center gap-1.5 text-slate-700">
                    <span className={hasAppliedFix ? 'text-emerald-600 font-bold' : 'text-red-500 font-bold'}>
                      {hasAppliedFix ? '✔' : 'ⓘ'}
                    </span> Cam kết thái quá
                  </span>
                  <span className={hasAppliedFix ? 'text-emerald-600 font-bold font-mono' : 'text-red-500 font-bold font-mono'}>
                    {hasAppliedFix ? 'Đạt' : 'Phát hiện'}
                  </span>
                </div>
              </div>
            </div>

            {/* Decision Action Buttons */}
            <div className="space-y-2 pt-2 border-t border-slate-100">
              <button 
                onClick={() => {
                  setIsApproved(true);
                  if (onApprovePost) onApprovePost();
                }}
                className={`w-full py-2.5 px-4 rounded-xl font-bold text-xs flex items-center justify-center gap-2 shadow-sm transition active:scale-[0.98] ${
                  isApproved 
                    ? 'bg-emerald-700 text-white' 
                    : 'bg-[#059669] hover:bg-[#047857] text-white'
                }`}
              >
                <Check className="w-4 h-4" />
                <span>{isApproved ? 'Đã duyệt bài thành công ✓' : 'Duyệt bài (Approve)'}</span>
              </button>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <button 
                  onClick={() => setShowEditModal(true)}
                  className="py-2 px-2.5 rounded-xl border border-slate-200 text-slate-700 font-semibold hover:bg-slate-50 flex items-center justify-center gap-1 transition"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                  <span>Sửa nội dung</span>
                </button>
                <button 
                  onClick={() => setIsApproved(false)}
                  className="py-2 px-2.5 rounded-xl border border-slate-200 text-slate-700 font-semibold hover:bg-slate-50 flex items-center justify-center gap-1 transition"
                >
                  <XCircle className="w-3.5 h-3.5 text-slate-400" />
                  <span>Từ chối (Reject)</span>
                </button>
              </div>
            </div>

          </div>
        </div>

      </div>

      {/* Edit Content Modal */}
      {showEditModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 space-y-4 shadow-2xl border border-slate-100">
            <div className="flex justify-between items-center pb-2 border-b">
              <h3 className="font-bold text-base text-slate-900">Chỉnh sửa nội dung bản thảo</h3>
              <button onClick={() => setShowEditModal(false)} className="text-slate-400 hover:text-slate-600 font-bold">✕</button>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 block mb-1">Tiêu đề / Hook</label>
                <textarea 
                  rows="2"
                  value={postContent.hook}
                  onChange={(e) => setPostContent({ ...postContent, hook: e.target.value })}
                  className="w-full p-2.5 border rounded-lg focus:outline-none focus:border-indigo-500"
                />
              </div>
              <div>
                <label className="font-bold text-slate-700 block mb-1">Thân bài</label>
                <textarea 
                  rows="3"
                  value={postContent.body}
                  onChange={(e) => setPostContent({ ...postContent, body: e.target.value })}
                  className="w-full p-2.5 border rounded-lg focus:outline-none focus:border-indigo-500"
                />
              </div>
            </div>
            <div className="flex justify-end gap-2 pt-3 border-t">
              <button onClick={() => setShowEditModal(false)} className="px-4 py-2 border rounded-lg text-slate-600 text-xs font-bold">Hủy</button>
              <button onClick={handleSaveEdit} className="px-4 py-2 bg-[#4F46E5] text-white rounded-lg text-xs font-bold shadow">Lưu thay đổi</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
