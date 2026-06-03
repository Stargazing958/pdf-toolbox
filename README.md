# PDF Toolbox

Free online PDF tools — merge, compress, split, and convert PDFs to Word. No signup, no watermark, no limits.

🔗 **Live site:** [freepdftools.top](http://freepdftools.top)

## Features

| Tool | API | Description |
|------|-----|-------------|
| Merge PDFs | `/merge` | Combine multiple PDFs into one |
| Compress PDF | `/compress` | Reduce file size (Ghostscript engine) |
| Split PDF | `/split` | Extract pages by range or split all |
| PDF to Word | `/convert` | Convert PDF to editable .docx |

- ✅ 100% free, unlimited use
- ✅ No signup required
- ✅ No watermarks
- ✅ Files auto-deleted after 10 minutes
- ✅ 50MB upload limit

## Tech Stack

- **Backend:** Python 3.12 + Flask
- **Compression:** Ghostscript
- **PDF parsing:** PyPDF2, pdf2docx
- **Server:** nginx + gunicorn
- **Infrastructure:** Alibaba Cloud lightweight server (Silicon Valley)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py --port 5000

# Open browser
open http://localhost:5000
```

## Deployment

```bash
# With gunicorn
gunicorn app:app --bind 0.0.0.0:8000

# Behind nginx (recommended)
# Add client_max_body_size 100m; in nginx config
```

## License

MIT
