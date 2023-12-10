from PIL import Image, ImageDraw, ImageFont

def font_factor(init_font, text_count, max_text_count):
    max = init_font // 2
    x = text_count - max_text_count
    
    factor = 0
    i = 0

    for j in range(x):
        factor += (init_font - pow(2, i)) // pow(2, i)
        print((init_font - pow(2, i)) // pow(2, i))
        if j % 2 == 0 or j == 0:
            i += 1
    
    return factor

def add_text_to_image(image_path, text):

    # Mở ảnh            
    img = Image.open(image_path)
    
    # Tính độ dài chữ
    text_len = img.width / 2
    text_count = len(text)

    # Tạo đối tượng vẽ và font
    draw = ImageDraw.Draw(img)
    if img.width < img.height:
        font_size = img.width // 6.75
    else:
        font_size = img.height // 6.75
    origin_font = font_size

    print(font_size)
    
    print(text_count)

    # Tìm dòng dài nhất trong chuỗi để làm mẫu tham chiếu cho các dòng khác
    lines = text.split('\n')
    print(lines)

    longest = max(filter(lambda line: len(line) > 0, lines), key=len)
    print(longest)


    # Xác định độ dài của chuỗi khi chúng đến giới hạn viền của ảnh
    font = ImageFont.truetype("Bungee.ttf", font_size)
    max_text_count = 0
    if draw.textlength(longest, font) > img.width:
        while draw.textlength(longest[:max_text_count], font) < img.width:
            max_text_count += 1
        max_text_count -= 1
        max_width = draw.textlength(longest[:max_text_count], font)
    else:
        max_text_count = text_count
        max_width = draw.textlength(longest, font)
    
    text_box = draw.textbbox((0, 0), text, font)

    # Kích thước của văn bản
    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]
    print("width: ", text_width)
    print("height: ", text_height)
    print(max_text_count)
    print(max_width)

    # Xác định kích cỡ font chữ khi càng nhiều chữ, chiều dài càng tăng
    ratio = 1
    if max_text_count < text_count:
        ratio = max_width / draw.textlength(longest, font)
        font_size = int(font_size * ratio)

    # Tính toán kích thước khung
    frame_height = img.height // 3
    frame_width = img.width
    
    # Sử dụng font mặc định
    font = ImageFont.load_default()
    
    # Chỉnh font
    font = ImageFont.truetype("Bungee.ttf", font_size)
    text_length = draw.textlength(longest, font)

    print(text_length)

    # Xác định box vẽ
    text_left, text_top = draw.textbbox((0, 0), text, font)[:2]

    print(text_left)
    print(text_top)
    print(font_size)
    
    # Tính toán vị trí của khung
    frame_x = 0
    frame_y = 0

    # Vẽ khung
    draw.rectangle([frame_x, frame_y, frame_x + frame_width, frame_y + frame_height], outline="red", width=2)

    # Xác định vị trí của chữ khi có nhiều dòng
    text_height_pos_factor = 0
    for i in range(1, len(lines) + 1):
        text_height_pos_factor += 1.5 / i

    # Xác định vị trí của chữ khi chữ nhỏ
    text_height_pos_factor += origin_font/font_size - 1
    print(text_height_pos_factor)

    # Nếu có nhiều dòng chữ sẽ nhỏ thêm
    for i in range(1, len(lines)):
        font_size -= int(40 * ratio)
        print("Giảm: ", font_size)

    font = ImageFont.truetype("Bungee.ttf", font_size)

    # Vẽ văn bản lên ảnh
    draw.multiline_text((text_len, frame_height // text_height_pos_factor), text, font=font, fill="white", anchor="ms", spacing=0, stroke_width=10, stroke_fill="black", align="center")
    
    # Lưu ảnh đã chỉnh sửa
    img.save("output_image.jpg")              
    

if __name__ == "__main__":

    add_text_to_image("sample.jpg", "Xin chào!TTTTTTTT\nTTTTTAbc123123123\n9128AAAAAAAAAA")
    # Xin chào! Tất cả mọi người"

    print("Chuỗi đã được thêm vào ảnh. Ảnh mới đã được lưu với tên 'output_image.jpg'.")
