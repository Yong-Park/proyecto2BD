from flask import Flask, render_template, request, url_for, redirect, flash, session
import psycopg2 #pip install psycopg2
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash, check_password_hash

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
    return render_template('editar_usuarios.html', list_users = list_users)

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

#para crear una nueva cuenta para ingresar
@app.route('/registro', methods=['GET','POST'])
def registrar():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # resvisar que fuera por funcion de post, que exista nombre_usuario la contrasena y el correo
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # variables que reciben los textos que se llenaron en registrar.html
        nombre_completo = request.form['nombre_completo']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        #hashea la contrasena
        _hashed_password = generate_password_hash(password)
        
        #revisar si la cuenta ya existe en la base de datos de cuentas
        cur.execute(
            """
            SELECT * FROM cuentas WHERE nombre_usuario = '{0}'
            """.format(username)
        )
        account = cur.fetchone()
        print(account)
        #si la cuenta mostrar error y chequeo de validaciones de otras
        if account:
            flash('La cuenta ya existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Email invalido!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('User Name solo debe de contener letras o numeros!')
        elif not username or not password or not email:
            flash('Porfavor llene las casillas!')
        else:
            # La cuenta no existe y todo esta bien entoces se ingresa a la base de datos
            cur.execute(
                """
                INSERT INTO cuentas (nombre, nombre_usuario, password, email) VALUES ('{0}','{1}','{2}','{3}')
                """.format(nombre_completo, username, _hashed_password, email)
                )
            conn.commit()
            flash('Te has registrado exitosamente!')
    elif request.method == 'POST':
        # los datos estan vacios y solo se realizo la funcion de post
        flash('Porfavor llene las casillas!')
    # mostrar este mensaje en caso que no esten llenas las casillas
    
    return render_template('/ingreso/registrar.html')

#para el login de un usuario existente
@app.route('/login/', methods=['GET', 'POST'])
def login():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # revisar si el username y la contrasena estan al darle post
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print("password ingresado ahorita en login: "+ str(password))

        #revisar si la el username existe en la base de datos
        cur.execute(
            """
            SELECT * FROM cuentas WHERE nombre_usuario = '{0}'
            """.format(username)
        )
        #fetch solo un dato
        account = cur.fetchone()
        print(account)

        if account:
            password_rs = account['password']
            print(password_rs)
            # si la cuenta existe
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['nombre_usuario']
                # redireccionar al homepage
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('username/contraseña Incorrecta')
        else:
            # Account doesnt exist or username/password incorrect
            flash('username/contraseña Incorrecta')

    return render_template('/ingreso/login.html')

#pantalla de home que sale luego de ingresar
@app.route('/home')
def home():
    # revisar si el usuario esta log in
    if 'loggedin' in session:
    
        # si es usuraio esta conectado mostrar pantalla de home
        return render_template('homepage/home.html', username=session['username'])
    # si el usuario no esta conectado redireccionarlo a la pantalla de home
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
#para mostrar el perfil del usuario
@app.route('/perfil')
def perfil(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM cuentas WHERE id = {0}'.format(session['id']))
        account = cursor.fetchone()
        print(account)
        # Show the profile page with account info
        return render_template('homepage/perfil.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#correr el programa
if __name__ == '__main__':
    app.run(debug=True)