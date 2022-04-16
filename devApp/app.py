from flask import Flask, render_template, request, url_for, redirect, flash, session
import psycopg2 #pip install psycopg2
import psycopg2.extras
import re
import random
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


#pagina donde se muestra todos los usuarios que hay
@app.route('/admin_usuarios', methods=['GET'])
def admin_usuarios():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM perfil;
        """
    )
    list_users = cur.fetchall()
    return render_template('administradores/admin_usuarios.html', list_users = list_users)

#abrir el admin_contenido.html y importar los datos de la tabla de contenido
@app.route('/admin_contenido')
def admin_contenido():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM contenido;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/admin_contenido.html', list_users = list_users)

#abrir el admin_anuncios.html y importar los datos de la tabla de contenido
@app.route('/admin_anuncios')
def admin_anuncios():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM anuncios;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/admin_anuncios.html', list_users = list_users)

#abrir el admin_actores.html y importar los datos de la tabla de contenido
@app.route('/admin_actores')
def admin_actores():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM actor;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/admin_actores.html', list_users = list_users)

#abrir el admin_director.html y importar los datos de la tabla de contenido
@app.route('/admin_director')
def admin_director():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM director;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/admin_director.html', list_users = list_users)

#abrir el admin_premio.html y importar los datos de la tabla de contenido
@app.route('/admin_premio')
def admin_premio():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM premios;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/admin_premio.html', list_users = list_users)

#abrir el admin_genero.html y importar los datos de la tabla de contenido
@app.route('/admin_genero')
def admin_genero():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM generos;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/admin_genero.html', list_users = list_users)

#abrir el agreagar_actor_contenido.html y importar los datos de la tabla de contenido
@app.route('/agregar_actor_contenido/<id>', methods=['GET','POST'])
def agregar_actor_contenido(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM actor;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/agregar_actor_contenido.html', list_users = list_users, id_contenido=id)

#agregar el actor al contido que se selecciono
@app.route('/agregar_actor_contenido_seleccionado/<id_actor>,<id_contenido>', methods=['GET','POST'])
def agregar_actor_contenido_seleccionado(id_actor,id_contenido):
    #revisar si el actor ya esta en el contenido 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM actor_contenido WHERE id_actor = '{0}' AND id_contenido = '{1}';
        """.format(id_actor,id_contenido)
    )
    existe = cur.fetchone()

    if existe:
        flash('No se puede debido a que el actor ya esta incluido para este contenido')
    else:
        cur.execute(
        """
        INSERT INTO actor_contenido (id_actor,id_contenido) VALUES ('{0}','{1}');
        """.format(id_actor,id_contenido)
        )
        conn.commit()
        flash("actor agregado exitosamente al contenido")
    return redirect(url_for('agregar_actor_contenido', id = id_contenido))

#eliminar el actor al contido que se selecciono
@app.route('/eliminar_actor_contenido_seleccionado/<id_actor>,<id_contenido>', methods=['GET','POST'])
def eliminar_actor_contenido_seleccionado(id_actor,id_contenido):
    #revisar si el actor ya esta en el contenido 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM actor_contenido WHERE id_actor = '{0}' AND id_contenido = '{1}';
        """.format(id_actor,id_contenido)
    )
    existe = cur.fetchone()

    if existe:
        cur.execute(
        """
        DELETE FROM actor_contenido WHERE id_actor = '{0}' AND id_contenido = '{1}';
        """.format(id_actor,id_contenido)
        )
        conn.commit()
        flash("actor eliminado exitosamente al contenido")
    else:
        flash('No se puede debido a que no existe el actor en el contenido')
    return redirect(url_for('agregar_actor_contenido', id = id_contenido))

#abrir el agreagar_director_contenido.html y importar los datos de la tabla de contenido
@app.route('/agregar_director_contenido/<id>', methods=['GET','POST'])
def agregar_director_contenido(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM director;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/agregar_director_contenido.html', list_users = list_users, id_contenido=id)

#agregar el director al contido que se selecciono
@app.route('/agregar_director_contenido_seleccionado/<id_director>,<id_contenido>', methods=['GET','POST'])
def agregar_director_contenido_seleccionado(id_director,id_contenido):
    #revisar si el director ya esta en el contenido 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM director_contenido WHERE id_director = '{0}' AND id_contenido = '{1}';
        """.format(id_director,id_contenido)
    )
    existe = cur.fetchone()

    if existe:
        flash('No se puede debido a que el director ya esta incluido para este contenido')
    else:
        #revisar si el contenido ya tiene director ya que puede tener solo un director por contenido
        cur.execute(
            """
            SELECT * FROM director_contenido WHERE id_contenido = '{0}'
            """.format(id_contenido)
        )
        tiene_director=cur.fetchall()
        if tiene_director:
            flash('No se puede debido a que el contenido ya contiene un director')
        else:
            cur.execute(
            """
            INSERT INTO director_contenido (id_director,id_contenido) VALUES ('{0}','{1}');
            """.format(id_director,id_contenido)
            )
            conn.commit()
            flash("Director agregado exitosamente al contenido")
    return redirect(url_for('agregar_director_contenido', id = id_contenido))

#eliminar el director al contido que se selecciono
@app.route('/eliminar_director_contenido_seleccionado/<id_director>,<id_contenido>', methods=['GET','POST'])
def eliminar_director_contenido_seleccionado(id_director,id_contenido):
    #revisar si el director ya esta en el contenido 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM director_contenido WHERE id_director = '{0}' AND id_contenido = '{1}';
        """.format(id_director,id_contenido)
    )
    existe = cur.fetchone()

    if existe:
        cur.execute(
        """
        DELETE FROM director_contenido WHERE id_director = '{0}' AND id_contenido = '{1}';
        """.format(id_director,id_contenido)
        )
        conn.commit()
        flash("Director eliminado exitosamente al contenido")
    else:
        flash('No se puede debido a que no existe el director en el contenido')
    return redirect(url_for('agregar_director_contenido', id = id_contenido))


#abrir el agreagar_genero_contenido.html y importar los datos de la tabla de contenido
@app.route('/agregar_genero_contenido/<id>', methods=['GET','POST'])
def agregar_genero_contenido(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM generos;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/agregar_genero_contenido.html', list_users = list_users, id_contenido=id)

#agregar el genero al contido que se selecciono
@app.route('/agregar_genero_contenido_seleccionado/<id_genero>,<id_contenido>', methods=['GET','POST'])
def agregar_genero_contenido_seleccionado(id_genero,id_contenido):
    #revisar si el genero ya esta en el contenido 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM genero_contenido WHERE id_genero = '{0}' AND id_contenido = '{1}';
        """.format(id_genero,id_contenido)
    )
    existe = cur.fetchone()

    if existe:
        flash('No se puede debido a que el genero ya esta incluido para este contenido')
    else:
        cur.execute(
        """
        INSERT INTO genero_contenido (id_genero,id_contenido) VALUES ('{0}','{1}');
        """.format(id_genero,id_contenido)
        )
        conn.commit()
        flash("genero agregado exitosamente al contenido")
    return redirect(url_for('agregar_genero_contenido', id = id_contenido))

#eliminar el genero al contido que se selecciono
@app.route('/eliminar_genero_contenido_seleccionado/<id_genero>,<id_contenido>', methods=['GET','POST'])
def eliminar_genero_contenido_seleccionado(id_genero,id_contenido):
    #revisar si el genero ya esta en el contenido 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM genero_contenido WHERE id_genero = '{0}' AND id_contenido = '{1}';
        """.format(id_genero,id_contenido)
    )
    existe = cur.fetchone()

    if existe:
        cur.execute(
        """
        DELETE FROM genero_contenido WHERE id_genero = '{0}' AND id_contenido = '{1}';
        """.format(id_genero,id_contenido)
        )
        conn.commit()
        flash("genero eliminado exitosamente al contenido")
    else:
        flash('No se puede debido a que no existe el genero en el contenido')
    return redirect(url_for('agregar_genero_contenido', id = id_contenido))

#abrir el agregar_premio_contenido.html e importar los datos de la tabla de contenido
@app.route('/agregar_premio_contenido/<id>', methods=['GET','POST'])
def agregar_premio_contenido(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM premios;
        """
    )
    list_users = cur.fetchall()
    return render_template('/administradores/agregar_premio_contenido.html', list_users = list_users, id_contenido=id)

#agregar el premio al contido que se selecciono
@app.route('/agregar_premio_contenido_seleccionado/<id_premio>,<id_contenido>', methods=['GET','POST'])
def agregar_premio_contenido_seleccionado(id_premio,id_contenido):
    #revisar si el premio ya esta en el contenido 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM premio_contenido WHERE id_premio = '{0}' AND id_contenido = '{1}';
        """.format(id_premio,id_contenido)
    )
    existe = cur.fetchone()

    if existe:
        flash('No se puede debido a que el premio ya esta incluido para este contenido')
    else:
        cur.execute(
        """
        INSERT INTO premio_contenido (id_premio,id_contenido) VALUES ('{0}','{1}');
        """.format(id_premio,id_contenido)
        )
        conn.commit()
        flash("premio agregado exitosamente al contenido")
    return redirect(url_for('agregar_premio_contenido', id = id_contenido))

#eliminar el premio al contido que se selecciono
@app.route('/eliminar_premio_contenido_seleccionado/<id_premio>,<id_contenido>', methods=['GET','POST'])
def eliminar_premio_contenido_seleccionado(id_premio,id_contenido):
    #revisar si el premio ya esta en el contenido 
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM genero_contenido WHERE id_premio = '{0}' AND id_contenido = '{1}';
        """.format(id_premio,id_contenido)
    )
    existe = cur.fetchone()

    if existe:
        cur.execute(
        """
        DELETE FROM genero_contenido WHERE id_premio = '{0}' AND id_contenido = '{1}';
        """.format(id_premio,id_contenido)
        )
        conn.commit()
        flash("premio eliminado exitosamente al contenido")
    else:
        flash('No se puede debido a que no existe el premio en el contenido')
    return redirect(url_for('agregar_premio_contenido', id = id_contenido))

#agregar usuarios a la base de datos
#en si no se puede agregar usuarios pero este se puede utilizar luego para la funcion de agregar peliculas y otros por
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        correo = request.form['correo']
        password= request.form['password']

        #hashea la contrasena
        _hashed_password = generate_password_hash(password)
        #agregar el nuevo perfil 
        cur.execute(
            """
            INSERT INTO perfil (nombre, nombre_usuario, password, email) VALUES ('{0}','{1}','{2}','{3}')
            """.format(nombre,username,_hashed_password,correo)
        )
        conn.commit()
        
        flash('Usuario agregado exitosamente')
        return redirect(url_for('admin_usuarios'))
#abrir la pantalla de agregar unas cuentas
@app.route('/usuario_agregar_cuentas', methods=['POST', 'GET'])
def usuario_agregar_cuentas():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM cuentas where id_perfil = '{0}' order by id;
        """.format(session['id'])
    )
    print('_______________________________________')
    print(session['tipo_cuenta'])
    print('_______________________________________')
    if int(session['tipo_cuenta']) == 1:
        list_users = cur.fetchmany(1)
        print(list_users)
    elif int(session['tipo_cuenta']) == 2:
        list_users = cur.fetchmany(4)
        print(list_users)
    else:
        list_users = cur.fetchall()

    return render_template('homepage/usuario_agregar_cuentas.html', list_users = list_users)

#agregar al cuentas pero en caso que el nombre_cuenta ya existe mostrar que este existe y que ingrese de nuevo
@app.route('/agregar_cuenta_usuario', methods=['POST','GET'])
def agregar_cuenta_usuario():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        username = request.form['username']
        #revisar si el username ya existe
        cur.execute(
            """
            SELECT * FROM cuentas WHERE nombre_cuenta = '{0}'
            """.format(username)
        )
        account_exist = cur.fetchone()
        print(account_exist)
        #si la cuenta mostrar error y chequeo de validaciones de otras
        if account_exist:
            flash('El username ya existe! use otro.')
            return redirect(url_for('usuario_agregar_cuentas'))
        else:
            #para obtener el tipo de supscripcion que tiene la cuenta
            cur.execute(
                """
                SELECT * FROM perfil WHERE id = '{0}'
                """.format(session['id'])
            )
            account = cur.fetchone()
            #para revisar la cantidad de cuentas que tiene el usuario
            cur.execute(
                """
                SELECT * FROM cuentas WHERE id_perfil = '{0}'
                """.format(session['id'])
            )
            account_users = cur.fetchall()
            print('estos son los usuarios que tiene la cuenta')
            print(account_users)
            print('el largo del de arriba es')
            print(len(account_users))
            print(type(account[5]))
            #revisar 
            if account[5]== 1:
                flash('No puedes agregar mas de 1 cuenta con tu tipo de supscripcion')
                return redirect(url_for('usuario_agregar_cuentas'))
            elif account[5]==2:
                if len(account_users) >= 4:
                    flash('No puedes tener agregar de 4 cuenta con tu tipo de supscripcion')
                    return redirect(url_for('usuario_agregar_cuentas'))
                else:
                    #agregar el nuevo perfil 
                    cur.execute(
                        """
                        INSERT INTO cuentas (id_perfil, nombre_cuenta) VALUES ('{0}','{1}')
                        """.format(session['id'], username)
                    )
                    conn.commit()
                    flash('Usuario agregado exitosamente')
            else:
                if len(account_users) >= 8:
                    flash('No puedes agregar mas de 8 cuenta con tu tipo de supscripcion')
                    return redirect(url_for('usuario_agregar_cuentas'))
                else:
                    #agregar el nuevo perfil 
                    cur.execute(
                        """
                        INSERT INTO cuentas (id_perfil, nombre_cuenta) VALUES ('{0}','{1}')
                        """.format(session['id'], username)
                    )
                    conn.commit()
                    flash('Usuario agregado exitosamente') 
        return redirect(url_for('usuario_agregar_cuentas'))

#para agregar contenido en la tabla de contenido
@app.route('/agregar_contenido', methods=['POST'])
def agregar_contenido():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        link = request.form['link']
        duracion= request.form['duracion']

        cur.execute(
            """
            INSERT INTO contenido (nombre, tipo, link, duracion) VALUES ('{0}','{1}','{2}','{3}')
            """.format(nombre,tipo,link,duracion)
        )
        conn.commit()
        flash('Contenido agregado exitosamente')
        return redirect(url_for('admin_contenido'))

#para agregar anuncios en la tabla de anuncios
@app.route('/agregar_anuncios', methods=['POST'])
def agregar_anuncios():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']
        link = request.form['link']

        cur.execute(
            """
            INSERT INTO anuncios (nombre, link) VALUES ('{0}','{1}')
            """.format(nombre,link)
        )
        conn.commit()
        flash('Anuncio agregado exitosamente')
        return redirect(url_for('admin_anuncios'))

#para agregar actores en la tabla de actor
@app.route('/agregar_actor', methods=['POST'])
def agregar_actor():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']

        cur.execute(
            """
            INSERT INTO actor (nombre) VALUES ('{0}')
            """.format(nombre,)
        )
        conn.commit()
        flash('Actor agregado exitosamente')
        return redirect(url_for('admin_actores'))

#para agregar director en la tabla de director
@app.route('/agregar_director', methods=['POST'])
def agregar_director():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']

        cur.execute(
            """
            INSERT INTO director (nombre) VALUES ('{0}')
            """.format(nombre,)
        )
        conn.commit()
        flash('Director agregado exitosamente')
        return redirect(url_for('admin_director'))

#para agregar director en la tabla de premio
@app.route('/agregar_premio', methods=['POST'])
def agregar_premio():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']

        cur.execute(
            """
            INSERT INTO premios (nombre) VALUES ('{0}')
            """.format(nombre,)
        )
        conn.commit()
        flash('Premoi agregado exitosamente')
        return redirect(url_for('admin_premio'))

#para agregar director en la tabla de genero
@app.route('/agregar_genero', methods=['POST'])
def agregar_genero():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nombre = request.form['nombre']

        cur.execute(
            """
            INSERT INTO generos (nombre) VALUES ('{0}')
            """.format(nombre,)
        )
        conn.commit()
        flash('Premoi agregado exitosamente')
        return redirect(url_for('admin_genero'))

#para agregar el username correspondiente a la tabla de contenido en reproduccion segun con el perfil que este conectado
@app.route('/agregar_contenido_en_reproduccion/<id_peli>', methods=['POST','GET'])
def agregar_contenido_en_reproduccion(id_peli):
    print(id_peli)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        INSERT INTO perfil_contenido_en_reproduccion (id_cuenta, id_contenido) VALUES ('{0}','{1}')
        """.format(session['id_conected'], id_peli)
    )
    #reivar el tipo de cuenta que tiene el usuario y segun ello ver si se agrega anuncios a su cuenta del contenido que esta viendo
    if session['tipo_cuenta'] == '1':
        cur.execute(
            """
            SELECT * FROM contenido WHERE id = '{0}'
            """.format(id_peli)
        )
        time = cur.fetchone()
        print("___________________________________")
        print(time)
        time = time[4]
        print(time)
        print(type(time))
        print("___________________________________")
        #realizar la division para que cada 15 minutos se genere un anuncio que se escoga de forma aleatoria
        cur.execute(
            """
            SELECT * FROM anuncios
            """
        )
        anuncios = cur.fetchall()
        numero_anuncios = time // 15
        for x in range(numero_anuncios):
            anuncio_escogido = random.choice(anuncios)
            print(anuncio_escogido)
            cur.execute(
                """
                INSERT INTO anuncios_contenido (id_perfil, id_contenido, id_anuncios) VALUES ('{0}','{1}','{2}')
                """.format(session['id'],id_peli,anuncio_escogido[0])
            )
    #revisar si su tipo de no es el gratis
    print('el tipo de cuenta es')
    print(session['tipo_cuenta'])
    if int(session['tipo_cuenta']) == 2 or int(session['tipo_cuenta']) == 3:
        print("_____________________________")
        print("se agregara al historial")
        print("_____________________________")
        cur.execute(
            """
            INSERT INTO historial_cuentas_avanzadas (id_perfil, id_contenido) VALUES ('{0}','{1}')
            """.format(session['id_conected'], id_peli)
        )

    conn.commit()
    flash('Contenido en reproduccion')
    return redirect(url_for('home'))

#para agregar el contenido con la cuenta que esta a favoritos en caso que ya esta en favoritos mostrar error que no se puede pq ya esta en favoritos
@app.route('/agregar_contenido_en_favoritos/<id_peli>', methods=['POST','GET'])
def agregar_contenido_en_favoritos(id_peli):
    print(id_peli)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM perfil_contenido_favoritos WHERE id_cuenta = '{0}' and id_contenido = '{1}'
        """.format(session['id_conected'], id_peli)
        )
    existe =cur.fetchone()
    print(existe)
    if existe:
        flash('No se puede debido a que ya esta en favoritos')
    else:
        cur.execute(
            """
            INSERT INTO perfil_contenido_favoritos (id_cuenta, id_contenido) VALUES ('{0}','{1}')
            """.format(session['id_conected'], id_peli)
        )
        conn.commit()
        flash('Contenido en agregado en favoritos')
        return redirect(url_for('home'))
    return redirect(url_for('home'))



#para agregar el contenido con la cuenta que esta a vistos en caso que ya esta en vistos mostrar error que no se puede pq ya esta en vistos
@app.route('/agregar_contenido_en_visto/<id_peli>', methods=['POST','GET'])
def agregar_contenido_en_visto(id_peli):
    print(id_peli)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM perfil_contenido_visto WHERE id_cuenta = '{0}' and id_contenido = '{1}'
        """.format(session['id_conected'], id_peli)
        )
    existe =cur.fetchone()
    print(existe)
    if existe:
        flash('No se puede debido a que ya esta en visto')
    else:
        cur.execute(
            """
            INSERT INTO perfil_contenido_visto (id_cuenta, id_contenido) VALUES ('{0}','{1}')
            """.format(session['id_conected'], id_peli)
        )
        conn.commit()
        flash('Contenido en agregado en visto')
        return redirect(url_for('home'))
    return redirect(url_for('home'))
        
#se manda al edit_users.html los valores del que se selecciono
@app.route('/edit_user/<string:id>', methods=['POST', 'GET'])
def obtener_usuario(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        """
        SELECT * FROM perfil WHERE id={0}
        """.format(id)
    )
    data = cur.fetchall()
    cur.close()
    print('se obtuvo el dato de usuario a actualizar')
    print(data[0])
    return render_template('administradores/edit_users.html', usuario = data[0])

#se manda al edit_contenido.html para poder modificar el contenido para luego hacerle un update
@app.route('/edit_contenido/<string:id>', methods=['POST', 'GET'])
def obtener_contenido(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        """
        SELECT * FROM contenido WHERE id={0}
        """.format(id)
    )
    data = cur.fetchall()
    cur.close()
    print('se obtuvo el contenido a actualizar')
    print(data[0])
    return render_template('administradores/edit_contenido.html', contenido = data[0])

#se manda al edit_anuncios.html para poder modificar el contenido para luego hacerle un update
@app.route('/edit_anuncios/<string:id>', methods=['POST', 'GET'])
def obtener_anuncios(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        """
        SELECT * FROM anuncios WHERE id={0}
        """.format(id)
    )
    data = cur.fetchall()
    cur.close()
    print('se obtuvo el anuncio a actualizar')
    print(data[0])
    return render_template('administradores/edit_anuncios.html', contenido = data[0])

#se manda al edit_actores.html para poder modificar el contenido para luego hacerle un update
@app.route('/edit_actor/<string:id>', methods=['POST', 'GET'])
def obtener_actor(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        """
        SELECT * FROM actor WHERE id={0}
        """.format(id)
    )
    data = cur.fetchall()
    cur.close()
    print('se obtuvo el actor a actualizar')
    print(data[0])
    return render_template('administradores/edit_actores.html', contenido = data[0])

#se manda al edit_director.html para poder modificar el contenido para luego hacerle un update
@app.route('/edit_director/<string:id>', methods=['POST', 'GET'])
def obtener_director(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        """
        SELECT * FROM director WHERE id={0}
        """.format(id)
    )
    data = cur.fetchall()
    cur.close()
    print('se obtuvo el director a actualizar')
    print(data[0])
    return render_template('administradores/edit_director.html', contenido = data[0])

#se manda al edit_premio.html para poder modificar el contenido para luego hacerle un update
@app.route('/edit_premio/<string:id>', methods=['POST', 'GET'])
def obtener_premio(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        """
        SELECT * FROM premios WHERE id={0}
        """.format(id)
    )
    data = cur.fetchall()
    cur.close()
    print('se obtuvo el premio a actualizar')
    print(data[0])
    return render_template('administradores/edit_premio.html', contenido = data[0])

#se manda al edit_genero.html para poder modificar el contenido para luego hacerle un update
@app.route('/edit_genero/<string:id>', methods=['POST', 'GET'])
def obtener_genero(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        """
        SELECT * FROM generos WHERE id={0}
        """.format(id)
    )
    data = cur.fetchall()
    cur.close()
    print('se obtuvo el genero a actualizar')
    print(data[0])
    return render_template('administradores/edit_genero.html', contenido = data[0])

#se selecciona el perfil que el usuario escoja entre todos los que tiene
@app.route('/seleccionar_user/<id>,<user>', methods=['POST', 'GET'])
def seleccionar_user(id,user):
    print(id)
    print(user)
    session['id_conected']= id
    print(session['id_conected'])
    session['username'] = user
    return redirect(url_for('perfil'))

#al darle update del edit_users.html este correra y obtendra los datos y se actualizara
@app.route('/update_user/<id>', methods=['POST'])
def actualizar_usuario(id):
    if request.method == 'POST':
        tipo_cuenta = request.form['tipo_cuenta']
        
        if tipo_cuenta == '1' or tipo_cuenta == '2' or tipo_cuenta== '3':
            print('se logro')
            session['tipo_cuenta'] = tipo_cuenta
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                """
                UPDATE perfil
                SET tipo_cuenta = '{0}'
                WHERE id = {1}
                """.format(tipo_cuenta, id)
            )
            flash('usuario actualizado exitosamente')
            conn.commit()
        else:
            print('error')
            flash('Porfavor que el tipo de cuenta sea 1,2 o 3')
            return redirect(url_for('obtener_usuario', id=id))
    return redirect(url_for('admin_usuarios'))

#al darle update del edit_contenido.html se correra este y actualizara la base de datos
@app.route('/update_contenido/<id>', methods=['POST'])
def actualizar_contenido(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo = request.form['tipo']
        link = request.form['link']
        duracion = request.form['duracion']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            UPDATE contenido
            SET nombre = '{0}',
                tipo = '{1}',
                link = '{2}',
                duracion = '{3}'
            WHERE id = {4}
            """.format(nombre,tipo,link,duracion, id)
        )
        flash('contenido actualizado exitosamente')
        conn.commit()
    return redirect(url_for('admin_contenido'))

#al darle update del edit_anuncios.html se correra este y actualizara la base de datos
@app.route('/update_anuncios/<id>', methods=['POST'])
def actualizar_anuncios(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        link = request.form['link']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            UPDATE anuncios
            SET nombre = '{0}',
                link = '{1}'
            WHERE id = {2}
            """.format(nombre,link, id)
        )
        flash('anuncio actualizado exitosamente')
        conn.commit()
    return redirect(url_for('admin_anuncios'))

#al darle update del edit_actores.html se correra este y actualizara la base de datos
@app.route('/update_actor/<id>', methods=['POST'])
def actualizar_actor(id):
    if request.method == 'POST':
        nombre = request.form['nombre']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            UPDATE actor
            SET nombre = '{0}'
            WHERE id = {1}
            """.format(nombre, id)
        )
        flash('actor actualizado exitosamente')
        conn.commit()
    return redirect(url_for('admin_actores'))

#al darle update del edit_director.html se correra este y actualizara la base de datos
@app.route('/update_director/<id>', methods=['POST'])
def actualizar_director(id):
    if request.method == 'POST':
        nombre = request.form['nombre']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            UPDATE director
            SET nombre = '{0}'
            WHERE id = {1}
            """.format(nombre, id)
        )
        flash('Director actualizado exitosamente')
        conn.commit()
    return redirect(url_for('admin_director'))

#al darle update del edit_premio.html se correra este y actualizara la base de datos
@app.route('/update_premio/<id>', methods=['POST'])
def actualizar_premio(id):
    if request.method == 'POST':
        nombre = request.form['nombre']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            UPDATE premios
            SET nombre = '{0}'
            WHERE id = {1}
            """.format(nombre, id)
        )
        flash('Premio actualizado exitosamente')
        conn.commit()
    return redirect(url_for('admin_premio'))

#al darle update del edit_genero.html se correra este y actualizara la base de datos
@app.route('/update_genero/<id>', methods=['POST'])
def actualizar_genero(id):
    if request.method == 'POST':
        nombre = request.form['nombre']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            """
            UPDATE generos
            SET nombre = '{0}'
            WHERE id = {1}
            """.format(nombre, id)
        )
        flash('Genero actualizado exitosamente')
        conn.commit()
    return redirect(url_for('admin_genero'))

#para eliminar usuarios
@app.route('/delete_user/<string:id>', methods =['POST','GET'])
def eliminar_usuario(id):
    print(id)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        """
        DELETE FROM perfil WHERE id ={0}
        """.format(id)
    )
    conn.commit()
    flash("Usuario elimnado exitosamente")
    return redirect(url_for('admin_usuarios'))

#para eliminar contenido
@app.route('/delete_contenido/<string:id>', methods =['POST','GET'])
def eliminar_contenido(id):
    print(id)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        """
        DELETE FROM contenido WHERE id ={0}
        """.format(id)
    )
    conn.commit()
    flash("Contenido elimnado exitosamente")
    return redirect(url_for('admin_contenido'))

#para eliminar anuncios
@app.route('/delete_anuncios/<string:id>', methods =['POST','GET'])
def eliminar_anuncios(id):
    print(id)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        DELETE FROM anuncios WHERE id ={0}
        """.format(id)
    )
    conn.commit()
    flash("Anuncio elimnado exitosamente")
    return redirect(url_for('admin_anuncios'))

#para eliminar actor
@app.route('/delete_actor/<string:id>', methods =['POST','GET'])
def eliminar_actor(id):
    print(id)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        DELETE FROM actor WHERE id ={0}
        """.format(id)
    )
    conn.commit()
    flash("Actor elimnado exitosamente")
    return redirect(url_for('admin_actores'))

#para eliminar director
@app.route('/delete_director/<string:id>', methods =['POST','GET'])
def eliminar_director(id):
    print(id)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        DELETE FROM director WHERE id ={0}
        """.format(id)
    )
    conn.commit()
    flash("Director elimnado exitosamente")
    return redirect(url_for('admin_director'))
    
#para eliminar premio
@app.route('/delete_premio/<string:id>', methods =['POST','GET'])
def eliminar_premio(id):
    print(id)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        DELETE FROM premios WHERE id ={0}
        """.format(id)
    )
    conn.commit()
    flash("Premio elimnado exitosamente")
    return redirect(url_for('admin_premio'))

#para eliminar genero
@app.route('/delete_genero/<string:id>', methods =['POST','GET'])
def eliminar_genero(id):
    print(id)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        DELETE FROM generos WHERE id ={0}
        """.format(id)
    )
    conn.commit()
    flash("Genero elimnado exitosamente")
    return redirect(url_for('admin_genero'))

#para eliminar los perfiles de las cuentas que se crearon de cada usuario
@app.route('/delete_cuentas/<string:id>,<string:nom_cuentas>', methods =['POST','GET'])
def eliminar_cuentas(id, nom_cuentas):
    print(id)
    print(nom_cuentas)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    #revisar si la cuenta que se esta escogiendo a elimina es parte la tabala de perfiles y en este caso mostrar que no es posible eliminarlo debido a que esta
    #es la cuenta principal
    cur.execute(
        """
        SELECT * FROM perfil WHERE nombre_usuario = '{0}'
        """.format(nom_cuentas)
    )
    account = cur.fetchone()
    print(account)
    if account:
        flash("No se puede elimar este debido a que es la cuenta principal")
    else:
        cur.execute(
            """
            DELETE FROM cuentas WHERE id ={0}
            """.format(id)
        )
        conn.commit()
        flash("Cuenta elimnado exitosamente")
        return redirect(url_for('usuario_agregar_cuentas'))
    return redirect(url_for('usuario_agregar_cuentas'))

#para crear una nueva cuenta para ingresar
@app.route('/', methods=['GET','POST'])
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
        
        #revisar si la cuenta ya existe en la base de datos de perfil
        cur.execute(
            """
            SELECT * FROM cuentas WHERE nombre_cuenta = '{0}'
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
                INSERT INTO perfil (nombre, nombre_usuario, password, email, tipo_cuenta) VALUES ('{0}','{1}','{2}','{3}', '1')
                """.format(nombre_completo, username, _hashed_password, email)
                )
            conn.commit()
            flash('Te has registrado exitosamente!')
            #obtener el id del perfil ingresado
            cur.execute(
                """
                SELECT * FROM perfil WHERE nombre_usuario = '{0}'
                """.format(username)
            )
            account_ = cur.fetchone()
            cur.execute(
                """
                INSERT INTO cuentas (id_perfil, nombre_cuenta) VALUES ('{0}','{1}')
                """.format(account_[0],username)
            )
            conn.commit()
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
            SELECT * FROM perfil WHERE nombre_usuario = '{0}'
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
                session['id_conected'] = account['id']
                session['tipo_cuenta'] = account['tipo_cuenta']
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
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # revisar si el usuario esta log in
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM perfil WHERE id = {0}'.format(session['id']))
        account = cursor.fetchone()
        print(account)
        cursor.execute(
        """
        SELECT * FROM contenido;
        """
        )
        list_users = cursor.fetchall()
        print(list_users)
        # si es usuraio esta conectado mostrar pantalla de home
        return render_template('homepage/home.html', account=account, list_users= list_users, user=session['username'])
    # si el usuario no esta conectado redireccionarlo a la pantalla de home
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('id_conected', None)
   session.pop('tipo_cuenta', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/logout_admin')
def logout_admin():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('admin'))

#para mostrar el perfil del usuario
@app.route('/perfil')
def perfil(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM perfil WHERE id = {0}'.format(session['id']))
        account = cursor.fetchone()
        print(account)
        print(session['username'])
        # Show the profile page with account info
        return render_template('homepage/perfil.html', account=account, user = session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/favoritos')
def favoritos():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # revisar si el usuario esta log in
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM perfil WHERE id = {0}'.format(session['id']))
        account = cursor.fetchone()
        print(account)
        cursor.execute(
        """
        select distinct c.id, c.nombre from perfil_contenido_favoritos pcf, contenido c
        where pcf.id_contenido = c.id and pcf.id_cuenta = {0};
        """.format(session['id_conected'])
        )
        list_users = cursor.fetchall()
        print(list_users)
        # si es usuraio esta conectado mostrar pantalla de home
        return render_template('homepage/favoritos.html', account=account, list_users= list_users, user=session['username'])
    # si el usuario no esta conectado redireccionarlo a la pantalla de home
    return redirect(url_for('favoritos'))

#para mostrar el perfil del administrador
@app.route('/perfil_admin')
def perfil_admin(): 
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM perfil WHERE id = {0}'.format(session['id']))
        account = cursor.fetchone()
        print(account)
        # Show the profile page with account info
        return render_template('administradores/perfil_admin.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('admin'))

#para ingresar como administrador
@app.route('/admin/', methods=['GET', 'POST'])
def admin():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # revisar si el username y la contrasena y el codigo de admin estan al darle post
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'codigo_admin' in request.form:
        username = request.form['username']
        password = request.form['password']
        adminpassword= request.form['codigo_admin']
        print("password ingresado ahorita en login: "+ str(password))

        #revisar si la el username existe en la base de datos
        cur.execute(
            """
            SELECT * FROM perfil WHERE nombre_usuario = '{0}'
            """.format(username)
        )
        #fetch solo un dato
        account = cur.fetchone()
        print(account)

        if account:
            password_rs = account['password']
            print(password_rs)
            # si la cuenta existe
            if check_password_hash(password_rs, password) and adminpassword == '123':
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['nombre_usuario']
                # redireccionar al homepage
                return redirect(url_for('admin_usuarios'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('username/contraseña/codigo Incorrecta')
        else:
            # Account doesnt exist or username/password incorrect
            flash('username/contraseña/codigo Incorrecta')

    return render_template('/ingreso/login_admin.html')
#este es para abrir el edit_tipo_supscripcion.html y poder editar el tipo de supscripcion del usuario que sera entre 1,2,3
@app.route('/cambiar_usuario_supscripcion', methods=['GET', 'POST'])
def cambiar_usuario_supscripcion():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cur.execute(
        """
        SELECT * FROM perfil WHERE id={0}
        """.format(session['id'])
    )
    data = cur.fetchall()
    cur.close()
    print('se obtuvo el perfil a actualizar')
    print(data[0])
    return render_template('homepage/edit_tipo_supscripcion.html', usuario = data[0])

#al darle update del edit_users.html este correra y obtendra los datos y se actualizara
@app.route('/update_user_tipo_cuenta/<id>', methods=['POST'])
def actualizar_usuario_tipo_cuenta(id):
    if request.method == 'POST':
        tipo_cuenta = request.form['tipo_cuenta']
        print(tipo_cuenta)
        if tipo_cuenta == '1' or tipo_cuenta == '2' or tipo_cuenta== '3':
            print('se logro')
            session['tipo_cuenta'] = tipo_cuenta
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(
                """
                UPDATE perfil
                SET tipo_cuenta = '{0}'
                WHERE id = {1}
                """.format(tipo_cuenta, id)
            )
            flash('usuario actualizado exitosamente')
            conn.commit()
        else:
            print('error')
            flash('Porfavor que el tipo de cuenta sea 1,2 o 3')
            return redirect(url_for('cambiar_usuario_supscripcion'))
    return redirect(url_for('perfil'))

#correr el programa
if __name__ == '__main__':
    app.run(debug=True)

