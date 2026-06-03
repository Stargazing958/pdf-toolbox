# Product Hunt 发布方案

---

## 基本信息

- **产品名：** Free PDF Tools
- **Tagline：** Merge, compress, split & convert PDFs — 100% free, no signup
- **URL：** freepdftools.top
- **价格：** Free
- **分类：** Productivity / Developer Tools

---

## 产品描述

Tired of PDF tools that make you sign up, add watermarks, or charge for basic features? Me too. So I built one that doesn't.

**What it does:**
🔄 Merge — Combine multiple PDFs into one
🗜️ Compress — Reduce file size with Ghostscript (actually works)
✂️ Split — Extract pages by range or split all
📝 PDF to Word — Convert to editable .docx, preserves layout

**Why it's different:**
- No account required. Ever.
- No watermarks. No page limits.
- Files auto-deleted 10 minutes after processing.
- Runs on a $68/year VPS (no VC funding, no exit strategy — just a useful tool)

**Built with:** Python (Flask), Ghostscript, pdf2docx, nginx, served from a Silicon Valley server.

---

## 第一评论（Maker Comment）

Hey everyone! I built this because I kept running into PDF tools that felt like they were designed to extract money rather than help people. The market leader (iLovePDF) gets 145M searches/month — clearly people need this — but the free options are awful.

A few things I'd love feedback on:
1. What's the ONE PDF feature you need that's missing?
2. The PDF to Word conversion — I tested it on academic papers, but would love to know if it handles specific formats well
3. Would you trust a tool like this for sensitive documents? (We don't store anything, but I know trust is a big ask)

Tech-wise: Ghostscript for compression was a game-changer. Tried pikepdf first — total headache. If anyone's building PDF tools, happy to share what I learned.

---

## 截图建议（准备这几张）

1. **首页全貌** — 四个 tab 全貌，默认在 Merge 页
2. **压缩对比** — 上传前/后的文件大小对比
3. **PDF 转 Word** — 转换结果展示
4. **空状态 + 隐私承诺** — 突出"No signup / Auto-deleted after 10 min"

---

## 发布时机

- 最佳：**周二/周三/周四** PST 凌晨 0:01（对应北京时间下午 15:01）
- 避开周五和周末（投票量减少）
- 避开美国节假日
