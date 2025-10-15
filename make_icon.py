from PIL import Image, ImageDraw

# Simple script to generate a PNG and multi-size ICO for the app.
# Run: python make_icon.py

size = 256
image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)
bg = (22, 120, 204, 255)
draw.rectangle((20, 20, size - 20, size - 20), fill=bg)
# glyph
draw.rectangle((96, 72, 160, 192), fill=(255,255,255,255))

png_path = 'shutdown_icon.png'
ico_path = 'shutdown_icon.ico'

image.save(png_path)
print(f'Created {png_path}')

# Create multi-resolution ICO
sizes = [256, 128, 64, 48, 32, 16]
icons = []
for s in sizes:
	im = image.resize((s, s), Image.LANCZOS)
	icons.append(im)

# Pillow can save list of images as .ico
icons[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes])
print(f'Created {ico_path}')
