from flask import render_template, redirect, url_for, make_response, request, session
from database import checkmail, add_user, checklogin, make_todo, check_id, todo_list
from uuid import uuid1
from app import app

session = {}


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/registry', methods=['GET', 'POST'])
def registry():
    if request.method == 'GET':
        return render_template('registry.html')

    elif request.method == 'POST':
        if not checkmail(request.form['email']):
            add_user(request.form.get('name'),
                     request.form.get('email'),
                     request.form.get('password'))
            return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':  # renderiza login.html se nao estiver logado
        return redirect(url_for('todo'))\
            if request.cookies.get('id_sessao')\
            else render_template('login.html')

    elif request.method == 'POST':  # checa login retorna todo.html se verdadeiro
        if not checklogin(request.form['email'], request.form['password']):
            return redirect('login.html')
        else:  # cria sessao se login verdadeiro
            id_sessao = str(uuid1())
            session[id_sessao] = request.form['email']
            response = make_response(redirect(url_for('todo')))
            response.set_cookie('id_sessao', id_sessao)
            return response


@app.route('/logout')
def logout():
    session.pop(request.cookies.get('id_sessao'), None)
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('id_sessao')
    return resp


@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'GET':
        return render_template('todo.html') \
            if request.cookies.get('id_sessao') \
            else redirect(url_for('login'))

    elif request.method == 'POST':
        make_todo(request.form['desc'], 
        check_id(session))
        return redirect(url_for('todolist'))


@app.route('/todolist')
def todolist():
    todos = todo_list(check_id(session))
    return render_template('todolist.html', lista=todos) \
        if request.cookies.get('id_sessao') \
        else redirect(url_for('login'))
