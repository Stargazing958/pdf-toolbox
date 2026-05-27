# PDF Toolbox — Free & Unlimited

4 个 PDF 工具合一的 Web 应用。

## 功能

| 工具 | API | 说明 |
|------|-----|------|
| PDF 合并 | `/merge` | 多文件合并为一个 |
| PDF 压缩 | `/compress` | 减小文件大小 |
| PDF 拆分 | `/split` | 按页拆分或提取指定页面 |
| PDF 转 Word | `/convert` | 转为可编辑 .docx |

## 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动
python app.py --port 5000

# 3. 打开浏览器
open http://localhost:5000
```

## 特性

- 无限次免费
- 无水印
- 文件 10 分钟后自动删除
- 50MB 上传上限
- 无需注册登录

## 部署

支持 Railway.app / Render.com / Fly.io 一键部署：

```bash
# Railway 部署
railway up

# 或者手动
gunicorn app:app --bind 0.0.0.0:$PORT
```
