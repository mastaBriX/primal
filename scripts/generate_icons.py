"""
生成 PWA 所需的 PNG 图标
从 SVG 图标生成不同尺寸的 PNG 图标
"""
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("需要安装 Pillow: pip install Pillow")
    sys.exit(1)

# 图标尺寸列表
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

# 输出目录
OUTPUT_DIR = Path(__file__).parent.parent / "src" / "static" / "icons"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_icon(size):
    """创建指定尺寸的图标"""
    # 创建图像
    img = Image.new('RGB', (size, size), color='#667eea')
    
    # 创建渐变背景
    draw = ImageDraw.Draw(img)
    
    # 绘制渐变矩形（简化版，使用两种颜色）
    for i in range(size):
        # 计算渐变颜色
        ratio = i / size
        r1, g1, b1 = 102, 126, 234  # #667eea
        r2, g2, b2 = 118, 75, 162   # #764ba2
        
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        draw.rectangle([(0, i), (size, i + 1)], fill=(r, g, b))
    
    # 绘制圆角矩形
    corner_radius = size // 10
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), (size, size)], corner_radius, fill=255)
    
    # 应用圆角
    output = Image.new('RGB', (size, size), (255, 255, 255))
    output.paste(img, (0, 0), mask)
    
    # 绘制 # 符号
    try:
        # 尝试使用系统字体
        font_size = int(size * 0.5)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
        except:
            # 使用默认字体
            font = ImageFont.load_default()
    
    draw = ImageDraw.Draw(output)
    
    # 计算文本位置（居中）
    text = "#"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - bbox[1]
    
    # 绘制文本
    draw.text((x, y), text, fill='white', font=font)
    
    return output


def main():
    """生成所有尺寸的图标"""
    print(f"生成图标到: {OUTPUT_DIR}")
    
    for size in ICON_SIZES:
        print(f"生成 {size}x{size} 图标...")
        icon = create_icon(size)
        output_path = OUTPUT_DIR / f"icon-{size}x{size}.png"
        icon.save(output_path, 'PNG')
        print(f"[OK] 已保存: {output_path}")
    
    print("\n所有图标生成完成！")


if __name__ == '__main__':
    main()

