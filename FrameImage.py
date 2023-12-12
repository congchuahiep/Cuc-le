from PIL import Image, ImageDraw, ImageFont
import color, TextImage

def what(img, text="", font_size=0):
    img_new = Image.new('RGB', (img.width, img.height), color.colors["black"])
    out_width = img.width
    out_height = img.height

    img = img.resize((int(0.7*img.width), int(0.7*img.height)))
    in_width = img.width

    gap = (out_width - in_width) // 2
    gap_top = out_height // 20

    img_new.paste(img, (gap, gap_top))

    draw = ImageDraw.Draw(img_new)
    draw.rectangle([(gap, gap_top),(gap + img.width, gap_top + img.height)], outline="white", width=img.width//500)

    img_new = TextImage.add_text_to_image(img_new, text=text, position="bottom", font_size=font_size)

    return img_new

def surround(img, color_name="white", position="top", text="", font_size=0):
    try: 
        background_color = color.colors[color_name]
    except:
        background_color = color.colors["white"]

    img_with_border = Image.new('RGB', (img.width, img.height), background_color)
    out_width = img.width
    out_height = img.height


    img = img.resize((int(0.95*img.width), int(0.95*img.height)))
    in_width = img.width
    in_height = img.height

    gap = (out_width - in_width) // 2
    gap_top = (out_height - in_height) // 2

    img_with_border.paste(img, (gap, gap_top))

    img_text = Image.new('RGBA', (out_width, out_height // 3), (0, 0, 0, 0))
    img_new = Image.new('RGB', (out_width, out_height + out_height // 3), background_color)

    # In chữ lên frame
    TextImage.add_text_to_image(img_text, text=text, position="middle", font_size=font_size)

    if position == 'bottom':
        img_new.paste(img_with_border, (0, 0))
        img_new.paste(img_text, (0, out_height))
    else:
        img_new.paste(img_text, (0, 0))
        img_new.paste(img_with_border, (0, out_height // 3))
    
    return img_new

def add(img, color_name="white", position="top", text="", font_size=0):
    try: 
        background_color = color.colors[color_name]
    except:
        background_color = color.colors["white"]

    img_text = Image.new('RGB', (img.width, img.height // 3), background_color)
    img_new = Image.new('RGB', (img.width, img.height + img.height // 3), background_color)

    # In chữ lên frame
    TextImage.add_text_to_image(img_text, text=text, position="middle", font_size=font_size)

    if position == 'bottom':
        img_new.paste(img, (0, 0))
        img_new.paste(img_text, (0, img.height))
    else:
        img_new.paste(img_text, (0, 0))
        img_new.paste(img, (0, img.height // 3))
    
    return img_new