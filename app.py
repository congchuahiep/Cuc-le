from flask import Flask, redirect, render_template, request, url_for, jsonify, session, send_from_directory, send_file
from flask_session import Session
import secrets
import main
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

# EXPORT_FOLDER = 'static/images/exports'
# app.config['DOWNLOAD_FOLDER'] = EXPORT_FOLDER

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Dùng để lưu trữ ánh xạ giữa token và đường dẫn ảnh
image_token_mapping = {}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.after_request
def after_request(response):
    """Ensure responses aren"t cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    session["file_path"] = ""
    session["user_token"] = ""
    session["watermark"] = ""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" in request.files:
        file = request.files["file"]
        # Lưu trữ file ở nơi bạn muốn (ví dụ: thư mục "uploads")
        file_path = os.path.join(file.filename)
        file.save("uploads/" + file_path)
        session["file_path"] = file_path
        return "Upload successful"
    return "No file provided", 400

@app.route("/upload_watermark", methods=["POST"])
def upload_watermark():
    if "file" in request.files:
        file = request.files["file"]
        # Lưu trữ file ở nơi bạn muốn (ví dụ: thư mục "uploads")
        watermark_image = os.path.join(file.filename)
        file.save("uploads/watermarks/" + watermark_image)
        session["watermark"] = watermark_image
        return "Upload successful"
    return "No file provided", 400

@app.route("/cancel_watermark", methods=["POST"])
def cancel_watermark():
    session["watermark"] = ""
    return jsonify({"cancel_watermark": "success"})

@app.route("/update_data", methods=["POST"])
def update_data():
    if request.method == "POST":
        # Lấy dữ liệu từ request
        file_path = session.get("file_path")
        watermark_image = session.get("watermark")
        data = request.get_json()

        # Xử lý dữ liệu
        main.edit_photo(img=file_path, text_top=data["top"], 
                        text_middle=data["middle"],
                        text_bottom=data["bottom"], 
                        frame=data["frame"], 
                        watermark_img=watermark_image,
                        watermark_text=data["watermark"], 
                        watermark_type=data["watermarkFrame"],
                        watermark_pos=data["watermarkPos"])
        
        # Tạo mã khoá bảo mật dữ liệu nhận
        token = secrets.token_urlsafe(16)
        session['user_token'] = token
        image_token_mapping[token] = f'static/images/exports/{file_path}'
        data = {'token': token}

        # Trả về phản hồi
        return jsonify(data)
    
# Kiểm tra độ tin cậy truy cập file
@app.route('/static/images/exports/<path:filename>')
def check_image(filename):
    # Kiểm tra xem token có trong session không
    if 'user_token' in session:
        user_token = session['user_token']
        
        # Lấy đường dẫn ảnh từ ánh xạ
        image_path = image_token_mapping.get(user_token)
        
        # [Lưu ý] cho việc phát triển sau này
        #   Có thể thấy là filename chưa được sử dụng vì lười
        #   kiểm tra file name và token, mà thay vào đó là lấy
        #   token đang có của user ra (khi lấy được token của
        #   user thì sẽ lấy được đường dẫn ảnh) và xuất ảnh luôn

        # Kiểm tra tính hợp lệ của đường dẫn ảnh
        if image_path:
            return send_file(image_path, as_attachment=True)
    
    return 'Unauthorized'

@app.route('/edit/', methods=['GET'])
def edit():
    data = {
        "img": request.args.get('img'),
        "top": request.args.get('top'),
        "middle": request.args.get('mid'),
        "bottom": request.args.get('bot'),
        "frame": request.args.get('fr'),
        "watermark": request.args.get('wtk'),
        "watermarkText": request.args.get('wtt'),
        "watermarkFrame": request.args.get('wtkf'),
        "watermarkPos": request.args.get('wtkp'),
    }


    print(data)
    # Xử lý dữ liệu
    image_filename = main.edit_photo_url(img=data["img"], text_top=data["top"], 
                    text_middle=data["middle"],
                    text_bottom=data["bottom"], 
                    frame=data["frame"], 
                    watermark_img=data["watermark"],
                    watermark_text=data["watermarkText"], 
                    watermark_type=data["watermarkFrame"],
                    watermark_pos=data["watermarkPos"])
    
    print("image_filename server:", image_filename)
    image_url = url_for('static', filename=f"edits/{image_filename}")

    return send_file(f"static/edits/{image_filename}")


@app.route('/download')
def download():
    # Trả về file từ thư mục UPLOAD_FOLDER
    file_path = session.get("file_path")
    if file_path == "":
        return redirect("/")
    return send_file("static/images/exports/" + file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)