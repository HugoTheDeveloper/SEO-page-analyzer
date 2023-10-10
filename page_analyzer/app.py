from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session


app = Flask(__name__)


@app.get('/')
def start_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/urls', methods=['GET', 'POST'])
def urls_list():
    if request.method == 'POST':

