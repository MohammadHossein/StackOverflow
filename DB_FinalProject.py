from flask import Flask
from flask.globals import request
from flask.templating import render_template
from pymongo.mongo_client import MongoClient

app = Flask(__name__)

db = MongoClient('localhost', 27017).FinallDB


@app.route('/')
def loginPage():
    return render_template('gui.html', massage='')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = db.users.find({'username': request.values['username']})
        for u in user:
            if 'password' in u.keys():
                if u['password'] == request.values['password']:
                    return render_template('login.html', username=request.values['username'])
                else:
                    return render_template('gui.html', massage='incorrect password')
            else:
                return render_template('gui.html', massage='unknown username')
        return render_template('gui.html', massage='unknown username')

    else:
        return render_template('gui.html', massage='')


@app.route('/sign-up')
def signUpPage():
    return render_template('SignUP.html')


@app.route('/signup', methods=['POST', 'GET'])
def signUP():
    if request.method == 'POST':
        try:
            user = db.users.find({'username': request.values['username']})
            for u in user:
                return render_template('SignUP.html', massage='username already taken!')
            user = db.users.find({'email': request.values['email']})
            for u in user:
                return render_template('SignUP.html', massage='email already taken!')
            user = {'name': request.values['Name'], 'password': request.values['Password'],
                    'username': request.values['username'], 'email': request.values['email'],
                    'favorites': request.values.getlist('favorite')}

            db.users.insert(user)

        except Exception as e:
            print(e)
    else:
        return render_template('SignUP.html')

    return render_template('gui.html')


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 5000)
