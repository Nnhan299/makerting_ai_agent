"""
Module xuất báo cáo Content Calendar và Audit Logs ra file Excel (.xlsx).
Sử dụng openpyxl với định dạng chuyên nghiệp 3 Sheet.
"""

import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def export_campaign_to_excel(campaign: dict, posts: list, audit_logs: list = None) -> bytes:
    """
    Tạo file Excel 3 sheet chuyên nghiệp từ dữ liệu chiến dịch.
    
    Returns:
        bytes: Dữ liệu file Excel dạng byte stream cho Streamlit download.
    """
    wb = openpyxl.Workbook()
    
    # Custom styles
    header_font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    title_font = Font(name="Arial", size=14, bold=True, color="1F4E78")
    bold_font = Font(name="Arial", size=10, bold=True)
    regular_font = Font(name="Arial", size=10)
    
    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    # ------------------------------------------------------------
    # SHEET 1: Tổng quan chiến dịch
    # ------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Tổng quan chiến dịch"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.append(["BÁO CÁO CHIẾN DỊCH MARKETING AI"])
    ws1.cell(row=1, column=1).font = title_font
    ws1.append([])
    
    overview_data = [
        ["ID Chiến dịch:", campaign.get("id")],
        ["Tên Chiến dịch:", campaign.get("name")],
        ["Sản phẩm/Dịch vụ:", campaign.get("product_name")],
        ["Đối tượng mục tiêu:", campaign.get("target_audience")],
        ["Ngân sách:", campaign.get("budget")],
        ["Kênh truyền thông:", campaign.get("channels")],
        ["Ngày bắt đầu:", str(campaign.get("start_date"))],
        ["Ngày kết thúc:", str(campaign.get("end_date"))],
        ["Trạng thái:", campaign.get("status")],
        ["Tổng số bài đăng:", len(posts)]
    ]
    
    for row in overview_data:
        ws1.append(row)
        
    for r in range(3, 13):
        ws1.cell(row=r, column=1).font = bold_font
        ws1.cell(row=r, column=2).font = regular_font

    # ------------------------------------------------------------
    # SHEET 2: Lịch bài đăng (Content Calendar)
    # ------------------------------------------------------------
    ws2 = wb.create_sheet(title="Lịch bài đăng")
    ws2.views.sheetView[0].showGridLines = True
    
    headers_posts = ["STT", "Giai đoạn", "Kênh", "Tiêu đề", "Nội dung", "Ngày đăng", "Trạng thái"]
    ws2.append(headers_posts)
    
    for col_num, header in enumerate(headers_posts, 1):
        cell = ws2.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    for idx, post in enumerate(posts, 1):
        row = [
            idx,
            post.get("stage"),
            post.get("channel"),
            post.get("title"),
            post.get("content"),
            str(post.get("scheduled_date")),
            post.get("status")
        ]
        ws2.append(row)
        
    # Auto adjust column widths for Sheet 2
    for col in ws2.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws2.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 60)

    # ------------------------------------------------------------
    # SHEET 3: Báo cáo kiểm duyệt
    # ------------------------------------------------------------
    ws3 = wb.create_sheet(title="Báo cáo kiểm duyệt")
    ws3.views.sheetView[0].showGridLines = True
    
    headers_audit = ["STT", "Post ID", "Điểm Tuân thủ", "Chi tiết Vi phạm", "Gợi ý Chỉnh sửa"]
    ws3.append(headers_audit)
    
    for col_num, header in enumerate(headers_audit, 1):
        cell = ws3.cell(row=1, column=col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        
    if audit_logs:
        for idx, audit in enumerate(audit_logs, 1):
            row = [
                idx,
                audit.get("post_id"),
                audit.get("compliance_score"),
                str(audit.get("violations_json")),
                audit.get("suggestions")
            ]
            ws3.append(row)

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()
