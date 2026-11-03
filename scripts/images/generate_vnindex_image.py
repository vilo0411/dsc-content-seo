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

def draw_3d_cube(draw, cx, cy, width, height, depth, color_top, color_left, color_right):
    dx = depth * math.cos(math.radians(30))
    dy = depth * math.sin(math.radians(30))
    w2 = width / 2
    
    # Top face
    top_poly = [
        (cx, cy - height - dy),
        (cx + w2, cy - height),
        (cx, cy - height + dy),
        (cx - w2, cy - height)
    ]
    draw.polygon(top_poly, fill=color_top)
    
    # Left face
    left_poly = [
        (cx - w2, cy - height),
        (cx, cy - height + dy),
        (cx, cy + dy),
        (cx - w2, cy)
    ]
    draw.polygon(left_poly, fill=color_left)
    
    # Right face
    right_poly = [
        (cx, cy - height + dy),
        (cx + w2, cy - height),
        (cx + w2, cy),
        (cx, cy + dy)
    ]
    draw.polygon(right_poly, fill=color_right)

def create_vnindex_image():
    w, h = 1000, 750
    img = Image.new("RGB", (w, h), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Subtle isometric grid
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill="#132338", width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill="#132338", width=1)
        
    # Baseline floor
    draw.line([(80, 600), (920, 600)], fill="#1A334E", width=2)
    
    # Rising 3D Candlestick & Volume Columns representing VN-Index market cycle
    bars = [
        (160, 580, 50, 100, 25, "#107823", "#0B5819", "#084112"),
        (280, 580, 50, 180, 25, "#00AD14", "#008B10", "#006B0D"),
        (400, 580, 50, 140, 25, "#168B29", "#116D20", "#0C5118"),
        (520, 580, 50, 240, 25, "#1FBF33", "#199A27", "#137A1F"),
        (640, 580, 50, 310, 25, "#2BE841", "#22BA34", "#199128"),
        (760, 580, 50, 390, 25, "#10E7B3", "#0DB88E", "#0A8F6E"),
        (880, 580, 50, 460, 25, "#48F28A", "#2BE841", "#1DB834"),
    ]
    
    for cx, cy, bw, bh, bd, c_top, c_left, c_right in bars:
        # Wick lines (candlestick wicks)
        draw.line([(cx, cy - bh - bd - 35), (cx, cy - bh - bd)], fill=c_top, width=3)
        draw.line([(cx, cy + bd), (cx, cy + bd + 20)], fill=c_left, width=3)
        draw_3d_cube(draw, cx, cy, bw, bh, bd, c_top, c_left, c_right)
        
    # Golden / Cyan exponential trend curve over the peaks
    curve_pts = [
        (160, 455),
        (280, 375),
        (400, 415),
        (520, 315),
        (640, 245),
        (760, 165),
        (880, 95)
    ]
    
    # Glowing trendline
    for i in range(len(curve_pts) - 1):
        draw.line([curve_pts[i], curve_pts[i+1]], fill="#10E7B3", width=4)
        
    for px, py in curve_pts:
        draw.ellipse([px-8, py-8, px+8, py+8], fill="#2BE841", outline="#FFFFFF", width=2)
        
    # Radiating halo at the latest peak (representing new breakthrough)
    peak_x, peak_y = 880, 95
    for r in [20, 40, 60]:
        draw.ellipse([peak_x-r, peak_y-int(r*0.6), peak_x+r, peak_y+int(r*0.6)], outline="#10E7B3", width=2)
        
    img = add_watermark_logo(img, is_dark_bg=True)
    os.makedirs('knowledge/4-content/images', exist_ok=True)
    out_path = 'knowledge/4-content/images/chi-so-vn-index-va-y-nghia-bieu-do-thi-truong.jpg'
    img.save(out_path, quality=95)
    print(f"Created {out_path}")

if __name__ == '__main__':
    create_vnindex_image()

