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
    # 4:3 ratio: 1200 x 900
    width, height = 1200, 900
    img = Image.new("RGBA", (width, height), "#E8F8F2")
    draw = ImageDraw.Draw(img)
    
    cy = height // 2 + 50
    cx = width // 2
    
    # Negative space pedestal
    draw.ellipse([cx - 300, cy + 120, cx + 300, cy + 240], fill="#D1FAE5")
    draw.ellipse([cx - 220, cy + 140, cx + 220, cy + 220], fill="#A7F3D0")
    
    # 3D restructuring blocks: pillar of recovery and solid base
    # Left base block
    draw_3d_cube(draw, cx - 140, cy + 60, 70, "#10E7B3", "#059669", "#047857")
    # Right base block
    draw_3d_cube(draw, cx + 140, cy + 60, 70, "#34D399", "#10B981", "#059669")
    # Central rising pillar (growth and resilience)
    draw_3d_cube(draw, cx, cy - 40, 95, "#2BE841", "#00AD14", "#065F46")
    # Floating top prism
    draw_3d_cube(draw, cx, cy - 200, 60, "#6EE7B7", "#10E7B3", "#047857")
    
    # Floating financial sphere elements
    draw.ellipse([cx - 240, cy - 80, cx - 190, cy - 30], fill="#00AD14")
    draw.ellipse([cx + 190, cy - 120, cx + 250, cy - 60], fill="#10E7B3")
    draw.ellipse([cx + 150, cy - 220, cx + 180, cy - 190], fill="#2BE841")

    img = add_watermark_logo(img, is_dark_bg=False)
    out_path = 'knowledge/4-content/images/co-nen-mua-co-phieu-pnj-bien-co-2026.jpg'
    img.convert("RGB").save(out_path, "JPEG", quality=92)
    print(f"Generated: {out_path}")

def generate_image_2():
    # 4:3 ratio: 1200 x 900
    width, height = 1200, 900
    img = Image.new("RGBA", (width, height), "#E8F8F2")
    draw = ImageDraw.Draw(img)
    
    cy = height // 2 + 50
    cx = width // 2
    
    # Base pedestal
    draw.ellipse([cx - 320, cy + 130, cx + 320, cy + 250], fill="#D1FAE5")
    draw.ellipse([cx - 240, cy + 150, cx + 240, cy + 230], fill="#A7F3D0")
    
    # 3D Balance scale / Valuation steps (Isometric stepping blocks)
    # Step 1 (Conservative value)
    draw_3d_cube(draw, cx - 180, cy + 80, 65, "#6EE7B7", "#059669", "#047857")
    # Step 2 (Core business franchise)
    draw_3d_cube(draw, cx - 40, cy + 10, 75, "#34D399", "#10B981", "#065F46")
    # Step 3 (Long-term target upside)
    draw_3d_cube(draw, cx + 110, cy - 70, 85, "#2BE841", "#00AD14", "#064E3B")
    
    # Connecting isometric balance beam / bridge
    dx = 150 * math.cos(math.radians(30))
    dy = 150 * math.sin(math.radians(30))
    bridge_poly = [
        (cx - 180, cy - 120),
        (cx + 180, cy - 20),
        (cx + 180, cy),
        (cx - 180, cy - 100)
    ]
    draw.polygon(bridge_poly, fill="#10E7B3")
    
    # Floating shield/diamond emblem in 3D (Teal & Emerald)
    draw_3d_cube(draw, cx, cy - 170, 50, "#10E7B3", "#00AD14", "#065F46")
    draw.ellipse([cx - 220, cy - 180, cx - 170, cy - 130], fill="#2BE841")
    draw.ellipse([cx + 200, cy - 140, cx + 245, cy - 95], fill="#059669")

    img = add_watermark_logo(img, is_dark_bg=False)
    out_path = 'knowledge/4-content/images/co-nen-mua-co-phieu-pnj-dinh-gia-2026.jpg'
    img.convert("RGB").save(out_path, "JPEG", quality=92)
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    generate_image_1()
    generate_image_2()

