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

def create_dxg_ecosystem_image():
    # 4:3 ratio: 1000x750
    w, h = 1000, 750
    img = Image.new("RGB", (w, h), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Background subtle grid lines
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill="#14283D", width=1)
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill="#14283D", width=1)
        
    # Central isometric hub and branches (representing DXG holding and subsidiaries/projects)
    # Center pillar (DXG Holding)
    draw_3d_cube(draw, 500, 360, 90, "#10E7B3", "#0DB88E", "#0A8F6E")
    
    # Orbiting / Connected pillars
    # West pillar (Dự án BDS: Gem Sky World, Opal)
    draw_3d_cube(draw, 260, 480, 65, "#2BE841", "#22BA34", "#199128")
    # East pillar (Môi giới DXS: Dat Xanh Services)
    draw_3d_cube(draw, 740, 480, 65, "#00AD14", "#008B10", "#006B0D")
    # North pillar (Xây dựng, tài chính dự án)
    draw_3d_cube(draw, 500, 200, 55, "#23C736", "#1B9E2B", "#157A22")
    
    # Connection glowing data lines
    connections = [
        ((500, 360), (260, 480)),
        ((500, 360), (740, 480)),
        ((500, 360), (500, 200)),
    ]
    for p1, p2 in connections:
        draw.line([p1, p2], fill="#48F28A", width=4)
        
    # Floating financial nodes
    nodes = [(380, 420), (620, 420), (500, 280), (260, 480), (740, 480)]
    for nx, ny in nodes:
        draw.ellipse([nx-8, ny-8, nx+8, ny+8], fill="#10E7B3", outline="#FFFFFF", width=2)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    os.makedirs('knowledge/4-content/images', exist_ok=True)
    out_path = 'knowledge/4-content/images/co-phieu-dxg-he-sinh-thai-2026.jpg'
    img.save(out_path, quality=95)
    print(f"Created {out_path}")

def create_dxg_cycle_image():
    # 4:3 ratio: 1000x750
    w, h = 1000, 750
    img = Image.new("RGB", (w, h), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Background subtle grid lines
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill="#14283D", width=1)
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill="#14283D", width=1)
        
    # Stepping ascending pillars representing Real Estate cycle recovery 2024 -> 2025 -> 2026 -> 2027
    steps = [
        (200, 560, 45, "#199A27", "#137A1F", "#0E5B17"),
        (380, 480, 55, "#00AD14", "#008B10", "#006B0D"),
        (560, 390, 65, "#23C736", "#1B9E2B", "#157A22"),
        (740, 290, 75, "#2BE841", "#22BA34", "#199128"),
        (880, 200, 85, "#10E7B3", "#0DB88E", "#0A8F6E"),
    ]
    for cx, cy, sz, c_top, c_left, c_right in steps:
        draw_3d_cube(draw, cx, cy, sz, c_top, c_left, c_right)
        
    # Curve trajectory connecting the cycle phases
    curve_points = [(200, 500), (380, 410), (560, 310), (740, 200), (880, 100)]
    for i in range(len(curve_points) - 1):
        draw.line([curve_points[i], curve_points[i+1]], fill="#48F28A", width=4)
    for px, py in curve_points:
        draw.ellipse([px-7, py-7, px+7, py+7], fill="#10E7B3", outline="#FFFFFF", width=2)
        
    # Target indicator ring around the peak 2027 target
    apex_x, apex_y = 880, 100
    for r in [25, 45, 65]:
        draw.ellipse([apex_x-r, apex_y-int(r*0.6), apex_x+r, apex_y+int(r*0.6)], outline="#10E7B3", width=2)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    os.makedirs('knowledge/4-content/images', exist_ok=True)
    out_path = 'knowledge/4-content/images/co-phieu-dxg-chu-ky-bat-dong-san-2026.jpg'
    img.save(out_path, quality=95)
    print(f"Created {out_path}")

if __name__ == '__main__':
    create_dxg_ecosystem_image()
    create_dxg_cycle_image()

