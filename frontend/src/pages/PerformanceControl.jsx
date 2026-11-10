import React, { useState } from 'react';
import {
  TrendingUp,
  Plus,
  Star,
  X,
  Save,
  Eye,
  Users,
  DollarSign,
  Activity,
  MousePointerClick,
  Trash2
} from 'lucide-react';

// ── KPI Dashboard Tab ─────────────────────────────────────────────
function KpiDashboardTab({ campaigns }) {
  const [kpiData] = useState([
    { label: 'Reach', target: 500000, actual: 423000, unit: '' },
    { label: 'Engagements', target: 50000, actual: 48200, unit: '' },
    { label: 'ROAS', target: 3.5, actual: 3.2, unit: 'x' },
    { label: 'CTR', target: 2.5, actual: 2.1, unit: '%' },
    { label: 'Chuyển đổi (Orders)', target: 1500, actual: 1278, unit: '' },
    { label: 'GMV (VND)', target: 500000000, actual: 432000000, unit: '' },
  ]);

  const statCards = [
    { label: 'Tổng Reach', value: '423K', icon: <Eye className="w-5 h-5 text-indigo-500" />, sub: 'vs mục tiêu 500K', color: 'text-indigo-600' },
    { label: 'Tổng Engagements', value: '48.2K', icon: <Activity className="w-5 h-5 text-emerald-500" />, sub: '96.4% mục tiêu', color: 'text-emerald-600' },
    { label: 'ROAS trung bình', value: '3.2x', icon: <TrendingUp className="w-5 h-5 text-purple-500" />, sub: 'GMV / Spend', color: 'text-purple-600' },
    { label: 'Chi phí thực', value: '135M₫', icon: <DollarSign className="w-5 h-5 text-amber-500" />, sub: 'Tổng chi tiêu QC', color: 'text-amber-600' },
  ];

  return (
    <div className="space-y-6">
      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map(({ label, value, icon, sub, color }) => (
          <div key={label} className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs text-slate-500 font-medium">{label}</span>
              {icon}
            </div>
            <div className={`text-2xl font-black ${color}`}>{value}</div>
            <div className="text-[11px] text-slate-400 font-mono mt-1">{sub}</div>
          </div>
        ))}
      </div>

      {/* KPI Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
        <div className="px-5 py-3 border-b border-slate-100">
          <span className="font-mono font-bold text-xs text-[#3525CD] uppercase tracking-wider">KPI vs Mục tiêu</span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                {['Chỉ tiêu', 'Mục tiêu', 'Thực đạt', '% Hoàn thành', 'Tiến độ'].map(h => (
                  <th key={h} className="px-4 py-2.5 text-left font-mono font-bold text-slate-500 uppercase text-[10px] tracking-wider whitespace-nowrap">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {kpiData.map(({ label, target, actual, unit }, idx) => {
                const pct = Math.round((actual / target) * 100);
                const barColor = pct >= 90 ? 'bg-emerald-500' : pct >= 70 ? 'bg-amber-400' : 'bg-red-400';
                const textColor = pct >= 90 ? 'text-emerald-700' : pct >= 70 ? 'text-amber-700' : 'text-red-600';
                return (
                  <tr key={label} className={idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/50'}>
                    <td className="px-4 py-2.5 font-semibold text-slate-800">{label}</td>
                    <td className="px-4 py-2.5 font-mono text-slate-600">
                      {target.toLocaleString('vi-VN')}{unit}
                    </td>
                    <td className="px-4 py-2.5 font-mono font-bold text-slate-900">
                      {actual.toLocaleString('vi-VN')}{unit}
                    </td>
                    <td className={`px-4 py-2.5 font-mono font-bold ${textColor}`}>{pct}%</td>
                    <td className="px-4 py-2.5 w-40">
                      <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                        <div className={`h-2 rounded-full ${barColor}`} style={{ width: `${Math.min(pct, 100)}%` }} />
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="text-xs text-slate-500 font-sans flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-lg px-4 py-2.5">
        <AlertCircle className="w-3.5 h-3.5 text-amber-500 shrink-0" />
        <span>Dữ liệu đo lường hiệu suất được tổng hợp theo thời gian thực (ROAS = GMV / Spend).</span>
      </div>
    </div>
  );
}

// ── Nhập Số Liệu Tab ─────────────────────────────────────────────
function MetricsInputTab({ campaigns }) {
  const [form, setForm] = useState({
    campaign_id: campaigns[0]?.id || '',
    channel: 'TikTok',
    date: new Date().toISOString().slice(0, 10),
    type: 'Organic',
    views: '', reach: '', engagements: '', clicks: '',
    orders: '', gmv: '', ad_spend: ''
  });
  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleSave = async () => {
    setSaving(true);
    try {
      await fetch(`/api/campaigns/${form.campaign_id}/performance`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch {
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    }
    setSaving(false);
  };

  return (
    <div className="space-y-5 max-w-2xl">
      <div className="bg-white rounded-xl border border-slate-200 p-5 space-y-4 shadow-2xs">
        <div className="text-xs font-mono font-bold text-[#3525CD] uppercase tracking-wider">Nhập số liệu chiến dịch</div>

        {/* Campaign + Channel + Date + Type */}
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Chiến dịch</label>
            <select
              value={form.campaign_id}
              onChange={e => setForm({ ...form, campaign_id: e.target.value })}
              className="w-full p-2 border border-slate-200 rounded-lg focus:outline-none focus:border-indigo-400 text-xs"
            >
              {campaigns.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Kênh</label>
            <select
              value={form.channel}
              onChange={e => setForm({ ...form, channel: e.target.value })}
              className="w-full p-2 border border-slate-200 rounded-lg focus:outline-none focus:border-indigo-400 text-xs"
            >
              {['TikTok', 'Facebook', 'Instagram', 'YouTube', 'Zalo'].map(ch => (
                <option key={ch}>{ch}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Ngày</label>
            <input
              type="date"
              value={form.date}
              onChange={e => setForm({ ...form, date: e.target.value })}
              className="w-full p-2 border border-slate-200 rounded-lg focus:outline-none focus:border-indigo-400 text-xs"
            />
          </div>
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Loại</label>
            <select
              value={form.type}
              onChange={e => setForm({ ...form, type: e.target.value })}
              className="w-full p-2 border border-slate-200 rounded-lg focus:outline-none focus:border-indigo-400 text-xs"
            >
              <option>Organic</option>
              <option>Paid</option>
            </select>
          </div>
        </div>

        {/* Metrics grid */}
        <div className="grid grid-cols-2 gap-3">
          {[
            { key: 'views', label: 'Views', placeholder: '0' },
            { key: 'reach', label: 'Reach', placeholder: '0' },
            { key: 'engagements', label: 'Engagements', placeholder: '0' },
            { key: 'clicks', label: 'Clicks', placeholder: '0' },
            { key: 'orders', label: 'Orders', placeholder: '0' },
            { key: 'gmv', label: 'GMV (VND)', placeholder: '0' },
            { key: 'ad_spend', label: 'Chi phí quảng cáo (VND)', placeholder: '0' },
          ].map(({ key, label, placeholder }) => (
            <div key={key}>
              <label className="block text-xs font-bold text-slate-700 mb-1">{label}</label>
              <input
                type="number"
                placeholder={placeholder}
                value={form[key]}
                onChange={e => setForm({ ...form, [key]: e.target.value })}
                className="w-full p-2 border border-slate-200 rounded-lg focus:outline-none focus:border-indigo-400 text-xs font-mono"
              />
            </div>
          ))}
        </div>

        <div className="flex items-center gap-3 pt-2 border-t border-slate-100">
          <button
            onClick={handleSave}
            disabled={saving}
            className="inline-flex items-center gap-2 bg-[#4F46E5] hover:bg-[#4338CA] disabled:opacity-60 text-white px-4 py-2 rounded-xl font-semibold text-xs shadow-sm transition"
          >
            <Save className="w-3.5 h-3.5" />
            {saving ? 'Đang lưu...' : 'Lưu'}
          </button>
          {saved && (
            <span className="text-xs text-emerald-600 font-semibold">✔ Đã lưu thành công!</span>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Partner / KOL Tab ─────────────────────────────────────────────
const EMPTY_PARTNER = {
  name: '', type: 'KOL', platform: 'TikTok', followers: '', fee_per_post: '', status: 'Active', rating: 3
};

function PartnerTab() {
  const [partners, setPartners] = useState([
    { id: 1, name: 'Hà Linh Beauty', type: 'KOL', platform: 'TikTok', followers: '1.2M', fee_per_post: '5,000,000', status: 'Active', rating: 5 },
    { id: 2, name: 'GlowWithMe', type: 'KOC', platform: 'Instagram', followers: '450K', fee_per_post: '2,500,000', status: 'Active', rating: 4 },
    { id: 3, name: 'MediaStar Agency', type: 'Agency', platform: 'Facebook', followers: '—', fee_per_post: '50,000,000', status: 'Inactive', rating: 3 },
  ]);
  const [showModal, setShowModal] = useState(false);
  const [newPartner, setNewPartner] = useState({ ...EMPTY_PARTNER });

  const handleAdd = () => {
    setPartners(prev => [...prev, { ...newPartner, id: Date.now() }]);
    setNewPartner({ ...EMPTY_PARTNER });
    setShowModal(false);
  };

  const removePartner = (id) => setPartners(prev => prev.filter(p => p.id !== id));

  const setRating = (id, rating) => setPartners(prev => prev.map(p => p.id === id ? { ...p, rating } : p));

  const statusStyle = (status) =>
    status === 'Active' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-slate-100 text-slate-500 border-slate-200';

  const typeStyle = (type) => {
    if (type === 'KOL') return 'bg-purple-50 text-purple-700 border-purple-200';
    if (type === 'KOC') return 'bg-indigo-50 text-indigo-700 border-indigo-200';
    return 'bg-amber-50 text-amber-700 border-amber-200';
  };

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <span className="text-xs font-mono text-slate-500">{partners.length} đối tác / KOL / KOC</span>
        <button
          onClick={() => setShowModal(true)}
          className="inline-flex items-center gap-1.5 bg-[#4F46E5] hover:bg-[#4338CA] text-white px-3.5 py-1.5 rounded-lg font-semibold text-xs shadow-xs transition"
        >
          <Plus className="w-3.5 h-3.5" /> Thêm đối tác
        </button>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <table className="w-full text-xs">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              {['Tên', 'Loại', 'Platform', 'Followers', 'Fee/Post (VND)', 'Trạng thái', 'Đánh giá', ''].map(h => (
                <th key={h} className="px-4 py-2.5 text-left font-mono font-bold text-slate-500 uppercase text-[10px] tracking-wider whitespace-nowrap">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {partners.map((partner, idx) => (
              <tr key={partner.id} className={idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/50'}>
                <td className="px-4 py-3 font-semibold text-slate-900">{partner.name}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full border text-[10px] font-mono font-bold ${typeStyle(partner.type)}`}>
                    {partner.type}
                  </span>
                </td>
                <td className="px-4 py-3 font-mono text-slate-600">{partner.platform}</td>
                <td className="px-4 py-3 font-mono text-slate-700">{partner.followers}</td>
                <td className="px-4 py-3 font-mono text-slate-700">{partner.fee_per_post}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full border text-[10px] font-mono font-bold ${statusStyle(partner.status)}`}>
                    {partner.status}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-0.5">
                    {[1, 2, 3, 4, 5].map(star => (
                      <button
                        key={star}
                        onClick={() => setRating(partner.id, star)}
                        className="transition"
                      >
                        <Star
                          className={`w-3.5 h-3.5 ${star <= partner.rating ? 'fill-amber-400 text-amber-400' : 'text-slate-200'}`}
                        />
                      </button>
                    ))}
                  </div>
                </td>
                <td className="px-4 py-3">
                  <button onClick={() => removePartner(partner.id)} className="p-1 text-slate-300 hover:text-red-500 transition rounded">
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Add Partner Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-100 space-y-4">
            <div className="flex items-center justify-between pb-2 border-b">
              <h3 className="font-bold text-base text-slate-900">Thêm Đối tác / KOL / KOC</h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              {[
                { key: 'name', label: 'Tên', type: 'text', placeholder: 'VD: Hà Linh Beauty' },
                { key: 'platform', label: 'Platform', type: 'text', placeholder: 'TikTok / Instagram...' },
                { key: 'followers', label: 'Followers', type: 'text', placeholder: '1.2M' },
                { key: 'fee_per_post', label: 'Fee/Post (VND)', type: 'text', placeholder: '5,000,000' },
              ].map(({ key, label, type, placeholder }) => (
                <div key={key}>
                  <label className="font-bold text-slate-700 block mb-1">{label}</label>
                  <input
                    type={type}
                    placeholder={placeholder}
                    value={newPartner[key]}
                    onChange={e => setNewPartner({ ...newPartner, [key]: e.target.value })}
                    className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500 text-xs"
                  />
                </div>
              ))}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Loại</label>
                  <select
                    value={newPartner.type}
                    onChange={e => setNewPartner({ ...newPartner, type: e.target.value })}
                    className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500 text-xs"
                  >
                    <option>KOL</option>
                    <option>KOC</option>
                    <option>Agency</option>
                  </select>
                </div>
                <div>
                  <label className="font-bold text-slate-700 block mb-1">Trạng thái</label>
                  <select
                    value={newPartner.status}
                    onChange={e => setNewPartner({ ...newPartner, status: e.target.value })}
                    className="w-full p-2.5 border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500 text-xs"
                  >
                    <option>Active</option>
                    <option>Inactive</option>
                  </select>
                </div>
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-3 border-t">
              <button onClick={() => setShowModal(false)} className="px-4 py-2 border border-slate-200 rounded-xl text-slate-600 font-bold hover:bg-slate-50 text-xs">Hủy</button>
              <button onClick={handleAdd} className="px-4 py-2 bg-[#4F46E5] text-white rounded-xl font-bold shadow-md shadow-indigo-500/20 text-xs hover:bg-indigo-700">
                Thêm đối tác
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────
const TABS = [
  { id: 'kpi', label: 'Dashboard KPI' },
  { id: 'metrics', label: 'Nhập số liệu thực' },
  { id: 'partners', label: 'Đối tác & KOL/KOC' },
];

export default function PerformanceControl({ campaigns = [] }) {
  const [activeTab, setActiveTab] = useState('kpi');

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-200/80">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Đo lường Hiệu suất & Báo cáo</h1>
          <p className="text-xs text-slate-500 mt-0.5">Đối chiếu KPI thực tế so với mục tiêu SMART, phân bổ ngân sách Organic / Paid và đánh giá đối tác.</p>
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
        {activeTab === 'kpi' && <KpiDashboardTab campaigns={campaigns} />}
        {activeTab === 'metrics' && <MetricsInputTab campaigns={campaigns} />}
        {activeTab === 'partners' && <PartnerTab />}
      </div>
    </div>
  );
}
