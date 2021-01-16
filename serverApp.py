from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

#----------------------------------------------->
#----------------------------------------------->

app = Flask( __name__ )

#----------------------------------------------->
#----------------------------------------------->

mysql = MySQL()
app.config[ 'MYSQL_DATABASE_HOST' ]     = 'localhost' 
app.config[ 'MYSQL_DATABASE_USER' ]     = 'root' 
app.config[ 'MYSQL_DATABASE_PASSWORD' ] = '' 
app.config[ 'MYSQL_DATABASE_DB' ]       = 'employeesdb' 
mysql.init_app( app )

#----------------------------------------------->
#----------------------------------------------->


@app.route( '/' )

def index():

    """ ### PRUEBA CONEXION 

    query = "INSERT INTO `employees` (`id`, `name`, `email`, `photo`) VALUES (NULL, 'test2', 'test2@gmail.com', 'photo2.jpg');"
    conn = mysql.connect()

    cursor = conn.cursor()
    cursor.execute( query )

    conn.commit()

    """

    query = "SELECT * FROM employees"
    conn = mysql.connect()

    cursor = conn.cursor()
    cursor.execute( query )

    response = cursor.fetchall()
    print( response )
    #conn.commit()

    return render_template( 'employees/index.html', employyes = response )


###############################################################################


@app.route( '/create_employye' )

def create():
    return render_template( 'employees/create.html' )


#---------------------------------------------------------|


@app.route( '/store', methods = [ 'POST' ] )

def storage():

    name  = request.form[ 'name' ]
    email = request.form[ 'email' ]
    photo = request.files[ 'photo' ]

    now = datetime.now()
    time = now.strftime( '%Y%H%M%S' )
    # Crea variable con fecha actual

    if photo.filename != "":

        newNamePhoto = time+photo.filename
        photo.save( 'uploads/'+newNamePhoto )
        # Crea nuevo nombre a la imagen segun la fecha y la guarda en la carpeta uploads
    

    query = "INSERT INTO `employees` ( `name`, `email`, `photo` ) VALUES ( %s, %s, %s );"
    data = ( name, email, newNamePhoto )

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute( query, data )
    conn.commit()

    return render_template( 'employees/index.html' )


###############################################################################

@app.route( '/edit_employye/<int:id>')

def startUpdate( id ):

    query = "SELECT * FROM employees WHERE id = {0}".format( id )
    conn = mysql.connect()

    cursor = conn.cursor()
    cursor.execute( query )

    response = cursor.fetchall()
    print( response )

    return render_template( 'employees/edit.html', employee = response )


#---------------------------------------------------------|


@app.route( "/update", methods = [ 'POST' ] )

def update():

    newNamePhoto = ""
    name  = request.form[ 'name' ]
    email = request.form[ 'email' ]
    photo = request.files[ 'photo' ]
    idEm    = request.form[ 'id' ]

    now = datetime.now()
    time = now.strftime( '%Y%H%M%S' )
    # Crea variable con fecha actual

    if photo.filename != "":

        newNamePhoto = time+photo.filename
        photo.save( 'uploads/'+newNamePhoto )


    query = "UPDATE employees SET name = %s, email = %s, photo = %s WHERE id = %s;"
    data = ( name, email, newNamePhoto, idEm )

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute( query, data )
    conn.commit()

    return redirect( '/' )


###############################################################################


@app.route( '/Delete/<int:id>' )

def delete( id ):

    query = "DELETE FROM employees WHERE id = {0}".format( id )
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute( query )
    conn.commit()

    return redirect( '/' )


#----------------------------------------------->
#----------------------------------------------->


if __name__ == '__main__':
    app.run( port = 3000, debug = True )