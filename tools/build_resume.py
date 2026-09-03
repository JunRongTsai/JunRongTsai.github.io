# -*- coding: utf-8 -*-
# 重新產生履歷 PDF：改動下面的內容後執行 `python tools/build_resume.py` 即可覆蓋 resume.pdf。
# 內嵌字型用系統內建的微軟正黑體 (與網站 CSS 字型一致)，需要在有安裝該字型的 Windows 環境執行；
# 若换到其他系統，把下面兩個 TTFont 路徑換成該系統上的繁中字型檔即可。
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle

FONT = "JhengHei"
FONT_BOLD = "JhengHeiBold"
pdfmetrics.registerFont(TTFont(FONT, "C:/Windows/Fonts/msjh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont(FONT_BOLD, "C:/Windows/Fonts/msjhbd.ttc", subfontIndex=0))

INK = colors.HexColor("#1a1f29")
MUTED = colors.HexColor("#54606e")
ACCENT = colors.HexColor("#1f6feb")
RULE = colors.HexColor("#d7dde3")

OUT_PATH = str(Path(__file__).resolve().parent.parent / "resume.pdf")

styles = {
    "name": ParagraphStyle("name", fontName=FONT_BOLD, fontSize=21, leading=25, textColor=INK),
    "title": ParagraphStyle("title", fontName=FONT, fontSize=12, leading=15, textColor=ACCENT, spaceAfter=2),
    "contact": ParagraphStyle("contact", fontName=FONT, fontSize=9.5, leading=13, textColor=MUTED),
    "summary": ParagraphStyle("summary", fontName=FONT, fontSize=9.5, leading=14.5, textColor=INK, spaceBefore=6, spaceAfter=2),
    "section": ParagraphStyle("section", fontName=FONT_BOLD, fontSize=12.5, leading=16, textColor=INK, spaceBefore=8, spaceAfter=4),
    "jobtitle": ParagraphStyle("jobtitle", fontName=FONT_BOLD, fontSize=10.5, leading=13.5, textColor=INK),
    "jobmeta": ParagraphStyle("jobmeta", fontName=FONT, fontSize=9, leading=12, textColor=MUTED, alignment=2),
    "bullet": ParagraphStyle("bullet", fontName=FONT, fontSize=9.3, leading=13.2, textColor=INK, leftIndent=12, spaceAfter=1.5,
                              bulletFontName=FONT, bulletFontSize=9.3, bulletIndent=2),
    "projtitle": ParagraphStyle("projtitle", fontName=FONT_BOLD, fontSize=10, leading=13, textColor=INK),
    "projdesc": ParagraphStyle("projdesc", fontName=FONT, fontSize=9.2, leading=13, textColor=INK, spaceAfter=1),
    "tags": ParagraphStyle("tags", fontName=FONT, fontSize=8.5, leading=11.5, textColor=ACCENT, spaceAfter=4),
    "skillcat": ParagraphStyle("skillcat", fontName=FONT_BOLD, fontSize=9.5, leading=13, textColor=INK),
    "skillitems": ParagraphStyle("skillitems", fontName=FONT, fontSize=9.3, leading=13, textColor=INK, spaceAfter=5),
    "edu": ParagraphStyle("edu", fontName=FONT, fontSize=9.5, leading=13.5, textColor=INK),
}

def rule():
    return HRFlowable(width="100%", thickness=0.75, color=RULE, spaceBefore=2, spaceAfter=8)

def section_title(text):
    return [Paragraph(text, styles["section"]), rule()]

def job_block(title, company, period, bullets):
    header_table = Table(
        [[Paragraph(f"{title}　<font color='#1f6feb'>{company}</font>", styles["jobtitle"]),
          Paragraph(period, styles["jobmeta"])]],
        colWidths=[128 * mm, 42 * mm],
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    flow = [header_table]
    for b in bullets:
        flow.append(Paragraph(b, styles["bullet"], bulletText="•"))
    flow.append(Spacer(1, 4))
    return flow

def project_block(title, desc, tags):
    return [
        Paragraph(title, styles["projtitle"]),
        Paragraph(desc, styles["projdesc"]),
        Paragraph("　".join(tags), styles["tags"]),
    ]

def skill_row(category, items):
    return Paragraph(f"<font name='{FONT_BOLD}'>{category}：</font>{items}", styles["skillitems"])


doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    topMargin=13 * mm, bottomMargin=12 * mm, leftMargin=18 * mm, rightMargin=18 * mm,
    title="蔡俊榮 (Rowan Tsai) - 履歷",
    author="蔡俊榮 (Rowan Tsai)",
)

story = []

# --- Header ---
story.append(Paragraph("蔡俊榮 <font color='#54606e'>Rowan Tsai</font>", styles["name"]))
story.append(Paragraph("後端軟體工程師 · 系統架構設計 · 自動化流程專家", styles["title"]))
story.append(Paragraph(
    '<link href="mailto:markben841027@gmail.com" color="#1f6feb">markben841027@gmail.com</link>　|　'
    '<link href="https://junrongtsai.github.io/" color="#1f6feb">junrongtsai.github.io</link>'
    '　|　國立高雄科技大學 資訊管理系',
    styles["contact"]
))
story.append(Paragraph(
    "熱衷於解決複雜的後端難題，專注於建構高效率、高可用的系統架構。"
    "擁有紮實的 C#、Java 與 Python 開發經驗，從自動化工具到企業級應用皆能得心應手，"
    "近期也將 AI 輔助開發工具導入日常工作流程，加速系統開發與維護效率。",
    styles["summary"]
))
story.append(Spacer(1, 4))
story.append(rule())

# --- Experience ---
story += section_title("職涯經歷")
story += job_block(
    "CIM 工程師 (後端開發與系統整合)", "華新科技 Walsin Technology", "2025/10 - 現今",
    [
        "MES 功能優化與開發：這一年主要負責既有 MES 功能優化，並持續開發新功能模組，確保產線資訊流高可用性。",
        "PLC 機台監控：串接產線 PLC 設備，即時掌握機台運作狀態與關鍵製程參數。",
        "環境溫溼度監控：建置各站點溫溼度監控機制，確保生產環境條件符合製程要求。",
        "監控資訊整合：將監控資訊串接至 SingleR 內部網頁，方便各單位人員即時查看設備狀態。",
        "異常告警通知：建立機台異常 LINE 即時通知機制，加快現場人員應變速度。",
        "廠區即時監控圖：開發廠區即時監控圖，視覺化呈現各產線與設備運作狀態。",
    ]
)
story += job_block(
    "MES 工程師 (C# 後端開發)", "先進光電 AOET", "2023/06 - 2025/09",
    [
        "系統客製化：使用 C# 設計後端邏輯與操作介面，優化作業流程。",
        "自動化排程：利用 WinForms 與批次腳本建立報表自動寄送機制。",
        "流程自動化 (RPA)：維護 UiPath 流程，大幅減少人工重複操作。",
        "資料處理：撰寫 Python 爬蟲與 Excel VBA，提升資料整合效率。",
    ]
)
story += job_block(
    "軟體工程師 (Java Web 開發)", "鼎新數智 Digiwin", "2019/10 - 2023/06",
    [
        "Web 全端開發：使用 Java Web, HTML, TypeScript 維護企業級系統。",
        "資料視覺化：使用 FineReport 整合 Oracle DB 開發商業報表。",
        "系統整合：協助 ETL 資料交換與 DevOps (Jenkins/SVN) 版控管理。",
    ]
)

# --- Projects ---
story += section_title("精選專案")
story += project_block(
    "即時監控系統開發",
    "透過 Modbus/TCP 協定與硬體設備通訊，實現高頻率自動輪詢 (Polling) 機制，即時掌握設備狀態與異常警報，確保系統穩定運行。",
    ["C#", "Modbus", "WinForms", "Multi-threading"]
)
story += project_block(
    "AutoBackup 自動化工具",
    "開發 Windows Service 工具，自動偵測關鍵資料夾變動並進行壓縮備份，包含完整 Log 記錄與排程設定，大幅降低人工備份的時間成本。",
    ["C#", "IO Stream", "Automation"]
)
story += project_block(
    "自動化報表系統",
    "整合 WinForms 與 Python 腳本，每日自動抓取數據並產出視覺化報表，將繁瑣的資料整理工作自動化，並自動寄送給相關部門。",
    ["Python", "VBA", "SMTP", "RPA"]
)

# --- Skills ---
story += section_title("專業技能")
story.append(skill_row("後端與系統開發", "C# (.NET)、Java (Spring)、Python、WinForms、RESTful API"))
story.append(skill_row("資料庫與工具", "Oracle SQL、SQL Server、Redis、Git / SVN、Jenkins"))
story.append(skill_row("領域知識", "MES 系統、PLC (Modbus)、RPA、ETL"))
story.append(skill_row("AI 協作開發", "AI Coding (Claude Code)、Prompt Engineering、AI 輔助除錯與重構"))

# --- Education ---
story += section_title("學歷")
story.append(Paragraph("<font name='%s'>國立高雄科技大學</font>　資訊管理系　(2014 - 2018)" % FONT_BOLD, styles["edu"]))

doc.build(story)
print("built", OUT_PATH)
