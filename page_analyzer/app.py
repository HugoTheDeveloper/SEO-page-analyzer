from flask import (Flask, render_template, request, redirect,
                   url_for, flash, get_flashed_messages)
from validators import url as validate_url
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import requests
from .tools import HTMLParser
from .database_manager import DbManager


load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


db = DbManager()


@app.route('/', methods=['GET'])
def start_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template('start_page.html', messages=messages)


@app.post('/urls')
def post_url():
    url_to_check = request.form.get('url')
    parsed_url = urlparse(url_to_check)
    normalized_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    if not validate_url(normalized_url):
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('start_page.html', messages=messages), 422
    if db.is_url_in_bd(normalized_url):
        flash('Страница уже существует', 'warning')
        url_id = db.get_id_from_url(normalized_url)
        return redirect(url_for('get_urls_checks_list', id=url_id))
    url = db.insert_url(normalized_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_urls_checks_list', id=url.id))


@app.get('/urls')
def get_urls_list():
    messages = get_flashed_messages(with_categories=True)
    all_saved_urls = db.get_urls_list()
    return render_template('urls_list.html', messages=messages,
                           urls=all_saved_urls)


@app.route('/urls/<int:id>', methods=['GET'])
def get_urls_checks_list(id):
    messages = get_flashed_messages(with_categories=True)
    url = db.get_url_from_urls_list(id)
    if not url:
        flash('Запрашиваемая страница не найдена', 'warning')
        return redirect(url_for('start_page'), 404)
    checks_list = db.get_url_from_urls_checks_list(id)
    return render_template('urls_checks_list.html', messages=messages,
                           url=url, checks_list=checks_list)


@app.route('/urls/<int:id>/check', methods=['POST'])
def check_url(id):
    url = db.get_url_from_urls_list(id).name
    if not url:
        flash('Запрашиваемая страница не найдена', 'warning')
        return redirect(url_for('start_page'), 404)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_urls_checks_list', id=id, code=400))

    responses_html = response.content
    soup = HTMLParser(responses_html)
    check = soup.check()
    full_check = check | {'url_id': id, 'response': response.status_code}

    db.insert_url_check(full_check)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_urls_checks_list', id=id))
