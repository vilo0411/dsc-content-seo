import os
import math
from PIL import Image, ImageDraw, ImageFilter

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

def create_image_1():
    # 1200x675 (16:9)
    img = Image.new("RGB", (1200, 675), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Background subtle grid lines
    for x in range(0, 1200, 60):
        draw.line([(x, 0), (x, 675)], fill="#13273D", width=1)
    for y in range(0, 675, 45):
        draw.line([(0, y), (1200, y)], fill="#13273D", width=1)
        
    # Draw ascending 3D isometric financial bars / wave
    # Palette: DSC Green #00AD14, #2BE841, Cyan #10E7B3, Deep navy tones
    cubes = [
        (280, 480, 50, "#10E7B3", "#0EBE93", "#008F6B"),
        (420, 430, 60, "#2BE841", "#23C736", "#199A27"),
        (560, 390, 70, "#00AD14", "#009110", "#006C0C"),
        (700, 340, 80, "#2BE841", "#23C736", "#199A27"),
        (840, 280, 95, "#10E7B3", "#0EBE93", "#008F6B"),
        (980, 230, 110, "#48F28A", "#2BE841", "#00AD14"),
    ]
    
    for cx, cy, sz, c_top, c_left, c_right in cubes:
        draw_3d_cube(draw, cx, cy, sz, c_top, c_left, c_right)
        
    # Floating financial geometric nodes
    nodes = [(350, 220), (520, 180), (680, 150), (860, 120)]
    for i in range(len(nodes)-1):
        draw.line([nodes[i], nodes[i+1]], fill="#10E7B3", width=3)
    for nx, ny in nodes:
        draw.ellipse([nx-8, ny-8, nx+8, ny+8], fill="#48F28A", outline="#FFFFFF", width=2)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    os.makedirs('knowledge/4-content/images', exist_ok=True)
    out_path = 'knowledge/4-content/images/chi-so-dxy-la-gi-dien-bien-vi-mo.jpg'
    img.save(out_path, quality=95)
    print(f"Created {out_path}")

def create_image_2():
    img = Image.new("RGB", (1200, 675), "#0A1420")
    draw = ImageDraw.Draw(img)
    
    # Radial or isometric grid
    for r in range(100, 600, 80):
        draw.ellipse([600-r, 360-int(r*0.5), 600+r, 360+int(r*0.5)], outline="#162D46", width=1)
        
    # Central 3D pillar (Exchange / Market core)
    draw_3d_cube(draw, 600, 360, 120, "#10E7B3", "#0EBE93", "#007A5A")
    
    # Surrounding orbital cubes (Sectors: Export, Import, Banking, FDI)
    satellites = [
        (340, 360, 55, "#2BE841", "#23C736", "#199A27"),
        (860, 360, 55, "#00AD14", "#009110", "#006C0C"),
        (470, 240, 45, "#48F28A", "#2BE841", "#199A27"),
        (730, 240, 45, "#10E7B3", "#0EBE93", "#008F6B"),
        (470, 480, 50, "#00AD14", "#00850F", "#005E0A"),
        (730, 480, 50, "#2BE841", "#23C736", "#168B23"),
    ]
    for cx, cy, sz, c_top, c_left, c_right in satellites:
        # Connect lines to center
        draw.line([(600, 360), (cx, cy)], fill="#1E4466", width=2)
        draw_3d_cube(draw, cx, cy, sz, c_top, c_left, c_right)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    out_path = 'knowledge/4-content/images/chi-so-dxy-la-gi-tac-dong-chung-khoan.jpg'
    img.save(out_path, quality=95)
    print(f"Created {out_path}")

if __name__ == '__main__':
    create_image_1()
    create_image_2()

