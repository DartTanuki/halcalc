from flask import Flask, render_template, redirect

from data.db_session import global_init
from data.db_session import create_session
from data.users import User

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
global_init('db/task.db')

class RegisterForm(FlaskForm):
    email = EmailField('Login / Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age')
    position = StringField('Position')
    speciality = StringField('Speciality')
    address = StringField('Address')
    submit = SubmitField('Button')


@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = RegisterForm()
    if form.validate_on_submit():
        print('YUP')
        if form.password.data != form.repeat_password.data:
            return render_template('prof.html', form=form, message="Пароли не совпадают!")
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('prof,html', form=form, message='Такой пользователь уже есть!')
        user = User(name=form.name.data, surname=form.surname.data, email=form.email.data,
                    age=form.age.data, position=form.position.data, speciality=form.speciality.data,
                    address=form.address.data, hashed_password=generate_password_hash(form.password.data))
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('prof.html', form=form, message="")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)