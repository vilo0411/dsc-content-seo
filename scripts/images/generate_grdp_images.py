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

def draw_3d_cube(draw, cx, cy, size, color_top, color_left, color_right, height_factor=1.0):
    dx = size * math.cos(math.radians(30))
    dy = size * math.sin(math.radians(30))
    h = size * height_factor
    
    top_poly = [
        (cx, cy - h),
        (cx + dx, cy - h + dy),
        (cx, cy - h + 2 * dy),
        (cx - dx, cy - h + dy)
    ]
    draw.polygon(top_poly, fill=color_top)
    
    left_poly = [
        (cx - dx, cy - h + dy),
        (cx, cy - h + 2 * dy),
        (cx, cy + 2 * dy),
        (cx - dx, cy + dy)
    ]
    draw.polygon(left_poly, fill=color_left)
    
    right_poly = [
        (cx, cy - h + 2 * dy),
        (cx + dx, cy - h + dy),
        (cx + dx, cy + dy),
        (cx, cy + 2 * dy)
    ]
    draw.polygon(right_poly, fill=color_right)

def create_featured_image():
    # 1200x675 (16:9)
    img = Image.new("RGB", (1200, 675), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Background subtle grid lines
    for x in range(0, 1200, 60):
        draw.line([(x, 0), (x, 675)], fill="#13273D", width=1)
    for y in range(0, 675, 45):
        draw.line([(0, y), (1200, y)], fill="#13273D", width=1)
        
    # Regional economic pillars (GRDP Growth & Scale)
    pillars = [
        (260, 480, 48, "#10E7B3", "#0EBE93", "#008F6B", 1.2),
        (420, 450, 52, "#2BE841", "#23C736", "#199A27", 1.8),
        (580, 420, 58, "#00AD14", "#009110", "#006C0C", 2.4),
        (740, 390, 64, "#2BE841", "#23C736", "#199A27", 3.0),
        (920, 350, 72, "#10E7B3", "#0EBE93", "#008F6B", 3.8),
    ]
    
    for cx, cy, sz, c_top, c_left, c_right, hf in pillars:
        draw_3d_cube(draw, cx, cy, sz, c_top, c_left, c_right, height_factor=hf)
        
    # Growth trajectory connecting peaks
    peak_nodes = [
        (260, 480 - int(48 * 1.2) + int(48 * math.sin(math.radians(30)))),
        (420, 450 - int(52 * 1.8) + int(52 * math.sin(math.radians(30)))),
        (580, 420 - int(58 * 2.4) + int(58 * math.sin(math.radians(30)))),
        (740, 390 - int(64 * 3.0) + int(64 * math.sin(math.radians(30)))),
        (920, 350 - int(72 * 3.8) + int(72 * math.sin(math.radians(30)))),
    ]
    for i in range(len(peak_nodes) - 1):
        draw.line([peak_nodes[i], peak_nodes[i+1]], fill="#10E7B3", width=3)
    for nx, ny in peak_nodes:
        draw.ellipse([nx-7, ny-7, nx+7, ny+7], fill="#48F28A", outline="#FFFFFF", width=2)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    os.makedirs('knowledge/4-content/images', exist_ok=True)
    out_path = 'knowledge/4-content/images/grdp-la-gi-featured.jpg'
    img.save(out_path, quality=95)
    print(f"Created {out_path}")

def create_ranking_image():
    # 1024x768 (4:3)
    img = Image.new("RGB", (1024, 768), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Subtle isometric grid
    for r in range(80, 520, 70):
        draw.ellipse([512-r, 420-int(r*0.45), 512+r, 420+int(r*0.45)], outline="#162D46", width=1)
        
    # Regional cluster nodes (North, Central, South hubs)
    hubs = [
        (320, 450, 45, "#10E7B3", "#0EBE93", "#007A5A", 2.2),
        (512, 380, 60, "#2BE841", "#23C736", "#199A27", 3.2),
        (704, 450, 45, "#00AD14", "#009110", "#006C0C", 2.6),
        (400, 260, 40, "#48F28A", "#2BE841", "#199A27", 1.8),
        (624, 260, 40, "#10E7B3", "#0EBE93", "#008F6B", 2.0),
    ]
    
    # Connect network lines
    connections = [(320, 450, 512, 380), (704, 450, 512, 380), (400, 260, 512, 380), (624, 260, 512, 380)]
    for x1, y1, x2, y2 in connections:
        draw.line([(x1, y1), (x2, y2)], fill="#1E4466", width=2)
        
    for cx, cy, sz, c_top, c_left, c_right, hf in hubs:
        draw_3d_cube(draw, cx, cy, sz, c_top, c_left, c_right, height_factor=hf)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    out_path = 'knowledge/4-content/images/grdp-la-gi-bang-xep-hang.jpg'
    img.save(out_path, quality=95)
    print(f"Created {out_path}")

if __name__ == '__main__':
    create_featured_image()
    create_ranking_image()

