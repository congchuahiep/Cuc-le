import TextImage

if __name__ == "__main__":

    img = TextImage.open_image("sample-11.jpg")
    img = TextImage.add_frame_to_image(img, text="Xin chào!\n Tất cả mọi người", color_name="white", position="bottom", style="surround")    
    # img = add_text_to_image(img, "Xin chào!", "top")
    # img = TextImage.add_text_to_image(img, "Xin chào!\n Tất cả mọi người,", "bottom")
    # img = add_text_to_image(img, "\nXin chào! Tất cả mọi người, lại là mình đâyyyy mình hôm nay rất vui", "top")
    # img = add_text_to_image(img, "Xin chào!\n Tất cả mọi người, lại là mình đâyyyy mình hôm nay rất vui", "bottom")
    # Xin chào! Tất cả mọi người
    # TTTTT
    # Xin chào!TTTTTTTTTTTTTTTTTT TT
    # Xin chào!\n Tất cả mọi người, lại là mình đâyyyy mình hôm nay rất vui

    TextImage.render_picture(img)
    print("Chuỗi đã được thêm vào ảnh. Ảnh mới đã được lưu với tên 'output_image.jpg'.")