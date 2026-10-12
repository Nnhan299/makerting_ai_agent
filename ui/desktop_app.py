import os
import sys
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox
try:
    import ttkbootstrap as tb
except ImportError:
    tb = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.connection import get_connection
from database.crud import (
    create_campaign,
    create_brand_rule,
    get_all_campaigns,
    get_all_brand_rules,
    get_posts_by_campaign,
    get_audits_by_campaign,
    get_campaign_by_id,
)
from utils.export_excel import export_campaign_to_excel
from utils.llm_client import LLMClient
from agents.orchestrator import AgentOrchestrator


def enable_windows_dpi_awareness():
    if sys.platform == "win32":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except (AttributeError, OSError):
                pass


class MarketingDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Marketing AI Agent")
        self.root.geometry("1400x780")
        self.root.minsize(1180, 680)
        self.root.configure(bg="#fdf6e3")

        self.sidebar_bg = "#eee8d5"
        self.panel_bg = "#fffdf5"
        self.content_bg = "#fdf6e3"
        self.surface_2 = "#eee8d5"
        self.accent = "#cb4b16"
        self.accent_2 = "#268bd2"
        self.accent_3 = "#b58900"
        self.accent_4 = "#dc322f"
        self.text = "#073642"
        self.muted = "#586e75"

        self.current_page = None
        self.pages = {}
        self.page_names = [
            ("campaigns", "▦  Chiến dịch", "Lập kế hoạch và theo dõi"),
            ("brand_rules", "◈  Quy tắc thương hiệu", "Kiểm duyệt giọng điệu"),
            ("pipeline", "✦  AI Pipeline", "Tạo nội dung với 3 agent"),
            ("calendar", "◷  Lịch đăng", "Theo dõi lịch xuất bản"),
            ("export", "⇩  Xuất báo cáo", "Tải báo cáo chiến dịch"),
        ]

        self.nav_buttons = {}
        self.setup_styles()
        self.build_layout()
        self.show_page("campaigns")

    def setup_styles(self):
        if tb is not None:
            style = tb.Style(master=self.root, theme="flatly")
        else:
            style = ttk.Style(self.root)
            style.theme_use("vista" if "vista" in style.theme_names() else "clam")
        self.sidebar_bg = "#eee8d5"
        self.panel_bg = "#fffdf5"
        self.content_bg = "#fdf6e3"
        self.surface_2 = "#eee8d5"
        self.accent = "#cb4b16"
        self.accent_2 = "#268bd2"
        self.accent_3 = "#b58900"
        self.accent_4 = "#dc322f"
        self.text = "#073642"
        self.muted = "#586e75"
        style.configure(
            "App.Treeview",
            background=self.panel_bg,
            foreground=self.text,
            fieldbackground=self.panel_bg,
            borderwidth=0,
            rowheight=36,
            font=("Segoe UI", 10),
        )
        style.configure(
            "App.Treeview.Heading",
            background=self.surface_2,
            foreground=self.muted,
            borderwidth=0,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("App.Treeview", background=[("selected", self.surface_2)], foreground=[("selected", self.text)])
        style.configure(
            "App.TCombobox",
            fieldbackground=self.panel_bg,
            background=self.panel_bg,
            foreground=self.text,
            arrowcolor=self.accent,
            borderwidth=0,
            padding=8,
            font=("Segoe UI", 10),
        )

    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_bg, width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        brand.pack(fill="x", padx=24, pady=(28, 28))
        mark = tk.Label(brand, text="MA", bg=self.accent, fg="#fdf6e3", font=("Arial", 15, "bold"), padx=10, pady=8)
        mark.pack(side="left")
        brand_text = tk.Frame(brand, bg=self.sidebar_bg)
        brand_text.pack(side="left", padx=10)
        tk.Label(brand_text, text="Marketing AI", bg=self.sidebar_bg, fg=self.text, font=("Arial", 14, "bold"), anchor="w").pack(anchor="w")
        tk.Label(brand_text, text="CAMPAIGN STUDIO", bg=self.sidebar_bg, fg=self.accent, font=("Segoe UI", 9, "bold"), anchor="w").pack(anchor="w", pady=(3, 0))

        tk.Label(self.sidebar, text="WORKSPACE", bg=self.sidebar_bg, fg=self.muted, font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", padx=26, pady=(0, 10))
        nav_frame = tk.Frame(self.sidebar, bg=self.sidebar_bg)
        nav_frame.pack(fill="both", expand=True, padx=14)

        for key, title, description in self.page_names:
            btn = tk.Button(
                nav_frame,
                text=f"{title}\n{description}",
                command=lambda page=key: self.show_page(page),
                anchor="w",
                justify="left",
                bg=self.sidebar_bg,
                fg=self.muted,
                activebackground=self.surface_2,
                activeforeground=self.text,
                relief="flat",
                bd=0,
                padx=14,
                pady=10,
                font=("Segoe UI", 10, "bold"),
                width=28,
                cursor="hand2",
            )
            btn.pack(fill="x", pady=3)
            btn.bind("<Enter>", lambda e, b=btn, page=key: b.configure(bg=self.surface_2 if self.current_page != page else "#e1d8ba"))
            btn.bind("<Leave>", lambda e, b=btn, page=key: b.configure(bg="#e1d8ba" if self.current_page == page else self.sidebar_bg))
            self.nav_buttons[key] = btn

        status_box = tk.Frame(self.sidebar, bg="#e1d8ba", bd=0)
        status_box.pack(fill="x", padx=18, pady=(12, 20))

        tk.Label(status_box, text="SYSTEM STATUS", bg="#e1d8ba", fg=self.muted, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
        tk.Label(status_box, text="●  PostgreSQL connected", bg="#e1d8ba", fg="#268bd2", font=("Segoe UI", 10)).pack(anchor="w", padx=14)
        tk.Label(status_box, text="●  3 agents ready", bg="#e1d8ba", fg="#cb4b16", font=("Segoe UI", 10)).pack(anchor="w", padx=14, pady=(2, 12))

        self.main = tk.Frame(self.root, bg=self.content_bg)
        self.main.pack(side="left", fill="both", expand=True)

        self.topbar = tk.Frame(self.main, bg="#fdf6e3", height=92)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        top_left = tk.Frame(self.topbar, bg="#fdf6e3")
        top_left.pack(side="left", padx=30, pady=18)
        self.title_label = tk.Label(
            top_left,
            text="Dashboard",
            bg="#fdf6e3",
            fg=self.text,
            font=("Arial", 21, "bold"),
            anchor="w",
        )
        self.title_label.pack(anchor="w")
        self.subtitle_label = tk.Label(top_left, text="Overview of your marketing operations", bg="#fdf6e3", fg=self.muted, font=("Segoe UI", 10), anchor="w")
        self.subtitle_label.pack(anchor="w", pady=(3, 0))

        self.status_label = tk.Label(
            self.topbar,
            text="●  Sẵn sàng",
            bg="#e1d8ba",
            fg=self.accent,
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            anchor="center",
            relief="flat",
        )
        self.status_label.pack(side="right", padx=30, pady=26)

        self.content = tk.Frame(self.main, bg=self.content_bg)
        self.content.pack(fill="both", expand=True, padx=30, pady=24)

    def set_status(self, text, color="#268bd2"):
        self.status_label.configure(text=text, fg=color)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_page(self, page_key):
        self.current_page = page_key
        self.clear_content()
        for key, button in self.nav_buttons.items():
            button.configure(
                bg="#e1d8ba" if key == page_key else self.sidebar_bg,
                fg=self.text if key == page_key else self.muted,
            )

        if page_key == "campaigns":
            self.render_campaigns_page()
        elif page_key == "brand_rules":
            self.render_rules_page()
        elif page_key == "pipeline":
            self.render_pipeline_page()
        elif page_key == "calendar":
            self.render_calendar_page()
        elif page_key == "export":
            self.render_export_page()

    def render_campaigns_page(self):
        self.title_label.configure(text="Chiến dịch")
        self.set_status("Trạng thái: Quản lý chiến dịch", self.accent_2)

        heading = tk.Label(
            self.content,
            text="Quản lý chiến dịch marketing",
            bg=self.content_bg,
            fg=self.text,
            font=("Arial", 18, "bold"),
            anchor="w",
        )
        heading.pack(anchor="w", pady=(8, 10))

        summary = tk.Frame(self.content, bg=self.content_bg)
        summary.pack(fill="x", pady=(0, 14))

        for idx, text, description, color in [
            ("01", "Lập kế hoạch", "Xây campaign và mục tiêu rõ ràng", self.accent_2),
            ("02", "Tạo nội dung", "Để 3 agent phối hợp thực thi", self.accent),
            ("03", "Kiểm duyệt", "Giữ mọi nội dung đúng brand", self.accent_3),
        ]:
            card = tk.Frame(summary, bg=self.panel_bg, bd=0)
            card.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=4)
            tk.Frame(card, bg=color, width=4).pack(side="left", fill="y")
            card_body = tk.Frame(card, bg=self.panel_bg)
            card_body.pack(side="left", fill="both", expand=True, padx=16, pady=14)
            tk.Label(card_body, text=idx, bg=self.panel_bg, fg=color, font=("Segoe UI", 10, "bold"), anchor="w").pack(anchor="w")
            tk.Label(card_body, text=text, bg=self.panel_bg, fg=self.text, font=("Arial", 12, "bold"), anchor="w").pack(anchor="w", pady=(6, 3))
            tk.Label(card_body, text=description, bg=self.panel_bg, fg=self.muted, font=("Segoe UI", 10), anchor="w").pack(anchor="w")

        table_frame = tk.Frame(self.content, bg=self.panel_bg, bd=0)
        table_frame.pack(fill="both", expand=True)

        header = tk.Label(table_frame, text="Campaign workspace", bg=self.panel_bg, fg=self.text, font=("Arial", 12, "bold"), anchor="w")
        header.pack(anchor="w", padx=18, pady=(18, 10))

        cols = ("ID", "Tên chiến dịch", "Sản phẩm", "Trạng thái")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=14, style="App.Treeview")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=200 if col != "ID" else 60, anchor="center")

        tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        try:
            conn = get_connection()
            campaigns = get_all_campaigns(conn)
            conn.close()
            for c in campaigns:
                tree.insert("", "end", values=(c.get("id"), c.get("name", ""), c.get("product_name", ""), c.get("status", "Draft")))
            if not campaigns:
                tree.insert("", "end", values=("-", "Chưa có dữ liệu", "-", "Draft"))
        except Exception as exc:
            tree.insert("", "end", values=("-", f"Lỗi DB: {exc}", "-", "Error"))
            self.set_status(f"Lỗi kết nối DB: {exc}", self.accent_4)

        actions = tk.Frame(self.content, bg=self.content_bg)
        actions.pack(fill="x", pady=(14, 0))
        tk.Button(
            actions,
            text="Tạo chiến dịch mới",
            bg=self.accent,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=18,
            pady=10,
            command=self.open_create_campaign_form,
        ).pack(side="left")
        tk.Button(
            actions,
            text="Tải lại",
            bg=self.accent_2,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=18,
            pady=10,
            command=lambda: self.show_page("campaigns"),
        ).pack(side="left", padx=8)

    def render_rules_page(self):
        self.title_label.configure(text="Quy tắc thương hiệu")
        self.set_status("Trạng thái: Quy tắc & kiểm duyệt", self.accent_3)

        heading = tk.Label(
            self.content,
            text="Bộ quy tắc kiểm duyệt thương hiệu",
            bg=self.content_bg,
            fg=self.text,
            font=("Arial", 18, "bold"),
            anchor="w",
        )
        heading.pack(anchor="w", pady=(8, 10))

        card = tk.Frame(self.content, bg=self.panel_bg, bd=0)
        card.pack(fill="both", expand=True)

        cols = ("ID", "Tên quy tắc", "Từ cấm", "Tone of voice")
        tree = ttk.Treeview(card, columns=cols, show="headings", height=16, style="App.Treeview")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=220 if col != "ID" else 60, anchor="center")
        tree.pack(fill="both", expand=True, padx=12, pady=12)

        try:
            conn = get_connection()
            rules = get_all_brand_rules(conn)
            conn.close()
            for r in rules:
                tree.insert("", "end", values=(r.get("id"), r.get("rule_name", ""), r.get("forbidden_words", "")[:50], r.get("tone_of_voice", "")))
            if not rules:
                tree.insert("", "end", values=("-", "Chưa có quy tắc", "-", "-"))
        except Exception as exc:
            tree.insert("", "end", values=("-", f"Lỗi: {exc}", "-", "-"))
            self.set_status(f"Không tải được quy tắc: {exc}", self.accent_4)
        action_bar = tk.Frame(self.content, bg=self.content_bg)
        action_bar.pack(fill="x", pady=(14, 0))
        tk.Button(
            action_bar,
            text="Tạo bộ quy tắc mới",
            bg=self.accent_3,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=18,
            pady=10,
            command=self.open_create_rule_form,
        ).pack(side="left")
    def render_pipeline_page(self):
        self.title_label.configure(text="AI Pipeline")
        self.set_status("Trạng thái: Chạy AI Multi-Agent", self.accent_2)

        heading = tk.Label(
            self.content,
            text="Chạy pipeline 3 agent theo thứ tự",
            bg=self.content_bg,
            fg=self.text,
            font=("Arial", 18, "bold"),
            anchor="w",
        )
        heading.pack(anchor="w", pady=(8, 12))

        panel = tk.Frame(self.content, bg=self.panel_bg, bd=0)
        panel.pack(fill="both", expand=True)

        tk.Label(panel, text="1. Chọn chiến dịch", bg=self.panel_bg, fg=self.text, font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(18, 6))
        campaigns = []
        try:
            conn = get_connection()
            campaigns = get_all_campaigns(conn)
            conn.close()
        except Exception as exc:
            self.set_status(f"DB rỗng hoặc chưa sẵn sàng: {exc}", self.accent_4)
        campaign_values = [f"{c.get('id')} - {c.get('name', '')}" for c in campaigns]
        self.campaign_var = tk.StringVar(value=campaign_values[0] if campaign_values else "Chưa có chiến dịch")
        campaign_combo = ttk.Combobox(panel, textvariable=self.campaign_var, values=campaign_values, state="readonly", width=56, style="App.TCombobox")
        campaign_combo.pack(anchor="w", padx=16, pady=(0, 12))

        tk.Label(panel, text="2. Chọn bộ quy tắc thương hiệu", bg=self.panel_bg, fg=self.text, font=("Arial", 11, "bold")).pack(anchor="w", padx=16, pady=(8, 6))
        rules = []
        try:
            conn = get_connection()
            rules = get_all_brand_rules(conn)
            conn.close()
        except Exception:
            rules = []
        rule_values = [f"{r.get('id')} - {r.get('rule_name', '')}" for r in rules]
        self.rule_var = tk.StringVar(value=rule_values[0] if rule_values else "Chưa có quy tắc")
        rule_combo = ttk.Combobox(panel, textvariable=self.rule_var, values=rule_values, state="readonly", width=56, style="App.TCombobox")
        rule_combo.pack(anchor="w", padx=16, pady=(0, 16))

        run_btn = tk.Button(
            panel,
            text="▶ Chạy AI Pipeline",
            bg=self.accent,
            fg="white",
            font=("Arial", 12, "bold"),
            padx=22,
            pady=10,
            command=self.run_pipeline_action,
            cursor="hand2",
        )
        run_btn.pack(anchor="w", padx=16, pady=(0, 16))

        self.pipeline_result = tk.Text(panel, height=12, width=110, bg=self.content_bg, fg=self.text, font=("Arial", 10), relief="flat", bd=0)
        self.pipeline_result.pack(fill="both", padx=16, pady=(0, 16))

    def run_pipeline_action(self):
        try:
            selected_campaign = self.campaign_var.get()
            selected_rule = self.rule_var.get()
            if not selected_campaign or selected_campaign.startswith("Chưa"):
                raise ValueError("Vui lòng tạo chiến dịch trước khi chạy AI.")
            if not selected_rule or selected_rule.startswith("Chưa"):
                raise ValueError("Vui lòng tạo quy tắc thương hiệu trước khi chạy AI.")

            campaign_id = int(str(selected_campaign).split(" - ")[0])
            brand_rule_id = int(str(selected_rule).split(" - ")[0])

            self.pipeline_result.delete("1.0", tk.END)
            self.pipeline_result.insert(tk.END, "Đang chạy pipeline...\n")
            self.update_idletasks()

            conn = get_connection()
            llm = LLMClient()
            orchestrator = AgentOrchestrator(llm_client=llm, db_connection=conn)
            output = orchestrator.run_pipeline(campaign_id=campaign_id, brand_rule_id=brand_rule_id)
            conn.close()

            summary = output.get("overall_score", 0)
            total_posts = output.get("total_posts", 0)
            self.pipeline_result.insert(tk.END, f"\nTổng bài viết: {total_posts}\n")
            self.pipeline_result.insert(tk.END, f"Điểm tuân thủ: {summary}/100\n")
            self.pipeline_result.insert(tk.END, "Pipeline hoàn tất.\n")
            self.set_status("Trạng thái: Pipeline đã hoàn tất", self.accent)
        except Exception as exc:
            self.pipeline_result.delete("1.0", tk.END)
            self.pipeline_result.insert(tk.END, f"Lỗi: {exc}\n")
            self.set_status(f"Pipeline lỗi: {exc}", self.accent_4)

    def render_calendar_page(self):
        self.title_label.configure(text="Lịch đăng")
        self.set_status("Trạng thái: Theo dõi đăng bài", self.accent_2)

        heading = tk.Label(self.content, text="Lịch đăng nội dung theo chiến dịch", bg=self.content_bg, fg=self.text, font=("Arial", 18, "bold"), anchor="w")
        heading.pack(anchor="w", pady=(8, 12))

        card = tk.Frame(self.content, bg=self.panel_bg, bd=0)
        card.pack(fill="both", expand=True)

        cols = ("Chiến dịch", "Giai đoạn", "Kênh", "Ngày đăng", "Tình trạng")
        tree = ttk.Treeview(card, columns=cols, show="headings", height=16, style="App.Treeview")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=190 if col != "Chiến dịch" else 260, anchor="center")
        tree.pack(fill="both", expand=True, padx=12, pady=12)

        try:
            conn = get_connection()
            campaigns = get_all_campaigns(conn)
            for c in campaigns:
                posts = get_posts_by_campaign(conn, c.get("id"))
                for p in posts:
                    tree.insert("", "end", values=(c.get("name", ""), p.get("stage", ""), p.get("channel", ""), p.get("scheduled_date", ""), p.get("status", "Pending")))
            if not campaigns:
                tree.insert("", "end", values=("Chưa có dữ liệu", "-", "-", "-", "-"))
            conn.close()
        except Exception as exc:
            tree.insert("", "end", values=(f"Lỗi: {exc}", "-", "-", "-", "-"))
            self.set_status(f"Không tải lịch đăng: {exc}", self.accent_4)

    def render_export_page(self):
        self.title_label.configure(text="Xuất báo cáo")
        self.set_status("Trạng thái: Xuất Excel & Email", self.accent_2)

        heading = tk.Label(self.content, text="Xuất báo cáo chiến dịch", bg=self.content_bg, fg=self.text, font=("Arial", 18, "bold"), anchor="w")
        heading.pack(anchor="w", pady=(8, 12))

        actions = tk.Frame(self.content, bg=self.content_bg)
        actions.pack(fill="x")

        tk.Button(actions, text="📥 Xuất Excel", bg=self.accent, fg="white", font=("Arial", 11, "bold"), padx=20, pady=12, command=self.export_selected_campaign).pack(side="left")
        tk.Button(actions, text="📧 Gửi Email", bg=self.accent_2, fg="white", font=("Arial", 11, "bold"), padx=20, pady=12, command=lambda: messagebox.showinfo("Gửi Email", "Chức năng gửi email sẽ được kích hoạt sau khi cấu hình SMTP trong .env.")).pack(side="left", padx=10)

        try:
            conn = get_connection()
            campaigns = get_all_campaigns(conn)
            conn.close()
        except Exception:
            campaigns = []

        self.export_campaign_var = tk.StringVar()
        if campaigns:
            self.export_campaign_var.set(f"{campaigns[0].get('id')} - {campaigns[0].get('name')}")
        else:
            self.export_campaign_var.set("Chưa có chiến dịch")

        selector = tk.Frame(self.content, bg=self.content_bg)
        selector.pack(fill="x", pady=(0, 14))
        tk.Label(selector, text="Chọn chiến dịch cần xuất: ", bg=self.content_bg, fg=self.text, font=("Segoe UI", 10, "bold")).pack(side="left")
        combo = ttk.Combobox(selector, textvariable=self.export_campaign_var, values=[f"{c.get('id')} - {c.get('name')}" for c in campaigns], state="readonly", width=50, style="App.TCombobox")
        combo.pack(side="left", padx=8)

        export_btn = tk.Button(
            selector,
            text="📥 Xuất Excel",
            bg=self.accent,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=18,
            pady=8,
            command=self.export_selected_campaign,
        )
        export_btn.pack(side="left", padx=8)

        info = tk.Frame(self.content, bg=self.panel_bg, bd=0)
        info.pack(fill="both", expand=True, pady=(20, 0))

        tk.Label(info, text="Lưu ý", bg=self.panel_bg, fg=self.accent_3, font=("Arial", 12, "bold")).pack(anchor="w", padx=16, pady=(16, 6))
        notice = (
            "- Mục menu đã được thiết kế rõ ràng hơn để người dùng dễ nhận biết chức năng.\n"
            "- Màu sắc được phân nhóm rõ theo từng module: chiến dịch, quy tắc, AI, lịch đăng, báo cáo.\n"
            "- Đây là ứng dụng desktop local, không chạy trên trình duyệt web."
        )
        tk.Label(info, text=notice, bg=self.panel_bg, fg=self.muted, justify="left", anchor="w", font=("Arial", 10), padx=16, pady=14).pack(anchor="w")

    def open_create_campaign_form(self):
        form = tk.Toplevel(self.root)
        form.title("Tạo chiến dịch mới")
        form.geometry("520x420")
        form.configure(bg=self.content_bg)

        tk.Label(form, text="Tạo chiến dịch marketing", bg=self.content_bg, fg=self.text, font=("Arial", 16, "bold")).pack(anchor="w", padx=18, pady=(18, 8))

        fields = {
            "name": ("Tên chiến dịch", ""),
            "product_name": ("Sản phẩm / dịch vụ", ""),
            "target_audience": ("Đối tượng mục tiêu", ""),
            "budget": ("Ngân sách", ""),
            "channels": ("Kênh truyền thông", ""),
            "start_date": ("Ngày bắt đầu (YYYY-MM-DD)", ""),
            "end_date": ("Ngày kết thúc (YYYY-MM-DD)", ""),
        }
        entries = {}

        for key, (label_text, default) in fields.items():
            frame = tk.Frame(form, bg=self.content_bg)
            frame.pack(fill="x", padx=18, pady=6)
            tk.Label(frame, text=label_text, bg=self.content_bg, fg=self.text, width=24, anchor="w").pack(side="left")
            entry = tk.Entry(frame, width=32, bg=self.panel_bg, fg=self.text, insertbackground=self.text, relief="solid", bd=1)
            entry.insert(0, default)
            entry.pack(side="right")
            entries[key] = entry

        def save_campaign():
            try:
                values = {k: v.get().strip() for k, v in entries.items()}
                if not values["name"] or not values["product_name"]:
                    raise ValueError("Tên chiến dịch và sản phẩm không được để trống.")
                conn = get_connection()
                create_campaign(
                    conn,
                    name=values["name"],
                    product_name=values["product_name"],
                    target_audience=values["target_audience"],
                    budget=values["budget"],
                    channels=values["channels"],
                    start_date=values["start_date"],
                    end_date=values["end_date"],
                )
                conn.close()
                form.destroy()
                self.show_page("campaigns")
                messagebox.showinfo("Thành công", "Chiến dịch đã được tạo.")
            except Exception as exc:
                messagebox.showerror("Lỗi", str(exc))

        tk.Button(form, text="Lưu chiến dịch", bg=self.accent, fg="white", font=("Arial", 10, "bold"), padx=18, pady=8, command=save_campaign).pack(pady=(18, 10))

    def open_create_rule_form(self):
        form = tk.Toplevel(self.root)
        form.title("Tạo bộ quy tắc thương hiệu")
        form.geometry("520x360")
        form.configure(bg=self.content_bg)

        tk.Label(form, text="Bộ quy tắc thương hiệu", bg=self.content_bg, fg=self.text, font=("Arial", 16, "bold")).pack(anchor="w", padx=18, pady=(18, 8))

        fields = {
            "rule_name": ("Tên bộ quy tắc", ""),
            "forbidden_words": ("Từ cấm", ""),
            "mandatory_keywords": ("Từ khóa bắt buộc", ""),
            "tone_of_voice": ("Tone of voice", ""),
        }
        entries = {}
        for key, (label_text, default) in fields.items():
            frame = tk.Frame(form, bg=self.content_bg)
            frame.pack(fill="x", padx=18, pady=6)
            tk.Label(frame, text=label_text, bg=self.content_bg, fg=self.text, width=24, anchor="w").pack(side="left")
            entry = tk.Entry(frame, width=32, bg=self.panel_bg, fg=self.text, insertbackground=self.text, relief="solid", bd=1)
            entry.insert(0, default)
            entry.pack(side="right")
            entries[key] = entry

        def save_rule():
            try:
                values = {k: v.get().strip() for k, v in entries.items()}
                if not values["rule_name"]:
                    raise ValueError("Tên bộ quy tắc không được để trống.")
                conn = get_connection()
                create_brand_rule(
                    conn,
                    rule_name=values["rule_name"],
                    forbidden_words=values["forbidden_words"],
                    mandatory_keywords=values["mandatory_keywords"],
                    tone_of_voice=values["tone_of_voice"],
                )
                conn.close()
                form.destroy()
                self.show_page("brand_rules")
                messagebox.showinfo("Thành công", "Bộ quy tắc đã được tạo.")
            except Exception as exc:
                messagebox.showerror("Lỗi", str(exc))

        tk.Button(form, text="Lưu bộ quy tắc", bg=self.accent_3, fg="white", font=("Arial", 10, "bold"), padx=18, pady=8, command=save_rule).pack(pady=(18, 10))

    def export_selected_campaign(self):
        try:
            selected = self.export_campaign_var.get()
            if not selected or selected.startswith("Chưa"):
                raise ValueError("Vui lòng chọn chiến dịch trước khi xuất Excel.")
            campaign_id = int(str(selected).split(" - ")[0])
            conn = get_connection()
            campaign = get_campaign_by_id(conn, campaign_id)
            posts = get_posts_by_campaign(conn, campaign_id)
            audit_logs = get_audits_by_campaign(conn, campaign_id)
            conn.close()

            if not campaign:
                raise ValueError("Không tìm thấy chiến dịch đã chọn.")

            excel_bytes = export_campaign_to_excel(campaign, posts, audit_logs)
            from tkinter import filedialog
            output_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                initialfile=f"Marketing_Campaign_{campaign_id}_Report.xlsx",
                filetypes=[("Excel file", "*.xlsx")],
            )
            if output_path:
                with open(output_path, "wb") as f:
                    f.write(excel_bytes)
                messagebox.showinfo("Thành công", f"File Excel đã được lưu tại: {output_path}")
        except Exception as exc:
            messagebox.showerror("Lỗi xuất Excel", str(exc))


def main():
    enable_windows_dpi_awareness()
    root = tk.Tk()
    root.option_add("*Font", "{Segoe UI} 10")
    app = MarketingDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
