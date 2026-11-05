import React, { useState } from 'react';
import { 
  Plus, 
  AlertTriangle, 
  CheckCircle2, 
  Save, 
  Trash2, 
  ShieldCheck, 
  Check, 
  Search,
  Sparkles,
  RefreshCw,
  FileText,
  Sliders,
  History,
  Activity,
  Layers,
  X
} from 'lucide-react';

export default function BrandRules() {
  const [activeRuleId, setActiveRuleId] = useState(1);
  const [newForbiddenWord, setNewForbiddenWord] = useState('');
  const [newMandatoryWord, setNewMandatoryWord] = useState('');
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [showAddRuleModal, setShowAddRuleModal] = useState(false);

  // Live test input state
  const [testText, setTestText] = useState('Serum PureGlow cam kết 100% trị dứt điểm kích ứng da chỉ sau 7 ngày!');
  const [testResult, setTestResult] = useState(null);

  const [ruleSets, setRuleSets] = useState([
    {
      id: 1,
      name: 'Quy định Dược Mỹ phẩm VN 2026',
      code: 'RULE-COSMETIC-VN',
      status: 'Active',
      description: 'Bộ quy tắc chuẩn hóa theo Bộ Y tế & Luật Dược. Tự động gắn cờ vi phạm cam kết tuyệt đối hóa.',
      forbidden_words: ['cam kết 100%', 'chữa khỏi hoàn toàn', 'đặc trị vĩnh viễn', 'số 1 Việt Nam', 'thần dược', 'trị dứt điểm'],
      mandatory_keywords: ['PureGlow', 'Serum B5', 'Phục hồi da', 'Đã kiểm nghiệm da liễu', 'Khoa học làn da', 'An toàn dịu nhẹ'],
      tone_of_voice: 'Chuyên gia & Thân thiện',
      compliance_threshold: 88
    },
    {
      id: 2,
      name: 'Tone of Voice Tinh tế & Chuyên gia',
      code: 'RULE-TONE-EXPERT',
      status: 'Standby',
      description: 'Dành riêng cho Whitepaper, Bác sĩ da liễu và các bài viết học thuật chuyên sâu.',
      forbidden_words: ['rẻ nhất', 'giá sốc', 'ôm hàng', 'cháy hàng', 'nhanh tay'],
      mandatory_keywords: ['Bác sĩ khuyên dùng', 'Chăm sóc khoa học', 'Củng cố màng ẩm', 'Nghiên cứu lâm sàng'],
      tone_of_voice: 'Tinh tế, Điềm đạm & Sang trọng',
      compliance_threshold: 90
    },
    {
      id: 3,
      name: 'Chiến dịch TikTok Viral GenZ',
      code: 'RULE-TIKTOK-GENZ',
      status: 'Active',
      description: 'Ngôn từ năng động, hạn chế biệt ngữ y khoa nặng nề, tập trung trải nghiệm 7 ngày mộc da.',
      forbidden_words: ['trước sau', 'before after', 'lột xác', 'giảm cân cấp tốc'],
      mandatory_keywords: ['Hiệu quả thực tế', 'Phù hợp mọi loại da', 'Glowy skin', 'Routine sáng da'],
      tone_of_voice: 'Trẻ trung, Năng lượng & Gần gũi',
      compliance_threshold: 80
    }
  ]);

  const selectedRule = ruleSets.find(r => r.id === activeRuleId) || ruleSets[0];

  const handleAddForbidden = (e) => {
    e.preventDefault();
    if (!newForbiddenWord.trim()) return;
    setRuleSets(prev => prev.map(r => {
      if (r.id === activeRuleId && !r.forbidden_words.includes(newForbiddenWord.trim())) {
        return { ...r, forbidden_words: [...r.forbidden_words, newForbiddenWord.trim()] };
      }
      return r;
    }));
    setNewForbiddenWord('');
  };

  const handleRemoveForbidden = (word) => {
    setRuleSets(prev => prev.map(r => {
      if (r.id === activeRuleId) {
        return { ...r, forbidden_words: r.forbidden_words.filter(w => w !== word) };
      }
      return r;
    }));
  };

  const handleAddMandatory = (e) => {
    e.preventDefault();
    if (!newMandatoryWord.trim()) return;
    setRuleSets(prev => prev.map(r => {
      if (r.id === activeRuleId && !r.mandatory_keywords.includes(newMandatoryWord.trim())) {
        return { ...r, mandatory_keywords: [...r.mandatory_keywords, newMandatoryWord.trim()] };
      }
      return r;
    }));
    setNewMandatoryWord('');
  };

  const handleRemoveMandatory = (word) => {
    setRuleSets(prev => prev.map(r => {
      if (r.id === activeRuleId) {
        return { ...r, mandatory_keywords: r.mandatory_keywords.filter(w => w !== word) };
      }
      return r;
    }));
  };

  const handleSave = () => {
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2500);
  };

  // Run live compliance check on testText
  const handleRunLiveTest = () => {
    const foundForbidden = selectedRule.forbidden_words.filter(w => 
      testText.toLowerCase().includes(w.toLowerCase())
    );
    const foundMandatory = selectedRule.mandatory_keywords.filter(w => 
      testText.toLowerCase().includes(w.toLowerCase())
    );

    let score = 100;
    score -= foundForbidden.length * 15;
    if (foundMandatory.length === 0) score -= 10;
    score = Math.max(0, Math.min(100, score));

    setTestResult({
      score,
      violations: foundForbidden,
      matches: foundMandatory,
      passed: score >= selectedRule.compliance_threshold
    });
  };

  return (
    <div className="space-y-6">
      
      {/* ------------------------------------------------------------ */}
      {/* TOP HEADER: BRAND RULES & GOVERNANCE                         */}
      {/* ------------------------------------------------------------ */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-3 border-b border-slate-200/80">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-[#3525CD] font-bold uppercase tracking-wider mb-1">
            <span>Brand Rules & Compliance Governance</span>
            <span className="w-1.5 h-1.5 rounded-full bg-slate-300" />
            <span className="text-slate-500 font-normal">SRS 3.2 · BRD-01..04</span>
          </div>
          <div className="flex items-baseline gap-3">
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
              Bộ Quy Tắc Thương Hiệu
            </h1>
            <span className="text-xs text-slate-500 hidden sm:inline">
              Kiểm soát thuật toán từ cấm, ngữ nghĩa pháp lý Dược phẩm và Tone of Voice đa kênh
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <div className="flex items-center gap-1.5 bg-[#EAEDFF] px-3 py-1.5 rounded-lg text-xs font-mono font-medium text-slate-800">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Neural Guard v4.8: Active</span>
          </div>

          <button 
            onClick={handleSave}
            className="inline-flex items-center gap-1.5 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-4 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition active:scale-95"
          >
            {savedSuccess ? <Check className="w-3.5 h-3.5" /> : <Save className="w-3.5 h-3.5" />}
            <span>{savedSuccess ? 'Đã lưu toàn hệ thống ✓' : 'Áp dụng toàn hệ thống'}</span>
          </button>
        </div>
      </div>

      {/* ------------------------------------------------------------ */}
      {/* MAIN LAYOUT: LEFT RULE-SET LIST & RIGHT RULE EDITOR          */}
      {/* ------------------------------------------------------------ */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left 4 Cols: Rule Sets & Performance Cards */}
        <div className="lg:col-span-4 space-y-4">
          
          {/* Rule Sets Container */}
          <div className="bg-white rounded-2xl border border-slate-200/90 p-4 shadow-2xs space-y-3">
            <div className="flex items-center justify-between pb-1">
              <span className="text-xs font-bold text-slate-700 uppercase font-mono tracking-wider flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-[#3525CD]" />
                BỘ QUY TẮC THƯƠNG HIỆU
              </span>
              <span className="text-[11px] font-mono text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                {ruleSets.length} bộ lọc
              </span>
            </div>

            {/* List of Rule Sets */}
            <div className="space-y-2">
              {ruleSets.map(rule => {
                const isSelected = rule.id === activeRuleId;
                return (
                  <div
                    key={rule.id}
                    onClick={() => setActiveRuleId(rule.id)}
                    className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                      isSelected 
                        ? 'bg-[#EAEDFF] border-[#3525CD] shadow-xs' 
                        : 'bg-white border-slate-200/80 hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <h4 className="font-bold text-slate-900 text-xs leading-snug">
                        {rule.name}
                      </h4>
                      <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-full ${
                        rule.status === 'Active' 
                          ? 'bg-emerald-100 text-emerald-800' 
                          : 'bg-slate-200 text-slate-700'
                      }`}>
                        {rule.status}
                      </span>
                    </div>

                    <p className="text-[11px] text-slate-500 line-clamp-2 leading-relaxed mb-2">
                      {rule.description}
                    </p>

                    <div className="flex items-center gap-3 text-[11px] font-mono text-slate-600 pt-1.5 border-t border-slate-200/60">
                      <span className="flex items-center gap-1 text-red-600 font-semibold">
                        <AlertTriangle className="w-3 h-3" />
                        {rule.forbidden_words.length} từ cấm
                      </span>
                      <span>•</span>
                      <span className="flex items-center gap-1 text-emerald-700 font-semibold">
                        <CheckCircle2 className="w-3 h-3" />
                        {rule.mandatory_keywords.length} từ khóa
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

            <button 
              onClick={() => {
                const newId = Date.now();
                const newRule = {
                  id: newId,
                  name: 'Quy tắc Mùa Sự Kiện Mới',
                  code: `RULE-EVT-${newId.toString().slice(-4)}`,
                  status: 'Active',
                  description: 'Bộ quy tắc tùy biến cho các đợt phát động chiến dịch tiếp thị ngắn hạn.',
                  forbidden_words: ['cam đoan', 'cam kết 100%'],
                  mandatory_keywords: ['Ưu đãi giới hạn', 'Chính hãng'],
                  tone_of_voice: 'Hào hứng & Thúc giục',
                  compliance_threshold: 85
                };
                setRuleSets([...ruleSets, newRule]);
                setActiveRuleId(newId);
              }}
              className="w-full py-2 bg-[#F2F3FF] hover:bg-indigo-100 text-[#3525CD] rounded-xl font-bold text-xs flex items-center justify-center gap-1.5 transition border border-indigo-200"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>+ Thêm bộ quy tắc mới</span>
            </button>
          </div>

          {/* Performance Card: Hiệu suất Guardrail */}
          <div className="bg-white rounded-2xl border border-slate-200/90 p-4 shadow-2xs space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-slate-900">Hiệu suất Guardrail</span>
              <Activity className="w-4 h-4 text-emerald-600" />
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-xl bg-[#F2F3FF] font-mono text-xs">
              <div>
                <span className="text-[10px] text-slate-500 block">Lượt quét 24h</span>
                <span className="text-lg font-bold text-slate-900">1,482</span>
              </div>
              <div className="text-right">
                <span className="text-emerald-700 font-bold block text-sm">✔ 99.4%</span>
                <span className="text-[10px] text-slate-500">Tuân thủ hoàn toàn</span>
              </div>
            </div>

            <div className="text-[11px] font-mono text-slate-500 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-[#3525CD]" />
              <span>LLM Engine: Gemini 1.5 Pro + Regulatory VectorDB</span>
            </div>
          </div>

          {/* Compliance Doc Reference Card */}
          <div className="rounded-2xl overflow-hidden bg-gradient-to-br from-indigo-900 to-slate-900 p-4 text-white space-y-2 shadow-xs">
            <div className="text-[10px] font-mono font-bold text-indigo-300 uppercase tracking-widest">
              BRD-COMPLIANCE-DOC
            </div>
            <h4 className="text-sm font-bold leading-snug">
              Bộ quy chuẩn Dược Mỹ Phẩm 2026
            </h4>
            <p className="text-[11px] text-slate-300 leading-relaxed">
              Tự động đồng bộ và cập nhật danh mục từ ngữ vi phạm cùng Cục Quản lý Dược Việt Nam.
            </p>
          </div>

        </div>

        {/* Right 8 Cols: Detailed Rule Editor & Live Tester */}
        <div className="lg:col-span-8 space-y-5">
          
          {/* Editor Card */}
          <div className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-2xs space-y-6">
            
            {/* Header info */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100">
              <div>
                <div className="text-[10px] font-mono font-bold text-[#3525CD] uppercase tracking-wider">
                  BRD-01: {selectedRule.status.toUpperCase()}
                </div>
                <h2 className="text-lg font-bold text-slate-900">
                  Cấu hình {selectedRule.name}
                </h2>
              </div>
              <div className="text-xs font-mono text-slate-500">
                Mã định danh: <strong className="text-slate-800">{selectedRule.code}</strong>
              </div>
            </div>

            {/* Negative Keywords (Blacklist / Từ cấm) */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                    <AlertTriangle className="w-4 h-4 text-red-500" />
                    Từ Cấm Tuyệt Đối (Negative Keywords / Blacklist)
                  </h4>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    Khi xuất hiện trong bản thảo, hệ thống sẽ báo đỏ và tự động gợi ý từ thay thế an toàn.
                  </p>
                </div>
                <span className="text-[11px] font-mono font-bold text-red-600 bg-red-50 px-2.5 py-0.5 rounded-full border border-red-200">
                  {selectedRule.forbidden_words.length} từ bị chặn
                </span>
              </div>

              {/* Tag Pills */}
              <div className="flex flex-wrap gap-2 p-3 rounded-xl bg-slate-50 border border-slate-200/80 min-h-[50px]">
                {selectedRule.forbidden_words.map(word => (
                  <span 
                    key={word}
                    className="inline-flex items-center gap-1.5 bg-red-100/90 text-red-800 border border-red-300 text-xs font-semibold px-2.5 py-1 rounded-lg shadow-2xs"
                  >
                    <span>{word}</span>
                    <button 
                      onClick={() => handleRemoveForbidden(word)}
                      className="hover:text-red-950 font-bold"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>

              {/* Add form */}
              <form onSubmit={handleAddForbidden} className="flex gap-2">
                <input
                  type="text"
                  placeholder="Nhập cụm từ cấm cần bổ sung (Ví dụ: cam kết 100%, khỏi hoàn toàn)..."
                  value={newForbiddenWord}
                  onChange={(e) => setNewForbiddenWord(e.target.value)}
                  className="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:bg-white transition"
                />
                <button
                  type="submit"
                  className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl font-bold text-xs shadow-xs transition active:scale-95"
                >
                  + Thêm từ cấm
                </button>
              </form>
            </div>

            {/* Mandatory Keywords (Whitelist / Từ bắt buộc) */}
            <div className="space-y-3 pt-3 border-t border-slate-100">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    Từ Khóa Bắt Buộc (Mandatory Keywords)
                  </h4>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    Các thuật ngữ khoa học và nhận diện thương hiệu cần có trong ít nhất 1 bài viết phễu Launch.
                  </p>
                </div>
                <span className="text-[11px] font-mono font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                  {selectedRule.mandatory_keywords.length} từ khóa
                </span>
              </div>

              {/* Tag Pills */}
              <div className="flex flex-wrap gap-2 p-3 rounded-xl bg-slate-50 border border-slate-200/80 min-h-[50px]">
                {selectedRule.mandatory_keywords.map(word => (
                  <span 
                    key={word}
                    className="inline-flex items-center gap-1.5 bg-emerald-100/90 text-emerald-800 border border-emerald-300 text-xs font-semibold px-2.5 py-1 rounded-lg shadow-2xs"
                  >
                    <span>{word}</span>
                    <button 
                      onClick={() => handleRemoveMandatory(word)}
                      className="hover:text-emerald-950 font-bold"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>

              {/* Add form */}
              <form onSubmit={handleAddMandatory} className="flex gap-2">
                <input
                  type="text"
                  placeholder="Nhập từ khóa bắt buộc cần bổ sung (Ví dụ: PureGlow, Serum B5)..."
                  value={newMandatoryWord}
                  onChange={(e) => setNewMandatoryWord(e.target.value)}
                  className="flex-1 px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:bg-white transition"
                />
                <button
                  type="submit"
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs shadow-xs transition active:scale-95"
                >
                  + Thêm từ khóa
                </button>
              </form>
            </div>

            {/* Tone of Voice & Compliance Threshold */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-3 border-t border-slate-100 text-xs">
              <div className="space-y-1">
                <label className="font-bold text-slate-800">Giọng Điệu Thương Hiệu (Tone of Voice)</label>
                <select
                  value={selectedRule.tone_of_voice}
                  onChange={(e) => {
                    const val = e.target.value;
                    setRuleSets(prev => prev.map(r => r.id === activeRuleId ? { ...r, tone_of_voice: val } : r));
                  }}
                  className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl font-semibold text-slate-800 focus:outline-none focus:border-indigo-500"
                >
                  <option value="Chuyên gia & Thân thiện">Chuyên gia & Thân thiện</option>
                  <option value="Tinh tế, Điềm đạm & Sang trọng">Tinh tế, Điềm đạm & Sang trọng</option>
                  <option value="Trẻ trung, Năng lượng & Gần gũi">Trẻ trung, Năng lượng & Gần gũi</option>
                  <option value="Khoa học Y khoa Chuyên sâu">Khoa học Y khoa Chuyên sâu</option>
                </select>
              </div>

              <div className="space-y-1">
                <div className="flex justify-between items-center">
                  <label className="font-bold text-slate-800">Điểm Đạt Chuẩn Tối Thiểu</label>
                  <span className="font-mono font-bold text-indigo-600">{selectedRule.compliance_threshold}/100</span>
                </div>
                <input
                  type="range"
                  min="70"
                  max="98"
                  value={selectedRule.compliance_threshold}
                  onChange={(e) => {
                    const val = Number(e.target.value);
                    setRuleSets(prev => prev.map(r => r.id === activeRuleId ? { ...r, compliance_threshold: val } : r));
                  }}
                  className="w-full mt-2 accent-indigo-600"
                />
              </div>
            </div>

          </div>

          {/* Interactive Live Compliance Tester */}
          <div className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-2xs space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-indigo-600" />
                <h3 className="font-bold text-xs text-slate-900 uppercase font-mono">
                  BỘ KIỂM THỬ TUÂN THỦ TỨC THÌ (LIVE COMPLIANCE TESTER)
                </h3>
              </div>
              <span className="text-[11px] font-mono text-slate-400">Kiểm tra ngay văn bản mẫu</span>
            </div>

            <textarea
              rows="3"
              value={testText}
              onChange={(e) => setTestText(e.target.value)}
              className="w-full p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-indigo-500 leading-relaxed font-sans"
              placeholder="Nhập hoặc dán nội dung quảng cáo để quét từ cấm..."
            />

            <div className="flex items-center justify-between">
              <button
                onClick={handleRunLiveTest}
                className="px-4 py-2 bg-[#3525CD] hover:bg-indigo-800 text-white rounded-xl font-bold text-xs flex items-center gap-1.5 shadow-xs transition active:scale-95"
              >
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Quét Tuân Thủ Ngay</span>
              </button>

              {testResult && (
                <div className="flex items-center gap-3 text-xs font-mono">
                  <span>Điểm: <strong className={testResult.passed ? 'text-emerald-600' : 'text-red-500'}>{testResult.score}/100</strong></span>
                  <span className={`px-2 py-0.5 rounded-full text-[11px] font-bold ${
                    testResult.passed ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-700'
                  }`}>
                    {testResult.passed ? '✔ Đạt chuẩn' : '⚠️ Vi phạm'}
                  </span>
                </div>
              )}
            </div>

            {testResult && testResult.violations.length > 0 && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-xs space-y-1">
                <div className="font-bold text-red-700 flex items-center gap-1">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>Phát hiện {testResult.violations.length} từ cấm:</span>
                </div>
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {testResult.violations.map(v => (
                    <span key={v} className="bg-red-200 text-red-900 font-bold px-2 py-0.5 rounded font-mono text-[11px]">
                      "{v}"
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

        </div>

      </div>

    </div>
  );
}
