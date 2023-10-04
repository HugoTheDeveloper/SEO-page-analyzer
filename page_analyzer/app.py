from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    messages = get_flashed_messages(with_categories=True)
    if request.method == 'GET':
        return render_template('index.html')
