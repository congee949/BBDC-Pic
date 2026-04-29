# BBDC-Pic

百词斩截图自动处理：重命名、压缩、OCR 提词、生成学习笔记。

## 功能

| 功能 | 说明 |
|------|------|
| 截图查找 | 扫描 Desktop 中包含 `IMG` 或 `screenshot` 的 PNG/JPG 文件 |
| 按日期重命名 | 根据文件修改时间重命名为 `MM-DD_N.ext` 格式 |
| 图片压缩 | PNG 转 JPG，质量 70%，平均压缩率约 88% |
| 按月归档 | 压缩后图片存入 `collaboration/MM/` 目录 |
| OCR 提词 | 从截图中识别英文单词，去重统计 |
| 学习笔记 | 自动生成含音标、释义、例句、搭配、记忆技巧的 Markdown 笔记 |
| 单词搭配 | `word_collocations.md` 汇总高频搭配与派生词 |

## 项目结构

```
BBDC-Pic/
├── process_screenshots.py    # 主流程：查找 -> 重命名 -> 压缩 -> 归档
├── compress_images.py        # 独立压缩工具（单文件 / 批量目录）
├── collaboration/            # 压缩后的截图，按月份存放
│   ├── 11/                   # 11 月截图（138 张）
│   ├── 12/                   # 12 月截图（18 张）
│   └── word_collocations.md  # 单词搭配汇总
├── reflection/               # 每日学习笔记（Markdown）
│   ├── 2025-11-29.md
│   ├── 2025-12-01.md
│   └── ...
├── process_report.json       # 处理报告（压缩前后大小、文件映射）
├── rename_log.json           # 重命名日志
├── processed_files.txt       # 已处理文件列表（供清理 Desktop 用）
└── upload_words_log_*.md     # 操作日志（完整执行记录）
```

## 使用

### 一键处理截图（重命名 + 压缩 + 归档）

```bash
python process_screenshots.py
```

脚本会自动扫描 `~/Desktop` 中的截图文件，按日期重命名，压缩后存入 `collaboration/` 对应月份目录，并生成 `processed_files.txt` 供后续清理。

### 单独压缩图片

```bash
# 压缩单个文件
python compress_images.py image.png

# 压缩单个文件并指定输出路径和质量
python compress_images.py image.png compressed.jpg 80

# 批量压缩目录下所有 PNG
python compress_images.py /path/to/images --dir /path/to/output 70
```

### 学习笔记格式

每篇笔记包含：

- 音标（IPA）
- 词性与释义
- 英文例句 + 中文翻译
- 常用搭配
- 词形变化
- 记忆技巧

## 链接

- 仓库：https://github.com/congee949/BBDC-Pic
