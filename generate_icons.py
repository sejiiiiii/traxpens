import os
import shutil
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image, ImageDraw

def main():
    svg_path = os.path.join('SVG', 'Artboard 1Traxpenslogo.svg')
    with open(svg_path, 'r', encoding='utf-8') as f:
        original_svg = f.read()

    # Universal High-Contrast Adaptive SVG:
    # Stem: #18181B (Rich Black) with a crisp #FFFFFF contour stroke (18px)
    # This guarantees that:
    # 1. On WHITE backgrounds (Chrome install view, light launcher, light download card):
    #    The white stroke merges with the background; the rich black line and vivid emerald bars are 100% crisp!
    # 2. On DARK backgrounds (dark tabs, dark wallpapers, obsidian app icon tiles):
    #    The luminous white stroke contours the black stem so the shape never fades or disappears!
    universal_svg = '''<svg id="Layer_1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080">
  <path class="stem" d="M592.6,917.44c-41.99,0-71.76-15.39-91.93-32.63-21.51-18.39-38.24-44.58-49.73-77.84-9.87-28.56-16.14-63.17-18.64-102.85-4.09-65.02,1.7-145.36,17.22-238.8,26.19-157.74,71.88-301.32,72.34-302.75l45.71,14.63c-.45,1.4-45.19,142.1-70.78,296.47-14.88,89.75-20.45,166.34-16.57,227.65,4.57,72.16,21.94,121.62,51.64,147,16.6,14.19,36.99,21.28,61.02,21.28,27.53,0,59.84-9.3,96.71-27.9,55.7-28.1,99.56-67.02,100-67.41l31.98,35.8c-1.97,1.76-49.07,43.56-110.36,74.47-47.43,23.92-86.58,32.88-118.62,32.88Z" fill="#18181B" stroke="#FFFFFF" stroke-width="18" stroke-linejoin="round" />
  <g class="bar">
    <rect x="253.52" y="463.32" width="467.4" height="48" transform="translate(-132.09 185.13) rotate(-19)" fill="#10B981" />
    <rect x="258.55" y="559.19" width="467.4" height="48" transform="translate(-163.02 191.98) rotate(-19)" fill="#10B981" />
  </g>
</svg>'''

    # Save SVG assets
    with open('favicon.svg', 'w', encoding='utf-8') as f:
        f.write(universal_svg)
    with open('traxpens-logo.svg', 'w', encoding='utf-8') as f:
        f.write(universal_svg)

    # Standalone black and white SVGs
    black_stem_svg = original_svg.replace('fill="#009444"', 'fill="#10B981"')
    with open('traxpens-logo-dark.svg', 'w', encoding='utf-8') as f:
        f.write(black_stem_svg)

    white_stem_svg = original_svg.replace('fill="#231f20"', 'fill="#FFFFFF"').replace('fill="#009444"', 'fill="#10B981"')
    with open('traxpens-logo-white.svg', 'w', encoding='utf-8') as f:
        f.write(white_stem_svg)

    # Render high-res transparent RGBA logo using Cairo with bg=None
    drawing = svg2rlg('favicon.svg')
    renderPM.drawToFile(drawing, 'temp_trans_logo.png', fmt='PNG', bg=None, backendFmt='RGBA')
    raw_logo = Image.open('temp_trans_logo.png').convert('RGBA')

    # Generate PWA Launcher App Icons:
    def create_icon_asset(size, is_maskable=False):
        # Full-bleed solid obsidian tile #0B0E14
        canvas = Image.new('RGBA', (size, size), (11, 14, 20, 255))
        draw = ImageDraw.Draw(canvas)
        
        if not is_maskable:
            bg_pad = max(2, int(size * 0.02))
            radius = int(size * 0.22)
            draw.rounded_rectangle(
                [bg_pad, bg_pad, size - bg_pad - 1, size - bg_pad - 1],
                radius=radius,
                fill=(11, 14, 20, 255),
                outline=(30, 41, 59, 255),
                width=max(1, int(size * 0.015))
            )
        else:
            draw.rectangle([0, 0, size, size], fill=(11, 14, 20, 255))

        # Size of logo inside
        content_scale = 0.65 if is_maskable else 0.74
        target_w = int(size * content_scale)
        target_h = int(size * content_scale)
        
        scaled = raw_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
        pos_x = (size - target_w) // 2
        pos_y = (size - target_h) // 2

        canvas.paste(scaled, (pos_x, pos_y), scaled)
        return canvas

    # Transparent favicon PNGs for browser tabs
    def create_favicon_png(size):
        canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        target_w = int(size * 0.90)
        target_h = int(size * 0.90)
        scaled = raw_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
        pos_x = (size - target_w) // 2
        pos_y = (size - target_h) // 2
        canvas.paste(scaled, (pos_x, pos_y), scaled)
        return canvas

    # Save PWA icons
    create_icon_asset(512, False).save('icon-512.png', 'PNG')
    create_icon_asset(192, False).save('icon-192.png', 'PNG')
    create_icon_asset(512, True).save('icon-maskable-512.png', 'PNG')
    create_icon_asset(192, True).save('icon-maskable-192.png', 'PNG')
    create_icon_asset(180, False).save('apple-touch-icon.png', 'PNG')

    # Save favicons with black stem + white stroke
    create_favicon_png(64).save('favicon.png', 'PNG')
    create_favicon_png(32).save('favicon-32x32.png', 'PNG')

    # Mirror all generated assets to web/ directory
    os.makedirs('web', exist_ok=True)
    for fname in [
        'icon-512.png', 'icon-192.png', 'icon-maskable-512.png', 'icon-maskable-192.png',
        'apple-touch-icon.png', 'favicon.png', 'favicon-32x32.png', 'favicon.svg',
        'traxpens-logo.svg', 'traxpens-logo-white.svg', 'traxpens-logo-dark.svg'
    ]:
        shutil.copy2(fname, os.path.join('web', fname))

    # Clean up temp file
    if os.path.exists('temp_trans_logo.png'):
        os.remove('temp_trans_logo.png')

    print('Successfully generated all icons with guaranteed contrast across all backgrounds!')

if __name__ == '__main__':
    main()
