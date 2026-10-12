import ctypes
import os
import sys
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from agents.orchestrator import AgentOrchestrator
from database.connection import get_connection
from database.crud import (
    create_brand_rule,
    create_campaign,
    get_all_brand_rules,
    get_all_campaigns,
    get_audits_by_campaign,
    get_campaign_by_id,
    get_posts_by_campaign,
)
from utils.export_excel import export_campaign_to_excel
from utils.llm_client import LLMClient


class MarketingDesktopApp:
    BG = "#f6f2ec"
    SURFACE = "#fffdfa"
    SIDEBAR = "#20252b"
    SIDEBAR_MUTED = "#aeb5bc"
    INK = "#20252b"
    MUTED = "#68727c"
    LINE = "#e3ded7"
    CORAL = "#e25b3f"
    BLUE = "#2b6f9f"
    GOLD = "#b7852d"
    GREEN = "#3b866e"

    def __init__(self, root):
        self.root = root
        self.root.title("Marketing AI Campaign Studio")
        self.root.geometry("1420x820")
        self.root.minsize(1100, 700)
        self.root.configure(bg=self.BG)
        self.current_page = "campaigns"
        self.nav_buttons = {}
        self.page_title = None
        self.status_label = None
        self.content = None
        self.setup_style()
        self.build_shell()
        self.show_page("campaigns")

    def setup_style(self):
        style = ttk.Style(self.root)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        else:
            style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("App.TFrame", background=self.BG)
        style.configure("Surface.TFrame", background=self.SURFACE)
        style.configure("Sidebar.TFrame", background=self.SIDEBAR)
        style.configure("Title.TLabel", background=self.BG, foreground=self.INK, font=("Segoe UI", 23, "bold"))
        style.configure("Subtitle.TLabel", background=self.BG, foreground=self.MUTED, font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", background=self.SURFACE, foreground=self.INK, font=("Segoe UI", 12, "bold"))
        style.configure("CardValue.TLabel", background=self.SURFACE, foreground=self.INK, font=("Segoe UI", 21, "bold"))
        style.configure("Muted.TLabel", background=self.SURFACE, foreground=self.MUTED, font=("Segoe UI", 10))
        style.configure("SidebarBrand.TLabel", background=self.SIDEBAR, foreground="#ffffff", font=("Segoe UI", 16, "bold"))
        style.configure("SidebarCaption.TLabel", background=self.SIDEBAR, foreground=self.SIDEBAR_MUTED, font=("Segoe UI", 9))
        style.configure("Nav.TButton", background=self.SIDEBAR, foreground="#e7eaed", borderwidth=0, anchor="w", padding=(16, 12), font=("Segoe UI", 10, "bold"))
        style.map("Nav.TButton", background=[("active", "#30383f")], foreground=[("active", "#ffffff")])
        style.configure("NavActive.TButton", background=self.CORAL, foreground="#ffffff", borderwidth=0, anchor="w", padding=(16, 12), font=("Segoe UI", 10, "bold"))
        style.configure("Primary.TButton", background=self.CORAL, foreground="#ffffff", padding=(16, 9), font=("Segoe UI", 10, "bold"))
        style.map("Primary.TButton", background=[("active", "#bd4932")])
        style.configure("Secondary.TButton", background="#e8e2da", foreground=self.INK, padding=(14, 9), font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", background=self.SURFACE, fieldbackground=self.SURFACE, foreground=self.INK, rowheight=38, borderwidth=0, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#eee8e0", foreground=self.INK, relief="flat", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#f6d9d1")], foreground=[("selected", self.INK)])
        style.configure("TCombobox", padding=8, font=("Segoe UI", 10))

    def build_shell(self):
        sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=260)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        brand = ttk.Frame(sidebar, style="Sidebar.TFrame")
        brand.pack(fill="x", padx=22, pady=(28, 30))
        ttk.Label(brand, text="MA", style="SidebarBrand.TLabel").pack(anchor="w")
        ttk.Label(brand, text="MARKETING AI", style="SidebarBrand.TLabel").pack(anchor="w", pady=(8, 0))
        ttk.Label(brand, text="CAMPAIGN STUDIO", style="SidebarCaption.TLabel").pack(anchor="w", pady=(3, 0))
        ttk.Label(sidebar, text="WORKSPACE", style="SidebarCaption.TLabel").pack(anchor="w", padx=22, pady=(0, 8))

        nav = ttk.Frame(sidebar, style="Sidebar.TFrame")
        nav.pack(fill="x", padx=10)
        pages = [
            ("campaigns", "Campaigns", "Plan and monitor"),
            ("brand_rules", "Brand rules", "Keep content on-brand"),
            ("pipeline", "AI pipeline", "Create with 3 agents"),
            ("calendar", "Content calendar", "Track scheduled posts"),
            ("export", "Reports", "Export campaign data"),
        ]
        for key, title, hint in pages:
            button = ttk.Button(nav, text=f"  {title}\n  {hint}", style="Nav.TButton", command=lambda p=key: self.show_page(p))
            button.pack(fill="x", pady=3)
            self.nav_buttons[key] = button

        status = ttk.Frame(sidebar, style="Sidebar.TFrame")
        status.pack(side="bottom", fill="x", padx=22, pady=24)
        ttk.Label(status, text="SYSTEM", style="SidebarCaption.TLabel").pack(anchor="w", pady=(0, 8))
        ttk.Label(status, text="●  Database layer ready", style="SidebarCaption.TLabel").pack(anchor="w", pady=2)
        ttk.Label(status, text="●  3 agents available", style="SidebarCaption.TLabel").pack(anchor="w", pady=2)

        main = ttk.Frame(self.root, style="App.TFrame")
        main.pack(side="left", fill="both", expand=True)
        top = ttk.Frame(main, style="App.TFrame", height=104)
        top.pack(fill="x", padx=34, pady=(26, 0))
        top.pack_propagate(False)
        self.page_title = ttk.Label(top, text="Campaigns", style="Title.TLabel")
        self.page_title.pack(anchor="w")
        self.subtitle = ttk.Label(top, text="Build, review, and ship better marketing campaigns.", style="Subtitle.TLabel")
        self.subtitle.pack(anchor="w", pady=(4, 0))
        self.status_label = ttk.Label(top, text="Ready", style="Subtitle.TLabel")
        self.status_label.pack(anchor="e", pady=(0, 8))
        self.content = ttk.Frame(main, style="App.TFrame")
        self.content.pack(fill="both", expand=True, padx=34, pady=(0, 28))

    def show_page(self, page):
        self.current_page = page
        for key, button in self.nav_buttons.items():
            button.configure(style="NavActive.TButton" if key == page else "Nav.TButton")
        for child in self.content.winfo_children():
            child.destroy()
        renderers = {
            "campaigns": self.render_campaigns,
            "brand_rules": self.render_rules,
            "pipeline": self.render_pipeline,
            "calendar": self.render_calendar,
            "export": self.render_export,
        }
        renderers[page]()

    def set_header(self, title, subtitle, status="Ready"):
        self.page_title.configure(text=title)
        self.subtitle.configure(text=subtitle)
        self.status_label.configure(text=status)

    def page_heading(self, text):
        ttk.Label(self.content, text=text, style="CardTitle.TLabel").pack(anchor="w", pady=(0, 14))

    def render_campaigns(self):
        self.set_header("Campaigns", "Build, review, and ship better marketing campaigns.", "Workspace ready")
        self.page_heading("Campaign workspace")
        metrics = ttk.Frame(self.content, style="App.TFrame")
        metrics.pack(fill="x", pady=(0, 18))
        for title, value, hint in [("Plan", "01", "Define the brief"), ("Create", "02", "Generate content"), ("Review", "03", "Audit brand fit")]:
            card = ttk.Frame(metrics, style="Surface.TFrame", padding=18)
            card.pack(side="left", fill="both", expand=True, padx=(0, 12))
            ttk.Label(card, text=title.upper(), style="Muted.TLabel").pack(anchor="w")
            ttk.Label(card, text=value, style="CardValue.TLabel").pack(anchor="w", pady=(5, 0))
            ttk.Label(card, text=hint, style="Muted.TLabel").pack(anchor="w")
        table = ttk.Frame(self.content, style="Surface.TFrame", padding=18)
        table.pack(fill="both", expand=True)
        ttk.Label(table, text="All campaigns", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 12))
        tree = self.make_tree(table, ("ID", "Campaign name", "Product", "Status"), (70, 280, 260, 130))
        try:
            conn = get_connection()
            campaigns = get_all_campaigns(conn)
            conn.close()
            for item in campaigns:
                tree.insert("", "end", values=(item.get("id"), item.get("name", ""), item.get("product_name", ""), item.get("status", "Draft")))
            if not campaigns:
                tree.insert("", "end", values=("-", "No campaigns yet", "Create your first brief", "Draft"))
        except Exception as exc:
            tree.insert("", "end", values=("-", "Database unavailable", str(exc)[:70], "Error"))
            self.status_label.configure(text="Database needs attention")
        actions = ttk.Frame(self.content, style="App.TFrame")
        actions.pack(fill="x", pady=(16, 0))
        ttk.Button(actions, text="Create campaign", style="Primary.TButton", command=self.open_campaign_form).pack(side="left")
        ttk.Button(actions, text="Refresh", style="Secondary.TButton", command=lambda: self.show_page("campaigns")).pack(side="left", padx=10)

    def make_tree(self, parent, columns, widths):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for column, width in zip(columns, widths):
            tree.heading(column, text=column)
            tree.column(column, width=width, anchor="w")
        tree.pack(fill="both", expand=True)
        return tree

    def render_rules(self):
        self.set_header("Brand rules", "Protect tone, language, and compliance across every channel.", "Rules workspace")
        self.page_heading("Rules library")
        card = ttk.Frame(self.content, style="Surface.TFrame", padding=18)
        card.pack(fill="both", expand=True)
        tree = self.make_tree(card, ("ID", "Rule set", "Forbidden words", "Tone of voice"), (70, 260, 300, 220))
        try:
            conn = get_connection()
            rules = get_all_brand_rules(conn)
            conn.close()
            for item in rules:
                tree.insert("", "end", values=(item.get("id"), item.get("rule_name", ""), item.get("forbidden_words", "")[:55], item.get("tone_of_voice", "")))
            if not rules:
                tree.insert("", "end", values=("-", "No rules yet", "Add a brand rule", "-"))
        except Exception as exc:
            tree.insert("", "end", values=("-", "Database unavailable", str(exc)[:60], "Error"))
        ttk.Button(self.content, text="Create brand rule", style="Primary.TButton", command=self.open_rule_form).pack(anchor="w", pady=(16, 0))

    def render_pipeline(self):
        self.set_header("AI pipeline", "Run market insight, copywriting, and brand audit in sequence.", "3 agents ready")
        self.page_heading("Create campaign content")
        panel = ttk.Frame(self.content, style="Surface.TFrame", padding=22)
        panel.pack(fill="both", expand=True)
        ttk.Label(panel, text="Campaign", style="CardTitle.TLabel").pack(anchor="w")
        campaigns = self.load_campaigns()
        self.campaign_var = tk.StringVar(value=campaigns[0] if campaigns else "No campaign available")
        ttk.Combobox(panel, textvariable=self.campaign_var, values=campaigns, state="readonly", width=60).pack(anchor="w", pady=(7, 18))
        ttk.Label(panel, text="Brand rule set", style="CardTitle.TLabel").pack(anchor="w")
        rules = self.load_rules()
        self.rule_var = tk.StringVar(value=rules[0] if rules else "No rule available")
        ttk.Combobox(panel, textvariable=self.rule_var, values=rules, state="readonly", width=60).pack(anchor="w", pady=(7, 18))
        ttk.Button(panel, text="Run AI pipeline", style="Primary.TButton", command=self.run_pipeline).pack(anchor="w")
        self.pipeline_result = tk.Text(panel, height=12, bg="#fffdfa", fg=self.INK, relief="flat", bd=1, padx=12, pady=12, font=("Consolas", 10))
        self.pipeline_result.pack(fill="both", expand=True, pady=(18, 0))

    def load_campaigns(self):
        try:
            conn = get_connection()
            data = get_all_campaigns(conn)
            conn.close()
            return [f"{item.get('id')} - {item.get('name', '')}" for item in data]
        except Exception:
            return []

    def load_rules(self):
        try:
            conn = get_connection()
            data = get_all_brand_rules(conn)
            conn.close()
            return [f"{item.get('id')} - {item.get('rule_name', '')}" for item in data]
        except Exception:
            return []

    def run_pipeline(self):
        try:
            if self.campaign_var.get().startswith("No ") or self.rule_var.get().startswith("No "):
                raise ValueError("Create a campaign and a brand rule before running the pipeline.")
            campaign_id = int(self.campaign_var.get().split(" - ")[0])
            rule_id = int(self.rule_var.get().split(" - ")[0])
            self.pipeline_result.delete("1.0", tk.END)
            self.pipeline_result.insert(tk.END, "Running the three-agent pipeline...\n")
            self.root.update_idletasks()
            conn = get_connection()
            output = AgentOrchestrator(LLMClient(), conn).run_pipeline(campaign_id=campaign_id, brand_rule_id=rule_id)
            conn.close()
            self.pipeline_result.insert(tk.END, f"\nPosts created: {output.get('total_posts', 0)}\nCompliance score: {output.get('overall_score', 0)}/100\nPipeline complete.\n")
            self.status_label.configure(text="Pipeline complete")
        except Exception as exc:
            self.pipeline_result.delete("1.0", tk.END)
            self.pipeline_result.insert(tk.END, f"Pipeline error:\n{exc}")
            self.status_label.configure(text="Pipeline needs attention")

    def render_calendar(self):
        self.set_header("Content calendar", "See every scheduled post by campaign, stage, and channel.", "Publishing view")
        self.page_heading("Scheduled content")
        card = ttk.Frame(self.content, style="Surface.TFrame", padding=18)
        card.pack(fill="both", expand=True)
        tree = self.make_tree(card, ("Campaign", "Stage", "Channel", "Publish date", "Status"), (250, 150, 160, 180, 130))
        try:
            conn = get_connection()
            for campaign in get_all_campaigns(conn):
                for post in get_posts_by_campaign(conn, campaign.get("id")):
                    tree.insert("", "end", values=(campaign.get("name", ""), post.get("stage", ""), post.get("channel", ""), post.get("scheduled_date", ""), post.get("status", "Pending")))
            conn.close()
        except Exception as exc:
            tree.insert("", "end", values=("Database unavailable", str(exc)[:40], "-", "-", "Error"))

    def render_export(self):
        self.set_header("Reports", "Export campaign performance, posts, and audit history.", "Export center")
        self.page_heading("Campaign report")
        panel = ttk.Frame(self.content, style="Surface.TFrame", padding=22)
        panel.pack(fill="both", expand=True)
        ttk.Label(panel, text="Select campaign", style="CardTitle.TLabel").pack(anchor="w")
        campaigns = self.load_campaigns()
        self.export_var = tk.StringVar(value=campaigns[0] if campaigns else "No campaign available")
        ttk.Combobox(panel, textvariable=self.export_var, values=campaigns, state="readonly", width=65).pack(anchor="w", pady=(7, 18))
        ttk.Button(panel, text="Export Excel report", style="Primary.TButton", command=self.export_report).pack(anchor="w")
        ttk.Label(panel, text="The report includes campaign details, generated posts, and brand audit logs.", style="Muted.TLabel").pack(anchor="w", pady=(18, 0))

    def export_report(self):
        try:
            if self.export_var.get().startswith("No "):
                raise ValueError("Create a campaign before exporting a report.")
            campaign_id = int(self.export_var.get().split(" - ")[0])
            conn = get_connection()
            campaign = get_campaign_by_id(conn, campaign_id)
            posts = get_posts_by_campaign(conn, campaign_id)
            audits = get_audits_by_campaign(conn, campaign_id)
            conn.close()
            output = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel workbook", "*.xlsx")], initialfile=f"campaign_{campaign_id}_report.xlsx")
            if output:
                with open(output, "wb") as handle:
                    handle.write(export_campaign_to_excel(campaign, posts, audits))
                messagebox.showinfo("Export complete", "The Excel report was saved successfully.")
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc))

    def open_campaign_form(self):
        self.open_form("Create campaign", [("name", "Campaign name"), ("product_name", "Product or service"), ("target_audience", "Target audience"), ("budget", "Budget"), ("channels", "Channels")], self.save_campaign)

    def open_rule_form(self):
        self.open_form("Create brand rule", [("rule_name", "Rule set name"), ("forbidden_words", "Forbidden words"), ("mandatory_keywords", "Mandatory keywords"), ("tone_of_voice", "Tone of voice")], self.save_rule)

    def open_form(self, title, fields, callback):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("560x430")
        dialog.configure(bg=self.BG)
        values = {}
        ttk.Label(dialog, text=title, style="Title.TLabel").pack(anchor="w", padx=28, pady=(24, 20))
        body = ttk.Frame(dialog, style="App.TFrame")
        body.pack(fill="both", expand=True, padx=28)
        for key, label in fields:
            ttk.Label(body, text=label, style="Subtitle.TLabel").pack(anchor="w", pady=(0, 4))
            entry = ttk.Entry(body, width=58)
            entry.pack(fill="x", pady=(0, 13))
            values[key] = entry
        ttk.Button(dialog, text="Save", style="Primary.TButton", command=lambda: callback(dialog, values)).pack(anchor="w", padx=28, pady=22)

    def save_campaign(self, dialog, fields):
        try:
            data = {key: entry.get().strip() for key, entry in fields.items()}
            if not data["name"] or not data["product_name"]:
                raise ValueError("Campaign name and product are required.")
            conn = get_connection()
            create_campaign(conn, **data)
            conn.close()
            dialog.destroy()
            self.show_page("campaigns")
        except Exception as exc:
            messagebox.showerror("Could not save campaign", str(exc), parent=dialog)

    def save_rule(self, dialog, fields):
        try:
            data = {key: entry.get().strip() for key, entry in fields.items()}
            if not data["rule_name"]:
                raise ValueError("Rule set name is required.")
            conn = get_connection()
            create_brand_rule(conn, **data)
            conn.close()
            dialog.destroy()
            self.show_page("brand_rules")
        except Exception as exc:
            messagebox.showerror("Could not save rule", str(exc), parent=dialog)


def enable_dpi_awareness():
    if sys.platform == "win32":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except (AttributeError, OSError):
                pass


def main():
    enable_dpi_awareness()
    root = tk.Tk()
    app = MarketingDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
