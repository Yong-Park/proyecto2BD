from flask import Flask, render_template

app = Flask(__name__)

@app.route('/registrar')
def registrar():
    return render_template('registrar.html')

if __name__ == '__main__':
    app.run(debug=True)