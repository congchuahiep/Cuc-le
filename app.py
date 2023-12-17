from flask import Flask, flash, redirect, render_template, request, url_for, jsonify, session
from flask_session import Session
import main
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

pictures = []

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

        # Trả về phản hồi
        return jsonify({"update_data": "success"})

@app.route("/cleanup", methods=["POST"])
def cleanup():
    # Xử lý yêu cầu cleanup ở đây
    data = request.get_json()
    action = data.get('action')
    print("Dong 1")
    if action == 'cleanup':
        # Thực hiện các hành động cleanup ở đây
        if 'file_path' in session:
            print("Dong 2")
            file_path = session.pop('file_path')
            os.remove("uploads/" + file_path)        
        print('Performing cleanup actions')

    return jsonify({'status': 'success'})

if __name__ == "__main__":
    app.run(debug=True)