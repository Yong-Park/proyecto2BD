from flask import Flask, render_template, request, url_for, redirect, flash
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
@app.route('/', methods=['GET'])
def mostrar_usuarios():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM usuarios;
        """
    )
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)
#agregar usuarios a la base de datos
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        cur.execute(
            """
            INSERT INTO usuarios (nombre, apellido, email) VALUES ('{0}','{1}','{2}')
            """.format(nombre,apellido,correo)
        )
        conn.commit()
        flash('Usuario agregado exitosamente')
        return redirect(url_for('mostrar_usuarios'))
#se manda al edit.html los valores del que se selecciono
@app.route('/edit/<string:id>', methods=['POST', 'GET'])
def obtener_usuario(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        """
        SELECT * FROM usuarios WHERE id={0}
        """.format(id)
    )
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', usuario = data[0])

#al darle update del edit.html este correra y obtendra los datos y se actualizara
@app.route('/update/<id>', methods=['POST'])
def actualizar_usuario(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['email']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            UPDATE usuarios
            SET nombre = '{0}',
                apellido = '{1}',
                email = '{2}'
            WHERE id = {3}
            """.format(nombre,apellido,correo, id)
        )
        flash('usuario actualizado exitosamente')
        conn.commit()
        return redirect(url_for('mostrar_usuarios'))

#para eliminar
@app.route('/delete/<string:id>', methods =['POST','GET'])
def eliminar_usuario(id):
    print(id)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        """
        DELETE FROM usuarios WHERE id ={0}
        """.format(id)
    )
    conn.commit()
    flash("Usuario elimnado exitosamente")
    return redirect(url_for('mostrar_usuarios'))

@app.route('/registro')
def registrar():
    return render_template('registrar.html')

if __name__ == '__main__':
    app.run(debug=True)