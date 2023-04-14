from flask import Flask, render_template

from data.db_session import global_init
from data.db_session import create_session
from data.users import User
from data.work import Jobs


app = Flask(__name__)


@app.route('/')
def main_page():
    global_init('db/task.db')
    db_sess = create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('prof.html', jobs=jobs)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)