from PIL import Image, ImageDraw, ImageFont
import os

def create_simple_icon():
    # 32x32 icon
    size = (32, 32)
    image = Image.new('RGBA', size, (44, 201, 133, 255)) # Emerald Green
    draw = ImageDraw.Draw(image)
    
    # Simple 'FW' text
    # Since we might not have a font, just draw some pixels or try a default font
    try:
        # Drawing simple pixels for 'F' and 'W'
        # F
        draw.line([(8, 8), (14, 8)], fill="white", width=2)
        draw.line([(8, 8), (8, 22)], fill="white", width=2)
        draw.line([(8, 15), (12, 15)], fill="white", width=2)
        
        # W
        draw.line([(18, 8), (18, 22)], fill="white", width=2)
        draw.line([(18, 22), (22, 15)], fill="white", width=2)
        draw.line([(22, 15), (26, 22)], fill="white", width=2)
        draw.line([(26, 22), (26, 8)], fill="white", width=2)
    except:
        pass
        
    if not os.path.exists('assets'):
        os.makedirs('assets')
    image.save('assets/icon.ico', format='ICO')
    print("Icon created.")

if __name__ == "__main__":
    create_simple_icon()
