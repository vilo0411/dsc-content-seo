import os
import math
from PIL import Image, ImageDraw

def add_watermark_logo(base_img, is_dark_bg=True):
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

def create_target_image():
    # 4:3 ratio for inline image: 1000x750
    w, h = 1000, 750
    img = Image.new("RGB", (w, h), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Background subtle grid lines
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill="#14283D", width=1)
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill="#14283D", width=1)
        
    # Target Resistance line (dashed glowing line representing target level)
    for lx in range(150, 900, 30):
        draw.line([(lx, 260), (lx + 18, 260)], fill="#10E7B3", width=3)
        
    # Stepping ascending 3D cubes reaching towards the target price
    pillars = [
        (220, 560, 45, "#199A27", "#137A1F", "#0E5B17"),
        (360, 480, 55, "#00AD14", "#008B10", "#006B0D"),
        (500, 400, 65, "#23C736", "#1B9E2B", "#157A22"),
        (640, 310, 75, "#2BE841", "#22BA34", "#199128"),
        (780, 240, 85, "#10E7B3", "#0DB88E", "#0A8F6E"),
    ]
    
    for cx, cy, sz, c_top, c_left, c_right in pillars:
        draw_3d_cube(draw, cx, cy, sz, c_top, c_left, c_right)
        
    # Trajectory curve connecting pillars to target
    curve_points = [(220, 490), (360, 405), (500, 315), (640, 215), (780, 135)]
    for i in range(len(curve_points) - 1):
        draw.line([curve_points[i], curve_points[i+1]], fill="#48F28A", width=3)
    for px, py in curve_points:
        draw.ellipse([px-7, py-7, px+7, py+7], fill="#10E7B3", outline="#FFFFFF", width=2)
        
    # Concentric target indicator rings around the apex (Bullseye metaphor)
    apex_x, apex_y = 780, 135
    for r in [25, 45, 65]:
        draw.ellipse([apex_x-r, apex_y-int(r*0.6), apex_x+r, apex_y+int(r*0.6)], outline="#10E7B3", width=2)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    os.makedirs('knowledge/4-content/images', exist_ok=True)
    out_path = 'knowledge/4-content/images/target-trong-chung-khoan-la-gi-chot-loi-ky-luat.jpg'
    img.save(out_path, quality=95)
    print(f"Created {out_path}")

if __name__ == '__main__':
    create_target_image()

