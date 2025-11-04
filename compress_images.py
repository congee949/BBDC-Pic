#!/usr/bin/env python3
"""
图片压缩脚本 - 将图片压缩到 70% 质量
"""
import os
import sys
from PIL import Image
from pathlib import Path


def compress_image(input_path, output_path=None, quality=70):
    """
    压缩图片到指定质量

    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径（如果为 None，则覆盖原文件）
        quality: 压缩质量 (1-100)
    """
    try:
        # 打开图片
        img = Image.open(input_path)

        # 如果是 PNG，转换为 RGB（因为 JPEG 不支持透明度）
        if img.mode in ('RGBA', 'LA', 'P'):
            # 创建白色背景
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 确定输出路径
        if output_path is None:
            output_path = input_path

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

        # 保存压缩后的图片
        img.save(output_path, 'JPEG', quality=quality, optimize=True)

        # 获取文件大小信息
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = (1 - compressed_size / original_size) * 100

        print(f"✓ 压缩完成: {os.path.basename(input_path)}")
        print(f"  原始大小: {original_size / 1024:.2f} KB")
        print(f"  压缩后: {compressed_size / 1024:.2f} KB")
        print(f"  减少: {reduction:.1f}%")

        return True
    except Exception as e:
        print(f"✗ 压缩失败 {input_path}: {str(e)}")
        return False


def compress_images_in_directory(directory, output_dir=None, quality=70, pattern="*.PNG"):
    """
    压缩目录中的所有图片

    Args:
        directory: 输入目录
        output_dir: 输出目录（如果为 None，则覆盖原文件）
        quality: 压缩质量
        pattern: 文件匹配模式
    """
    path = Path(directory)
    images = list(path.glob(pattern))

    if not images:
        print(f"在 {directory} 中没有找到匹配 {pattern} 的文件")
        return

    print(f"找到 {len(images)} 个图片文件\n")

    success_count = 0
    for img_path in images:
        if output_dir:
            output_path = Path(output_dir) / f"{img_path.stem}.jpg"
        else:
            output_path = img_path.with_suffix('.jpg')

        if compress_image(str(img_path), str(output_path), quality):
            success_count += 1
        print()

    print(f"压缩完成: {success_count}/{len(images)} 个文件成功")


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  压缩单个文件: python compress_images.py <input_file> [output_file] [quality]")
        print("  压缩目录: python compress_images.py <input_dir> --dir [output_dir] [quality]")
        print()
        print("示例:")
        print("  python compress_images.py image.png")
        print("  python compress_images.py image.png compressed.jpg 70")
        print("  python compress_images.py /path/to/images --dir /path/to/output 70")
        sys.exit(1)

    input_path = sys.argv[1]

    # 检查是否为目录模式
    if '--dir' in sys.argv:
        dir_index = sys.argv.index('--dir')
        output_dir = sys.argv[dir_index + 1] if len(sys.argv) > dir_index + 1 and not sys.argv[dir_index + 1].isdigit() else None
        quality = int(sys.argv[-1]) if sys.argv[-1].isdigit() else 70
        compress_images_in_directory(input_path, output_dir, quality)
    else:
        # 单文件模式
        output_path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].isdigit() else None
        quality = int(sys.argv[-1]) if sys.argv[-1].isdigit() and len(sys.argv) > 2 else 70
        compress_image(input_path, output_path, quality)


if __name__ == '__main__':
    main()
