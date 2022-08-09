from flask import Flask, render_template, request, redirect, url_for
import os
import requests
from datetime import datetime, timedelta
from random import randint
# from app.dateForm import DateForm

app = Flask(__name__)
SECRET_KEY = os.urandom(32)

@app.route('/')
def index():
    today = datetime.now()
    return redirect(f"/dailyImage/{today.year}/{today.month}/{today.day}")

@app.route('/dailyImage/<year>/<month>/<day>')
def daily_image(year, month, day):
    str(month).zfill(2)
    str(day).zfill(2)

    response = requests.get(f"https://api.nasa.gov/planetary/apod?date={year}-{month}-{day}&api_key={os.getenv('API_KEY')}")

    print(response)

    if response.status_code != 200:
        return redirect(url_for('error_page', status_code=response.status_code))

    responseBody = response.json()
    # form = DateForm(request.form)

    if "media_type" in responseBody.keys() and responseBody["media_type"] == 'video':
        current_page_date = datetime(int(year), int(month), int(day))
        yesterday = current_page_date - timedelta(days = 1)

        return redirect(url_for('daily_image', year=yesterday.year, month=yesterday.month, day=yesterday.day))

    return render_template('dailyImage.html', daily_image=responseBody)

@app.route('/dailyImage/random')
def random_daily_image():
    earliest_image_date = datetime(1995, 6, 16)
    today = datetime.now()
    date_delta = today - earliest_image_date

    random_date = earliest_image_date + timedelta(days = randint(0, date_delta.days))
    
    return redirect(url_for('daily_image', year=random_date.year, month=random_date.month, day=random_date.day))

@app.route('/mars')
def mars():
    return render_template('mars.html')

@app.route('/error/<status_code>')
def error_page(status_code):
    return render_template('errorPage.html', status_code=status_code)