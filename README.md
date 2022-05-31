# proyecto2BD
En este proyecto se trabajo en el uso de una conexion de base de datos con python y html, en donde se realizo una pagina para reproducciones de peliculas con el cual, 
se generan datos y se revisan ciertos datos que se requiren. 

## Tecnologias utilizadas

### flask
![image](https://flask.palletsprojects.com/en/2.1.x/_images/flask-logo.png)

[flask](https://flask.palletsprojects.com/en/2.1.x/) es un framework minimalista escrito en Python que permite crear aplicaciones web rápidamente y con un mínimo número de líneas de código. Está basado en la especificación WSGI de Werkzeug y el motor de templates Jinja2 y tiene una licencia BSD.

```bash
$ pip install Flask
```

### bootstrap

![image](https://getbootstrap.com/docs/5.2/assets/brand/bootstrap-logo-shadow.png)

[bootstrap](https://getbootstrap.com/) es una biblioteca multiplataforma o conjunto de herramientas de código abierto para diseño de sitios y aplicaciones web.

```bash
 <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
 <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
```

### jinja
![image](https://jinja.palletsprojects.com/en/3.1.x/_images/jinja-logo.png)

[jinja](https://jinja.palletsprojects.com/en/3.1.x/) es un motor de plantillas web para el lenguaje de programación Python. Fue creado por Armin Ronacher y tiene una licencia BSD. Jinja es similar al motor de plantillas de Django, pero proporciona expresiones similares a las de Python al tiempo que garantiza que las plantillas se evalúen en un espacio aislado.


## Como correrlo
Tienes que tener el archivo localizado en tu disco local, debido a que de lo contrario flask no logra ubicarse. 
Asegurar estar dentro de la carpeta de proyecto2BD, luego escribir en la terminal.
```bash
venv\scripts\activate
cd devApp
flask run
```
