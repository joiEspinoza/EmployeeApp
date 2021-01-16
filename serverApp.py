from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os

#----------------------------------------------->
#----------------------------------------------->

app = Flask( __name__ )

app.secret_key="KingDevelopment"
# flash

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

FOLDER = os.path.join( 'uploads' )
app.config[ 'FOLDER' ] = FOLDER

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
    #print( response )


    return render_template( 'employees/index.html', employyes = response )


#---------------------------------------------------------|

@app.route( '/uploads/<photoName>' )

def uploads( photoName ):

   return send_from_directory( app.config[ 'FOLDER' ], photoName )


###############################################################################


@app.route( '/create_employye' )

def startStorage():

    return render_template( 'employees/create.html' )


#---------------------------------------------------------|


@app.route( '/store', methods = [ 'POST' ] )

def storage():

    name  = request.form[ 'name' ]
    email = request.form[ 'email' ]
    photo = request.files[ 'photo' ]

    if name == '' or email == '' or photo == '':
        flash( 'All fields are required' )
        return redirect( url_for( 'startStorage' ) )


    now = datetime.now()
    time = now.strftime( '%Y%H%M%S' )
    # Crea variable con fecha actual

    if photo.filename != '':

        newNamePhoto = time+photo.filename
        photo.save( 'uploads/'+newNamePhoto )
        # Crea nuevo nombre a la imagen segun la fecha y la guarda en la carpeta uploads
    

    query = "INSERT INTO `employees` ( `name`, `email`, `photo` ) VALUES ( %s, %s, %s );"
    data = ( name.capitalize(), email, newNamePhoto )

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute( query, data )
    conn.commit()

    return redirect( "/" )


###############################################################################


@app.route( '/startupdate/<int:id>')

def startUpdate( id ):

    query = "SELECT * FROM employees WHERE id = {0}".format( id )
    conn = mysql.connect()

    cursor = conn.cursor()
    cursor.execute( query )

    response = cursor.fetchall()
    #print( response )

    return render_template( 'employees/edit.html', employee = response )


#---------------------------------------------------------|


@app.route( "/update", methods = [ 'POST' ] )

def update():

    newNamePhoto = ""
    name  = request.form[ 'name' ]
    email = request.form[ 'email' ]
    photo = request.files[ 'photo' ]
    idEm  = request.form[ 'id' ]

    if name == '' or email == '':
        flash( 'Name and Email are required' )
        return redirect( url_for( 'startUpdate', id = idEm ) )

    query = "UPDATE employees SET name = %s, email = %s WHERE id = %s;"
    data = ( name, email, idEm )

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    time = now.strftime( '%Y%H%M%S' )

    if photo.filename != '':

        newNamePhoto = time + photo.filename
        photo.save( 'uploads/'+newNamePhoto )

        cursor.execute( "SELECT photo FROM employees WHERE id = {0}".format( idEm ) )
        row = cursor.fetchall()
        #print( row )
        os.remove( os.path.join( app.config[ 'FOLDER' ], row[0][0] ) )
        cursor.execute( "UPDATE employees SET photo = %s WHERE id = %s",( newNamePhoto, idEm ) )

        conn.commit()

    cursor.execute( query, data )
    conn.commit()

    return redirect( '/' )


###############################################################################


@app.route( '/Delete/<int:id>' )

def delete( id ):

    query = "DELETE FROM employees WHERE id = {0}".format( id )
    conn = mysql.connect()

    cursor = conn.cursor()

    cursor.execute( "SELECT photo FROM employees WHERE id = {0}".format( id ) )
    row = cursor.fetchall()
    #print( row )
    os.remove( os.path.join( app.config[ 'FOLDER' ], row[0][0] ) )

    cursor.execute( query )
    conn.commit()

    return redirect( '/' )


#----------------------------------------------->
#----------------------------------------------->


if __name__ == '__main__':
    app.run( port = 3000, debug = True )