import os
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image, ImageDraw

def main():
    # Read the original SVG from SVG/Artboard 1Traxpenslogo.svg
    svg_path = os.path.join('SVG', 'Artboard 1Traxpenslogo.svg')
    with open(svg_path, 'r', encoding='utf-8') as f:
        original_svg = f.read()

    # Create high-contrast versions of the SVG:
    # 1. Dark Theme / App Icon version:
    # Stem: #FFFFFF (White)
    # Slanted bars: #10B981 (Vivid emerald)
    svg_white_stem = original_svg.replace('fill="#231f20"', 'fill="#FFFFFF"').replace('fill="#009444"', 'fill="#10B981"')
    
    # Save standalone SVGs for web use:
    with open('traxpens-logo-white.svg', 'w', encoding='utf-8') as f:
        f.write(svg_white_stem)

    # 2. Light Theme version:
    # Stem: #0F172A (Deep charcoal)
    # Slanted bars: #009444 (Vivid green)
    svg_dark_stem = original_svg.replace('fill="#231f20"', 'fill="#0F172A"')
    with open('traxpens-logo-dark.svg', 'w', encoding='utf-8') as f:
        f.write(svg_dark_stem)

    # 3. Adaptive SVG with media queries (for favicon.svg and responsive <img>):
    adaptive_svg = '''<svg id="Layer_1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080">
  <style>
    .stem { fill: #0F172A; }
    .bar { fill: #009444; }
    @media (prefers-color-scheme: dark) {
      .stem { fill: #F0F4F8; }
      .bar { fill: #10B981; }
    }
  </style>
  <path class="stem" d="M592.6,917.44c-41.99,0-71.76-15.39-91.93-32.63-21.51-18.39-38.24-44.58-49.73-77.84-9.87-28.56-16.14-63.17-18.64-102.85-4.09-65.02,1.7-145.36,17.22-238.8,26.19-157.74,71.88-301.32,72.34-302.75l45.71,14.63c-.45,1.4-45.19,142.1-70.78,296.47-14.88,89.75-20.45,166.34-16.57,227.65,4.57,72.16,21.94,121.62,51.64,147,16.6,14.19,36.99,21.28,61.02,21.28,27.53,0,59.84-9.3,96.71-27.9,55.7-28.1,99.56-67.02,100-67.41l31.98,35.8c-1.97,1.76-49.07,43.56-110.36,74.47-47.43,23.92-86.58,32.88-118.62,32.88Z"/>
  <g class="bar">
    <rect x="253.52" y="463.32" width="467.4" height="48" transform="translate(-132.09 185.13) rotate(-19)"/>
    <rect x="258.55" y="559.19" width="467.4" height="48" transform="translate(-163.02 191.98) rotate(-19)"/>
  </g>
</svg>'''
    with open('favicon.svg', 'w', encoding='utf-8') as f:
        f.write(adaptive_svg)
    with open('traxpens-logo.svg', 'w', encoding='utf-8') as f:
        f.write(adaptive_svg)

    # Render base high-res logo from the white stem SVG
    drawing = svg2rlg('traxpens-logo-white.svg')
    # Scale to 1024
    scale = 1024 / 1080.0
    drawing.scale(scale, scale)
    drawing.width = 1024
    drawing.height = 1024

    renderPM.drawToFile(drawing, 'temp_raw_logo.png', fmt='PNG')
    raw_logo = Image.open('temp_raw_logo.png').convert('RGBA')
    print('Raw high-res logo rendered:', raw_logo.size)

    # Generate PWA App Icons:
    def create_icon_asset(size, is_maskable=False):
        canvas = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)
        
        # High contrast background tile:
        # Slate/Obsidian #090C10 with high-contrast subtle border
        # This guarantees the icon has solid contrast on ANY wallpaper (dark, light, colorful, or photo)
        bg_pad = 0 if is_maskable else max(2, int(size * 0.02))
        radius = 0 if is_maskable else int(size * 0.22)
        
        if not is_maskable:
            draw.rounded_rectangle(
                [bg_pad, bg_pad, size - bg_pad - 1, size - bg_pad - 1],
                radius=radius,
                fill=(9, 12, 16, 255),
                outline=(30, 41, 59, 255),
                width=max(1, int(size * 0.015))
            )
        else:
            # Maskable icon requires full-bleed background for Android safe zone
            draw.rectangle([0, 0, size, size], fill=(9, 12, 16, 255))

        # Size of logo inside
        # Maskable: must fit 80% circle safe zone
        content_scale = 0.65 if is_maskable else 0.76
        target_w = int(size * content_scale)
        target_h = int(size * content_scale)
        
        scaled = raw_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
        pos_x = (size - target_w) // 2
        pos_y = (size - target_h) // 2

        canvas.paste(scaled, (pos_x, pos_y), scaled)
        return canvas

    # Save all standard PWA / browser sizes
    create_icon_asset(512, False).save('icon-512.png', 'PNG')
    create_icon_asset(192, False).save('icon-192.png', 'PNG')
    create_icon_asset(512, True).save('icon-maskable-512.png', 'PNG')
    create_icon_asset(192, True).save('icon-maskable-192.png', 'PNG')
    create_icon_asset(180, False).save('apple-touch-icon.png', 'PNG')
    create_icon_asset(64, False).save('favicon.png', 'PNG')
    create_icon_asset(32, False).save('favicon-32x32.png', 'PNG')

    # Also copy to web/ folder
    os.makedirs('web', exist_ok=True)
    import shutil
    for fname in [
        'icon-512.png', 'icon-192.png', 'icon-maskable-512.png', 'icon-maskable-192.png',
        'apple-touch-icon.png', 'favicon.png', 'favicon-32x32.png', 'favicon.svg',
        'traxpens-logo.svg', 'traxpens-logo-white.svg', 'traxpens-logo-dark.svg'
    ]:
        shutil.copy2(fname, os.path.join('web', fname))

    # Clean up temp file
    if os.path.exists('temp_raw_logo.png'):
        os.remove('temp_raw_logo.png')

    print('Successfully generated and mirrored all icon and logo assets!')

if __name__ == '__main__':
    main()
