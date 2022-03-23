from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def hello_world():
    return '<h1>Hello world but bigger</h1>'


@app.route('/about/<username>')
def about_page(username):
    return f'<h1>This is the about page of {username}</h1>'


if __name__ == '__main__':
    app.run()
