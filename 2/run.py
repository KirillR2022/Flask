from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        response = make_response(redirect(url_for('welcome')))
        response.set_cookie('username', name)
        return response
    return render_template('index.html')


# Страница приветствия
@app.route('/welcome')
def welcome():
    username = request.cookies.get('username')
    if username:
        return render_template('welcome.html', username=username)
    else:
        return redirect(url_for('index'))


# Обработка выхода
@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('username', '', expires=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)
