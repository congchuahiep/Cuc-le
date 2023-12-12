import TextImage, Watermark, timeit



if __name__ == "__main__":
    start = timeit.default_timer()
    img = TextImage.open_image("sample-11.jpg")
    # img = TextImage.add_frame_to_image(img, text="Xin chào!\n Tất cả mọi người", color_name="white", position="bottom", style="surround")    
    img = TextImage.add_text_to_image(img, "Xin chào!", "middle", align="left")
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
    watermark1 = Watermark.text("congchuahiep")
    watermark2 = Watermark.text("congchuahiep", position="bottom-right")
    watermark3 = Watermark.text("congchuahiep", position="top-right")
    watermark4 = Watermark.text("congchuahiep", position="top-left")
    img = Watermark.conner(img, watermark1, text=2)
    img = Watermark.conner(img, watermark2, text=2, position="bottom-right")
    img = Watermark.conner(img, watermark3, text=2, position="top-right")
    img = Watermark.conner(img, watermark4, text=2, position="top-left")


    TextImage.render_picture(img)
    print("Chuỗi đã được thêm vào ảnh. Ảnh mới đã được lưu với tên 'output_image.jpg'.")


    #Your statements here

    stop = timeit.default_timer()

    print('runime: ', stop - start) 