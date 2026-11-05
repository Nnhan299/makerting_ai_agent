# 🌟 AuraAI Enterprise OS - React.js Frontend

Giao diện người dùng độc lập (Decoupled Frontend) được chuyển đổi **pixel-perfect** từ 6 màn hình thiết kế Figma của dự án Marketing AI thông qua Builder.io.

---

## 🗂️ Cấu trúc Thư mục (`frontend/`)

```
frontend/
├── package.json           # Danh sách thư viện (React 18, Vite, Tailwind CSS, Lucide Icons)
├── vite.config.js         # Cấu hình máy chủ phát triển Vite (Port 3000)
├── tailwind.config.js     # Bảng màu thiết kế Figma AuraAI (#283044, #4F46E5, #6FFBBE, #FAF8FF)
├── postcss.config.js      # Bộ xử lý CSS
├── index.html             # HTML Shell tích hợp Google Fonts (Plus Jakarta Sans, Inter, JetBrains Mono)
└── src/
    ├── main.jsx           # Điểm khởi chạy React DOM
    ├── App.jsx            # Trình điều hướng phân quyền & chuyển đổi 5 Workspaces
    ├── index.css          # Tùy biến thanh cuộn và base style
    ├── components/
    │   └── Sidebar.jsx    # Thanh điều hướng chuẩn AuraAI Enterprise OS (Logo, User badge, Status)
    └── pages/
        ├── Login.jsx          # 1. Đăng nhập Hệ thống (Dual Split Card & SSO)
        ├── Campaigns.jsx      # 2. Quản lý Chiến dịch & KPI Analytics (CAM-01..05)
        ├── BrandRules.jsx     # 3. Quy tắc Thương hiệu & Blacklist (BRD-01..04)
        ├── StudioCanvas.jsx   # 4. Studio Split-Canvas (Social Mockup & Soát lỗi AI)
        ├── CalendarReview.jsx # 5. Lịch Phát sóng Đa kênh & Tự động Đăng bài (Meta API)
        └── AdminPortal.jsx    # 6. Admin Quản trị & Cấu hình Bảo mật (SRS-FR-ADM)
```

---

## 🚀 Hướng dẫn Cài đặt & Khởi chạy

### Bước 1: Cài đặt Node.js
Nếu máy tính của bạn chưa có Node.js:
1. Tải bản LTS tại trang chủ: 👉 **[https://nodejs.org/](https://nodejs.org/)**
2. Cài đặt theo mặc định (Next $\rightarrow$ Next $\rightarrow$ Finish).

### Bước 2: Chạy Frontend
Mở Terminal tại thư mục `frontend/` và gõ:

```bash
# 1. Cài đặt các thư viện cần thiết
npm install

# 2. Khởi chạy máy chủ giao diện
npm run dev
```

Trình duyệt sẽ tự động mở giao diện tại địa chỉ: 👉 **`http://localhost:3000`**

---

## ✨ Điểm Nổi Bật Của Giao Diện:
1. **100% Khớp Thiết Kế Figma:** Toàn bộ màu sắc chuẩn công ty, font chữ, hiệu ứng viền mờ và tỷ lệ layout.
2. **Interactive Mockup:** Màn hình Studio Canvas cho phép bấm thử nút *"Áp dụng sửa ngay (1-Click Fix)"* để xem AI sửa lỗi vi phạm luật quảng cáo trực quan trên khung điện thoại.
3. **Demo 1-Click:** Màn hình Đăng nhập có sẵn 3 nút đăng nhập nhanh (*Admin, Marketing Lead, Content Creator*) để demo trước hội đồng chấm đồ án.

