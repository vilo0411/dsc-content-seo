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

def draw_3d_building(draw, cx, cy, width, depth, height, color_top, color_left, color_right):
    dx = width * math.cos(math.radians(30))
    dy = width * math.sin(math.radians(30))
    dz = depth * math.cos(math.radians(30))
    dw = depth * math.sin(math.radians(30))
    h = height
    
    # Top face
    top_poly = [
        (cx, cy - h),
        (cx + dx, cy - h + dy),
        (cx + dx - dz, cy - h + dy + dw),
        (cx - dz, cy - h + dw)
    ]
    draw.polygon(top_poly, fill=color_top)
    
    # Left face
    left_poly = [
        (cx - dz, cy - h + dw),
        (cx + dx - dz, cy - h + dy + dw),
        (cx + dx - dz, cy + dy + dw),
        (cx - dz, cy + dw)
    ]
    draw.polygon(left_poly, fill=color_left)
    
    # Front-right face
    right_poly = [
        (cx + dx - dz, cy - h + dy + dw),
        (cx + dx, cy - h + dy),
        (cx + dx, cy + dy),
        (cx + dx - dz, cy + dy + dw)
    ]
    draw.polygon(right_poly, fill=color_right)

def create_tch_image():
    w, h = 1000, 750
    img = Image.new("RGB", (w, h), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # Background subtle grid lines
    for x in range(0, w, 50):
        draw.line([(x, 0), (x, h)], fill="#14283D", width=1)
    for y in range(0, h, 50):
        draw.line([(0, y), (w, y)], fill="#14283D", width=1)
        
    # Flowing river / canal representing Hai Phong riverfront (Bac Song Cam)
    river_points = [
        (-50, 480), (200, 500), (450, 530), (700, 520), (1050, 560),
        (1050, 680), (700, 640), (450, 650), (200, 620), (-50, 600)
    ]
    draw.polygon(river_points, fill="#0A3641")
    
    # Bridge / infrastructure connecting lines
    for offset in range(-20, 30, 10):
        draw.line([(350 + offset, 450), (480 + offset, 670)], fill="#10E7B3", width=2)
        
    # Isometric ground platform for modern urban center
    base_cx, base_cy = 500, 420
    draw.polygon([
        (500, 180),
        (850, 360),
        (500, 540),
        (150, 360)
    ], fill="#11273F", outline="#1E456E", width=2)
    
    # Draw urban cluster of high-rises and commercial complexes (Hoang Huy New City & Commerce)
    # Background towers
    draw_3d_building(draw, 420, 320, 50, 40, 140, "#10E7B3", "#008A10", "#00AD14")
    draw_3d_building(draw, 500, 300, 60, 50, 190, "#2BE841", "#00AD14", "#096B15")
    draw_3d_building(draw, 580, 330, 45, 45, 120, "#10E7B3", "#00AD14", "#085714")
    
    # Midground modern towers
    draw_3d_building(draw, 340, 380, 55, 45, 160, "#2BE841", "#008A10", "#00AD14")
    draw_3d_building(draw, 460, 400, 75, 60, 240, "#39FF14", "#10E7B3", "#00AD14")
    draw_3d_building(draw, 560, 410, 65, 50, 170, "#10E7B3", "#00AD14", "#096B15")
    draw_3d_building(draw, 660, 370, 50, 45, 130, "#2BE841", "#008A10", "#00AD14")
    
    # Low-rise villa blocks (Green River & New City low-rises)
    for i in range(4):
        cx = 280 + i * 45
        cy = 440 + i * 22
        draw_3d_building(draw, cx, cy, 30, 25, 40, "#2BE841", "#085714", "#00AD14")
        
    for i in range(4):
        cx = 540 + i * 40
        cy = 480 - i * 18
        draw_3d_building(draw, cx, cy, 30, 25, 45, "#10E7B3", "#085714", "#00AD14")

    # Financial growth vectors (arrows / glowing graph lines)
    graph_points = [(180, 420), (320, 370), (460, 260), (620, 200), (820, 120)]
    for i in range(len(graph_points) - 1):
        draw.line([graph_points[i], graph_points[i+1]], fill="#2BE841", width=4)
        draw.ellipse([graph_points[i][0]-5, graph_points[i][1]-5, graph_points[i][0]+5, graph_points[i][1]+5], fill="#10E7B3")
    draw.ellipse([graph_points[-1][0]-7, graph_points[-1][1]-7, graph_points[-1][0]+7, graph_points[-1][1]+7], fill="#FFFFFF", outline="#2BE841", width=3)

    # Watermark logo
    img = add_watermark_logo(img, is_dark_bg=True)
    
    out_dir = "knowledge/4-content/images"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "co-phieu-tch-tong-quan-danh-gia-va-cap-nhat-ket-qua-kinh-doanh-moi-nhat-quy-dat-hai-phong.jpg")
    img.save(out_path, format="JPEG", quality=92)
    print(f"Generated TCH 3D image at: {out_path}")

if __name__ == "__main__":
    create_tch_image()

