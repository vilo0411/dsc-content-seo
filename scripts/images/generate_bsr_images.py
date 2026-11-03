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
    draw.rectangle([cx - r, cy - h, cx + r, cy], fill=color_side)
    draw.ellipse([cx - r, cy - r // 3, cx + r, cy + r // 3], fill=color_side)
    draw.ellipse([cx - r, cy - h - r // 3, cx + r, cy - h + r // 3], fill=color_top)

def create_bsr_image():
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
        glow_box = [center_x - rad, center_y - rad // 2, center_x + rad, center_y + rad // 2]
        draw.ellipse(glow_box, fill="#0A3D2E")
        
    # Isometric platform base
    base_cx, base_cy = 500, 470
    draw_3d_cube(draw, base_cx, base_cy, 270, 270, 25, "#1B3B36", "#0E2421", "#142F2A")
    draw_3d_cube(draw, base_cx, base_cy - 25, 250, 250, 15, "#10E7B3", "#0B6651", "#084C3C")
    draw_3d_cube(draw, base_cx, base_cy - 40, 235, 235, 20, "#19352F", "#0F2621", "#142F2A")
    
    # Refining Distillation Columns (Towers)
    tower1_x, tower1_y = 410, 390
    draw_cylinder(draw, tower1_x, tower1_y, 28, 120, "#2BE841", "#008F11")
    draw_cylinder(draw, tower1_x, tower1_y - 120, 16, 40, "#10E7B3", "#0B8C6C")
    
    tower2_x, tower2_y = 470, 420
    draw_cylinder(draw, tower2_x, tower2_y, 35, 95, "#10E7B3", "#08664F")
    
    # Large Spherical / Cylindrical Storage Tanks
    tank1_x, tank1_y = 570, 430
    draw_cylinder(draw, tank1_x, tank1_y, 50, 55, "#2BE841", "#00AD14")
    
    tank2_x, tank2_y = 660, 390
    draw_cylinder(draw, tank2_x, tank2_y, 45, 50, "#10E7B3", "#0B8C6C")
    
    # Processing Unit / Facility Blocks
    draw_3d_cube(draw, 530, 350, 50, 50, 65, "#2BE841", "#008F11", "#00AD14")
    draw_3d_cube(draw, 350, 460, 40, 40, 50, "#10E7B3", "#0A7F62", "#0C9D79")
    
    # Industrial pipeline network (Isometric green conduits)
    draw.line([(tower1_x, tower1_y - 60), (tower2_x, tower2_y - 50)], fill="#2BE841", width=4)
    draw.line([(tower2_x, tower2_y - 50), (530, 340)], fill="#10E7B3", width=4)
    draw.line([(530, 340), (tank1_x, tank1_y - 30)], fill="#2BE841", width=4)
    draw.line([(tank1_x, tank1_y - 30), (tank2_x, tank2_y - 25)], fill="#10E7B3", width=4)
    
    # Floating growth indicator pillars (Crack spread & expansion surge)
    draw_3d_cube(draw, 300, 500, 20, 20, 40, "#2BE841", "#008F11", "#00AD14")
    draw_3d_cube(draw, 330, 520, 20, 20, 65, "#10E7B3", "#0A7F62", "#0C9D79")
    draw_3d_cube(draw, 360, 540, 20, 20, 95, "#2BE841", "#00AD14", "#10E7B3")
    
    # Energy nodes / Pulse points
    for nx, ny in [(tower1_x, tower1_y - 60), (tower2_x, tower2_y - 50), (530, 340), (tank1_x, tank1_y - 30), (tank2_x, tank2_y - 25)]:
        draw.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill="#FFFFFF", outline="#2BE841", width=2)
        
    # Add watermark logo
    img = add_watermark_logo(img, is_dark_bg=True)
    
    os.makedirs("knowledge/4-content/images", exist_ok=True)
    out_path = "knowledge/4-content/images/co-phieu-bsr-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat-nang-cap-dung-quat.jpg"
    img.save(out_path, "JPEG", quality=92)
    print(f"Created image: {out_path}")

if __name__ == "__main__":
    create_bsr_image()

