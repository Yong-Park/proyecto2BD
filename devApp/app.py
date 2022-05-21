from datetime import datetime, timedelta
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

#abrir el admin_reportes
@app.route('/admin_reportes')
def admin_reportes():
    return render_template('/administradores/admin_reportes.html')

#abrir el admin_datos
@app.route('/admin_generar_datos')
def admin_generar_datos():
    return render_template('/administradores/admin_generar_datos.html')

@app.route('/admin_reporte1', methods=['POST', 'GET'])
def admin_reporte1():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    list_users = []

    if request.method == 'POST':
        fecha_inicio = str(request.form['fecha_inicio'])
        fecha_final = str(request.form['fecha_final'])

        if(fecha_inicio != '' and fecha_final != ''):
            cur.execute(
            """
            select g.nombre, sum(c.duracion) from contenido c, perfil_contenido_visto pcv, genero_contenido gc, generos g 
            where g.id = gc.id_genero and c.id = gc.id_contenido and pcv.fecha between '{0}' and '{1}'
            group by g.nombre
            order by sum(c.duracion) desc limit 10;
            """.format(fecha_inicio, fecha_final)
            )
            list_users = cur.fetchall()
        else:
            flash("Por favor ingrese los datos de fechas")

    return render_template('/administradores/admin_reporte1.html', list_users = list_users)

@app.route('/admin_reporte2', methods=['POST', 'GET'])
def admin_reporte2():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    list_users = []

    if request.method == 'POST':
        fecha_inicio = str(request.form['fecha_inicio'])
        fecha_final = str(request.form['fecha_final'])

        if(fecha_inicio != '' and fecha_final != ''):
            cur.execute(
            """
            select p.tipo_cuenta as tipo_de_cuenta, g.nombre, count(pcer.id_contenido) as Cantidad_de_reproducciones from contenido as c
            join perfil_contenido_en_reproduccion as pcer on c.id = pcer.id_contenido 
            join cuentas as c2 on c2.id = pcer.id_cuenta
            join perfil as p on p.id =c2.id_perfil 
            join genero_contenido as gc on gc.id_contenido = pcer.id_contenido 
            join generos as g on gc.id_genero = g.id
            where pcer.fecha between '{0}' and '{1}' 
            group by g.nombre, tipo_de_cuenta
            order by sum(c.duracion) desc limit 10;
            """.format(fecha_inicio, fecha_final)
            )
            list_users = cur.fetchall()
            for i in list_users:
                if(i[0] == 1):
                    i[0] = 'Basica'
                elif(i[0] == 2):
                    i[0] = 'Estandar'
                elif(i[0] == 3):
                    i[0] = 'Avanzada'
        else:
            flash("Por favor ingrese los datos de fechas")

    return render_template('/administradores/admin_reporte2.html', list_users = list_users)

@app.route('/admin_reporte3')
def admin_reporte3():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute(
        """
        select d.nombre, count(d.id) from contenido c, perfil_contenido_visto pcv, cuentas c2, perfil p, director d, director_contenido dc 
        where c.id = pcv.id_contenido and c2.id = pcv.id_cuenta and c2.id_perfil = p.id
        and d.id = dc.id_director and c.id = dc.id_contenido and (p.tipo_cuenta = 2 or p.tipo_cuenta = 3)
        group by d.nombre
        order by count(d.id) desc limit 10;
        """
    )

    list_directores = cur.fetchall()

    cur.execute(
        """
        select a.nombre, count(a.id) from contenido c, perfil_contenido_visto pcv, cuentas c2, perfil p, actor a, actor_contenido ac
        where c.id = pcv.id_contenido and c2.id = pcv.id_cuenta and c2.id_perfil = p.id
        and a.id = ac.id_actor and c.id = ac.id_contenido and (p.tipo_cuenta = 2 or p.tipo_cuenta = 3)
        group by a.nombre
        order by count(a.id) desc limit 10;
        """
    )
    
    list_actores = cur.fetchall()

    return render_template('/administradores/admin_reporte3.html', list_directores = list_directores, list_actores = list_actores)

@app.route('/admin_reporte4', methods=['POST', 'GET'])
def admin_reporte4():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    fecha_actual = datetime.today() + timedelta(days=1)
    fecha_meses = fecha_actual - timedelta(days=183)

    print(fecha_actual)
    print(fecha_meses)

    cur.execute(
        """
        select count(fctp.id) from fecha_cambio_tipo_perfil fctp, perfil p
        where fctp.id_perfil = p.id
        and fctp.fecha between '{0}' and '{1}';
        """.format(fecha_meses, fecha_actual)
    )

    list_cuentas = cur.fetchall()

    return render_template('/administradores/admin_reporte4.html', list_cuentas = list_cuentas)

@app.route('/admin_reporte5', methods=['POST', 'GET'])
def admin_reporte5():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    list_hours = []

    if request.method == 'POST':

        fecha_inicio = request.form['fecha_inicio']

        if(fecha_inicio != ''):
            fecha_final = datetime.strptime(fecha_inicio, '%Y-%m-%d') + timedelta(days=1)
            cur.execute(
            """
            select extract(hour from fecha), count(extract(hour from fecha)) as cantidad from historial_conexiones hc
            where fecha between '{0}' and '{1}'
            group by extract(hour from fecha)
            order by cantidad desc limit 1; 
            """.format(fecha_inicio, fecha_final)
            )
            list_hours = cur.fetchall()
            print(list_hours)

        else:
            flash("Por favor ingrese los datos de fechas")

    return render_template('/administradores/admin_reporte5.html', list_hours = list_hours)

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

    cur.execute(
        """
        select a.id, a.nombre from actor_contenido ac, actor a 
        where ac.id_contenido = {0} and ac.id_actor = a.id;
        """.format(id)
    )
    
    list_actors = cur.fetchall()

    cur.execute(
        """
        select * from contenido
        where id = {0};
        """.format(id)
    )

    contenido = cur.fetchone()

    return render_template('/administradores/agregar_actor_contenido.html', list_users = list_users, id_contenido=id, list_actors = list_actors, contenido = contenido)

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

    cur.execute(
        """
        select d.id, d.nombre from director_contenido dc, director d 
        where dc.id_contenido = {0} and dc.id_director = d.id;
        """.format(id)
    )
    
    list_director = cur.fetchall()

    cur.execute(
        """
        select * from contenido
        where id = {0};
        """.format(id)
    )

    contenido = cur.fetchone()

    return render_template('/administradores/agregar_director_contenido.html', list_users = list_users, id_contenido=id, list_director = list_director, contenido = contenido)

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

    cur.execute(
        """
        select  g.id, g.nombre from genero_contenido gc, generos g
        where gc.id_contenido = {0} and gc.id_genero = g.id;
        """.format(id)
    )
    
    list_generos = cur.fetchall()

    cur.execute(
        """
        select * from contenido
        where id = {0};
        """.format(id)
    )

    contenido = cur.fetchone()

    return render_template('/administradores/agregar_genero_contenido.html', list_users = list_users, id_contenido=id, list_generos = list_generos, contenido = contenido)

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

    cur.execute(
        """
        select p.id, p.nombre from premio_contenido pc, premios p
        where pc.id_contenido = {0} and pc.id_premio = p.id;
        """.format(id)
    )
    
    list_premios = cur.fetchall()

    cur.execute(
        """
        select * from contenido
        where id = {0};
        """.format(id)
    )

    contenido = cur.fetchone()

    return render_template('/administradores/agregar_premio_contenido.html', list_users = list_users, id_contenido=id, list_premios = list_premios, contenido = contenido)

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

#para agrear nuevo usuario por parte del admin a la tabla de usuarios
@app.route('/agregar_usuario_admin', methods=['POST','GET'])
def agregar_usaurio_admin():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # resvisar que fuera por funcion de post, que exista nombre_usuario la contrasena y el correo
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # variables que reciben los textos que se llenaron en registrar.html
        nombre_completo = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        #hashea la contrasena
        _hashed_password = generate_password_hash(password)
        
        #revisar si el nombre existe en la base de datos
        cur.execute(
            """
            SELECT * FROM perfil WHERE nombre = '{0}'
            """.format(nombre_completo)
        )
        perfil = cur.fetchone()
        print(perfil)
        if perfil:
            flash('Ese perfil con ese nombre ya existe!')
        else:
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
            elif not username or not password or not email or not nombre_completo:
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
        
    return redirect(url_for('admin_usuarios'))
    

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
#generar  una hora de forma aleatoria
def randomTimeRange():
    start_time_input = '00:00:01'
    end_time_input = '23:59:59'

    start_time = start_time_input.split(':')
    end_time = end_time_input.split(':')

    start_hour = start_time[0]
    start_minute = start_time[1]
    start_seconds = start_time[2]

    end_hour = end_time[0]
    end_minute = end_time[1]
    end_seconds = end_time[2]

    # Get maximum end time for randrange
    if end_hour == '23' and end_minute != '00':
        max_hour = 23 + 1
    else:
        max_hour = start_hour

    if start_minute > end_minute:
        minutes = random.randrange(int(end_minute), int(start_minute))
    elif start_minute < end_minute:
        minutes = random.randrange(int(start_minute), int(end_minute))

    if start_hour == end_hour:
        hours = start_hour
    elif start_hour != end_hour:
        hours = random.randrange(int(start_hour), int(max_hour))

    if str(hours) == str(end_hour):
        minutes = random.randrange(int(start_minute), int(end_minute))
    else:
        minutes = random.randrange(0, 59)

    if start_seconds == end_seconds:
        seconds = start_seconds
    elif start_seconds > end_seconds:
        seconds = random.randrange(int(start_seconds), int(59))
    elif start_seconds < end_seconds:
        seconds = random.randrange(int(start_seconds), int(end_seconds))

    h = int(hours)
    m = int(minutes)
    s = int(seconds)

    return f"{h:02d}" + ':' + f"{m:02d}" + ':' + f"{s:02d}"

#para generar datos y agregarlos al perfil
@app.route('/generar_historial_conteido', methods=['POST','GET'])
def generar_historial_conteido():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        #guardar todos las cuentas existentes que hay de la base de datos
        cur.execute(
            """
            SELECT id FROM cuentas
            """
        )
        cuentas = cur.fetchall()
        print("id de las cuenta")
        print(cuentas)
        cur.execute(
            """
            SELECT id FROM contenido
            """
        )
        contenido = cur.fetchall()
        print("id de los contenidos")
        print(contenido)
        #recibir los parametros
        date = request.form['date']
        cantidad = request.form['cantidad']
        print(cantidad)
        print(date)
        print(type(cantidad))
        for x in range (int(cantidad)):
            time = randomTimeRange()
            date_time = date + ' ' + time
            cuenta_escogida = random.choice(cuentas)
            contenido_escogido = random.choice(contenido)
            cur.execute(
                """
                INSERT INTO perfil_contenido_en_reproduccion (id_cuenta, id_contenido, fecha) VALUES ('{0}','{1}','{2}')
                """.format(cuenta_escogida[0],contenido_escogido[0], date_time)
            )
        conn.commit()
        flash('Datos generados exitosamente')
        return redirect(url_for('admin_generar_datos'))

#para generar datos y agregarlos al perfil
@app.route('/generar_historial_vistas', methods=['POST','GET'])
def generar_historial_vistas():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        #guardar todos las cuentas existentes que hay de la base de datos
        cur.execute(
            """
            SELECT id FROM cuentas
            """
        )
        cuentas = cur.fetchall()
        print("id de las cuenta")
        print(cuentas)
        cur.execute(
            """
            SELECT id FROM contenido
            """
        )
        contenido = cur.fetchall()
        print("id de los contenidos")
        print(contenido)
        #recibir los parametros
        date = request.form['date']
        cantidad = request.form['cantidad']
        print(cantidad)
        print(date)
        print(type(cantidad))
        for x in range (int(cantidad)):
            time = randomTimeRange()
            date_time = date + ' ' + time
            cuenta_escogida = random.choice(cuentas)
            contenido_escogido = random.choice(contenido)
            cur.execute(
                """
                INSERT INTO perfil_contenido_visto (id_cuenta, id_contenido, fecha) VALUES ('{0}','{1}','{2}')
                """.format(cuenta_escogida[0],contenido_escogido[0], date_time)
            )
        conn.commit()
        flash('Datos generados exitosamente')
        return redirect(url_for('admin_generar_datos'))

#para generar datos y agregarlos al perfil
@app.route('/generar_historial_reproduccion_vistas', methods=['POST','GET'])
def generar_historial_reproduccion_vistas():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        #guardar todos las cuentas existentes que hay de la base de datos
        cur.execute(
            """
            SELECT id FROM cuentas
            """
        )
        cuentas = cur.fetchall()
        print("id de las cuenta")
        print(cuentas)
        cur.execute(
            """
            SELECT id FROM contenido
            """
        )
        contenido = cur.fetchall()
        print("id de los contenidos")
        print(contenido)
        #recibir los parametros
        date = request.form['date']
        cantidad = request.form['cantidad']
        print(cantidad)
        print(date)
        print(type(cantidad))
        for x in range (int(cantidad)):
            time = randomTimeRange()
            date_time = date + ' ' + time
            cuenta_escogida = random.choice(cuentas)
            contenido_escogido = random.choice(contenido)
            cur.execute(
                """
                INSERT INTO perfil_contenido_en_reproduccion (id_cuenta, id_contenido, fecha) VALUES ('{0}','{1}','{2}')
                """.format(cuenta_escogida[0],contenido_escogido[0], date_time)
            )
            time = randomTimeRange()
            date_time = date + ' ' + time
            cuenta_escogida = random.choice(cuentas)
            contenido_escogido = random.choice(contenido)
            cur.execute(
                """
                INSERT INTO perfil_contenido_visto (id_cuenta, id_contenido, fecha) VALUES ('{0}','{1}','{2}')
                """.format(cuenta_escogida[0],contenido_escogido[0], date_time)
            )
        conn.commit()
        flash('Datos generados exitosamente')
        return redirect(url_for('admin_generar_datos'))

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
                """.format(session['id_conected'],id_peli,anuncio_escogido[0])
            )
    #revisar si su tipo de no es el gratis
    print('el tipo de cuenta es')
    print(session['tipo_cuenta'])
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
        INSERT INTO perfil_contenido_visto (id_cuenta, id_contenido) VALUES ('{0}','{1}')
        """.format(session['id_conected'], id_peli)
    )
    conn.commit()
    flash('Contenido en agregado en visto')
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
    #revisar si la el user ya esta conectado
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM cuenta_conectada WHERE id_cuenta={0}
        """.format(id)
    )
    cuenta_contectada = cur.fetchone()
    if cuenta_contectada:
        flash('No se puede debido a que alguien ya esta usando esta cuenta')
    else:
        cur.execute(
            """
            DELETE FROM cuenta_conectada WHERE id_cuenta = '{0}'
            """.format(session['id_conected'])
        )
        cur.execute(
            """
            INSERT INTO cuenta_conectada (id_cuenta) VALUES ('{0}')
            """.format(id)
        )
        conn.commit()
        session['id_conected']= id
        print(session['id_conected'])
        session['username'] = user
    return redirect(url_for('perfil'))

#se selecciona el perfil que el usuario escoja entre todos los que tiene
@app.route('/seleccionar_user_a_tomar/<id>,<user>', methods=['POST', 'GET'])
def seleccionar_user_a_tomar(id,user):
    print(id)
    print(user)
    #revisar si la el user ya esta conectado
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        SELECT * FROM cuenta_conectada WHERE id_cuenta={0}
        """.format(id)
    )
    cuenta_contectada = cur.fetchone()
    if cuenta_contectada:
        flash('No se puede debido a que alguien ya esta usando esta cuenta')
    else:
        cur.execute(
            """
            DELETE FROM cuenta_conectada WHERE id_cuenta = '{0}'
            """.format(session['id_conected'])
        )
        cur.execute(
            """
            INSERT INTO cuenta_conectada (id_cuenta) VALUES ('{0}')
            """.format(id)
        )
        conn.commit()
        session['id_conected']= id
        print(session['id_conected'])
        session['username'] = user
        return redirect(url_for('home'))
    return redirect(url_for('escoger_cuenta'))


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
        flash('Contenido Actualizado Exitosamente')
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
        flash('Anuncio Actualizado Exitosamente')
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

#abrir la pantalla de agregar unas cuentas
@app.route('/escoger_cuenta', methods=['POST', 'GET'])
def escoger_cuenta():
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

    return render_template('homepage/escoger_cuenta.html', list_users = list_users)

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
                #agregar la cuenta esta como conectada en la tabla de cuenta_conectada
                cur.execute(
                    """
                    SELECT * FROM cuenta_conectada WHERE id_cuenta = '{0}'
                    """.format(session['id_conected'])
                )
                existe = cur.fetchone()
                if existe:
                    flash('No se puede debido a que alguien esta conectado a esta cuenta actualmente escoja uno de los que tiene disponible')
                    return redirect(url_for('escoger_cuenta'))
                else:
                    cur.execute(
                        """
                        INSERT INTO cuenta_conectada (id_cuenta) VALUES ('{0}')
                        """.format(session['id_conected'])
                    )
                    cur.execute(
                        """
                        INSERT INTO historial_conexiones (id_cuenta) VALUES ('{0}')
                        """.format(session['id'])
                    )
                    conn.commit()
                
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

@app.route('/logout', methods=['GET','POST'])
def logout():
    # Remove session data, this will log the user out
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
        DELETE FROM cuenta_conectada where id_cuenta = '{0}'
        """.format(session['id_conected'])
    )
    conn.commit()
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

@app.route('/reproduccion')
def reproduccion():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # revisar si el usuario esta log in
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM perfil WHERE id = {0}'.format(session['id']))
        account = cursor.fetchone()
        print(account)
        cursor.execute(
        """
        select distinct c.id, c.nombre from perfil_contenido_en_reproduccion pcer, contenido c
        where pcer.id_contenido = c.id and pcer.id_cuenta = {0};
        """.format(session['id_conected'])
        )
        list_users = cursor.fetchall()
        print(list_users)
        # si es usuraio esta conectado mostrar pantalla de home
        return render_template('homepage/reproduccion.html', account=account, list_users= list_users, user=session['username'])
    # si el usuario no esta conectado redireccionarlo a la pantalla de home
    return redirect(url_for('reproduccion'))

@app.route('/visto')
def visto():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # revisar si el usuario esta log in
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM perfil WHERE id = {0}'.format(session['id']))
        account = cursor.fetchone()
        print(account)
        cursor.execute(
        """
        select distinct c.id, c.nombre from perfil_contenido_visto pcv, contenido c
        where pcv.id_contenido = c.id and pcv.id_cuenta = {0};
        """.format(session['id_conected'])
        )
        list_users = cursor.fetchall()
        print(list_users)
        # si es usuraio esta conectado mostrar pantalla de home
        return render_template('homepage/visto.html', account=account, list_users= list_users, user=session['username'])
    # si el usuario no esta conectado redireccionarlo a la pantalla de home
    return redirect(url_for('visto'))

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
            if tipo_cuenta == '3':
                cur.execute(
                    """
                    INSERT INTO fecha_cambio_tipo_perfil (id_perfil) VALUES ('{0}')
                    """.format(session['id'])
                )
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

@app.route('/buscar', methods=['POST','GET'])
def buscar():
    # revisar si el usuario esta log in
    if 'loggedin' in session:
        # si es usuraio esta conectado mostrar pantalla de home
        return render_template('homepage/buscar.html')
    # si el usuario no esta conectado redireccionarlo a la pantalla de home
    return render_template(url_for('buscar'))

@app.route('/buscar_contenido', methods=['POST','GET'])
def buscar_contenido():
    actor = request.form['actor']
    director = request.form['director']
    contenido = request.form['contenido']
    genero = request.form['genero']
    premio = request.form['premio']
    tipo = request.form['tipo']
    print(actor)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # revisar si el usuario esta log in
    if 'loggedin' in session:
        cur.execute(
            """
            select distinct c.id, c.nombre, c.tipo, c.link, d.nombre, a.nombre, g.nombre, p.nombre from contenido c, director_contenido dc, director d, actor_contenido ac, actor a, genero_contenido gc, generos g,
            premio_contenido pc, premios p where c.id = dc.id_contenido and dc.id_director = d.id and c.id = ac.id_contenido and ac.id_actor = a.id
            and c.id = gc.id_contenido and gc.id_genero = g.id and c.id = pc.id_contenido and pc.id_premio = p.id and (lower(c.nombre) like lower('{0}%') and 
            lower(c.tipo) like lower('{1}%') and lower(d.nombre) like lower('{2}%') and lower(a.nombre) like lower('{3}%') and lower(g.nombre) like lower('{4}%') and
            lower(p.nombre) like lower('{5}%'))
            """.format(contenido, tipo, director,actor, genero, premio)
        )

        list_users = cur.fetchall()
        print(list_users)
        # si es usuraio esta conectado mostrar pantalla de home
        return render_template('homepage/mostrar_buscado.html', list_users=list_users)
    # si el usuario no esta conectado redireccionarlo a la pantalla de home
    return render_template(url_for('buscar'))

#correr el programa
if __name__ == '__main__':
    app.run(debug=True)

