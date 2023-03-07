from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import pandas
from fileinput import filename
import json

views = Blueprint('views', __name__)

user = current_user

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(file.filename)
    data = pandas.read_excel(file)
    return data.to_html()
    return render_template('upload.html', data=data, user=current_user)





