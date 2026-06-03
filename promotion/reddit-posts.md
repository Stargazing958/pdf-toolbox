# Reddit 推广文案

---

## 帖子 1：r/InternetIsBeautiful（1660 万用户）

**标题：** freepdftools.top — Free PDF tools. No signup, no watermark, no limits.

**正文：**
Just a clean, simple site I built. Merge, compress, split, and convert PDFs to Word. Everything happens in your browser. Files are auto-deleted after 10 minutes — we don't store anything.

Why I built it: every "free" PDF tool I found either makes you sign up, adds a watermark, limits you to 2 pages, or charges money. So I built one that doesn't do any of that.

Costs me $103/year to run. Happy to keep it free.

---

## 帖子 2：r/software（350 万用户）

**标题：** I got tired of PDF tools that nickel-and-dime you, so I built my own — 100% free, no BS

**正文：**
Every time I needed to merge or compress a PDF, it was the same story:

- Sign up for an account
- "Upgrade to Pro for unlimited pages"
- Watermark on every page
- "Your free trial has expired"

So over the past few weeks, I built freepdftools.top. Here's what it does:

**Merge PDFs** — Combine multiple files into one
**Compress PDFs** — Reduce file size (uses Ghostscript, actually works)
**Split PDFs** — Extract pages by range
**PDF to Word** — Convert to editable .docx, preserves layout

**The deal:**
- No signup. No account. Ever.
- No watermarks. No page limits.
- Files are auto-deleted 10 minutes after processing.
- No tracking, no analytics (yet — might add privacy-friendly analytics to see if anyone's using it)

**Tech stack:** Flask + nginx + Ghostscript on a $68/year VPS. Domain was $35. Total cost: $103/year.

**What's next:** I'm planning to add rotate, reorder pages, and maybe an image-to-PDF tool. Open to suggestions.

Would love any feedback — especially on what PDF features you'd actually use.

---

## 帖子 3：r/SideProject（20 万用户）

**标题：** Built a free PDF toolbox after getting frustrated with paywalled tools — $103/year to run

**正文：**
The "aha" moment: I was trying to compress a PDF, and every free tool either required signup, added watermarks, or limited me to 2 pages. iLovePDF — the market leader — gets 145 million searches/month. The demand is massive, but the free options are garbage.

So I built this:
freepdftools.top

4 tools: Merge / Compress / Split / PDF to Word
All free. No signup. No limits. Files auto-deleted in 10 minutes.

**What I learned:**
- Ghostscript is the way to go for PDF compression (pikepdf's image manipulation is unreliable)
- nginx reverse proxy + gzip makes a huge difference on a cheap VPS
- pdf2docx handles academic papers surprisingly well (tested on a 4.8MB thesis)

**Costs:** $68/year (Alibaba Cloud Silicon Valley) + $35/year (domain) = $103/year total. No ad revenue yet — figuring that out.

Would love to hear what you'd add next, or any feedback on the UX.

---

## 帖子 4：r/Freebies（500 万用户）

**标题：** [FREE] Online PDF tools — merge, compress, split, convert to Word. No signup, no limits.

**正文：**
freepdftools.top is a completely free PDF toolbox:

✅ Merge multiple PDFs
✅ Compress PDFs (Ghostscript engine — actually reduces file size)
✅ Split PDF by page range
✅ Convert PDF to editable Word document (.docx)

No account required. No watermarks. Files deleted after 10 minutes.

Just a passion project — hope it helps someone out there.
