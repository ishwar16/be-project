import random
import string
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import measure_object_size as mOs
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'Uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg'}

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_random_string(length):
   # choose from all lowercase letter
   letters = string.ascii_lowercase
   result_str = ''.join(random.choice(letters) for i in range(length))
   print("Random string of length", length, "is:", result_str)
   return result_str

def processIMG():
   print(IMG_1, IMG_2)
   mOs.proccessIMG(IMG_1)
   mOs.proccessIMG(IMG_2)
   return mOs.volumeCalculation()

@app.route('/home')
def mainPage():
   return render_template("index.html")

@app.route('/home', methods=['POST','GET'])
def index():
   if request.method == 'POST':
      # check if the post request has the file part
      print(request.files)
      if 'files[]' not in request.files:
         print('No file part')
         return redirect(request.url)
      files = request.files.getlist('files[]')
      r = get_random_string(7)
      i = 0
      for file in files:
         print(file.filename)
         if i == 0:
            name = r + "_SV.jpg"
            global IMG_1
            IMG_1 = name
         else:
            name = r + "_TV.jpg"
            global IMG_2
            IMG_2 = name
         file.filename = name
         i = i + 1
         if file and allowed_file(file.filename):
            print(os.path.join(app.config['UPLOAD_FOLDER']))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
      print('File(s) successfully uploaded')
      print(IMG_1, IMG_2)
      x = processIMG()
      print(x)
      return render_template('index.html', param1=IMG_1, param2=IMG_2, vol=x)
   return render_template('index.html')

@app.route('/display')
def display_image():
   param1 = request.args.get('param1')
   param2 = request.args.get('param2')
   vol = request.args.get('vol')
   return redirect(request.url)

# @app.route('/display/<obj>')
# def display_image(file):
# 	return redirect(url_for('static', filename = '/Uploads/' + filename), code=301)

app.run(debug=True, host="192.168.188.51", port=8888)