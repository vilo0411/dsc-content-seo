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

def generate_featured_image():
    # 16:9 banner: 1200 x 675
    w, h = 1200, 675
    img = Image.new("RGBA", (w, h), "#E8F8F2")
    draw = ImageDraw.Draw(img)
    
    cx, cy = w // 2, h // 2 + 30
    
    # Soft background platform shadow
    draw.ellipse([cx - 280, cy + 130, cx + 280, cy + 220], fill="#D1FAE5")
    draw.ellipse([cx - 200, cy + 150, cx + 200, cy + 200], fill="#A7F3D0")
    
    # Draw isometric support floor grid line
    floor_pts = [
        (cx - 320, cy + 100),
        (cx, cy + 160),
        (cx + 320, cy + 100),
        (cx, cy + 40)
    ]
    draw.polygon(floor_pts, fill="#E0F2FE", outline="#10E7B3", width=3)
    
    # Draw lower shadow (wick / tail) of Hammer candle
    wick_w = 12
    draw.rectangle([cx - wick_w//2, cy - 80, cx + wick_w//2, cy + 110], fill="#047857")
    
    # Draw 3D Hammer head (candle body) at the top of wick
    body_size = 65
    draw_3d_cube(draw, cx, cy - 80, body_size, "#2BE841", "#00AD14", "#047857")
    
    # Upward energy chevron / bounce arrow
    arrow_pts = [
        (cx + 140, cy + 40),
        (cx + 180, cy - 40),
        (cx + 200, cy - 30),
        (cx + 190, cy - 90),
        (cx + 130, cy - 70),
        (cx + 150, cy - 60),
        (cx + 110, cy + 20)
    ]
    draw.polygon(arrow_pts, fill="#10E7B3", outline="#00AD14", width=2)
    
    img = add_watermark_logo(img, is_dark_bg=False)
    out_path = 'knowledge/4-content/images/mo-hinh-nen-hammer-la-gi-featured.jpg'
    img.convert("RGB").save(out_path, quality=95)
    print("Saved:", out_path)

def generate_trading_image():
    # 4:3 inline: 1200 x 900
    w, h = 1200, 900
    img = Image.new("RGBA", (w, h), "#E8F8F2")
    draw = ImageDraw.Draw(img)
    
    cx, cy = w // 2, h // 2 + 40
    
    # Base platform
    draw.ellipse([cx - 300, cy + 180, cx + 300, cy + 290], fill="#D1FAE5")
    draw.ellipse([cx - 220, cy + 200, cx + 220, cy + 270], fill="#A7F3D0")
    
    # Support trendline plane (3D isometric strip)
    strip_pts = [
        (cx - 380, cy + 120),
        (cx + 380, cy + 40),
        (cx + 380, cy + 80),
        (cx - 380, cy + 160)
    ]
    draw.polygon(strip_pts, fill="#BAE6FD", outline="#0284C7", width=2)
    
    # Preceding candle (bearish breakdown attempt)
    draw.rectangle([cx - 150 - 4, cy - 20, cx - 150 + 4, cy + 130], fill="#64748B")
    draw_3d_cube(draw, cx - 150, cy + 30, 40, "#94A3B8", "#64748B", "#475569")
    
    # Hammer candle (at support)
    draw.rectangle([cx - 5, cy - 100, cx + 5, cy + 140], fill="#047857")
    draw_3d_cube(draw, cx, cy - 100, 55, "#2BE841", "#00AD14", "#047857")
    
    # Confirmation candle (strong bullish breakout next)
    draw.rectangle([cx + 160 - 4, cy - 200, cx + 160 + 4, cy + 20], fill="#047857")
    draw_3d_cube(draw, cx + 160, cy - 120, 65, "#34D399", "#10B981", "#059669")
    
    # Entry point & Stop Loss target markers (geometric indicator rings)
    # Stop loss marker below wick
    draw.ellipse([cx - 40, cy + 135, cx + 40, cy + 155], fill="#CBD5E1", outline="#64748B", width=2)
    # Entry point marker above hammer head
    draw.ellipse([cx + 120, cy - 180, cx + 200, cy - 160], fill="#A7F3D0", outline="#00AD14", width=3)
    
    img = add_watermark_logo(img, is_dark_bg=False)
    out_path = 'knowledge/4-content/images/mo-hinh-nen-hammer-la-gi-giao-dich.jpg'
    img.convert("RGB").save(out_path, quality=95)
    print("Saved:", out_path)

if __name__ == '__main__':
    os.makedirs('knowledge/4-content/images', exist_ok=True)
    generate_featured_image()
    generate_trading_image()

