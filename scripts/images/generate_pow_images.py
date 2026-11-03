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

def draw_3d_cube(draw, cx, cy, size_x, size_y, size_z, color_top, color_left, color_right):
    dx = size_x * math.cos(math.radians(30))
    dy = size_x * math.sin(math.radians(30))
    h = size_z
    
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
        (cx, cy + dy),
        (cx - dx, cy)
    ]
    draw.polygon(left_poly, fill=color_left)
    
    right_poly = [
        (cx, cy - h + 2 * dy),
        (cx + dx, cy - h + dy),
        (cx + dx, cy),
        (cx, cy + dy)
    ]
    draw.polygon(right_poly, fill=color_right)

def draw_cylinder(draw, cx, cy, r, h, color_top, color_side):
    # side
    draw.rectangle([cx - r, cy - h, cx + r, cy], fill=color_side)
    # bottom ellipse
    draw.ellipse([cx - r, cy - r // 3, cx + r, cy + r // 3], fill=color_side)
    # top ellipse
    draw.ellipse([cx - r, cy - h - r // 3, cx + r, cy - h + r // 3], fill=color_top)

def create_pow_image():
    # 4:3 ratio: 1000x750
    w, h = 1000, 750
    img = Image.new("RGB", (w, h), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Background subtle grid lines
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill="#14283D", width=1)
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill="#14283D", width=1)
        
    # Large glowing radial backdrop
    center_x, center_y = 520, 430
    for rad in range(260, 40, -20):
        alpha = int(18 * (1 - rad / 260))
        glow_box = [center_x - rad, center_y - rad // 2, center_x + rad, center_y + rad // 2]
        draw.ellipse(glow_box, fill="#0A3D2E")
        
    # Isometric platform base
    base_cx, base_cy = 500, 470
    draw_3d_cube(draw, base_cx, base_cy, 260, 260, 25, "#1B3B36", "#0E2421", "#142F2A")
    draw_3d_cube(draw, base_cx, base_cy - 25, 240, 240, 15, "#10E7B3", "#0B6651", "#084C3C")
    draw_3d_cube(draw, base_cx, base_cy - 40, 225, 225, 20, "#19352F", "#0F2621", "#142F2A")
    
    # LNG Storage Tanks (Cylinders)
    tank1_x, tank1_y = 400, 400
    draw_cylinder(draw, tank1_x, tank1_y, 45, 60, "#2BE841", "#00AD14")
    
    tank2_x, tank2_y = 480, 440
    draw_cylinder(draw, tank2_x, tank2_y, 40, 50, "#10E7B3", "#0B8C6C")
    
    # Power Generation Units (Turbine Hall)
    gen_x, gen_y = 570, 370
    draw_3d_cube(draw, gen_x, gen_y, 60, 60, 80, "#2BE841", "#008F11", "#00AD14")
    draw_3d_cube(draw, gen_x + 50, gen_y + 30, 45, 45, 60, "#10E7B3", "#0A7F62", "#0C9D79")
    
    # Cooling Towers / Stacks
    draw_cylinder(draw, 590, 280, 18, 55, "#FFFFFF", "#2BE841")
    draw_cylinder(draw, 630, 305, 15, 45, "#E8F8F2", "#10E7B3")
    
    # Transmission Lines & Grid pylons (Isometric energy lines)
    draw.line([(380, 370), (base_cx, base_cy - 70)], fill="#2BE841", width=3)
    draw.line([(base_cx, base_cy - 70), (gen_x, gen_y - 20)], fill="#10E7B3", width=3)
    draw.line([(gen_x, gen_y - 20), (660, 380)], fill="#2BE841", width=3)
    draw.line([(660, 380), (740, 340)], fill="#10E7B3", width=3)
    
    # Energy nodes / Glowing pulses
    for nx, ny in [(380, 370), (base_cx, base_cy - 70), (gen_x, gen_y - 20), (660, 380), (740, 340)]:
        draw.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill="#FFFFFF", outline="#2BE841", width=2)
        
    # Floating growth indicator bars (Isometric pillars)
    draw_3d_cube(draw, 340, 480, 22, 22, 45, "#2BE841", "#008F11", "#00AD14")
    draw_3d_cube(draw, 370, 500, 22, 22, 70, "#10E7B3", "#0A7F62", "#0C9D79")
    draw_3d_cube(draw, 400, 520, 22, 22, 100, "#2BE841", "#00AD14", "#10E7B3")
    
    # Add watermark logo
    img = add_watermark_logo(img, is_dark_bg=True)
    
    os.makedirs("knowledge/4-content/images", exist_ok=True)
    out_path = "knowledge/4-content/images/co-nen-mua-co-phieu-pow-hay-khong-nhon-trach-3-4.jpg"
    img.save(out_path, "JPEG", quality=92)
    print(f"Created image: {out_path}")

if __name__ == "__main__":
    create_pow_image()

