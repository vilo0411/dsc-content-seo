import os
import math
from PIL import Image, ImageDraw

def add_watermark_logo(base_img, is_dark_bg=False):
    logo_path = 'knowledge/1-brand/assets/logos/logo-for-dark-bg.png' if is_dark_bg else 'knowledge/1-brand/assets/logos/logo-for-light-bg.png'
    if not os.path.exists(logo_path):
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

def draw_3d_cube(draw, cx, cy, size, h_size, color_top, color_left, color_right):
    dx = size * math.cos(math.radians(30))
    dy = size * math.sin(math.radians(30))
    
    top_poly = [
        (cx, cy - h_size),
        (cx + dx, cy - h_size + dy),
        (cx, cy - h_size + 2 * dy),
        (cx - dx, cy - h_size + dy)
    ]
    draw.polygon(top_poly, fill=color_top)
    
    left_poly = [
        (cx - dx, cy - h_size + dy),
        (cx, cy - h_size + 2 * dy),
        (cx, cy + dy),
        (cx - dx, cy)
    ]
    draw.polygon(left_poly, fill=color_left)
    
    right_poly = [
        (cx, cy - h_size + 2 * dy),
        (cx + dx, cy - h_size + dy),
        (cx + dx, cy),
        (cx, cy + dy)
    ]
    draw.polygon(right_poly, fill=color_right)

def generate_roa_by_industry():
    width, height = 1200, 675
    img = Image.new("RGBA", (width, height), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    cy = height // 2 + 80
    
    # 4 Industry Pillars (Banking, Real Estate, Manufacturing/Retail, Tech)
    bars = [
        (250, 60, "#475569", "#334155", "#1E293B"),    # Banking (heavy asset)
        (480, 110, "#00AD14", "#065F46", "#047857"),   # Real Estate
        (710, 180, "#2BE841", "#00AD14", "#065F46"),   # Manufacturing / Retail
        (940, 260, "#10E7B3", "#2BE841", "#00AD14")    # Tech / Services (high ROA)
    ]
    
    # Base grid lines
    for x in range(150, 1050, 120):
        draw.line([(x, cy + 40), (x + 100, cy - 20)], fill="#1E293B", width=2)
        
    for cx, h, c_top, c_left, c_right in bars:
        draw_3d_cube(draw, cx, cy, 50, h, c_top, c_left, c_right)
        
    # Glow trend line
    trend_points = [(250, cy - 60), (480, cy - 110), (710, cy - 180), (940, cy - 260)]
    draw.line(trend_points, fill="#10E7B3", width=6)
    for px, py in trend_points:
        draw.ellipse([px-10, py-10, px+10, py+10], fill="#2BE841", outline="#FFFFFF", width=2)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    out_dir = "knowledge/4-content/images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "chi-so-roa-la-gi-y-nghia-va-cach-su-dung-roa-by-industry.jpg")
    img.convert("RGB").save(out_path, quality=95)
    print(f"Generated {out_path}")

def generate_dupont_model():
    width, height = 1200, 675
    img = Image.new("RGBA", (width, height), "#E8F8F2")
    draw = ImageDraw.Draw(img)
    
    cy = height // 2
    
    # DuPont Formula Nodes: ROE = ROA x Financial Leverage
    # Left: ROA Node
    cx1 = 300
    draw.ellipse([cx1 - 100, cy - 60, cx1 + 100, cy + 60], fill="#00AD14", outline="#065F46", width=4)
    draw_3d_cube(draw, cx1, cy + 10, 35, 40, "#2BE841", "#00AD14", "#065F46")
    
    # Center Operator (x)
    draw.line([(450, cy), (510, cy)], fill="#0D1B2A", width=8)
    draw.line([(480, cy - 30), (480, cy + 30)], fill="#0D1B2A", width=8)
    
    # Middle: Financial Leverage Node
    cx2 = 650
    draw.ellipse([cx2 - 100, cy - 60, cx2 + 100, cy + 60], fill="#10E7B3", outline="#00AD14", width=4)
    draw_3d_cube(draw, cx2, cy + 10, 35, 60, "#2BE841", "#10E7B3", "#00AD14")
    
    # Equals Sign (=)
    draw.line([(800, cy - 15), (860, cy - 15)], fill="#0D1B2A", width=8)
    draw.line([(800, cy + 15), (860, cy + 15)], fill="#0D1B2A", width=8)
    
    # Right: ROE Core Output
    cx3 = 980
    draw.ellipse([cx3 - 120, cy - 80, cx3 + 120, cy + 80], fill="#0D1B2A", outline="#10E7B3", width=6)
    draw_3d_cube(draw, cx3, cy + 10, 45, 80, "#10E7B3", "#2BE841", "#00AD14")
    
    img = add_watermark_logo(img, is_dark_bg=False)
    out_dir = "knowledge/4-content/images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "chi-so-roa-la-gi-y-nghia-va-cach-su-dung-dupont-model.jpg")
    img.convert("RGB").save(out_path, quality=95)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_roa_by_industry()
    generate_dupont_model()

