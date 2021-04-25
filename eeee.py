from data import db_session
from flask import Flask, render_template, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('db/users_data.db')
app.run()