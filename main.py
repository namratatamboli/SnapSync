from flask import Flask, render_template, request
import uuid, os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        print(request.files.keys())
        rec_id = request.form.get("uuid")#collects uuid
        desc = request.form.get("text")#collects text
        input_files = []
        for key, value in request.files.items():
            print(key, value)
            # upload the file
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                if(not(os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], rec_id,)))):
                    os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], rec_id,))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, filename))
                input_files.append(file.filename)
            # capture the description and save it to the file
            with open(os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "desc.txt"), "w") as f:
                f.write(desc)
        input_txt_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id, "input.txt")
        with open(input_txt_path, "w") as f:
            for i, fl in enumerate(input_files):
                f.write(f"file '{fl}'\n")
                if i != len(input_files) - 1:
                    f.write("duration 2\n")




    return render_template("create.html", myid=myid)

@app.route("/gallery")
def gallery():
    reels = [
        reel for reel in os.listdir("static/reels")
        if reel.endswith(".mp4")
    ]
    return render_template("gallery.html", reels=reels)

app.run(debug=True)