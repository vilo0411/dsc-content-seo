import os
import math
from PIL import Image, ImageDraw, ImageFilter

def add_watermark_logo(base_img, is_dark_bg=False):
    """Paste logo cleanly at Top-Left (lề 4%) without any box or border."""
    logo_path = 'knowledge/1-brand/assets/logos/logo-for-dark-bg.png' if is_dark_bg else 'knowledge/1-brand/assets/logos/logo-for-light-bg.png'
    if not os.path.exists(logo_path):
        print(f"Logo not found at {logo_path}")
        return base_img
    
    logo = Image.open(logo_path).convert("RGBA")
    target_w = 180
    aspect = logo.height / logo.width
    target_h = int(target_w * aspect)
    logo = logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Top-Left (lề 4% = 48px)
    pad_x = int(base_img.width * 0.04)
    pad_y = int(base_img.height * 0.04)
    
    base_img.paste(logo, (pad_x, pad_y), logo)
    return base_img

def draw_3d_cube(draw, cx, cy, size, color_top, color_left, color_right):
    """Draw a 3D isometric cube block."""
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

def draw_3d_shield(draw, cx, cy, w, h, fill_color, outline_color):
    """Draw a sleek 3D protective shield emblem."""
    points = [
        (cx, cy - h//2),
        (cx + w//2, cy - h//3),
        (cx + w//2, cy + h//6),
        (cx, cy + h//2),
        (cx - w//2, cy + h//6),
        (cx - w//2, cy - h//3)
    ]
    draw.polygon(points, fill=fill_color, outline=outline_color, width=4)

def generate_concept_1():
    # 1200x900 (4:3 aspect ratio) - INLINE COMPARISON DIAGRAM (NO-TEXT)
    width, height = 1200, 900
    img = Image.new("RGBA", (width, height), "#E8F8F2")
    draw = ImageDraw.Draw(img)
    
    cy = height // 2 + 40
    
    # Left Platform: Emotional Volatility (Slate / Grey tones)
    cx_left = 340
    draw.ellipse([cx_left - 200, cy + 100, cx_left + 200, cy + 190], fill="#CBD5E1")
    draw.ellipse([cx_left - 150, cy + 120, cx_left + 150, cy + 170], fill="#94A3B8")
    
    # Unstable Volatility Wave Pillars
    draw_3d_cube(draw, cx_left - 80, cy + 40, 40, "#64748B", "#475569", "#334155")
    draw_3d_cube(draw, cx_left, cy - 20, 50, "#475569", "#334155", "#1E293B")
    draw_3d_cube(draw, cx_left + 80, cy + 60, 35, "#94A3B8", "#64748B", "#475569")
    
    # Right Platform: DSC Disciplined Investment (Emerald & Teal Glowing)
    cx_right = 860
    draw.ellipse([cx_right - 220, cy + 100, cx_right + 220, cy + 190], fill="#D1FAE5")
    draw.ellipse([cx_right - 170, cy + 120, cx_right + 170, cy + 170], fill="#A7F3D0")
    
    # Steady Upward Growth Steps (Emerald / Neon / Teal)
    draw_3d_cube(draw, cx_right - 100, cy + 50, 45, "#00AD14", "#065F46", "#047857")
    draw_3d_cube(draw, cx_right - 30, cy + 10, 55, "#2BE841", "#00AD14", "#065F46")
    draw_3d_cube(draw, cx_right + 40, cy - 30, 65, "#10E7B3", "#2BE841", "#00AD14")
    
    # Elevated Shield of Discipline on Top Right
    draw_3d_shield(draw, cx_right + 40, cy - 140, 100, 130, "#0D1B2A", "#10E7B3")
    draw.polygon([
        (cx_right + 20, cy - 140),
        (cx_right + 35, cy - 125),
        (cx_right + 65, cy - 155),
        (cx_right + 35, cy - 110)
    ], fill="#2BE841")

    # Center Comparison Divider Line / Symbol
    draw.line([(width // 2, 220), (width // 2, 750)], fill="#00AD14", width=3)
    draw.ellipse([width // 2 - 35, cy - 35, width // 2 + 35, cy + 35], fill="#0D1B2A", outline="#10E7B3", width=3)
    draw_3d_cube(draw, width // 2, cy, 22, "#2BE841", "#00AD14", "#10E7B3")

    # Top-Left Official DSC Logo watermark
    img = add_watermark_logo(img, is_dark_bg=False)
    
    output_path = 'knowledge/4-content/images/fomo-trong-dau-tu-chung-khoan-la-gi-concept1.jpg'
    img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"Generated Rich Inline Diagram {output_path}")

def generate_concept_2():
    # 1200x900 (4:3 aspect ratio) - INLINE 4-STRATEGY DIAGRAM (NO-TEXT)
    width, height = 1200, 900
    img = Image.new("RGBA", (width, height), "#0D1B2A")
    draw = ImageDraw.Draw(img)
    
    # 4 Strategy Diagram Nodes (2x2 grid layout connected by glowing cyan-emerald lines)
    nodes = [
        (280, 280),  # Node 1: Stop Loss Shield
        (920, 280),  # Node 2: Tranche Allocation Steps
        (280, 640),  # Node 3: App Price Alert Bell
        (920, 640)   # Node 4: 1:1 Advisor Consultation
    ]
    
    # Connecting Lines
    draw.line([nodes[0], nodes[1]], fill="#10E7B3", width=4)
    draw.line([nodes[0], nodes[2]], fill="#00AD14", width=4)
    draw.line([nodes[1], nodes[3]], fill="#00AD14", width=4)
    draw.line([nodes[2], nodes[3]], fill="#10E7B3", width=4)
    
    # Central Hub Core
    cx, cy = width // 2, height // 2
    draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill="#162A45", outline="#2BE841", width=3)
    draw_3d_shield(draw, cx, cy, 80, 100, "#0D1B2A", "#10E7B3")
    draw_3d_cube(draw, cx, cy - 10, 25, "#2BE841", "#00AD14", "#10E7B3")
    
    # Node 1: Stop Loss 5-7% Shield Emblem
    x, y = nodes[0]
    draw.rounded_rectangle([x - 140, y - 100, x + 140, y + 100], radius=16, fill="#162A45", outline="#00AD14", width=2)
    draw_3d_shield(draw, x, y, 90, 110, "#0D1B2A", "#00AD14")
    draw_3d_cube(draw, x, y, 25, "#00AD14", "#065F46", "#047857")

    # Node 2: Tranche Allocation Steps (3D Staircase Cubes)
    x, y = nodes[1]
    draw.rounded_rectangle([x - 140, y - 100, x + 140, y + 100], radius=16, fill="#162A45", outline="#10E7B3", width=2)
    draw_3d_cube(draw, x - 40, y + 20, 22, "#00AD14", "#065F46", "#047857")
    draw_3d_cube(draw, x, y - 10, 28, "#2BE841", "#00AD14", "#065F46")
    draw_3d_cube(draw, x + 40, y - 40, 34, "#10E7B3", "#2BE841", "#00AD14")

    # Node 3: App DSC Price Alert Bell Emblem
    x, y = nodes[2]
    draw.rounded_rectangle([x - 140, y - 100, x + 140, y + 100], radius=16, fill="#162A45", outline="#2BE841", width=2)
    draw.ellipse([x - 40, y - 50, x + 40, y + 30], fill="#0D1B2A", outline="#2BE841", width=2)
    draw_3d_cube(draw, x, y - 10, 32, "#2BE841", "#10E7B3", "#00AD14")

    # Node 4: 1:1 Advisor Consultation Badge
    x, y = nodes[3]
    draw.rounded_rectangle([x - 140, y - 100, x + 140, y + 100], radius=16, fill="#162A45", outline="#00AD14", width=2)
    draw.ellipse([x - 45, y - 45, x + 45, y + 45], fill="#0D1B2A", outline="#00AD14", width=2)
    draw_3d_cube(draw, x, y - 5, 30, "#00AD14", "#2BE841", "#10E7B3")

    # Top-Left Official DSC Logo watermark
    img = add_watermark_logo(img, is_dark_bg=True)
    
    output_path = 'knowledge/4-content/images/fomo-trong-dau-tu-chung-khoan-la-gi-concept2.jpg'
    img.convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"Generated Rich Inline Diagram {output_path}")

if __name__ == '__main__':
    generate_concept_1()
    generate_concept_2()
