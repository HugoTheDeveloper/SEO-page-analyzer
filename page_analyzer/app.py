from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, session
from validators import url as validate_url
from dotenv import load_dotenv
import os
from .database_manager import DbManager
from urllib.parse import urlparse
import requests


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


db = DbManager()


@app.route('/', methods=['GET'])
def start_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template('start_page.html', messages=messages)


@app.route('/urls', methods=['GET', 'POST'])
def urls_list():
    if request.method == 'POST':
        url_to_check = request.form.get('url')
        parsed_url = urlparse(url_to_check)
        normalized_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
        if not validate_url(normalized_url):
            flash('Указанный url не корректный!', 'danger')
            return redirect(url_for('start_page'))
        if db.is_url_in_bd(normalized_url):
            flash('Страница указанного url уже существует', 'warning')
            url_id = db.get_id_from_url(normalized_url)
            return redirect(url_for('get_urls_checks_list', id=url_id)), 302
        url = db.insert_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_urls_checks_list', id=url.id)), 302
    if request.method == 'GET':
        messages = get_flashed_messages(with_categories=True)
        all_saved_urls = db.get_urls_list()
        return render_template('urls_list.html', messages=messages,
                               urls=all_saved_urls)


@app.route('/urls/<int:id>', methods=['GET'])
def get_urls_checks_list(id):
    messages = get_flashed_messages(with_categories= True)
    flag = db.is_url_id_in_bd(id)
    if not flag:
        flash('Запрашиваемая страница не найдена', 'warning')
        return redirect(url_for('start_page')), 404
    url_info = db.get_url_from_urls_list(id)
    checks_list = db.get_url_from_urls_checks_list(id)
    return render_template('urls_checks_list.html', messages=messages,
                           url=url_info, checks_list=checks_list)


@app.route('/urls/<int:id>/check', methods=['POST'])
def check_url(id):
    if not db.is_url_id_in_bd(id):
        flash('Запрашиваемая страница не найдена', 'warning')
        return redirect(url_for('start_page')), 404
    url = db.get_url_from_urls_list(id).name
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_urls_checks_list', id=id)), 400

    db.insert_url_check(id, response.status_code)
    flash('Страница успешно проверена!', 'success')
    return redirect(url_for('get_urls_checks_list', id=id))
