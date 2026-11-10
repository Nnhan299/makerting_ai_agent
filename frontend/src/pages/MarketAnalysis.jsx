import React, { useState } from 'react';
import {
  BarChart2,
  Plus,
  Trash2,
  Download,
  Sparkles,
  ChevronRight,
  X,
  User,
  Globe,
  Target,
  Loader2,
  Zap,
  AlertTriangle,
  TrendingUp,
  ShieldCheck,
  Check,
  Copy
} from 'lucide-react';

// ── Helper: call AI job ─────────────────────────────────────────
async function callAiJob(agent, payload) {
  try {
    const res = await fetch('/api/ai-jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ agent, ...payload })
    });
    return res.ok ? await res.json() : null;
  } catch {
    return null;
  }
}

// ── SWOT Tab ─────────────────────────────────────────────────────
function SwotTab() {
  const [swot, setSwot] = useState({
    strengths: 'Công thức độc quyền Niacinamide 10% + Panthenol B5 5% phục hồi màng ẩm sinh học; giá thành cạnh tranh ($15,000 ngân sách).',
    weaknesses: 'Nhận diện thương hiệu mới, chưa có kênh phân phối trực tiếp chuỗi Guardian/Watsons.',
    opportunities: 'Xu hướng Skintellectual bùng nổ trên TikTok Shop; nhu cầu phục hồi da mụn nhạy cảm tăng cao.',
    threats: 'Cạnh tranh gay gắt từ hàng xách tay; siết chặt quy định quảng cáo Dược Mỹ phẩm VN 2026.'
  });
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState(null);
  const [copied, setCopied] = useState(false);

  const cells = [
    { key: 'strengths', label: 'Điểm mạnh (Strengths)', icon: <Zap className="w-4 h-4 text-emerald-600" />, badge: 'Nội tại', border: 'border-slate-200 focus-within:border-emerald-500' },
    { key: 'weaknesses', label: 'Điểm yếu (Weaknesses)', icon: <AlertTriangle className="w-4 h-4 text-amber-600" />, badge: 'Hạn chế', border: 'border-slate-200 focus-within:border-amber-500' },
    { key: 'opportunities', label: 'Cơ hội (Opportunities)', icon: <TrendingUp className="w-4 h-4 text-indigo-600" />, badge: 'Thị trường', border: 'border-slate-200 focus-within:border-indigo-500' },
    { key: 'threats', label: 'Thách thức (Threats)', icon: <ShieldCheck className="w-4 h-4 text-rose-600" />, badge: 'Rủi ro', border: 'border-slate-200 focus-within:border-rose-500' },
  ];

  const handleAiAnalyze = async () => {
    setAiLoading(true);
    setAiResult(null);
    const result = await callAiJob('market_intel', { type: 'swot', data: swot });
    setAiResult(result ? (result.output || result.message || 'Phân tích hoàn tất.') : 'Không thể kết nối AI.');
    setAiLoading(false);
  };

  const copyToClipboard = () => {
    if (!aiResult) return;
    navigator.clipboard.writeText(typeof aiResult === 'string' ? aiResult : JSON.stringify(aiResult, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cells.map(({ key, label, icon, badge, border }) => (
          <div key={key} className={`bg-white rounded-xl border ${border} p-4 transition shadow-2xs`}>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                {icon}
                <span className="text-xs font-bold text-slate-800">{label}</span>
              </div>
              <span className="text-[10px] font-medium text-slate-400 bg-slate-100 px-2 py-0.5 rounded-full">{badge}</span>
            </div>
            <textarea
              rows="4"
              placeholder={`Nhập ${label.toLowerCase()}...`}
              value={swot[key]}
              onChange={(e) => setSwot({ ...swot, [key]: e.target.value })}
              className="w-full text-xs text-slate-700 placeholder-slate-400 focus:outline-none resize-none leading-relaxed"
            />
          </div>
        ))}
      </div>

      <div className="flex items-center justify-between pt-1">
        <div className="flex items-center gap-2">
          <button
            onClick={handleAiAnalyze}
            disabled={aiLoading}
            className="inline-flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white px-3.5 py-2 rounded-lg font-semibold text-xs shadow-xs transition cursor-pointer"
          >
            {aiLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
            AI Phân tích SWOT
          </button>
          <button
            onClick={() => {
              const blob = new Blob([JSON.stringify(swot, null, 2)], { type: 'application/json' });
              const url = URL.createObjectURL(blob);
              const a = document.createElement('a'); a.href = url; a.download = 'swot-analysis.json'; a.click();
            }}
            className="inline-flex items-center gap-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 px-3 py-2 rounded-lg font-semibold text-xs transition cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" /> Xuất JSON
          </button>
        </div>
      </div>

      {aiResult && (
        <div className="bg-white border border-indigo-100 rounded-xl p-4 shadow-sm space-y-2">
          <div className="flex items-center justify-between border-b border-slate-100 pb-2">
            <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-700">
              <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
              <span>Báo cáo Chiến lược SWOT từ Agent 01</span>
            </div>
            <button
              onClick={copyToClipboard}
              className="inline-flex items-center gap-1 text-[11px] text-slate-500 hover:text-slate-800 transition"
            >
              {copied ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
              <span>{copied ? 'Đã sao chép' : 'Sao chép'}</span>
            </button>
          </div>
          <div className="text-xs text-slate-700 whitespace-pre-line leading-relaxed font-sans">
            {typeof aiResult === 'string' ? aiResult : JSON.stringify(aiResult, null, 2)}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Competitor Tab ────────────────────────────────────────────────
const DEFAULT_COMPETITORS = [
  { id: 1, name: 'La Roche-Posay (B5)', positioning: 'Dược mỹ phẩm cao cấp', channels: 'Shopee Mall, Bệnh viện', strengths: 'Uy tín lâm sàng, bác sĩ tin dùng', weaknesses: 'Giá cao (450k-600k), hàng xách tay giả nhiều', data_source: 'Social Blade & TMĐT' },
  { id: 2, name: 'The Ordinary (Niacinamide)', positioning: 'Tối giản nồng độ cao', channels: 'TikTok Shop, Xách tay', strengths: 'Giá rẻ, nồng độ cao', weaknesses: 'Dễ châm chích, nhiều hàng nhái', data_source: 'KOL Reviews' },
  { id: 3, name: 'Cocoon Vietnam', positioning: 'Mỹ phẩm thuần chay bản địa', channels: 'Watsons, Hasaki, Shopee', strengths: 'Câu chuyện thương hiệu hay, phủ điểm bán tốt', weaknesses: 'Chưa tập trung sâu vào phục hồi màng ẩm', data_source: 'Báo cáo ngành 2025' }
];

function CompetitorTab() {
  const [competitors, setCompetitors] = useState(DEFAULT_COMPETITORS);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState(null);

  const addRow = () => setCompetitors(prev => [...prev, { id: Date.now(), name: '', positioning: '', channels: '', strengths: '', weaknesses: '', data_source: '' }]);
  const removeRow = (id) => setCompetitors(prev => prev.filter(c => c.id !== id));
  const updateRow = (id, field, value) =>
    setCompetitors(prev => prev.map(c => c.id === id ? { ...c, [field]: value } : c));

  const handleAiAnalyze = async () => {
    setAiLoading(true);
    setAiResult(null);
    const result = await callAiJob('market_intel', { type: 'competitor', data: competitors });
    setAiResult(result ? (result.output || result.message || 'Phân tích hoàn tất.') : 'Không thể kết nối AI.');
    setAiLoading(false);
  };

  return (
    <div className="space-y-4">
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="bg-slate-50/80 border-b border-slate-200 text-slate-500 font-semibold">
                <th className="px-3 py-2.5 text-left w-36">Đối thủ</th>
                <th className="px-3 py-2.5 text-left w-32">Định vị</th>
                <th className="px-3 py-2.5 text-left w-36">Kênh phân phối</th>
                <th className="px-3 py-2.5 text-left">Điểm mạnh</th>
                <th className="px-3 py-2.5 text-left">Điểm yếu</th>
                <th className="px-3 py-2.5 text-left w-32">Nguồn data</th>
                <th className="px-2 py-2.5 w-10"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {competitors.map((comp) => (
                <tr key={comp.id} className="hover:bg-slate-50/50 transition">
                  <td className="p-2">
                    <input
                      type="text"
                      placeholder="Tên đối thủ..."
                      value={comp.name}
                      onChange={e => updateRow(comp.id, 'name', e.target.value)}
                      className="w-full p-1.5 border border-slate-200 rounded-lg text-xs font-semibold text-slate-800 focus:outline-none focus:border-indigo-500 bg-white"
                    />
                  </td>
                  <td className="p-2">
                    <input
                      type="text"
                      placeholder="Định vị..."
                      value={comp.positioning}
                      onChange={e => updateRow(comp.id, 'positioning', e.target.value)}
                      className="w-full p-1.5 border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:border-indigo-500 bg-white"
                    />
                  </td>
                  <td className="p-2">
                    <input
                      type="text"
                      placeholder="Kênh..."
                      value={comp.channels}
                      onChange={e => updateRow(comp.id, 'channels', e.target.value)}
                      className="w-full p-1.5 border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:border-indigo-500 bg-white"
                    />
                  </td>
                  <td className="p-2">
                    <input
                      type="text"
                      placeholder="Điểm mạnh..."
                      value={comp.strengths}
                      onChange={e => updateRow(comp.id, 'strengths', e.target.value)}
                      className="w-full p-1.5 border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:border-indigo-500 bg-white"
                    />
                  </td>
                  <td className="p-2">
                    <input
                      type="text"
                      placeholder="Điểm yếu..."
                      value={comp.weaknesses}
                      onChange={e => updateRow(comp.id, 'weaknesses', e.target.value)}
                      className="w-full p-1.5 border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:border-indigo-500 bg-white"
                    />
                  </td>
                  <td className="p-2">
                    <input
                      type="text"
                      placeholder="Nguồn..."
                      value={comp.data_source}
                      onChange={e => updateRow(comp.id, 'data_source', e.target.value)}
                      className="w-full p-1.5 border border-slate-200 rounded-lg text-xs text-slate-500 focus:outline-none focus:border-indigo-500 bg-white"
                    />
                  </td>
                  <td className="p-2 text-center">
                    <button onClick={() => removeRow(comp.id)} className="p-1 text-slate-400 hover:text-rose-600 transition">
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button onClick={addRow} className="inline-flex items-center gap-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 px-3 py-1.5 rounded-lg font-semibold text-xs transition cursor-pointer">
          <Plus className="w-3.5 h-3.5" /> Thêm đối thủ
        </button>
        <button
          onClick={handleAiAnalyze}
          disabled={aiLoading}
          className="inline-flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white px-3.5 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition cursor-pointer"
        >
          {aiLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
          AI Tìm Khoảng Trống Thị Trường
        </button>
      </div>

      {aiResult && (
        <div className="bg-white border border-indigo-100 rounded-xl p-4 shadow-sm space-y-2">
          <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-700 border-b border-slate-100 pb-2">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span>Phân tích Cạnh tranh & Khoảng trống Thị trường</span>
          </div>
          <div className="text-xs text-slate-700 whitespace-pre-line leading-relaxed font-sans">
            {typeof aiResult === 'string' ? aiResult : JSON.stringify(aiResult, null, 2)}
          </div>
        </div>
      )}
    </div>
  );
}

// ── STP Tab ───────────────────────────────────────────────────────
function StpTab() {
  const [stp, setStp] = useState({
    segment: 'Khách hàng thành thị 18 - 32 tuổi, da dầu mụn nhạy cảm hoặc treatment quá đà.',
    target: 'Gen Z & Millennial Skintellectuals: Mua hàng dựa trên bảng hoạt chất minh bạch và review khoa học.',
    positioning: 'Siêu tinh chất phục hồi màng ẩm sinh học chuẩn Dược mỹ phẩm với giá thành nội địa tiếp cận.',
  });

  const [personas, setPersonas] = useState([
    { id: 1, name: 'Nguyễn Hoàng My', age_range: '23–27', needs: 'Phục hồi màng ẩm sau mụn, không bóng nhờn', pain_points: 'Dùng treatment da khô rát, sợ kích ứng', channels: 'TikTok Shop, Instagram Reels' },
    { id: 2, name: 'Lê Tuấn Kiệt', age_range: '19–24', needs: 'Kiểm soát dầu thừa, dưỡng sáng vết thâm mụn', pain_points: 'Ngại quy trình nhiều bước, cần serum thấm nhanh', channels: 'Facebook Groups, YouTube Review' }
  ]);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState(null);

  const addPersona = () => setPersonas(prev => [...prev, { id: Date.now(), name: '', age_range: '', needs: '', pain_points: '', channels: '' }]);
  const removePersona = (id) => setPersonas(prev => prev.filter(p => p.id !== id));
  const updatePersona = (id, field, value) =>
    setPersonas(prev => prev.map(p => p.id === id ? { ...p, [field]: value } : p));

  const handleAiAnalyze = async () => {
    setAiLoading(true);
    setAiResult(null);
    const result = await callAiJob('market_intel', { type: 'stp', data: { stp, personas } });
    setAiResult(result ? (result.output || result.message || 'Phân tích hoàn tất.') : 'Không thể kết nối AI.');
    setAiLoading(false);
  };

  return (
    <div className="space-y-4">
      {/* 3 Pillars STP */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { key: 'segment', label: '1. Phân khúc (Segment)', desc: 'Tiêu chí địa lý, nhân khẩu học & hành vi', icon: <Globe className="w-4 h-4 text-indigo-600" /> },
          { key: 'target', label: '2. Thị trường mục tiêu (Target)', desc: 'Nhóm khách hàng cốt lõi tạo ra 80% doanh thu', icon: <Target className="w-4 h-4 text-indigo-600" /> },
          { key: 'positioning', label: '3. Định vị thương hiệu (Positioning)', desc: 'Lý do độc nhất để khách hàng lựa chọn bạn', icon: <BarChart2 className="w-4 h-4 text-indigo-600" /> },
        ].map(({ key, label, desc, icon }) => (
          <div key={key} className="bg-white border border-slate-200 rounded-xl p-4 shadow-2xs space-y-2">
            <div className="flex items-center gap-2">
              {icon}
              <span className="font-bold text-xs text-slate-800">{label}</span>
            </div>
            <p className="text-[11px] text-slate-400">{desc}</p>
            <textarea
              rows="3"
              value={stp[key]}
              onChange={e => setStp({ ...stp, [key]: e.target.value })}
              className="w-full border border-slate-200 rounded-lg p-2 text-xs text-slate-700 focus:outline-none focus:border-indigo-500 resize-none leading-relaxed"
            />
          </div>
        ))}
      </div>

      {/* Personas Section */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 space-y-3 shadow-2xs">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <User className="w-4 h-4 text-indigo-600" />
            <span className="font-bold text-xs text-slate-800">Chân dung Khách hàng Mục tiêu (Buyer Personas)</span>
          </div>
          <button onClick={addPersona} className="inline-flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-800 font-semibold transition cursor-pointer">
            <Plus className="w-3.5 h-3.5" /> Thêm Persona
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {personas.map((persona, idx) => (
            <div key={persona.id} className="border border-slate-200 rounded-xl p-3 bg-slate-50/40 relative space-y-2">
              <div className="flex items-center justify-between">
                <input
                  type="text"
                  placeholder="Tên Persona..."
                  value={persona.name || `Persona #${idx + 1}`}
                  onChange={e => updatePersona(persona.id, 'name', e.target.value)}
                  className="font-bold text-xs text-slate-800 bg-transparent focus:outline-none border-b border-transparent focus:border-indigo-400 pb-0.5"
                />
                {personas.length > 1 && (
                  <button onClick={() => removePersona(persona.id)} className="text-slate-400 hover:text-rose-600 p-1">
                    <X className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-[10px] text-slate-400 uppercase font-semibold block">Độ tuổi</span>
                  <input
                    type="text"
                    value={persona.age_range}
                    onChange={e => updatePersona(persona.id, 'age_range', e.target.value)}
                    className="w-full p-1 bg-white border border-slate-200 rounded text-xs text-slate-700"
                  />
                </div>
                <div>
                  <span className="text-[10px] text-slate-400 uppercase font-semibold block">Kênh tiếp cận</span>
                  <input
                    type="text"
                    value={persona.channels}
                    onChange={e => updatePersona(persona.id, 'channels', e.target.value)}
                    className="w-full p-1 bg-white border border-slate-200 rounded text-xs text-slate-700"
                  />
                </div>
                <div className="col-span-2">
                  <span className="text-[10px] text-slate-400 uppercase font-semibold block">Nhu cầu chính</span>
                  <input
                    type="text"
                    value={persona.needs}
                    onChange={e => updatePersona(persona.id, 'needs', e.target.value)}
                    className="w-full p-1 bg-white border border-slate-200 rounded text-xs text-slate-700"
                  />
                </div>
                <div className="col-span-2">
                  <span className="text-[10px] text-slate-400 uppercase font-semibold block">Nỗi đau (Pain Points)</span>
                  <input
                    type="text"
                    value={persona.pain_points}
                    onChange={e => updatePersona(persona.id, 'pain_points', e.target.value)}
                    className="w-full p-1 bg-white border border-slate-200 rounded text-xs text-slate-700"
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex items-center gap-2">
        <button
          onClick={handleAiAnalyze}
          disabled={aiLoading}
          className="inline-flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white px-3.5 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition cursor-pointer"
        >
          {aiLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
          AI Tối ưu Chiến lược STP
        </button>
      </div>

      {aiResult && (
        <div className="bg-white border border-indigo-100 rounded-xl p-4 shadow-sm space-y-2">
          <div className="flex items-center gap-1.5 text-xs font-bold text-indigo-700 border-b border-slate-100 pb-2">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span>Đề xuất Tối ưu Phân khúc & Định vị từ AI</span>
          </div>
          <div className="text-xs text-slate-700 whitespace-pre-line leading-relaxed font-sans">
            {typeof aiResult === 'string' ? aiResult : JSON.stringify(aiResult, null, 2)}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────
const TABS = [
  { id: 'swot', label: 'Ma trận SWOT' },
  { id: 'competitor', label: 'Phân tích đối thủ' },
  { id: 'stp', label: 'Chiến lược STP & Persona' },
];

export default function MarketAnalysis() {
  const [activeTab, setActiveTab] = useState('swot');

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-200/80">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Phân tích Thị trường & Chiến lược</h1>
          <p className="text-xs text-slate-500 mt-0.5">Nghiên cứu ma trận cạnh tranh, phân khúc khách hàng và định vị thương hiệu trước khi lập chiến dịch.</p>
        </div>

        {/* Tab switcher */}
        <div className="flex items-center gap-1 bg-slate-100 p-0.5 rounded-xl border border-slate-200/60 self-start sm:self-auto">
          {TABS.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer select-none ${
                activeTab === tab.id
                  ? 'bg-white text-indigo-700 shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab content */}
      <div>
        {activeTab === 'swot' && <SwotTab />}
        {activeTab === 'competitor' && <CompetitorTab />}
        {activeTab === 'stp' && <StpTab />}
      </div>
    </div>
  );
}
