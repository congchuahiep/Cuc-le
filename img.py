from PIL import Image, ImageDraw, ImageFont

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

    # Tìm thử xem, với kích cỡ của ảnh và kích cỡ font thì một dòng có thể chứa tối đa bao nhiêu từ
    demo_text = 'w'
    max_letter_in_line = 0
    font = ImageFont.truetype("Bungee.ttf", font_size // 3)
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

    font = ImageFont.truetype("Bungee.ttf", font_size)

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

    # Tính toán kích thước khung
    frame_height = img.height // 3
    
    # Sử dụng font mặc định
    font = ImageFont.load_default()
    
    # Chỉnh font lại sau khi đã có kích cỡ mới
    font_size = int(font_size)
    font = ImageFont.truetype("Bungee.ttf", font_size)

    # Vẽ văn bản lên ảnh
    draw.multiline_text((text_len, frame_height // (len(lines) + 1)), text, font=font, fill="white", anchor="ms", spacing=font_size//6, stroke_width=font_size//20, stroke_fill="black", align="center")

    # Lưu ảnh đã chỉnh sửa
    img.save("output_image.jpg")              
    

if __name__ == "__main__":

    add_text_to_image("sample-11.jpg", "Xin chào!\n Tất cả mọi người, lại là mình đâyyyy mình hôm nay rất vui")
    # Xin chào! Tất cả mọi người
    # TTTTT
    # Xin chào!TTTTTTTTTTTTTTTTTT TT
    # Xin chào!\n Tất cả mọi người, lại là mình đâyyyy mình hôm nay rất vui

    print("Chuỗi đã được thêm vào ảnh. Ảnh mới đã được lưu với tên 'output_image.jpg'.")
