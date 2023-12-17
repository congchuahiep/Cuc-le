from PIL import Image, ImageDraw, ImageFont
import FrameImage

# Mở ảnh
def open_image(image_path):
    img = Image.open(image_path)
    return img

# Xác định kích cỡ Font ban đầu
def calculate_font_size(img):
    if img.width < img.height:
        font_size = img.width // 6.75
    else:
        font_size = img.height // 6.75
    return font_size

# Thêm khung vào ảnh, hầu hết mọi trường hợp sẽ in cả text vào khung
def add_frame_to_image(img, color_name="white", position="top", text="", style="default"):
    
    # Trước khi in, xác định kích cỡ font chữ
    font_size = calculate_font_size(img)

    # Xét style của khung
    if style == "what":
        img_new = FrameImage.what(img, text=text, font_size=font_size)
    elif style == "surround" or style == "frame" or style == "polaroid":
        img_new = FrameImage.surround(img, color_name=color_name, position=position, text=text, font_size=font_size)
    else:
        img_new = FrameImage.add(img, color_name=color_name, position=position, text=text, font_size=font_size)
    
    return img_new

# Thêm chữ vào ảnh
def add_text_to_image(img, text, position="top", font_size=0, align="center"):
    
    # Tính độ dài chữ
    text_count = len(text)

    # Tạo đối tượng vẽ và font
    draw = ImageDraw.Draw(img)
    if font_size == 0:
        font_size = calculate_font_size(img)

    # [For testing] Font size gốc
    origin_font_size = font_size

    # Tìm thử xem, với kích cỡ của ảnh và kích cỡ font thì một dòng có thể chứa tối đa bao nhiêu từ
    demo_text = 'w'
    max_letter_in_line = 0
    font = ImageFont.truetype("font/Bungee.ttf", font_size // 3)
    while draw.textlength(demo_text[:max_letter_in_line], font) < img.width - img.width * 0.1:
        demo_text += 'm'
        max_letter_in_line += 1
    max_letter_in_line -= 1

    # Tự động chia dòng
    words = text.split(' ')
    text = ''
    temp = 0
    for word in words:
        text += word
        if len(text) - temp >= max_letter_in_line:
            text += '\n'
            temp = len(text) 
        elif '\n' in word:
            temp = len(text)
        else:
            text += ' '

    font = ImageFont.truetype("font/Bungee.ttf", font_size)

    # Tìm dòng dài nhất trong chuỗi để làm mẫu tham chiếu cho các dòng khác
    lines = text.split('\n')
    longest = max(filter(lambda line: draw.textlength(line, font), lines), key=len)

    # Xác định độ dài của chuỗi khi chúng đến giới hạn viền của ảnh
    # Khúc này để xác định lúc nào chữ sẽ bắt đầu thu nhỏ lại
    max_text_count = 0
    if draw.textlength(longest, font) > img.width:
        while draw.textlength(longest[:max_text_count], font) < img.width:
            max_text_count += 1
        max_text_count -= 1
        max_width = draw.textlength(longest[:max_text_count], font)
    else:
        max_text_count = text_count
        max_width = draw.textlength(longest, font)

    # Xác định kích cỡ font chữ khi càng nhiều chữ, chiều dài càng tăng
    ratio = 1
    if max_text_count < text_count:
        ratio = max_width / draw.textlength(longest, font)
        font_size = int(font_size * ratio)
        if (img.height < img.width):
            font_size = 0.9 * font_size
    
    # Sử dụng font mặc định
    font = ImageFont.load_default()
    
    # Chỉnh font lại sau khi đã có kích cỡ mới
    font_size = int(font_size)
    font = ImageFont.truetype("font/Bungee.ttf", font_size)

    # Xác định vị trí in text
    pos_text_width = {
        "center": img.width / 2,
    }

    if align == "left":
        pos_text_width["left"] = img.width // 25 + draw.textlength(text, font) // 2
    elif align == "right":
        pos_text_width["right"] = img.width - img.width // 25 - draw.textlength(text, font) // 2,

    pos_text_height = {
        "top": img.height * 1 / 25,
        "middle": img.height * 1 / 2,
    }

    anchor = {
        "top": "ma",
        "middle": "mm",
        "bottom": "mm"
    }

    if position == "bottom":
        try:
            pos_text_height["bottom"] = img.height * (7 - len(lines)) / (8 - len(lines))
        except:
            pos_text_height["bottom"] = 0
    # Nếu người dùng một position bậy bạ
    elif position != "top" and position != "middle":
        position = "top"

    draw.multiline_text((pos_text_width[align], pos_text_height[position]), text, font=font, fill="white", anchor=anchor[position], spacing=font_size//6, stroke_width=font_size//20, stroke_fill="black", align=align)

    # [For Testing] Vị trí box chữ
    # box_left, box_top, box_right, box_bottom = draw.multiline_textbbox((img.width / 2, pos_text_height[position]), text, font=font, anchor="mm", spacing=font_size//6, stroke_width=font_size//20, align="center")
    # draw.rectangle([(box_left, box_top), (box_right, box_bottom)], outline="red", width=10)

    # [For Testing] Ghi các thông số
    print('img.width', img.width)
    print('img.height', img.height)
    print("font size", font_size)
    print("origin_font_size", origin_font_size)
    print("text_count", text_count)
    print("max_text_count", max_text_count)
    print("max_letter_in_line", max_letter_in_line)
    
    # Lưu ảnh đã chỉnh sửa
    return img

# Xuất ảnh
def render_picture(img, name):
    img.save(f"static/images/exports/{name}")
