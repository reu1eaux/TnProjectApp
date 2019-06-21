from flask import Flask, render_template, request, session, redirect
import DataManager

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

data = DataManager.DataManager()



@app.route('/')
def main():
    if 'user_id' not in session:
        return render_template('login.html')
    elif session['user_id'] > 0:
        data.loadUserDataById(session['user_id'])
        data.prepareData()
        return render_template('index.html', data=data)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('family_id', None)
    return redirect('/')

@app.route('/reg', methods=['POST'])
def registration():
    username = request.values.get("username")
    user_name = request.values.get("user_name")
    family_name = request.values.get("family_name")
    password = request.values.get("password")

    if data.checkUsername(username) > 0: return 'Пользователь с логином ' + str(username) + ' уже сущестует!'
    data.addFamily(username, user_name, family_name, password)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.values.get("username")
    password = request.values.get("password")

    if data.checkUsernamAndPassword(username, password) < 1: return 'Пользователь с таким логином и паролем не найден'
    data.loadUserData(username)
    session['user_id'] = data.user.id
    session['family_id'] = data.family.id
    return redirect('/')

@app.route('/addTransaction', methods=['POST'])
def addTransaction():
    type = request.values.get("type")
    amount = request.values.get("amount")
    category = request.values.get("category")
    data.addTransaction(type, amount, category, session['user_id'])
    return redirect('/')

@app.route('/addCategory', methods=['POST'])
def addCategory():
    name = request.values.get("Name")
    data.loadUserDataById(session['user_id'])
    data.addCategory(name, data.user.family_id)
    return redirect('/')

@app.route('/addInFamily', methods=['GET'])
def addInFamily():
    id = request.values.get("id")
    _from = request.values.get("from")
    if 'user_id' in session: return "Ошибка! Вы уже авторизованы"

    data = DataManager.DataManager()
    data.loadUserData(_from)

    if data.user.username is None or data.user.username != _from: return "Ошибка."

    return render_template('reg.html')

@app.route('/regUser', methods=['POST'])
def regUser():
    id = request.values.get("family_id")
    username = request.values.get("username")
    user_name = request.values.get("user_name")
    password = request.values.get("password")
    status = request.values.get("status")
    if data.checkUsername(username) > 0: return 'Пользователь с логином ' + str(username) + ' уже сущестует!'
    data.addUser(username, user_name, password, id, status)
    return redirect('/')

@app.route('/removeCategory', methods=['GET'])
def removeCategory():
    id = request.values.get("id")
    data.removeCategory(id)
    return redirect('/')

@app.route('/changeSafeMode')
def changeSafeMode():
    enable = request.values.get("enable")
    data.updateSafeMode(enable, session['user_id'])
    return redirect('/')

if __name__ == '__main__':
    app.run()
