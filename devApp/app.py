from flask import Flask, render_template
import psycopg2 #pip install psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

conn = psycopg2.connect(
    database ="cpjklpze",
    user = "cpjklpze",
    password = "PbGV_JLGulr8ftaX3luPjvUZbk7q9nOI",
    host = "raja.db.elephantsql.com",
    port = "5432"
)


#pagina defaul que mostrara al correr
@app.route('/')
def registrar():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = """
    SELECT * FROM usuarios;
    """
    cur.execute(s)
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)

if __name__ == '__main__':
    app.run(debug=True)