from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from validators import url as validate_url
from validators import ValidationError
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/', methods=['GET'])
def start_page():
    messages = get_flashed_messages(with_categories=True)
    if request.method == 'GET':
        return render_template('index.html', messages=messages)


@app.route('/urls', methods=['GET', 'POST'])
def urls_list():
    if request.method == 'POST':
        request_dict = request.form.to_dict()
        url_to_check = request_dict.get('url')
        flash('Указанный url не корректный', 'danger')
        return render_template('index.html', previous_request=url_to_check, messages=messages)



