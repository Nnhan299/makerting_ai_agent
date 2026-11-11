import React, { useState, useEffect } from 'react';
import '../brand-rules.css';
import { 
  fetchBrandRules, 
  createBrandRuleApi, 
  updateBrandRuleApi 
} from '../api';

const COMPLIANCE_RULES = [
  { code: 'CORE-001', pack: 'core_ads_vn', severity: 'critical', name: 'Cam kết tuyệt đối', 
    keywords: ['cam kết 100%', 'đảm bảo 100%', 'chắc chắn 100%'],
    message: 'Cam kết tuyệt đối không có bằng chứng vi phạm quy định quảng cáo.',
    suggestion: 'Dùng: "có thể giúp cải thiện..." hoặc dẫn kết quả nghiên cứu cụ thể.' },
  { code: 'CORE-002', pack: 'core_ads_vn', severity: 'warning', name: 'Từ ngữ so sánh tuyệt đối',
    keywords: ['số 1', 'tốt nhất', 'duy nhất', 'hàng đầu'],
    message: 'Từ ngữ tuyệt đối yêu cầu bằng chứng kiểm chứng độc lập.',
    suggestion: 'Thêm nguồn: "theo khảo sát X" hoặc "được chứng nhận bởi..."' },
  { code: 'COS-001', pack: 'cosmetics_vn', severity: 'critical', name: 'Ngôn ngữ điều trị bệnh',
    keywords: ['chữa khỏi', 'trị dứt điểm', 'điều trị', 'chữa bệnh', 'thần dược'],
    message: 'Mỹ phẩm không được quảng cáo như thuốc điều trị bệnh.',
    suggestion: 'Dùng: "giúp làm dịu", "hỗ trợ cải thiện", "làm giảm biểu hiện"' },
  { code: 'COS-002', pack: 'cosmetics_vn', severity: 'critical', name: 'Thay thế thuốc',
    keywords: ['thay thế thuốc', 'không cần thuốc', 'hiệu quả hơn thuốc'],
    message: 'Nghiêm cấm gợi ý mỹ phẩm thay thế thuốc điều trị.',
    suggestion: 'Chỉ mô tả công dụng làm đẹp, không so sánh với thuốc.' },
  { code: 'COS-003', pack: 'cosmetics_vn', severity: 'warning', name: 'Trước/sau & chứng nhận',
    keywords: ['trước sau', 'kết quả thực tế', 'chứng minh lâm sàng'],
    message: 'Hình ảnh/số liệu trước-sau cần có bằng chứng kiểm chứng.',
    suggestion: 'Thêm: nguồn nghiên cứu, số mẫu thử, điều kiện đo lường.' },
  { code: 'CORE-003', pack: 'core_ads_vn', severity: 'critical', name: 'Thiếu nhãn quảng cáo',
    keywords: [],
    description: 'Bài paid_ad hoặc creator_partnership phải có nhãn "#QuảngCáo" hoặc "Nội dung tài trợ".',
    message: 'Nội dung có quan hệ thương mại phải công khai minh bạch.',
    suggestion: 'Thêm #QuảngCáo hoặc "Nội dung được tài trợ bởi [Thương hiệu]".' },
];

const SEVERITY_CONFIG = {
  critical: { icon: '●', label: 'Nghiêm trọng (Critical)', cls: 'compliance-rule-critical' },
  warning:  { icon: '▲', label: 'Cảnh báo (Warning)',  cls: 'compliance-rule-warning'  },
  info:     { icon: '◆', label: 'Lưu ý (Info)',      cls: 'compliance-rule-info'     },
};

const PACK_LABELS = {
  core_ads_vn: 'CORE (Mọi ngành)',
  cosmetics_vn: 'COSMETICS_VN (Mỹ phẩm)',
  brand: 'BRAND (Thương hiệu)',
};

export default function BrandRules() {
  const [activeRuleId, setActiveRuleId] = useState(1);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newRuleName, setNewRuleName] = useState('');
  const [newRuleDesc, setNewRuleDesc] = useState('');
  const [activeMainTab, setActiveMainTab] = useState('config'); // 'config' | 'compliance-rules'

  // Default rich rule sets matching user's HTML specification
  const [ruleSets, setRuleSets] = useState([
    {
      id: 1,
      code: 'RULE-BRD-01',
      name: 'Quy tắc Quảng cáo Việt Nam',
      status: 'Standby',
      description: 'Kiểm định từ ngữ tuyệt đối hóa theo Luật Quảng cáo số 16/2012/QH13 & Nghị định 38/2021.',
      scope: 'Facebook Ads, TikTok Shop, Landing Page',
      forbidden_list: [
        { word: 'tốt nhất', suggest: 'tối ưu' },
        { word: 'số 1', suggest: 'hàng đầu' },
        { word: 'duy nhất', suggest: 'chuyên biệt' },
        { word: 'cam kết', suggest: 'hỗ trợ' },
        { word: 'đảm bảo 100%', suggest: 'hiệu quả kiểm nghiệm' },
        { word: 'cam kết 100%', suggest: 'hỗ trợ phục hồi rõ rệt' },
        { word: 'trị dứt điểm', suggest: 'làm dịu chuyên sâu' }
      ],
      mandatory_list: [
        { word: 'PureGlow', type: 'Brand' },
        { word: 'Serum B5', type: 'Hoạt chất' },
        { word: 'Phục hồi da', type: 'Công dụng' }
      ],
      tone_of_voice: 'expert-friendly',
      compliance_threshold: 88
    },
    {
      id: 2,
      code: 'RULE-BRD-02',
      name: 'Quy tắc ngành Mỹ phẩm & Dược mỹ phẩm',
      status: 'Active',
      description: 'Kiểm soát tuyên bố công dụng (Cosmetic Claims), tránh gây hiểu nhầm sản phẩm là thuốc điều trị.',
      scope: 'Tất cả bài đăng & Kịch bản Video',
      forbidden_list: [
        { word: 'chữa khỏi hoàn toàn', suggest: 'hỗ trợ cải thiện' },
        { word: 'đặc trị vĩnh viễn', suggest: 'chăm sóc chuyên sâu' },
        { word: 'thần dược', suggest: 'tinh chất phục hồi' },
        { word: 'trị dứt điểm', suggest: 'giảm thiểu rõ rệt' },
        { word: 'khỏi mụn sau 24h', suggest: 'hỗ trợ gom cồi mụn' },
        { word: 'tận gốc', suggest: 'chăm sóc tận màng ẩm' },
        { word: 'cam kết 100%', suggest: 'được kiểm nghiệm da liễu' }
      ],
      mandatory_list: [
        { word: 'PureGlow', type: 'Brand' },
        { word: 'Đã kiểm nghiệm da liễu', type: 'Chứng nhận' }
      ],
      tone_of_voice: 'clinical',
      compliance_threshold: 90
    }
  ]);

  // Form input states for adding keywords
  const [forbiddenInput, setForbiddenInput] = useState('');
  const [replacementInput, setReplacementInput] = useState('');
  const [mandatoryInput, setMandatoryInput] = useState('');

  // Live Tester State
  const [complianceText, setComplianceText] = useState('Serum PureGlow cam kết 100% trị dứt điểm kích ứng da chỉ sau 7 ngày!');
  const [scanResult, setScanResult] = useState({
    scanned: true,
    score: 54,
    passed: false,
    violations: ['cam kết 100%', 'trị dứt điểm'],
    matchedMandatory: ['PureGlow'],
    missingMandatory: ['Serum B5', 'Phục hồi da'],
    rewrite: 'PureGlow Serum B5 hỗ trợ làm dịu kích ứng và phục hồi da hiệu quả, cảm nhận làn da khỏe hơn sau 7 ngày sử dụng.'
  });

  // Selected Rule helper
  const selectedRule = ruleSets.find(r => r.id === activeRuleId) || ruleSets[0];

  // Load from DB on mount
  useEffect(() => {
    async function loadDbRules() {
      const dbRules = await fetchBrandRules();
      if (dbRules && dbRules.length > 0) {
        // Merge DB data with rich frontend structure
        setRuleSets(prev => {
          const merged = [...prev];
          dbRules.forEach(dbr => {
            const existingIdx = merged.findIndex(r => r.id === dbr.id || r.name === dbr.name);
            const fbWords = Array.isArray(dbr.forbidden_words) 
              ? dbr.forbidden_words 
              : (dbr.forbidden_words || '').split(',').map(w => w.trim()).filter(Boolean);
            const mdWords = Array.isArray(dbr.mandatory_keywords)
              ? dbr.mandatory_keywords
              : (dbr.mandatory_keywords || '').split(',').map(w => w.trim()).filter(Boolean);

            const ruleObj = {
              id: dbr.id,
              code: dbr.code || `RULE-BRD-${String(dbr.id).padStart(2, '0')}`,
              name: dbr.name || dbr.rule_name || 'Quy tắc thương hiệu',
              status: dbr.status || 'Active',
              description: dbr.description || `Bộ quy tắc chuẩn thương hiệu ${dbr.name}`,
              scope: 'Facebook Ads, TikTok Shop, Landing Page',
              forbidden_list: fbWords.map(w => ({ word: w, suggest: 'tối ưu an toàn' })),
              mandatory_list: mdWords.map(w => ({ word: w, type: 'Brand' })),
              tone_of_voice: dbr.tone_of_voice || 'expert-friendly',
              compliance_threshold: dbr.compliance_threshold || 88
            };

            if (existingIdx >= 0) {
              merged[existingIdx] = { ...merged[existingIdx], ...ruleObj };
            } else {
              merged.push(ruleObj);
            }
          });
          return merged;
        });
      }
    }
    loadDbRules();
  }, []);

  // Run Real-time scanner whenever text or selected rule changes
  const runComplianceScan = (textToScan = complianceText) => {
    const textLower = textToScan.toLowerCase();
    const foundForbidden = [];
    selectedRule.forbidden_list.forEach(item => {
      if (textLower.includes(item.word.toLowerCase())) {
        foundForbidden.push(item.word);
      }
    });

    const matchedMandatory = [];
    const missingMandatory = [];
    selectedRule.mandatory_list.forEach(item => {
      if (textLower.includes(item.word.toLowerCase())) {
        matchedMandatory.push(item.word);
      } else {
        missingMandatory.push(item.word);
      }
    });

    let score = 100;
    score -= foundForbidden.length * 20;
    score -= missingMandatory.length * 8;
    score = Math.max(20, Math.min(100, score));

    const passed = score >= selectedRule.compliance_threshold;

    // AI Safe Rewrite generator
    let rewritten = textToScan;
    selectedRule.forbidden_list.forEach(item => {
      if (rewritten.toLowerCase().includes(item.word.toLowerCase())) {
        const regex = new RegExp(item.word, 'gi');
        rewritten = rewritten.replace(regex, item.suggest || 'hỗ trợ an toàn');
      }
    });

    setScanResult({
      scanned: true,
      score,
      passed,
      violations: foundForbidden,
      matchedMandatory,
      missingMandatory,
      rewrite: rewritten !== textToScan 
        ? rewritten 
        : 'PureGlow Serum B5 hỗ trợ làm dịu kích ứng và phục hồi da hiệu quả, cảm nhận làn da khỏe hơn sau 7 ngày sử dụng.'
    });
  };

  // Toggle active status
  const handleToggleStatus = async () => {
    const newStatus = selectedRule.status === 'Active' ? 'Standby' : 'Active';
    setRuleSets(prev => prev.map(r => r.id === activeRuleId ? { ...r, status: newStatus } : r));
    if (selectedRule.id) {
      await updateBrandRuleApi(selectedRule.id, {
        rule_name: selectedRule.name,
        forbidden_words: selectedRule.forbidden_list.map(f => f.word).join(', '),
        mandatory_keywords: selectedRule.mandatory_list.map(m => m.word).join(', '),
        status: newStatus
      });
    }
  };

  // Add Forbidden word
  const handleAddForbidden = (e) => {
    e.preventDefault();
    if (!forbiddenInput.trim()) return;
    const newWord = forbiddenInput.trim();
    const newSuggest = replacementInput.trim() || 'tối ưu';

    setRuleSets(prev => prev.map(r => {
      if (r.id === activeRuleId) {
        return {
          ...r,
          forbidden_list: [...r.forbidden_list, { word: newWord, suggest: newSuggest }]
        };
      }
      return r;
    }));

    setForbiddenInput('');
    setReplacementInput('');
    setTimeout(() => runComplianceScan(), 100);
  };

  // Remove Forbidden word
  const handleRemoveForbidden = (wordToRemove) => {
    setRuleSets(prev => prev.map(r => {
      if (r.id === activeRuleId) {
        return {
          ...r,
          forbidden_list: r.forbidden_list.filter(f => f.word !== wordToRemove)
        };
      }
      return r;
    }));
    setTimeout(() => runComplianceScan(), 100);
  };

  // Add Mandatory keyword
  const handleAddMandatory = (e) => {
    e.preventDefault();
    if (!mandatoryInput.trim()) return;
    const newKw = mandatoryInput.trim();

    setRuleSets(prev => prev.map(r => {
      if (r.id === activeRuleId) {
        return {
          ...r,
          mandatory_list: [...r.mandatory_list, { word: newKw, type: 'Thuật ngữ' }]
        };
      }
      return r;
    }));

    setMandatoryInput('');
    setTimeout(() => runComplianceScan(), 100);
  };

  // Remove Mandatory keyword
  const handleRemoveMandatory = (kwToRemove) => {
    setRuleSets(prev => prev.map(r => {
      if (r.id === activeRuleId) {
        return {
          ...r,
          mandatory_list: r.mandatory_list.filter(m => m.word !== kwToRemove)
        };
      }
      return r;
    }));
    setTimeout(() => runComplianceScan(), 100);
  };

  // Update Score Threshold
  const handleThresholdChange = (val) => {
    setRuleSets(prev => prev.map(r => r.id === activeRuleId ? { ...r, compliance_threshold: Number(val) } : r));
  };

  // Update Tone
  const handleToneChange = (val) => {
    setRuleSets(prev => prev.map(r => r.id === activeRuleId ? { ...r, tone_of_voice: val } : r));
  };

  // Export JSON configuration
  const handleExportJSON = () => {
    const configData = {
      project: 'AuraAI Marketing Intelligence',
      version: '2.4',
      exported_at: new Date().toISOString(),
      rule: selectedRule
    };
    const blob = new Blob([JSON.stringify(configData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AuraAI_BrandRule_${selectedRule.code}_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
  };

  // Apply to DB
  const handleApplyToSystem = async () => {
    setSavedSuccess(true);
    if (selectedRule.id) {
      await updateBrandRuleApi(selectedRule.id, {
        rule_name: selectedRule.name,
        forbidden_words: selectedRule.forbidden_list.map(f => f.word).join(', '),
        mandatory_keywords: selectedRule.mandatory_list.map(m => m.word).join(', '),
        tone_of_voice: selectedRule.tone_of_voice,
        compliance_threshold: selectedRule.compliance_threshold
      });
    }
    setTimeout(() => setSavedSuccess(false), 3000);
  };

  // Create new rule
  const handleCreateRule = async (e) => {
    e.preventDefault();
    if (!newRuleName.trim()) return;

    const newRule = {
      id: Date.now(),
      code: `RULE-BRD-${String(ruleSets.length + 1).padStart(2, '0')}`,
      name: newRuleName.trim(),
      status: 'Active',
      description: newRuleDesc.trim() || `Bộ quy tắc thương hiệu ${newRuleName.trim()}`,
      scope: 'Toàn bộ kênh phân phối',
      forbidden_list: [
        { word: 'cam kết 100%', suggest: 'được chứng minh' },
        { word: 'trị dứt điểm', suggest: 'hỗ trợ cải thiện' }
      ],
      mandatory_list: [
        { word: 'PureGlow', type: 'Brand' }
      ],
      tone_of_voice: 'expert-friendly',
      compliance_threshold: 88
    };

    setRuleSets([...ruleSets, newRule]);
    setActiveRuleId(newRule.id);
    setShowAddModal(false);
    setNewRuleName('');
    setNewRuleDesc('');

    await createBrandRuleApi({
      rule_name: newRule.name,
      forbidden_words: 'cam kết 100%, trị dứt điểm',
      mandatory_keywords: 'PureGlow',
      tone_of_voice: 'Chuyên gia & Thân thiện'
    });
  };

  // Calculate words and chars for counter
  const wordCount = complianceText.trim() ? complianceText.trim().split(/\s+/).length : 0;
  const charCount = complianceText.length;

  return (
    <div className="brd-page-container">

      {/* PAGE HEADER */}
      <section className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Quy Chuẩn Thương Hiệu & Tuân Thủ</h1>
          <p className="page-subtitle">
            Hệ thống sàng lọc tuân thủ 3 lớp: Luật quảng cáo cốt lõi, Quy chuẩn Dược mỹ phẩm và Tone of Voice thương hiệu
          </p>
        </div>

        <div className="page-header-actions">
          <div className="engine-badge">
            <span className="status-dot dot-green"></span>
            <span className="mono-text">Sàng lọc tuân thủ AI: Active</span>
          </div>
          
          <button className="btn btn-secondary" type="button" onClick={handleExportJSON}>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            <span>Xuất cấu hình JSON</span>
          </button>

          <button className="btn btn-primary" type="button" onClick={handleApplyToSystem}>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
              <polyline points="17 21 17 13 7 13 7 21"/>
              <polyline points="7 3 7 8 15 8"/>
            </svg>
            <span>{savedSuccess ? 'Đã áp dụng vào DB ✓' : 'Áp dụng toàn hệ thống'}</span>
          </button>
        </div>
      </section>

      {/* WORKSPACE GRID */}
      <div className="workspace-grid">

        {/* LEFT SIDEBAR */}
        <aside className="sidebar">

          {/* Rule Sets Card */}
          <div className="panel">
            <div className="panel-header">
              <div className="panel-title-group">
                <svg className="icon-brand" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                <h2 className="panel-title-sm">BỘ QUY TẮC THƯƠNG HIỆU</h2>
              </div>
              <span className="badge badge-neutral">{ruleSets.length} bộ lọc</span>
            </div>

            <div className="rule-list">
              {ruleSets.map(rule => {
                const isSelected = rule.id === activeRuleId;
                const isActiveStatus = rule.status === 'Active';
                return (
                  <div 
                    key={rule.id} 
                    className={`rule-card ${isSelected ? 'selected' : ''}`}
                    onClick={() => setActiveRuleId(rule.id)}
                    tabIndex={0}
                  >
                    <div className="rule-card-top">
                      <span className="rule-id mono-text">{rule.code}</span>
                      <span className={`badge ${isActiveStatus ? 'badge-success' : 'badge-warning'}`}>
                        {rule.status}
                      </span>
                    </div>
                    <h3 className="rule-name">{rule.name}</h3>
                    <p className="rule-desc">{rule.description}</p>
                    <div className="rule-metrics">
                      <span className="metric-item metric-danger">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
                          <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                        </svg>
                        {rule.forbidden_list.length} từ cấm
                      </span>
                      <span className="metric-sep">&bull;</span>
                      <span className="metric-item metric-success">
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                          <polyline points="22 4 12 14.01 9 11.01"/>
                        </svg>
                        {rule.mandatory_list.length} từ khóa
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>

            <button className="btn-add-rule" type="button" onClick={() => setShowAddModal(true)}>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              <span>Thêm bộ quy tắc mới</span>
            </button>
          </div>

          {/* Guardrail Performance Card */}
          <div className="panel">
            <div className="panel-header">
              <h2 className="panel-title-base">Hiệu suất Guardrail</h2>
              <svg className="icon-success" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
              </svg>
            </div>

            <div className="stats-box">
              <div className="stats-col">
                <span className="stats-label">Lượt quét 24h</span>
                <strong className="stats-value mono-text">1,482</strong>
              </div>
              <div className="stats-col stats-col-right">
                <span className="stats-rate mono-text">&#10003; 99.4%</span>
                <span className="stats-sub">Tuân thủ hoàn toàn</span>
              </div>
            </div>

            <div className="stats-breakdown">
              <div className="breakdown-row">
                <span>Tự động viết lại an toàn</span>
                <strong className="mono-text">142 bản thảo</strong>
              </div>
              <div className="breakdown-row">
                <span>Chặn vi phạm nghiêm trọng</span>
                <strong className="mono-text text-danger">9 bản thảo</strong>
              </div>
            </div>

            <div className="engine-footer mono-text">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L14.8 9.2L22 12L14.8 14.8L12 22L9.2 14.8L2 12L9.2 9.2L12 2Z"/>
              </svg>
              <span>LLM Engine: Gemini 1.5 Pro + Regulatory VectorDB</span>
            </div>
          </div>

          {/* Compliance Doc Promo Card */}
          <div className="compliance-banner">
            <div className="banner-eyebrow mono-text">BRD-COMPLIANCE-DOC</div>
            <h3 className="banner-title">Bộ quy chuẩn Dược Mỹ Phẩm 2026</h3>
            <p className="banner-desc">
              Tự động đồng bộ và cập nhật danh mục từ ngữ vi phạm cùng Cục Quản lý Dược Việt Nam (DAV).
            </p>
            <div className="banner-footer">
              <span className="mono-text">Cập nhật: Hôm nay, 08:30</span>
              <a href="#" className="banner-link">Xem tài liệu &rarr;</a>
            </div>
          </div>

        </aside>

        {/* RIGHT MAIN WORKSPACE */}
        <div className="main-content">

          {/* MAIN TAB SWITCHER */}
          <div className="main-tab-bar">
            <button
              className={`main-tab-btn ${activeMainTab === 'config' ? 'main-tab-active' : ''}`}
              onClick={() => setActiveMainTab('config')}
            >
              ⚙️ Cấu hình Brand Rule
            </button>
            <button
              className={`main-tab-btn ${activeMainTab === 'compliance-rules' ? 'main-tab-active' : ''}`}
              onClick={() => setActiveMainTab('compliance-rules')}
            >
              🛡️ Quy tắc tuân thủ
            </button>
          </div>

          {/* CONFIG TAB */}
          {activeMainTab === 'config' && (<>

          {/* RULE CONFIGURATION PANEL */}
          <section className="panel config-panel">
            {/* Config Header */}
            <div className="config-header">
              <div>
                <div className="config-meta">
                  <span className="badge badge-warning-outline mono-text">
                    {selectedRule.code} &bull; {selectedRule.status.toUpperCase()}
                  </span>
                  <span className="meta-scope">Áp dụng: {selectedRule.scope || 'Toàn bộ chiến dịch'}</span>
                </div>
                <h2 className="config-title">Cấu hình {selectedRule.name}</h2>
              </div>

              <div className="config-header-controls">
                <label className="toggle-control" htmlFor="ruleActiveToggle">
                  <span className="toggle-label">Kích hoạt bộ lọc</span>
                  <input 
                    type="checkbox" 
                    id="ruleActiveToggle" 
                    checked={selectedRule.status === 'Active'}
                    onChange={handleToggleStatus}
                  />
                  <span className="toggle-Track"></span>
                </label>
              </div>
            </div>

            <hr className="section-divider" />

            {/* SECTION 1: NEGATIVE KEYWORDS / BLACKLIST */}
            <div className="rule-section">
              <div className="section-head">
                <div className="section-head-left">
                  <div className="section-title-row">
                    <span className="icon-badge icon-badge-danger">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                        <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/>
                        <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                      </svg>
                    </span>
                    <h3 className="section-title">Từ Cấm Tuyệt Đối (Negative Keywords / Blacklist)</h3>
                  </div>
                  <p className="section-subtitle">
                    Khi xuất hiện trong bản thảo, hệ thống sẽ báo đỏ và tự động gợi ý cụm từ thay thế hợp lệ.
                  </p>
                </div>
                <span className="badge badge-danger-soft mono-text">
                  {selectedRule.forbidden_list.length} từ bị chặn
                </span>
              </div>

              {/* Tag Box with Replacement Logic */}
              <div className="tag-container tag-container-danger" id="blacklistContainer">
                {selectedRule.forbidden_list.map((item, idx) => (
                  <div key={idx} className="keyword-chip chip-danger">
                    <span className="chip-Forbidden">{item.word}</span>
                    <span className="chip-arrow">&rarr;</span>
                    <span className="chip-suggest">{item.suggest || 'tối ưu'}</span>
                    <button 
                      type="button" 
                      className="chip-remove" 
                      aria-label="Xóa"
                      onClick={() => handleRemoveForbidden(item.word)}
                    >
                      &times;
                    </button>
                  </div>
                ))}
              </div>

              {/* Logical Dual Input Row */}
              <form onSubmit={handleAddForbidden} className="input-group-row">
                <div className="input-wrapper">
                  <input
                    type="text"
                    id="forbiddenInput"
                    className="form-input"
                    value={forbiddenInput}
                    onChange={(e) => setForbiddenInput(e.target.value)}
                    placeholder="Nhập cụm từ cấm (VD: trị dứt điểm, khỏi hoàn toàn)..."
                  />
                </div>
                <div className="input-wrapper input-wrapper-sm">
                  <input
                    type="text"
                    id="replacementInput"
                    className="form-input"
                    value={replacementInput}
                    onChange={(e) => setReplacementInput(e.target.value)}
                    placeholder="Từ thay thế an toàn (VD: làm dịu da)..."
                  />
                </div>
                <button className="btn btn-danger" type="submit" id="addForbiddenBtn">
                  + Thêm từ cấm
                </button>
              </form>
            </div>

            <hr className="section-divider" />

            {/* SECTION 2: MANDATORY KEYWORDS */}
            <div className="rule-section">
              <div className="section-head">
                <div className="section-head-left">
                  <div className="section-title-row">
                    <span className="icon-badge icon-badge-success">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                        <polyline points="22 4 12 14.01 9 11.01"/>
                      </svg>
                    </span>
                    <h3 className="section-title">Từ Khóa Bắt Buộc (Mandatory Keywords)</h3>
                  </div>
                  <p className="section-subtitle">
                    Các thuật ngữ khoa học và nhận diện thương hiệu cần xuất hiện ít nhất 1 lần trong bài viết phễu Launch.
                  </p>
                </div>
                <span className="badge badge-success-soft mono-text">
                  {selectedRule.mandatory_list.length} từ khóa
                </span>
              </div>

              <div className="tag-container tag-container-success" id="mandatoryContainer">
                {selectedRule.mandatory_list.map((item, idx) => (
                  <div key={idx} className="keyword-chip chip-success">
                    <span>{item.word}</span>
                    <span className="chip-tag-type">{item.type || 'Thuật ngữ'}</span>
                    <button 
                      type="button" 
                      className="chip-remove" 
                      aria-label="Xóa"
                      onClick={() => handleRemoveMandatory(item.word)}
                    >
                      &times;
                    </button>
                  </div>
                ))}
              </div>

              <form onSubmit={handleAddMandatory} className="input-group-row">
                <div className="input-wrapper">
                  <input
                    type="text"
                    id="mandatoryInput"
                    className="form-input"
                    value={mandatoryInput}
                    onChange={(e) => setMandatoryInput(e.target.value)}
                    placeholder="Nhập từ khóa bắt buộc cần bổ sung (Ví dụ: Panthenol 5%, Cấp ẩm sâu)..."
                  />
                </div>
                <button className="btn btn-success" type="submit" id="addMandatoryBtn">
                  + Thêm từ khóa
                </button>
              </form>
            </div>

            <hr className="section-divider" />

            {/* SECTION 3: TONE OF VOICE & THRESHOLD SCORE */}
            <div className="parameters-grid">
              <div className="param-box">
                <label className="param-label" htmlFor="toneSelect">
                  Giọng Điệu Thương Hiệu (Tone of Voice)
                </label>
                <div className="select-wrapper">
                  <select 
                    id="toneSelect" 
                    className="form-select"
                    value={selectedRule.tone_of_voice || 'expert-friendly'}
                    onChange={(e) => handleToneChange(e.target.value)}
                  >
                    <option value="expert-friendly">Chuyên gia &amp; Thân thiện (Dermatological &amp; Empathetic)</option>
                    <option value="clinical">Khoa học Lâm sàng (Clinical &amp; Evidence-based)</option>
                    <option value="luxury">Cao cấp &amp; Tinh tế (Premium Skincare)</option>
                    <option value="genz">Trẻ trung &amp; Năng động (Gen Z Social)</option>
                  </select>
                </div>
                <span className="param-hint">Định hướng văn phong khi AI tự động viết lại câu vi phạm.</span>
              </div>

              <div className="param-box">
                <div className="slider-header">
                  <label className="param-label" htmlFor="scoreSlider">
                    Điểm Đạt Chuẩn Tối Thiểu (Auto-Pass Threshold)
                  </label>
                  <span className="score-pill mono-text" id="scoreValueDisplay">
                    {selectedRule.compliance_threshold} / 100
                  </span>
                </div>
                <input
                  type="range"
                  id="scoreSlider"
                  className="range-slider"
                  min="50"
                  max="100"
                  value={selectedRule.compliance_threshold}
                  onChange={(e) => handleThresholdChange(e.target.value)}
                />
                <div className="threshold-legend">
                  <span className="legend-item legend-danger">&lt; 70: Chặn tự động</span>
                  <span className="legend-item legend-warning">70–87: Duyệt thủ công</span>
                  <span className="legend-item legend-success">&ge; 88: Tự động duyệt</span>
                </div>
              </div>
            </div>
          </section>

          {/* LIVE COMPLIANCE TESTER PANEL */}
          <section className="panel tester-panel">
            <div className="tester-header">
              <div className="tester-title-group">
                <svg className="icon-brand" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L14.8 9.2L22 12L14.8 14.8L12 22L9.2 14.8L2 12L9.2 9.2L12 2Z"/>
                </svg>
                <h2 className="panel-title-sm">BỘ KIỂM THỬ TUÂN THỦ TỨC THÌ (LIVE COMPLIANCE TESTER)</h2>
              </div>

              <div className="sample-actions">
                <span className="sample-label">Mẫu thử nhanh:</span>
                <button 
                  type="button" 
                  className="btn-chip" 
                  id="loadViolationSample"
                  onClick={() => {
                    const sample = 'Serum PureGlow cam kết 100% trị dứt điểm kích ứng da chỉ sau 7 ngày!';
                    setComplianceText(sample);
                    runComplianceScan(sample);
                  }}
                >
                  Mẫu vi phạm
                </button>
                <button 
                  type="button" 
                  className="btn-chip" 
                  id="loadStandardSample"
                  onClick={() => {
                    const sample = 'PureGlow Serum B5 giúp cấp ẩm sâu, làm dịu nhanh và hỗ trợ phục hồi da nhạy cảm chỉ sau 7 ngày.';
                    setComplianceText(sample);
                    runComplianceScan(sample);
                  }}
                >
                  Mẫu đạt chuẩn
                </button>
              </div>
            </div>

            <div className="tester-body">
              {/* Input Column */}
              <div className="tester-input-col">
                <label htmlFor="complianceInput" className="sub-label">Bản thảo nội dung cần kiểm tra</label>
                <textarea 
                  id="complianceInput" 
                  className="tester-textarea" 
                  rows="4"
                  value={complianceText}
                  onChange={(e) => {
                    setComplianceText(e.target.value);
                  }}
                />

                <div className="tester-toolbar">
                  <span className="char-counter mono-text">
                    {charCount} ký tự &bull; {wordCount} từ
                  </span>
                  <button 
                    type="button" 
                    className="btn btn-primary" 
                    id="runScanBtn"
                    onClick={() => runComplianceScan()}
                  >
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                      <path d="m9 12 2 2 4-4"/>
                    </svg>
                    <span>Quét Tuân Thủ Ngay</span>
                  </button>
                </div>
              </div>

              {/* Diagnostic Output Column */}
              <div className="tester-result-col">
                <div className="result-header">
                  <div className="result-status-group">
                    <span className={`badge ${scanResult.passed ? 'badge-success' : 'badge-danger'}`}>
                      {scanResult.passed ? 'ĐẠT CHUẨN TUÂN THỦ' : 'VI PHẠM QUY TẮC'}
                    </span>
                    <span className="mono-text result-rule-ref">{selectedRule.code}</span>
                  </div>
                  <div className="result-score-box">
                    <span className="score-label">Điểm tuân thủ:</span>
                    <strong className={`score-number mono-text ${scanResult.passed ? 'score-pass' : 'score-fail'}`}>
                      {scanResult.score}/100
                    </strong>
                    <span className="score-req mono-text">
                      (Yêu cầu &ge; {selectedRule.compliance_threshold})
                    </span>
                  </div>
                </div>

                {/* Highlighted Violations & Missing Keywords */}
                <div className="diagnostic-list">
                  {scanResult.violations.length > 0 ? (
                    <div className="diag-item diag-danger">
                      <span className="diag-badge">
                        Từ cấm phát hiện ({scanResult.violations.length})
                      </span>
                      <p className="diag-text">
                        Phát hiện cụm từ vi phạm:&nbsp;
                        {scanResult.violations.map((v, i) => (
                          <span key={i}>
                            <mark className="hl-danger">{v}</mark>
                            {i < scanResult.violations.length - 1 ? ', ' : '.'}
                          </span>
                        ))}
                      </p>
                    </div>
                  ) : (
                    <div className="diag-item diag-success">
                      <span className="diag-badge">Từ cấm: An toàn</span>
                      <p className="diag-text">Không phát hiện từ ngữ tuyệt đối hóa hoặc vi phạm luật Dược mỹ phẩm.</p>
                    </div>
                  )}

                  <div className={`diag-item ${scanResult.missingMandatory.length > 0 ? 'diag-warning' : 'diag-success'}`}>
                    <span className="diag-badge">
                      Từ khóa bắt buộc ({scanResult.matchedMandatory.length}/{selectedRule.mandatory_list.length})
                    </span>
                    <p className="diag-text">
                      {scanResult.matchedMandatory.length > 0 && (
                        <span>
                          Đã có: {scanResult.matchedMandatory.map((kw, i) => (
                            <span key={i} className="kw-ok">
                              {kw}{i < scanResult.matchedMandatory.length - 1 ? ', ' : ''}
                            </span>
                          ))}
                        </span>
                      )}
                      {scanResult.missingMandatory.length > 0 && (
                        <span>
                          {scanResult.matchedMandatory.length > 0 ? ' • ' : ''}
                          Còn thiếu: {scanResult.missingMandatory.map((kw, i) => (
                            <span key={i} className="kw-missing">
                              {kw}{i < scanResult.missingMandatory.length - 1 ? ', ' : ''}
                            </span>
                          ))}
                        </span>
                      )}
                    </p>
                  </div>
                </div>

                {/* AI Safe Rewrite Suggestion */}
                <div className="ai-rewrite-box">
                  <div className="rewrite-top">
                    <span className="rewrite-title">
                      &#10024; Gợi ý viết lại an toàn (Chuẩn Tone Chuyên gia &amp; Thân thiện):
                    </span>
                    <button 
                      type="button" 
                      className="btn-copy" 
                      id="applyRewriteBtn"
                      onClick={() => {
                        setComplianceText(scanResult.rewrite);
                        setTimeout(() => runComplianceScan(scanResult.rewrite), 100);
                      }}
                    >
                      Áp dụng câu này
                    </button>
                  </div>
                  <p className="rewrite-content" id="rewriteText">
                    "{scanResult.rewrite}"
                  </p>
                </div>
              </div>
            </div>
          </section>

          </>)}

          {/* COMPLIANCE RULES TAB */}
          {activeMainTab === 'compliance-rules' && (
            <section className="panel compliance-rules-panel">
              <div className="panel-header">
                <div className="panel-title-group">
                  <svg className="icon-brand" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                  </svg>
                  <h2 className="panel-title-sm">QUY TẮC TUÂN THỦ 3 LỚP — COMPLIANCE ENGINE</h2>
                </div>
                <span className="badge badge-neutral">{COMPLIANCE_RULES.length} quy tắc</span>
              </div>

              {/* Group by pack */}
              {Object.entries(
                COMPLIANCE_RULES.reduce((acc, r) => {
                  (acc[r.pack] = acc[r.pack] || []).push(r);
                  return acc;
                }, {})
              ).map(([pack, rules]) => (
                <div key={pack} className="compliance-pack-group">
                  <div className="compliance-pack-header">
                    <span className="compliance-pack-label">{PACK_LABELS[pack] || pack}</span>
                    <span className="badge badge-neutral mono-text">{rules.length} quy tắc</span>
                  </div>
                  <div className="compliance-rules-table">
                    {rules.map(rule => {
                      const sev = SEVERITY_CONFIG[rule.severity] || SEVERITY_CONFIG.info;
                      return (
                        <div key={rule.code} className={`compliance-rule-row ${sev.cls}`}>
                          <div className="compliance-rule-top">
                            <span className="compliance-severity-badge">
                              {sev.icon} <span className="mono-text">{sev.label}</span>
                            </span>
                            <span className="compliance-rule-code mono-text">{rule.code}</span>
                            <span className="compliance-rule-name">{rule.name}</span>
                          </div>
                          <p className="compliance-rule-message">{rule.message}</p>
                          {rule.keywords && rule.keywords.length > 0 && (
                            <div className="compliance-keywords">
                              <span className="compliance-kw-label">Từ khóa trigger:</span>
                              {rule.keywords.map(kw => (
                                <span key={kw} className="compliance-kw-chip">{kw}</span>
                              ))}
                            </div>
                          )}
                          <p className="compliance-rule-suggestion">💡 {rule.suggestion}</p>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </section>
          )}

        </div>
      </div>

      {/* Modal: Thêm bộ quy tắc mới */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200 space-y-4">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="font-bold text-base text-slate-900">Thêm Bộ Quy Tắc Mới</h3>
              <button onClick={() => setShowAddModal(false)} className="text-slate-400 hover:text-slate-700 font-bold text-lg">&times;</button>
            </div>
            <form onSubmit={handleCreateRule} className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Tên bộ quy tắc</label>
                <input 
                  type="text"
                  required
                  value={newRuleName}
                  onChange={(e) => setNewRuleName(e.target.value)}
                  className="w-full p-2.5 border rounded-lg text-xs focus:outline-none focus:border-indigo-600"
                  placeholder="Ví dụ: Quy tắc Facebook Ads Hè 2026..."
                />
              </div>
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Mô tả quy tắc</label>
                <textarea 
                  rows="2"
                  value={newRuleDesc}
                  onChange={(e) => setNewRuleDesc(e.target.value)}
                  className="w-full p-2.5 border rounded-lg text-xs focus:outline-none focus:border-indigo-600"
                  placeholder="Kiểm soát nội dung và đảm bảo tiêu chuẩn truyền thông..."
                />
              </div>
              <div className="flex justify-end gap-2 pt-2 border-t">
                <button type="button" onClick={() => setShowAddModal(false)} className="px-3.5 py-1.5 border rounded-lg text-xs font-semibold text-slate-600">Hủy</button>
                <button type="submit" className="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-bold shadow">Tạo quy tắc</button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
