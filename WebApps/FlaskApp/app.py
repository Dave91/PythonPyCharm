from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash


app = Flask(__name__)
mysql = MySQL()

with open("dbcon.txt") as dbcon:
    dbconf = [{i: line.strip()} for i, line in enumerate(dbcon.readlines())]
dbcon.close()

app.config['MYSQL_DATABASE_USER'] = dbconf[0]
app.config['MYSQL_DATABASE_PASSWORD'] = dbconf[1]
app.config['MYSQL_DATABASE_DB'] = dbconf[2]
app.config['MYSQL_DATABASE_HOST'] = dbconf[3]
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    # render_template külön html lap??
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _name and _email and _password:
        # külön lapra iratni?? print('All fields are OK !')
        _hashed_password = generate_password_hash(_password)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message': 'User created successfully !'})
        else:
            return json.dumps({'error': str(data[0])})
    else:
        return json.dumps({'html': '<span>Error: Empty fields !!</span>'})


if __name__ == '__main__':
    app.run()
