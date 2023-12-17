import TextImage, Watermark, timeit

def edit_photo(img, text_top="", text_middle="", text_bottom="", frame ="None", watermark_text="", watermark_img="", watermark_type="", watermark_pos=""):
    start = timeit.default_timer()
    name = img
    img = TextImage.open_image(f"uploads/{img}")
    
    # Xét từng điều kiện Frame
    # Vì để đỡ tốn thời gian chạy nhất, ta nhét chúng trong các
    #   điều kiện if/else, tránh chạy các hàm không xử lí thông tin
    #   gì khi thông tin đó rỗng
    # Nếu frame là add (thêm khoảng trắng trống để điền chữ)
    if frame == "add":
        if text_top != "":
            img = TextImage.add_frame_to_image(img, position="top", text=text_top, style="add")
        if text_bottom != "":
            img = TextImage.add_frame_to_image(img, position="bottom", text=text_bottom, style="add")

    # Nếu frame là surround (bao quanh như portfolio)
    elif frame == "surround":
        if text_top != "":
            img = TextImage.add_frame_to_image(img, position="top", text=text_top, style="surround")
        if text_bottom != "":
            img = TextImage.add_frame_to_image(img, position="bottom", text=text_bottom, style="surround")
        if text_top == "" and text_bottom == "":
            img = TextImage.add_frame_to_image(img, position="None", text="", style="surround")
        
    # Nếu frame là what? (như cái meme)
    elif frame == "what":
        img = TextImage.add_frame_to_image(img, position="bottom", text=text_bottom, style="what")
    # Nếu không có Frame
    else:
        if text_top != "":
            img = TextImage.add_text_to_image(img, text_top, "top")
        if text_middle != "":
            img = TextImage.add_text_to_image(img, text_middle, "middle")
        if text_bottom != "":
            img = TextImage.add_text_to_image(img, text_bottom, "bottom")

    # Xử lí Watermark
    if watermark_img != "" or watermark_text != "":
        if watermark_img != "":
            watermark = Watermark.add(watermark_path="uploads/watermarks/" + watermark_img)
        elif watermark_text != "":
            watermark = Watermark.text(text=watermark_text)
        if watermark_type == "tum lum":
            img = Watermark.tum_lum(img, watermark)
        elif watermark_type == "big one":
            img = Watermark.big_one(img, watermark=watermark)
        else:
            img = Watermark.conner(img, watermark=watermark, position=watermark_pos)

    
    # img = TextImage.add_text_to_image(img, "Xin chào!\n Tất cả mọi người,", "top")
    # img = add_text_to_image(img, "\nXin chào! Tất cả mọi người, lại là mình đâyyyy mình hôm nay rất vui", "top")
    # img = add_text_to_image(img, "Xin chào!\n Tất cả mọi người, lại là mình đâyyyy mình hôm nay rất vui", "bottom")
    # Xin chào! Tất cả mọi người
    # TTTTT
    # Xin chào!TTTTTTTTTTTTTTTTTT TT
    # Xin chào!\n Tất cả mọi người, lại là mình đâyyyy mình hôm nay rất vui
    # watermark = Watermark.add("watermark.png")
    # watermark = Watermark.text("congchuahiep")
    # img = Watermark.tum_lum(img, watermark)

    # Nếu Watermark là chữ
    # watermark1 = Watermark.text("congchuahiep")
    # watermark2 = Watermark.text("congchuahiep", position="bottom-right")
    # watermark3 = Watermark.text("congchuahiep", position="top-right")
    # watermark4 = Watermark.text("congchuahiep", position="top-left")
    # img = Watermark.conner(img, watermark1, text=2)
    # img = Watermark.conner(img, watermark2, text=2, position="bottom-right")
    # img = Watermark.conner(img, watermark3, text=2, position="top-right")
    # img = Watermark.conner(img, watermark4, text=2, position="top-left")


    TextImage.render_picture(img, name)
    print("Chuỗi đã được thêm vào ảnh. Ảnh mới đã được lưu với tên 'output_image.jpg'.")





    stop = timeit.default_timer()

    print('runime: ', stop - start) 

# [For Testing]
# test = TextImage.open_image("uploads/sample-11.jpg")
# test = TextImage.add_text_to_image(test, "Xin chào tất cả các bạn quá bạn iu quá giàu", "top")
# test = TextImage.add_frame_to_image(test, position="bottom", text="Chữ này nằm bên dưới", style="surround")
# TextImage.render_picture(test, "testing.jpg")