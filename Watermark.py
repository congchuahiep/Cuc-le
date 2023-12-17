from PIL import Image, ImageDraw, ImageFont

# Mở watermark
def add(watermark_path):
    # Mở file với chế độ "RGBA" để biết là ảnh có độ trong suốt
    watermark = Image.open(watermark_path).convert("RGBA")
        
    # Trả về watermark và mask
    return watermark

def text(text="", position="bottom-left"):
    text_count = len(text)
    img_text = Image.new('RGBA', (83 * text_count, 200), (0, 0, 0, 0))

    # Tính độ dài chữ
    draw = ImageDraw.Draw(img_text)
    font_size = 110
    font = ImageFont.truetype("font/Bungee.ttf", font_size)

    # Căn lề cho chữ
    align ={
        "top-left": "left",
        "top-right": "right",
        "bottom-left": "left",
        "bottom-right": "right"
    }

    # Tìm vị trí mốc chữ
    anchor = {
        "top-left": "lt",
        "top-right": "rt",
        "bottom-left": "lb",
        "bottom-right": "rb"
    }

    # Tìm vị chí chèn
    pos_x = {
        "top-left": 0,
        "top-right": img_text.width,
        "bottom-left": 0,
        "bottom-right": img_text.width
    }
    pos_y = {
        "top-left": 0,
        "top-right": 0,
        "bottom-left": img_text.height,
        "bottom-right": img_text.height
    }

    draw.text((pos_x[position], pos_y[position]), text, font=font, fill="white", anchor=anchor[position], spacing=font_size//6, stroke_width=font_size//20, stroke_fill="black", align=align)

    # [For Testing]
    # draw.rectangle([(0, 0), (img_text.width, img_text.height)], outline="red", width=10)
    return img_text

# Tính kích thước watermark và tạo mask để chèn in mờ
def calculate_size(img, watermark, divide=8, opacity=0.6, text=1):

    # Tuỳ chỉnh kích thước watermark để phù hợp với ảnh
    watermark_width = int (img.width // divide) * text
    watermark_height = (watermark.height * watermark_width) // watermark.width 

    watermark = watermark.resize((watermark_width, watermark_height))

    mask = watermark
    if opacity != 1:
        mask = mask.convert("L").point(lambda p: p * opacity)

    # [For Testing]
    print("watermark_width", watermark_width, watermark.width)
    print("watermark_height", watermark_height, watermark.height)

    return watermark, mask


# Đặt watermark ở các góc
def conner(img, watermark, position="bottom-left", text=0):

    watermark, mask = calculate_size(img, watermark, text=text + 1)

    # Xác định góc dán
    if position == "top" or position == "top-left":
        pos_x = img.width // 30
        pos_y = pos_x
    elif position == "top-right":
        pos_y = img.width // 30
        pos_x = img.width - watermark.width - pos_y

    elif position == "bottom-right":     
        pos_x = img.width - watermark.width - img.width // 30
        pos_y = img.height - watermark.height - img.width // 30
    else:
        pos_x = img.width // 30
        pos_y = img.height - pos_x - watermark.height
    
    # Dán watermark vào ảnh
    img.paste(watermark, (pos_x, pos_y), mask)

    return img

# Đặt watermark tùm lum
def tum_lum(img, watermark):
    # Tính kích cỡ
    watermark, mask = calculate_size(img, watermark)

    # Dàn block, hoạt động như grid, chia ảnh thành các ô nhỏ
    block = img.width // 10

    # Tính khoảng cách giữa các watermark
    space = 2
    gap = space - 1

    # Chèn watermark vào
    i = space
    while (i * block < img.width * 2):
        j = 0
        k = i
        while (j * block < img.height * 2):
            if k * block < img.width or j * block < img.height:
                img.paste(watermark, (j * block, k * block), mask)
            j += 1 + gap
            k -= 1 + gap
        i += 1 + space

    return img

# Watermark khổng lồ
def big_one(img, watermark, size=90):
    # Tính hệ số để tuỳ chỉnh kích thước watermark
    scale = float(size / 100)
    watermark, mask = calculate_size(img, watermark, divide= 8 - 5 - 2*scale)

    # Tính vị trí cần chèn và dán lên ảnh
    pos_x = (img.width - watermark.width) // 2
    pos_y = (img.height - watermark.height) // 2

    img.paste(watermark, (pos_x, pos_y), mask)

    return img