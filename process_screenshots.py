#!/usr/bin/env python3
"""
处理截图：重命名、压缩并保存到对应月份文件夹
"""
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
from PIL import Image

def get_file_modification_date(filepath):
    """获取文件修改日期"""
    timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp)

def find_screenshot_files(desktop_path):
    """查找 Desktop 中包含 IMG 或 screenshot 的图片文件"""
    files = []
    for file in os.listdir(desktop_path):
        filepath = os.path.join(desktop_path, file)
        if os.path.isfile(filepath):
            lower_name = file.lower()
            if ('img' in lower_name or 'screenshot' in lower_name) and \
               (lower_name.endswith('.png') or lower_name.endswith('.jpg') or lower_name.endswith('.jpeg')):
                files.append(filepath)

    # 按修改时间排序
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

def compress_image(input_path, output_path, quality=70):
    """压缩图片到指定质量"""
    try:
        # 打开图片
        img = Image.open(input_path)

        # 如果是 PNG，转换为 RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 保存压缩后的图片
        img.save(output_path, 'JPEG', quality=quality, optimize=True)

        # 获取文件大小信息
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = (1 - compressed_size / original_size) * 100

        return True, original_size, compressed_size, reduction
    except Exception as e:
        print(f"✗ 压缩失败 {input_path}: {str(e)}")
        return False, 0, 0, 0

def main():
    desktop_path = "/Users/Apple/Desktop"
    base_path = "/Users/Apple/BBDC-Pic"
    collab_path = os.path.join(base_path, "collaboration")

    print("=" * 60)
    print("开始处理截图文件")
    print("=" * 60)

    # 1. 查找文件
    print("\n[1/4] 查找图片文件...")
    files = find_screenshot_files(desktop_path)

    if not files:
        print("未找到任何图片文件")
        return

    print(f"找到 {len(files)} 个文件")

    # 2. 按日期分组重命名
    print("\n[2/4] 按日期重命名文件...")
    file_groups = {}
    for filepath in files:
        mod_date = get_file_modification_date(filepath)
        date_key = mod_date.strftime("%m-%d")
        if date_key not in file_groups:
            file_groups[date_key] = []
        file_groups[date_key].append((filepath, mod_date))

    renamed_files = []
    for date_key in sorted(file_groups.keys()):
        group_files = file_groups[date_key]
        for idx, (filepath, mod_date) in enumerate(group_files, 1):
            ext = os.path.splitext(filepath)[1]
            new_name = f"{date_key}_{idx}{ext}"
            new_path = os.path.join(desktop_path, new_name)

            # 如果目标文件已存在，先删除
            if os.path.exists(new_path) and new_path != filepath:
                os.remove(new_path)

            if new_path != filepath:
                os.rename(filepath, new_path)
                print(f"  重命名: {os.path.basename(filepath)} -> {new_name}")
            renamed_files.append((new_path, mod_date))

    # 3. 压缩图片
    print("\n[3/4] 压缩图片...")
    compressed_files = []
    total_original_size = 0
    total_compressed_size = 0

    for filepath, mod_date in renamed_files:
        month = mod_date.strftime("%m")
        month_dir = os.path.join(collab_path, month)
        os.makedirs(month_dir, exist_ok=True)

        basename = os.path.splitext(os.path.basename(filepath))[0]
        output_path = os.path.join(month_dir, f"{basename}.jpg")

        success, orig_size, comp_size, reduction = compress_image(filepath, output_path, quality=70)

        if success:
            total_original_size += orig_size
            total_compressed_size += comp_size
            compressed_files.append(output_path)
            print(f"  ✓ {basename}.jpg")
            print(f"    原始: {orig_size / 1024:.2f} KB -> 压缩: {comp_size / 1024:.2f} KB (减少 {reduction:.1f}%)")

    # 4. 输出统计信息
    print("\n[4/4] 处理完成!")
    print("=" * 60)
    print(f"处理的图片数量: {len(compressed_files)}")
    print(f"压缩前总大小: {total_original_size / 1024:.2f} KB")
    print(f"压缩后总大小: {total_compressed_size / 1024:.2f} KB")
    if total_original_size > 0:
        total_reduction = (1 - total_compressed_size / total_original_size) * 100
        print(f"总体减少: {total_reduction:.1f}%")
    print("=" * 60)

    # 保存原始文件路径列表供后续删除使用
    with open(os.path.join(base_path, "processed_files.txt"), "w") as f:
        for filepath, _ in renamed_files:
            f.write(filepath + "\n")

    print(f"\n已保存原始文件列表到: {os.path.join(base_path, 'processed_files.txt')}")

if __name__ == '__main__':
    main()
