from flask import Flask
app = Flask(__name__)

@app.route('/hola')
def hola():
    return 'hola mundo jejeje'

if __name__=='__main__':
    app.run(debug = True)