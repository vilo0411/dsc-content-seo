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

def draw_iso_block(draw, cx, cy, w, h, d, c_top, c_left, c_right):
    dx = d * math.cos(math.radians(30))
    dy = d * math.sin(math.radians(30))
    w2 = w / 2
    
    # Top face
    top_poly = [
        (cx, cy - h - dy),
        (cx + w2, cy - h),
        (cx, cy - h + dy),
        (cx - w2, cy - h)
    ]
    draw.polygon(top_poly, fill=c_top)
    
    # Left face
    left_poly = [
        (cx - w2, cy - h),
        (cx, cy - h + dy),
        (cx, cy + dy),
        (cx - w2, cy)
    ]
    draw.polygon(left_poly, fill=c_left)
    
    # Right face
    right_poly = [
        (cx, cy - h + dy),
        (cx + w2, cy - h),
        (cx + w2, cy),
        (cx, cy + dy)
    ]
    draw.polygon(right_poly, fill=c_right)

def create_5step_pipeline_image():
    # 4:3 ratio: 1000x750
    w, h = 1000, 750
    img = Image.new("RGB", (w, h), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Grid lines
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill="#14283D", width=1)
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill="#14283D", width=1)
        
    # Draw 5 ascending isometric platforms
    steps_data = [
        (220, 520, 90, 40, 60, "#00AD14", "#008510", "#00640C"),
        (360, 470, 90, 70, 60, "#10E7B3", "#0DB88E", "#0A8A6B"),
        (500, 420, 90, 100, 60, "#2BE841", "#22BA34", "#198C27"),
        (640, 370, 90, 130, 60, "#10E7B3", "#0DB88E", "#0A8A6B"),
        (780, 320, 90, 160, 60, "#2BE841", "#00AD14", "#008510")
    ]
    
    # Connecting pipeline curve
    points = [(cx, cy - h_val - 20) for (cx, cy, _, h_val, _, _, _, _) in steps_data]
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill="#2BE841", width=5)
        
    for cx, cy, bw, bh, bd, c_top, c_left, c_right in steps_data:
        draw_iso_block(draw, cx, cy, bw, bh, bd, c_top, c_left, c_right)
        # Small glowing orb on top
        orb_y = cy - bh - 20
        draw.ellipse([(cx - 12, orb_y - 12), (cx + 12, orb_y + 12)], fill="#E8F8F2", outline="#2BE841", width=2)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    out_dir = "knowledge/4-content/images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau-quy-trinh-5-buoc.jpg")
    img.save(out_path, quality=95)
    print(f"Saved: {out_path}")

def create_capital_calculation_image():
    # 4:3 ratio: 1000x750
    w, h = 1000, 750
    img = Image.new("RGB", (w, h), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Background pattern
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill="#14283D", width=1)
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill="#14283D", width=1)
        
    # Central isometric base
    draw_iso_block(draw, 500, 560, 380, 30, 220, "#19354E", "#13283B", "#0E1D2B")
    
    # 3 distinct pillars representing 3 asset allocations / 100 shares lot
    draw_iso_block(draw, 380, 500, 70, 110, 50, "#10E7B3", "#0DB88E", "#0A8A6B")
    draw_iso_block(draw, 500, 480, 70, 160, 50, "#2BE841", "#22BA34", "#198C27")
    draw_iso_block(draw, 620, 460, 70, 210, 50, "#00AD14", "#008510", "#00640C")
    
    # Floating coin cylinders on top
    for cx, top_y, c_top in [(380, 500 - 110 - 30, "#E8F8F2"), (500, 480 - 160 - 30, "#E8F8F2"), (620, 460 - 210 - 30, "#E8F8F2")]:
        draw.ellipse([(cx - 25, top_y - 12), (cx + 25, top_y + 12)], fill=c_top, outline="#2BE841", width=2)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    out_dir = "knowledge/4-content/images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cach-mua-co-phieu-online-cho-nguoi-moi-bat-dau-bang-tinh-von.jpg")
    img.save(out_path, quality=95)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    create_5step_pipeline_image()
    create_capital_calculation_image()

