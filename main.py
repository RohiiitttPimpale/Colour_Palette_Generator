import numpy as np
from flask import Flask, render_template,url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import SubmitField,FileField
from wtforms.validators import DataRequired
from PIL import Image
import os

class UploadForm(FlaskForm):
    image = FileField(label="Upload Image", validators=[DataRequired()])
    submit = SubmitField(label="submit")


app = Flask(__name__)
bootstrap = Bootstrap5(app=app)

app.secret_key = os.environ.get("FLASK_KEY")
app.config['UPLOAD_FOLDER'] = 'static/image'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@app.route("/",methods=["GET","POST"])
def home():
    folder_path = "static/image"
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    my_form = UploadForm()
    if my_form.validate_on_submit():
        img = my_form.image.data
        img.save(os.path.join(app.config["UPLOAD_FOLDER"],img.filename))
        return redirect(url_for("colour", name=img.filename))
    return render_template("home.html",form = my_form)

@app.route("/generator_colour_palette/<name>")
def colour(name):
    image = Image.open(f"static/image/{name}")
    image = image.convert("RGB")
    image_array = np.array(image)

    pixels = image_array.reshape(-1, image_array.shape[-1])
    unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
    sort_id = np.flip(np.argsort(counts))
    top_10 = []
    for i in range(0,100,10):
        col = unique_colors[sort_id][i]
        lis = []
        for ele in col:
            lis.append(int(ele))
        top_10.append(tuple(lis))

    return render_template("colour.html",image=name,top_10=top_10)

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
