import os
import math
from PIL import Image, ImageDraw

def add_watermark_logo(base_img, is_dark_bg=False):
    logo_path = 'knowledge/1-brand/assets/logos/logo-for-dark-bg.png' if is_dark_bg else 'knowledge/1-brand/assets/logos/logo-for-light-bg.png'
    if not os.path.exists(logo_path):
        print(f"Logo not found at {logo_path}")
        return base_img
    
    logo = Image.open(logo_path).convert("RGBA")
    target_w = 180
    aspect = logo.height / logo.width
    target_h = int(target_w * aspect)
    logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    pad_x = int(base_img.width * 0.04)
    pad_y = int(base_img.height * 0.04)
    
    base_img.paste(logo, (pad_x, pad_y), logo)
    return base_img

def draw_3d_cube(draw, cx, cy, size, color_top, color_left, color_right):
    dx = size * math.cos(math.radians(30))
    dy = size * math.sin(math.radians(30))
    
    top_poly = [
        (cx, cy - size),
        (cx + dx, cy - size + dy),
        (cx, cy - size + 2 * dy),
        (cx - dx, cy - size + dy)
    ]
    draw.polygon(top_poly, fill=color_top)
    
    left_poly = [
        (cx - dx, cy - size + dy),
        (cx, cy - size + 2 * dy),
        (cx, cy + dy),
        (cx - dx, cy)
    ]
    draw.polygon(left_poly, fill=color_left)
    
    right_poly = [
        (cx, cy - size + 2 * dy),
        (cx + dx, cy - size + dy),
        (cx + dx, cy),
        (cx, cy + dy)
    ]
    draw.polygon(right_poly, fill=color_right)

def generate_image_1():
    width, height = 1200, 900
    img = Image.new("RGBA", (width, height), "#E8F8F2")
    draw = ImageDraw.Draw(img)
    
    cy = height // 2 + 30
    cx = width // 2
    
    draw.ellipse([cx - 250, cy + 120, cx + 250, cy + 220], fill="#D1FAE5")
    draw.ellipse([cx - 180, cy + 140, cx + 180, cy + 200], fill="#A7F3D0")
    
    draw_3d_cube(draw, cx - 140, cy + 60, 50, "#00AD14", "#065F46", "#047857")
    draw_3d_cube(draw, cx - 40, cy + 20, 65, "#2BE841", "#00AD14", "#065F46")
    draw_3d_cube(draw, cx + 60, cy - 30, 80, "#10E7B3", "#2BE841", "#00AD14")
    draw_3d_cube(draw, cx + 160, cy - 90, 95, "#0D1B2A", "#10E7B3", "#00AD14")

    img = add_watermark_logo(img, is_dark_bg=False)
    
    os.makedirs('knowledge/4-content/images', exist_ok=True)
    output_path = 'knowledge/4-content/images/bien-loi-nhuan-rong-khai-niem.jpg'
    img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"Generated image: {output_path}")

def generate_image_2():
    width, height = 1200, 900
    img = Image.new("RGBA", (width, height), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    nodes = [
        (280, 260),  # Revenue
        (600, 260),  # Operating
        (920, 260),  # Net Profit
        (600, 620)   # Retention
    ]
    
    draw.line([nodes[0], nodes[1]], fill="#10E7B3", width=5)
    draw.line([nodes[1], nodes[2]], fill="#2BE841", width=5)
    draw.line([nodes[1], nodes[3]], fill="#00AD14", width=5)
    
    for i, (x, y) in enumerate(nodes):
        draw.rounded_rectangle([x - 120, y - 80, x + 120, y + 80], radius=16, fill="#162A45", outline="#2BE841", width=3)
        colors = [("#00AD14", "#065F46", "#047857"), ("#2BE841", "#00AD14", "#065F46"), ("#10E7B3", "#2BE841", "#00AD14"), ("#00AD14", "#10E7B3", "#2BE841")]
        draw_3d_cube(draw, x, y, 32, colors[i][0], colors[i][1], colors[i][2])
    
    img = add_watermark_logo(img, is_dark_bg=True)
    
    output_path = 'knowledge/4-content/images/bien-loi-nhuan-rong-so-do-dong-tien.jpg'
    img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"Generated image: {output_path}")

if __name__ == '__main__':
    generate_image_1()
    generate_image_2()

