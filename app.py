"""
PDF Toolbox — Free & Unlimited
Flask 后端：合并 / 压缩 / 拆分 / 转 Word
"""

import os, time, uuid, zipfile, threading, shutil, subprocess
from datetime import datetime
from flask import Flask, request, send_file, jsonify, render_template
from PyPDF2 import PdfReader, PdfWriter

# ========== 配置 ==========
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
FILE_TTL = 600  # 10 分钟后自动删除

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE


# ========== 清理函数 ==========
def cleanup_later(path, delay=FILE_TTL):
    def _clean():
        time.sleep(delay)
        try:
            if os.path.isfile(path):
                os.remove(path)
        except OSError:
            pass
    t = threading.Thread(target=_clean, daemon=True)
    t.start()


# ========== 首页 ==========
@app.route("/")
def index():
    return render_template("index.html")


# ========== PDF 合并 ==========
@app.route("/merge", methods=["POST"])
def merge_pdfs():
    files = request.files.getlist("files")
    if not files or len(files) < 2:
        return jsonify({"error": "至少上传 2 个 PDF 文件"}), 400

    writer = PdfWriter()
    temp_files = []

    for f in files:
        if not f.filename.lower().endswith(".pdf"):
            return jsonify({"error": f"'{f.filename}' 不是 PDF 文件"}), 400
        tmp = os.path.join(UPLOAD_DIR, f"merge_{uuid.uuid4().hex}.pdf")
        f.save(tmp)
        temp_files.append(tmp)
        reader = PdfReader(tmp)
        for page in reader.pages:
            writer.add_page(page)

    out_name = f"merged_{uuid.uuid4().hex[:8]}.pdf"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    with open(out_path, "wb") as out:
        writer.write(out)

    for t in temp_files:
        try:
            os.remove(t)
        except OSError:
            pass

    cleanup_later(out_path)
    return send_file(out_path, as_attachment=True, download_name="merged.pdf")


# ========== PDF 压缩 ==========
@app.route("/compress", methods=["POST"])
def compress_pdf():
    f = request.files.get("file")
    if not f or not f.filename.lower().endswith(".pdf"):
        return jsonify({"error": "请上传一个 PDF 文件"}), 400

    tmp = os.path.join(UPLOAD_DIR, f"compress_{uuid.uuid4().hex}.pdf")
    f.save(tmp)
    original_size = os.path.getsize(tmp)

    out_name = f"compressed_{uuid.uuid4().hex[:8]}.pdf"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    try:
        result = subprocess.run([
            "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={out_path}", tmp
        ], capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise RuntimeError(f"Ghostscript failed: {result.stderr}")
    except Exception:
        shutil.copy2(tmp, out_path)

    compressed_size = os.path.getsize(out_path)

    should_delete = True
    if compressed_size >= original_size:
        try:
            os.remove(out_path)
        except OSError:
            pass
        out_path = tmp
        compressed_size = original_size
        should_delete = False

    reduction = round((1 - compressed_size / original_size) * 100, 1) if original_size > 0 else 0

    try:
        if out_path != tmp:
            os.remove(tmp)
    except OSError:
        pass

    if should_delete:
        cleanup_later(out_path)
    response = send_file(out_path, as_attachment=True, download_name="compressed.pdf")
    response.headers["X-Reduction"] = f"{reduction}%"
    return response


# ========== PDF 拆分 ==========
@app.route("/split", methods=["POST"])
def split_pdf():
    f = request.files.get("file")
    if not f or not f.filename.lower().endswith(".pdf"):
        return jsonify({"error": "请上传一个 PDF 文件"}), 400

    pages_str = request.form.get("pages", "").strip()
    tmp = os.path.join(UPLOAD_DIR, f"split_{uuid.uuid4().hex}.pdf")
    f.save(tmp)

    reader = PdfReader(tmp)
    total = len(reader.pages)

    if pages_str:
        indices = set()
        for part in pages_str.split(","):
            part = part.strip()
            if "-" in part:
                a, b = part.split("-", 1)
                for i in range(int(a.strip()) - 1, int(b.strip())):
                    if 0 <= i < total:
                        indices.add(i)
            else:
                i = int(part) - 1
                if 0 <= i < total:
                    indices.add(i)
        indices = sorted(indices)
    else:
        indices = list(range(total))

    if len(indices) <= 1:
        writer = PdfWriter()
        writer.add_page(reader.pages[indices[0]] if indices else reader.pages[0])
        out_name = f"split_{uuid.uuid4().hex[:8]}.pdf"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        with open(out_path, "wb") as out:
            writer.write(out)
        try:
            os.remove(tmp)
        except OSError:
            pass
        cleanup_later(out_path)
        return send_file(out_path, as_attachment=True,
                         download_name=f"page_{indices[0]+1 if indices else 1}.pdf")

    zip_name = f"split_{uuid.uuid4().hex[:8]}.zip"
    zip_path = os.path.join(OUTPUT_DIR, zip_name)
    with zipfile.ZipFile(zip_path, "w") as zf:
        for idx in indices:
            writer = PdfWriter()
            writer.add_page(reader.pages[idx])
            page_path = os.path.join(OUTPUT_DIR, f"page_{idx+1}_{uuid.uuid4().hex[:4]}.pdf")
            with open(page_path, "wb") as out:
                writer.write(out)
            zf.write(page_path, f"page_{idx+1}.pdf")
            os.remove(page_path)

    try:
        os.remove(tmp)
    except OSError:
        pass

    cleanup_later(zip_path)
    return send_file(zip_path, as_attachment=True, download_name="split_pages.zip")


# ========== PDF 转 Word ==========
@app.route("/convert", methods=["POST"])
def convert_to_word():
    f = request.files.get("file")
    if not f or not f.filename.lower().endswith(".pdf"):
        return jsonify({"error": "请上传一个 PDF 文件"}), 400

    tmp = os.path.join(UPLOAD_DIR, f"convert_{uuid.uuid4().hex}.pdf")
    f.save(tmp)

    out_name = f"converted_{uuid.uuid4().hex[:8]}.docx"
    out_path = os.path.join(OUTPUT_DIR, out_name)

    try:
        from pdf2docx import Converter as DocxConverter
        cv = DocxConverter(tmp)
        cv.convert(out_path, start=0, end=None)
        cv.close()
    except Exception as e:
        try:
            os.remove(tmp)
        except OSError:
            pass
        return jsonify({"error": f"转换失败: {str(e)}"}), 500

    try:
        os.remove(tmp)
    except OSError:
        pass

    cleanup_later(out_path)
    return send_file(out_path, as_attachment=True, download_name="converted.docx")


# ========== PDF 旋转 ==========
@app.route("/rotate", methods=["POST"])
def rotate_pdf():
    f = request.files.get("file")
    if not f or not f.filename.lower().endswith(".pdf"):
        return jsonify({"error": "请上传一个 PDF 文件"}), 400

    angle_str = request.form.get("angle", "90")
    try:
        angle = int(angle_str)
        if angle not in (90, 180, 270):
            return jsonify({"error": "旋转角度必须是 90, 180 或 270"}), 400
    except ValueError:
        return jsonify({"error": "无效的旋转角度"}), 400

    tmp = os.path.join(UPLOAD_DIR, f"rotate_{uuid.uuid4().hex}.pdf")
    f.save(tmp)

    reader = PdfReader(tmp)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(angle)
        writer.add_page(page)

    out_name = f"rotated_{uuid.uuid4().hex[:8]}.pdf"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    with open(out_path, "wb") as out:
        writer.write(out)

    try:
        os.remove(tmp)
    except OSError:
        pass

    cleanup_later(out_path)
    return send_file(out_path, as_attachment=True, download_name=f"rotated_{angle}.pdf")


# ========== 删除页面 ==========
@app.route("/delete", methods=["POST"])
def delete_pages():
    f = request.files.get("file")
    if not f or not f.filename.lower().endswith(".pdf"):
        return jsonify({"error": "请上传一个 PDF 文件"}), 400

    pages_str = request.form.get("pages", "").strip()
    if not pages_str:
        return jsonify({"error": "请指定要删除的页面（如 1,3,5-7）"}), 400

    tmp = os.path.join(UPLOAD_DIR, f"delete_{uuid.uuid4().hex}.pdf")
    f.save(tmp)

    reader = PdfReader(tmp)
    total = len(reader.pages)

    delete_set = set()
    for part in pages_str.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            for i in range(int(a.strip()) - 1, int(b.strip())):
                if 0 <= i < total:
                    delete_set.add(i)
        else:
            i = int(part) - 1
            if 0 <= i < total:
                delete_set.add(i)

    writer = PdfWriter()
    for i in range(total):
        if i not in delete_set:
            writer.add_page(reader.pages[i])

    if len(writer.pages) == 0:
        try:
            os.remove(tmp)
        except OSError:
            pass
        return jsonify({"error": "删除后没有剩余页面"}), 400

    out_name = f"deleted_{uuid.uuid4().hex[:8]}.pdf"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    with open(out_path, "wb") as out:
        writer.write(out)

    try:
        os.remove(tmp)
    except OSError:
        pass

    cleanup_later(out_path)
    return send_file(out_path, as_attachment=True, download_name="deleted_pages.pdf")


# ========== 图片转 PDF ==========
@app.route("/img2pdf", methods=["POST"])
def img2pdf():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "请上传至少一张图片"}), 400

    allowed = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    temp_images = []

    for f in files:
        ext = os.path.splitext(f.filename.lower())[1]
        if ext not in allowed:
            return jsonify({"error": f"'{f.filename}' 不是支持的图片格式（JPG/PNG/WEBP/BMP）"}), 400
        tmp = os.path.join(UPLOAD_DIR, f"img_{uuid.uuid4().hex}{ext}")
        f.save(tmp)
        temp_images.append(tmp)

    try:
        from PIL import Image

        if len(temp_images) == 1:
            out_name = f"img2pdf_{uuid.uuid4().hex[:8]}.pdf"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            img = Image.open(temp_images[0])
            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            img.save(out_path, "PDF")
        else:
            pdf_pages = []
            for img_path in temp_images:
                img = Image.open(img_path)
                if img.mode in ("RGBA", "P", "LA"):
                    img = img.convert("RGB")
                pp = os.path.join(OUTPUT_DIR, f"page_{uuid.uuid4().hex[:4]}.pdf")
                img.save(pp, "PDF")
                pdf_pages.append(pp)

            merger = PdfWriter()
            for pp in pdf_pages:
                merger.append(pp)
                os.remove(pp)

            out_name = f"img2pdf_{uuid.uuid4().hex[:8]}.pdf"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            with open(out_path, "wb") as out:
                merger.write(out)
    except Exception as e:
        for t in temp_images:
            try:
                os.remove(t)
            except OSError:
                pass
        return jsonify({"error": f"转换失败: {str(e)}"}), 500

    for t in temp_images:
        try:
            os.remove(t)
        except OSError:
            pass

    cleanup_later(out_path)
    return send_file(out_path, as_attachment=True, download_name="images_to_pdf.pdf")


# ========== 健康检查 ==========
@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.now().isoformat()})


# ========== 启动 ==========
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=5000)
    p.add_argument("--debug", action="store_true")
    args = p.parse_args()
    print(f"\n  PDF Toolbox 已启动 → http://localhost:{args.port}\n")
    app.run(host="0.0.0.0", port=args.port, debug=args.debug)
