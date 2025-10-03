from PIL import Image
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.loginform import LoginForm
from data.registerform import RegisterForm
from data.users import User

import requests

import urllib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    print(user_id)
    return db_sess.query(User).get({'id': user_id})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    # p = requests.get('')
    # out = open('static/img/.png', 'wb')
    # out.write(p.content)
    # out.close()
    session = db_session.create_session()
    for user in session.query(User).all():
        print(user.id, 1)
    users = session.query(User).all()
    names = {name.id: (name.name) for name in users}
    return render_template('start.html', names=names)


@app.route('/world')
def world():
    return render_template('world.html')


@app.route('/edem')
def edem():
    return render_template('edem.html')


@app.route('/hell')
def hell():
    return render_template('hell.html')


@app.route('/hist')
def hist():
    return render_template('hist.html')


@app.route('/earth')
def earth():
    m = ['30.314997,59.938784,vkbkm', '95.270118,73.282112,vkbkm', '144.158095,63.988118,vkbkm',
         '-70.203879,-6.370066,vkbkm', '-122.235129,73.023610,vkbkm', '123.858621,-27.540349,vkbkm',
         '31.219977,29.980068,vkbkm', "138.634851,35.461570,vkbkm", "94.028448,35.819696,vkbkm",
        "-85.687854,46.387159,vkbkm", "-36.214257,80.302533,vkbkm", "140.665648,75.651605,vkbkm"]
    map_request = (
        f"https://static-maps.yandex.ru/1.x/?ll=90.0,90.0&z=0&size=600,450&bbox=0.0,83.0~82.0,0.0&pt={'~'.join(m)}&l=map")
    response = requests.get(map_request)
    map_file = "static/img/map.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)
    mpf = Image.open("static/img/map.jpg")
    mp = mpf.crop((0, 100, 525, 450))
    mp.save("static/img/map.png")
    return render_template('earth.html')


@app.route('/fantom')
def fantom():
    return render_template('fantom.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)  # form.remember_me.data)
            print('qwertyui')
            return redirect('/')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['POST', 'GET'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            read=''
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/promo')
def promo():
    return render_template('promo.html')
  
  
@app.route('/face')
def face():
    return render_template('face.html')

  
@app.route('/zodi')
def zodi():
    return render_template('zodi.html')
  
  
@app.route('/dr')
def dr():
    return render_template('dr.html')
  
  
@app.route('/drz')
def drz():
    return render_template('drz.html')
  
  
@app.route('/histn')
def histn():
    return render_template('histn.html')
  
  
@app.route('/histz')
def histz():
    return render_template('histz.html')
  
  
@app.route('/mirz')
def mirz():
    return render_template('mirz.html')
  
  
@app.route('/nimf')
def nimf():
    return render_template('nimf.html')
  
  
@app.route('/drn')
def drn():
    return render_template('drn.html')
  

def main():
    db_session.global_init("db/users.db")
    app.run()


if __name__ == '__main__':
    main()
