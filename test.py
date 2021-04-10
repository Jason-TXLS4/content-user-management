#Basic Flask application

from flask import Flask
app=Flask(__name__)

@app.route('/')
def index():
  return '<h1>Learning Flask</h1>'

@app.route('/user/<name>')
def user(name):
  return 'Hello, %s' % format(name)
