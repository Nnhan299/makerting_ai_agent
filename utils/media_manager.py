"""
Module Quản lý Thư viện Hình ảnh (Media Assets Manager).
Hỗ trợ:
1. Lưu trữ và quản lý ảnh sản phẩm tải lên thư mục assets/media_library.
2. Bộ sưu tập ảnh mẫu chuẩn ngành (Công nghệ, Mỹ phẩm, Ẩm thực, Thời trang, Sale/Ưu đãi).
3. Tự động gán hình ảnh phù hợp từ thư viện cho bài viết AI tạo theo từng giai đoạn phễu.
"""

import os
import re
import glob
import base64
import html
from typing import List, Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(BASE_DIR, "assets", "media_library")
os.makedirs(MEDIA_DIR, exist_ok=True)

# Bộ sưu tập ảnh chất lượng cao phân loại theo ngành và giai đoạn phễu
CURATED_PRESETS = [
    # 📱 CÔNG NGHỆ & SMARTPHONE
    {
        "id": "tech_teaser_1",
        "title": "Bí ẩn Công nghệ AI (Bóng mờ flagship)",
        "category": "Công nghệ & Smartphone",
        "stage": "Teaser",
        "url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "tech_launch_1",
        "title": "Cận cảnh Cụm Camera & Màn hình Tràn viền",
        "category": "Công nghệ & Smartphone",
        "stage": "Launch",
        "url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "tech_launch_2",
        "title": "Hiệu năng Gaming & Tản nhiệt Bứt phá",
        "category": "Công nghệ & Smartphone",
        "stage": "Launch",
        "url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "tech_cta_1",
        "title": "Hộp sản phẩm & Quà tặng Pre-order",
        "category": "Công nghệ & Smartphone",
        "stage": "CTA",
        "url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=900&auto=format&fit=crop&q=80"
    },

    # 💄 MỸ PHẨM & CHĂM SÓC DA
    {
        "id": "cosmetic_teaser_1",
        "title": "Bí mật làn da căng bóng ngậm nước",
        "category": "Mỹ phẩm & Skincare",
        "stage": "Teaser",
        "url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "cosmetic_launch_1",
        "title": "Serum & Tinh chất phục hồi chuyên sâu",
        "category": "Mỹ phẩm & Skincare",
        "stage": "Launch",
        "url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "cosmetic_cta_1",
        "title": "Set quà tặng cao cấp & Ưu đãi Mua 1 Tặng 1",
        "category": "Mỹ phẩm & Skincare",
        "stage": "CTA",
        "url": "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=900&auto=format&fit=crop&q=80"
    },

    # ☕ F&B, ẨM THỰC & ĐỒ UỐNG
    {
        "id": "fnb_teaser_1",
        "title": "Hương vị mới sắp đánh thức vị giác",
        "category": "F&B & Ẩm thực",
        "stage": "Teaser",
        "url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "fnb_launch_1",
        "title": "Ly cà phê đậm đà nghệ thuật Barista",
        "category": "F&B & Ẩm thực",
        "stage": "Launch",
        "url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "fnb_cta_1",
        "title": "Combo món ngon & Voucher giảm giá 50%",
        "category": "F&B & Ẩm thực",
        "stage": "CTA",
        "url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=900&auto=format&fit=crop&q=80"
    },

    # 👗 THỜI TRANG & LIFESTYLE
    {
        "id": "fashion_teaser_1",
        "title": "Bộ sưu tập mùa mới sắp đổ bộ",
        "category": "Thời trang & Lifestyle",
        "stage": "Teaser",
        "url": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "fashion_launch_1",
        "title": "Phong cách thanh lịch & Chất liệu cao cấp",
        "category": "Thời trang & Lifestyle",
        "stage": "Launch",
        "url": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "fashion_cta_1",
        "title": "Tuần lễ vàng - Giảm giá toàn bộ Lookbook",
        "category": "Thời trang & Lifestyle",
        "stage": "CTA",
        "url": "https://images.unsplash.com/photo-1489987707025-afc232f7ea0f?w=900&auto=format&fit=crop&q=80"
    },

    # ⚡ FLASH SALE & ƯU ĐÃI CHUNG
    {
        "id": "promo_cta_1",
        "title": "Đại tiệc Flash Sale - Số lượng có hạn",
        "category": "Khuyến mãi & Sự kiện",
        "stage": "CTA",
        "url": "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=900&auto=format&fit=crop&q=80"
    },
    {
        "id": "promo_cta_2",
        "title": "Quà tặng tri ân khách hàng thân thiết",
        "category": "Khuyến mãi & Sự kiện",
        "stage": "CTA",
        "url": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?w=900&auto=format&fit=crop&q=80"
    }
]


def get_media_library_dir() -> str:
    """Trả về đường dẫn tuyệt đối đến thư mục lưu trữ ảnh nội bộ."""
    return MEDIA_DIR


def list_local_media() -> List[Dict[str, Any]]:
    """Lấy danh sách các tệp hình ảnh đã được tải lên thư mục assets/media_library."""
    valid_exts = (".png", ".jpg", ".jpeg", ".webp", ".gif")
    local_files = []
    
    for f in os.listdir(MEDIA_DIR):
        ext = os.path.splitext(f)[1].lower()
        if ext in valid_exts:
            full_path = os.path.join(MEDIA_DIR, f)
            size_kb = round(os.path.getsize(full_path) / 1024, 1)
            # Tạo data URL cho ảnh local để Streamlit và HTML hiển thị trực tiếp
            try:
                with open(full_path, "rb") as img_f:
                    b64 = base64.b64encode(img_f.read()).decode("utf-8")
                mime = f"image/{ext[1:]}" if ext != ".jpg" else "image/jpeg"
                data_url = f"data:{mime};base64,{b64}"
            except Exception:
                data_url = ""

            local_files.append({
                "id": f"local_{f}",
                "title": f,
                "category": "Ảnh tải lên từ máy tính",
                "stage": "Tất cả",
                "url": data_url or full_path,
                "file_path": full_path,
                "size_kb": size_kb,
                "is_local": True
            })
            
    return local_files


def get_all_available_media() -> List[Dict[str, Any]]:
    """Tổng hợp toàn bộ ảnh từ máy tính (local) và thư viện mẫu chuẩn ngành."""
    locals_list = list_local_media()
    presets_list = [dict(p, is_local=False) for p in CURATED_PRESETS]
    return locals_list + presets_list


def save_uploaded_media(uploaded_file, custom_name: str = None) -> Dict[str, Any]:
    """
    Lưu một file tải lên từ Streamlit st.file_uploader vào thư mục assets/media_library.
    Trả về dict thông tin file và data URL để preview ngay lập tức.
    """
    clean_name = custom_name or uploaded_file.name
    # Làm sạch tên file chỉ giữ ký tự an toàn
    clean_name = re.sub(r"[^\w\.-]", "_", clean_name)
    save_path = os.path.join(MEDIA_DIR, clean_name)
    
    file_bytes = uploaded_file.getbuffer()
    with open(save_path, "wb") as f:
        f.write(file_bytes)
        
    ext = os.path.splitext(clean_name)[1].lower()
    b64 = base64.b64encode(file_bytes).decode("utf-8")
    mime = f"image/{ext[1:]}" if ext != ".jpg" else "image/jpeg"
    data_url = f"data:{mime};base64,{b64}"
    
    return {
        "id": f"local_{clean_name}",
        "title": clean_name,
        "category": "Ảnh tải lên từ máy tính",
        "stage": "Tất cả",
        "url": data_url,
        "file_path": save_path,
        "size_kb": round(len(file_bytes) / 1024, 1),
        "is_local": True
    }


def auto_assign_images(posts: List[Dict[str, Any]], product_name: str = "") -> List[Dict[str, Any]]:
    """
    Tự động gán hình ảnh đẹp và phù hợp từ Thư viện Media cho từng bài viết:
    - Ưu tiên ảnh local người dùng đã tải lên.
    - Nếu không có, lọc ảnh theo ngành hàng từ product_name và giai đoạn phễu (Teaser, Launch, CTA).
    - Bảo đảm các bài viết kề nhau không bị lặp lại hình ảnh giống nhau.
    """
    all_media = get_all_available_media()
    if not all_media:
        return posts

    prod_lower = (product_name or "").lower()
    
    # Xác định ngành hàng từ tên sản phẩm
    matched_cat = "Công nghệ & Smartphone"
    if any(k in prod_lower for k in ["kem", "da", "serum", "son", "mỹ phẩm", "cosmetic", "nước hoa"]):
        matched_cat = "Mỹ phẩm & Skincare"
    elif any(k in prod_lower for k in ["cà phê", "trà", "bánh", "ăn", "uống", "coffee", "quán", "món"]):
        matched_cat = "F&B & Ẩm thực"
    elif any(k in prod_lower for k in ["áo", "quần", "váy", "giày", "thời trang", "lookbook", "túi"]):
        matched_cat = "Thời trang & Lifestyle"

    updated_posts = []
    stage_counters = {"Teaser": 0, "Launch": 0, "CTA": 0}

    for p in posts:
        post_copy = dict(p)
        # Nếu bài viết đã có media_url riêng thì giữ nguyên
        if post_copy.get("media_url"):
            updated_posts.append(post_copy)
            continue

        stage = post_copy.get("stage", "Launch")
        
        # Tìm danh sách ảnh phù hợp nhất theo giai đoạn và ngành
        matching_pool = [
            m for m in all_media 
            if m.get("is_local") or (m.get("category") == matched_cat and m.get("stage") == stage)
        ]
        
        # Nếu không có đủ, nới lỏng tìm theo stage bất kể ngành
        if not matching_pool:
            matching_pool = [m for m in all_media if m.get("stage") == stage or m.get("stage") == "Tất cả"]
            
        if not matching_pool:
            matching_pool = all_media

        idx = stage_counters.get(stage, 0) % len(matching_pool)
        selected_img = matching_pool[idx]
        post_copy["media_url"] = selected_img["url"]
        stage_counters[stage] = stage_counters.get(stage, 0) + 1
        
        updated_posts.append(post_copy)

    return updated_posts

