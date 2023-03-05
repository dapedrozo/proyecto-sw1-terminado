from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime, date, time

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1098741116'
app.config['MYSQL_DB'] = 'monsteracmebd'


#ahora vamos a inicializar una sesion es decir datos que guarda nuestro servidor para luego poder reutilizarlos
#en este caso lo vamos a guardar dentro de la memoria de la aplicacion
#con secret_key le decimos como va a ir protegida nuestra sesion
app.secret_key = 'mysecretkey'

mysql = MySQL(app)
#cada vez que un usuario entre a nuestra ruta principal vamos a devolverle algo es esta linea:


@app.route('/login')
def login():
    return redirect(url_for('opindex'))

@app.route('/')
def opindex():
    if session:
        if 'Usertype' in session:
            Usertype = session['Usertype']
            print(Usertype)
        if 'Nombre' in session:
            Nombre = session['Nombre']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM servicios')
            data = cur.fetchall()
        return render_template('index.html', servicios = data, session = Usertype, session2 = Nombre)
    else:
        return render_template('login.html')

#opciones de usuarios y funcion para el proceso de creacion:
@app.route('/opuser')
def opuser():
    if session:
        if 'Usertype' in session:
            Usertype = session['Usertype']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM usuarios')
            data = cur.fetchall()
        return render_template('opuser.html', usuarios = data, session = Usertype)
    else:
        flash('por favor, inicia sesion')
        return render_template('login.html')
    
@app.route('/add-user')
def createuser():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empresa')
    data = cur.fetchall()
    return render_template('add-user.html', empresas = data)

#opciones de clientes y funcion para el proceso de creacion:

@app.route('/opclien')
def opclien():
    if session:
        if 'Usertype' in session:
            Usertype = session['Usertype']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM clientes')
            data = cur.fetchall()
        return render_template('opclien.html', clientes = data, session = Usertype)
    else:
        flash('por favor, inicia sesion')
        return render_template('login.html')


@app.route('/add-cliente')
def createcliente():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empresa')
    data = cur.fetchall()
    return render_template('add-cliente.html', empresas = data)

#opciones de reportes y funcion para el proceso de creacion:
@app.route('/oprepor')
def oprepor():
    if session:
        if 'Usertype' in session:
            Usertype = session['Usertype']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM reportes_enviados')
            data = cur.fetchall()
        return render_template('oprepor.html', reportes = data, session = Usertype)
    else:
        flash('por favor, inicia sesion')
        return render_template('login.html')

@app.route('/add-repor')
def createrepor():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    return render_template('add-repor.html', clientes = data)

#opciones de equipos y funcion para el proceso de creacion:
@app.route('/opequipo')
def opequipo():
    if session:
        if 'Usertype' in session:
            Usertype = session['Usertype']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM equipos_computo')
            data = cur.fetchall()
        return render_template('opequipo.html', equipos = data, session = Usertype)
    else:
        flash('por favor, inicia sesion')
        return render_template('login.html')

@app.route('/add-equipo')
def createequipo():
    return render_template('add-equipo.html')

#opciones de servicios y funcion para el proceso de creacion:
@app.route('/opservicio')
def opservicio():
    if session:
        if 'Usertype' in session:
            Usertype = session['Usertype']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM servicios')
            data = cur.fetchall()
        return render_template('opservicio.html', servicios = data, session = Usertype)
    else:
        flash('por favor, inicia sesion')
        return render_template('login.html')

@app.route('/add-servicio')
def createservicio():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM usuarios WHERE UsuTipo = "TECNICO"')
    data2 = cur2.fetchall()
    cur3 = mysql.connection.cursor()
    cur3.execute('SELECT * FROM equipos_computo')
    data3 = cur3.fetchall()
    return render_template('add-servicio.html', clientes = data, tecnicos = data2, equipos = data3)

#opciones de fotos y funcion para el proceso de creacion:
@app.route('/opfoto')
def opfoto():
    if session:
        if 'Usertype' in session:
            Usertype = session['Usertype']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM fotos_servicios')
            data = cur.fetchall()
        return render_template('opfoto.html', fotos = data, session = Usertype)
    else:
        flash('por favor, inicia sesion')
        return render_template('login.html')

@app.route('/add-foto')
def createfoto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM servicios')
    data = cur.fetchall()
    return render_template('add-foto.html', servicios = data)


# metodos iniciar y cerrar sesion
# metodo inicio de sesion a la aplicacion
@app.route('/loginU',methods=['POST'])  
def loginU():
    if request.method == 'POST':
        UsuUser = request.form['LG00']
        Usupass = request.form['LG01']
        cur = mysql.connection.cursor()
        sql=('SELECT U.UsuNom,U.UsuApe,U.UsuTipDoc,U.UsuNumDoc,U.UsuTipo,U.UsuEstado,U.UsuTel,U.UsuDir,U.UsuTipoContrat,U.UsuFechRegist,U.UsuHorRegist,U.UsuVenciContrat,U.UsuEstadoContrat,U.UsuUser,U.Usupass,U.EmpresaId,E.IdEmpresa,E.EmpNomRazSoc,E.EmpTipoDoc,E.EmpNumDoc FROM usuarios AS U INNER JOIN empresa AS E ON U.EmpresaId=E.IdEmpresa WHERE U.UsuUser="{0}" AND U.Usupass="{1}" AND U.UsuEstadoContrat="{2}"'.format(UsuUser,Usupass,"ACTIVO"))
        cur.execute(sql)
        data = cur.fetchall()
        mysql.connection.commit()
        cur2 = mysql.connection.cursor()
        sql2=('SELECT C.CliNumDoc,C.CliDir,C.CliTel,C.EmpresaId,C.CliNomRazSoc,C.CliTipoDoc,S.IdServicio,S.CliNumDoc,S.IdEquipo,S.SerDes,S.SerFech,S.SerHora,S.SerFechAsig,S.SerHorAsig,S.SerClasifica,S.UsuNumDoc,S.Estado FROM clientes as C INNER JOIN servicios as S on S.CliNumDoc=C.CliNumDoc')
        cur2.execute(sql2)
        data2 = cur2.fetchall()
        if len(data)>0:            
            session['Usertype'] = data[0][4]
            session['Nombre'] = data[0][0]
            return render_template('index.html',servicios = data2, session = session['Usertype'],session2 = session['Nombre'])
        else:
            flash('usuario o contraseña incorrectos o el usuario no se encuentra registrado')
            return render_template('login.html')
    
@app.route('/logout')
def logout():
    if session:
        if 'Usertype' in session:
            session.pop('Usertype')
        if 'Nombre' in session:
            session.pop('Nombre')
        return render_template('login.html')
    else:
        flash('por favor, inicia sesion')
        return render_template('login.html')


#funciones de añadir

#añadir clientes
@app.route('/add_client',methods=['POST'])  
def add_client():
    if request.method == 'POST':
        CliNomRazSoc = request.form['CliNomRazSoc']
        CliTipoDoc = request.form['CliTipoDoc']
        CliNumDoc = request.form['CliNumDoc']
        CliDir = request.form['CliDir']
        CliTel = request.form['CliTel']
        IdEmpresa = request.form['IdEmpresa']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO clientes (CliNumDoc,CliDir,CliTel,EmpresaId,CliNomRazSoc,CliTipoDoc) VALUES (%s,%s,%s,%s,%s,%s)',(CliNumDoc,CliDir,CliTel,IdEmpresa,CliNomRazSoc,CliTipoDoc))
        mysql.connection.commit()
        flash('cliente registrado satisfactoriamente')
        return redirect(url_for('opclien'))

#añadir empresa
@app.route('/add_empresa',methods=['POST'])  
def add_empresa():
    if request.method == 'POST':
        EmpNomRazSoc = request.form['fullname']
        EmpTipoDoc = request.form['fullname']
        EmpNumDoc = request.form['fullname']
        cur = mysql.connection.cursor()
        cur.execute("""
        'INSERT INTO empresa 
        (EmpNomRazSoc,EmpTipoDoc,EmpNumDoc) 
        VALUES (%s,%s,%s)'
        """,(EmpNomRazSoc,EmpTipoDoc,EmpNumDoc))
        mysql.connection.commit()
        flash('empresa registrada satisfactoriamente')
        return redirect(url_for('Index'))

#añadir equipos de computo
@app.route('/add_equipo',methods=['POST'])  
def add_equipo():
    if request.method == 'POST':
        IdEquipo = request.form['IdEquipo']
        NomEquipo = request.form['NomEquipo']
        DesEquipo = request.form['DesEquipo']
        CodEquipo = request.form['CodEquipo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO equipos_computo (IdEquipo,NomEquipo,DesEquipo,CodEquipo) VALUES (%s,%s,%s,%s)',(IdEquipo,NomEquipo,DesEquipo,CodEquipo))
        mysql.connection.commit()
        flash('equipo registrado satisfactoriamente')
        return redirect(url_for('opequipo'))

#añadir fotos de servicios
@app.route('/add_foto',methods=['POST'])  
def add_foto():
    if request.method == 'POST':
        ahora = datetime.now()
        IdServicio = request.form['IdServicio']
        FotoDes = request.form['FotoDes']
        fecha_actual = date(ahora.year, ahora.month, ahora.day)
        FotoFech = fecha_actual
        hora_actual = time(ahora.hour, ahora.minute, ahora.second)
        FotoHor = hora_actual
        FotoTipo = request.form['FotoTipo']
        Imagen = request.form['Imagen']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO fotos_servicios (IdServicio,FotoDes,FotoFech,FotoHor,FotoTipo,Imagen) VALUES (%s,%s,%s,%s,%s,%s)',(IdServicio,FotoDes,FotoFech,FotoHor,FotoTipo,Imagen))
        mysql.connection.commit()
        flash('imagen añadida satisfactoriamente')
        return redirect(url_for('opfoto'))

#añadir reportes
@app.route('/add_reporte',methods=['POST'])  
def add_reporte():
    if request.method == 'POST':
        ahora = datetime.now()
        CliNumDoc = request.form['CliNumDoc']
        fecha_actual = date(ahora.year, ahora.month, ahora.day)
        RepFechEnvi = fecha_actual
        hora_actual = time(ahora.hour, ahora.minute, ahora.second)
        RepHorEnvi = hora_actual
        RepTipo = request.form['RepTipo']
        Estado = request.form['Estado']
        LinkDrive = request.form['LinkDrive']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO reportes_enviados (CliNumDoc,RepFechEnvi,RepHorEnvi,RepTipo,LinkDrive,Estado) VALUES (%s,%s,%s,%s,%s,%s)',(CliNumDoc,RepFechEnvi,RepHorEnvi,RepTipo,LinkDrive,Estado))
        mysql.connection.commit()
        flash('reporte creado satisfactoriamente')
        return redirect(url_for('oprepor'))

#añadir servicios realizados
@app.route('/add_servicio',methods=['POST'])  
def add_servicio():
    if request.method == 'POST':
        ahora = datetime.now()
        CliNumDoc = request.form['CliNumDoc']
        IdEquipo = request.form['IdEquipo']
        SerDes = request.form['SerDes']
        fecha_actual = date(ahora.year, ahora.month, ahora.day)
        SerFech = fecha_actual
        hora_actual = time(ahora.hour, ahora.minute, ahora.second)
        SerHora = hora_actual
        SerFechAsig = request.form['SerFechAsig']
        SerHorAsig = request.form['SerHorAsig']
        SerClasifica = request.form['SerClasifica']
        UsuNumDoc = request.form['UsuNumDoc']
        Estado = request.form['Estado']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO servicios (CliNumDoc,IdEquipo,SerDes,SerFech,SerHora,SerFechAsig,SerHorAsig,SerClasifica,UsuNumDoc,Estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(CliNumDoc,IdEquipo,SerDes,SerFech,SerHora,SerFechAsig,SerHorAsig,SerClasifica,UsuNumDoc,Estado))
        mysql.connection.commit()
        flash('servicio añadido satisfactoriamente')
        return redirect(url_for('opservicio'))

#añadir usuarios
@app.route('/add_usuario',methods=['POST'])  
def add_usuario():
    if request.method == 'POST':
        ahora = datetime.now()
        UsuNom = request.form['UsuNom']
        UsuApe = request.form['UsuApe']
        UsuTipDoc = request.form['UsuTipDoc']
        UsuNumDoc = request.form['UsuNumDoc']
        UsuTipo = request.form['UsuTipo']
        UsuEstado = request.form['UsuEstado']
        UsuTel = request.form['UsuTel']
        UsuDir = request.form['UsuDir']
        UsuTipoContrat = request.form['UsuTipoContrat']
        fecha_actual = date(ahora.year, ahora.month, ahora.day)
        UsuFechRegist = fecha_actual
        hora_actual = time(ahora.hour, ahora.minute, ahora.second)
        UsuHorRegist = hora_actual
        UsuVenciContrat = request.form['UsuVenciContrat']
        UsuEstadoContrat = request.form['UsuEstadoContrat']
        UsuUser = request.form['UsuUser']
        Usupass =  request.form['Usupass']
        IdEmpresa =  request.form['IdEmpresa']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (UsuNom,UsuApe,UsuTipDoc,UsuNumDoc,UsuTipo,UsuEstado,UsuTel,UsuDir,UsuTipoContrat,UsuFechRegist,UsuHorRegist,UsuVenciContrat,UsuEstadoContrat,UsuUser,Usupass,IdEmpresa) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(UsuNom,UsuApe,UsuTipDoc,UsuNumDoc,UsuTipo,UsuEstado,UsuTel,UsuDir,UsuTipoContrat,UsuFechRegist,UsuHorRegist,UsuVenciContrat,UsuEstadoContrat,UsuUser,Usupass,IdEmpresa))
        mysql.connection.commit()
        flash('usuario guardado satisfactoriamente')
        return redirect(url_for('opuser'))


#funciones de eliminar

#eliminar clientes
@app.route('/delete-clientes/<id>')
def delete_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE CliNumDoc = {0}'.format(id))
    mysql.connection.commit()
    flash('cliente eliminado satisfactoriamente')
    return redirect(url_for('opclien'))

#eliminar empresa
@app.route('/delete-empresa/<id>')
def delete_empresa(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM empresa WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('empresa eliminada satisfactoriamente')
    return redirect(url_for('Index'))

#eliminar equipo de computo
@app.route('/delete-equipo-computo/<id>')
def delete_equipo(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM equipos_computo WHERE Id = {0}'.format(id))
    mysql.connection.commit()
    flash('equipo eliminado satisfactoriamente')
    return redirect(url_for('opequipo'))

#eliminar fotos de servicio
@app.route('/delete-fotos-servicio/<id>')
def delete_fotos(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM fotos_servicios WHERE IdFoto = {0}'.format(id))
    mysql.connection.commit()
    flash('imagen eliminada satisfactoriamente')
    return redirect(url_for('opfoto'))

#eliminar reportes
@app.route('/delete-reportes/<id>')
def delete_reportes(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM reportes_enviados WHERE IdReporte = {0}'.format(id))
    mysql.connection.commit()
    flash('reporte eliminado satisfactoriamente')
    return redirect(url_for('oprepor'))

#eliminar servicios realizados
@app.route('/delete-servicios/<id>')
def delete_servicios(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM servicios WHERE IdServicio = {0}'.format(id))
    mysql.connection.commit()
    flash('servicio eliminado satisfactoriamente')
    return redirect(url_for('opservicio'))

#eliminar usuarios
@app.route('/delete-usuarios/<id>')
def delete_usuarios(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuarios WHERE UsuNumDoc = {0}'.format(id))
    mysql.connection.commit()
    flash('usuario eliminado satisfactoriamente')
    return redirect(url_for('opuser'))


#funciones de editar

#editar clientes
@app.route('/edit-clientes/<id>')
def edit_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE CliNumDoc= {0}'.format(id))
    dataedit = cur.fetchall()
    cur2= mysql.connection.cursor()
    cur2.execute('SELECT * FROM empresa')
    dataedit2 = cur2.fetchall()
    return render_template('edit-cliente.html', cliente = dataedit[0], empresas= dataedit2)

@app.route('/update-cliente/<id>', methods=['POST'])
def update_cliente(id):
    if request.method == 'POST':
        CliNomRazSoc = request.form['CliNomRazSoc']
        CliTipoDoc = request.form['CliTipoDoc']
        CliNumDoc = request.form['CliNumDoc']
        CliDir = request.form['CliDir']
        CliTel = request.form['CliTel']
        IdEmpresa = request.form['IdEmpresa']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE clientes 
        SET CliNumDoc= %s,
            CliDir=%s,
            CliTel=%s,
            IdEmpresa=%s,
            CliNomRazSoc=%s,
            CliTipoDoc=%s
        WHERE CliNumDoc =%s
        """,(CliNumDoc,CliDir,CliTel,IdEmpresa,CliNomRazSoc,CliTipoDoc,id))
        mysql.connection.commit()
        flash('cliente actualizado satisfactoriamente')
        return redirect(url_for('opclien'))

#editar empresa
@app.route('/edit-empresa/<id>')
def edit_empresa(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empresa WHERE id= {0}'.format(id))
    dataedit = cur.fetchall()
    return render_template('edit_empresa.html', contact = dataedit[0])

@app.route('/update-empresa/<id>', methods=['POST'])
def update_empresa(id):
    if request.method == 'POST':
        EmpNomRazSoc = request.form['fullname']
        EmpTipoDoc = request.form['fullname']
        EmpNumDoc = request.form['fullname']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE empresa 
        SET EmpNomRazSoc= %s,
            EmpTipoDoc=%s,
            EmpNumDoc=%s,
        WHERE id =%s
        """,(EmpNomRazSoc,EmpTipoDoc,EmpNumDoc,id))
        mysql.connection.commit()
        flash('empresa actualizado satisfactoriamente')
        return redirect(url_for('Index'))


#editar equipo de computo
@app.route('/edit-equipo-computo/<id>')
def edit_equipo(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM equipos_computo WHERE Id= {0}'.format(id))
    dataedit = cur.fetchall()
    return render_template('edit-equipo.html', equipo = dataedit[0])

@app.route('/update-equipo-computo/<id>', methods=['POST'])
def update_equipo(id):
    if request.method == 'POST':
        IdEquipo = request.form['IdEquipo']
        NomEquipo = request.form['NomEquipo']
        DesEquipo = request.form['DesEquipo']
        CodEquipo = request.form['CodEquipo']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE equipos_computo 
        SET IdEquipo= %s,
            NomEquipo= %s,
            DesEquipo=%s,
            CodEquipo=%s
        WHERE Id =%s
        """,(IdEquipo,NomEquipo,DesEquipo,CodEquipo,id))
        mysql.connection.commit()
        flash('equipo actualizado satisfactoriamente')
        return redirect(url_for('opequipo'))


#editar fotos de servicio
@app.route('/edit-foto/<id>')
def edit_fotos(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM fotos_servicios WHERE IdFoto= {0}'.format(id))
    dataedit = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM servicios')
    data2 = cur2.fetchall()
    return render_template('edit-foto.html', foto = dataedit[0], servicios = data2)

@app.route('/update-fotos/<id>', methods=['POST'])
def update_fotos(id):
    if request.method == 'POST':
        ahora = datetime.now()
        IdServicio = request.form['IdServicio']
        FotoDes = request.form['FotoDes']
        fecha_actual = date(ahora.year, ahora.month, ahora.day)
        FotoFech = fecha_actual
        hora_actual = time(ahora.hour, ahora.minute, ahora.second)
        FotoHor = hora_actual
        FotoTipo = request.form['FotoTipo']
        Imagen = request.form['Imagen']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE fotos_servicios 
        SET IdServicio=%s,
            FotoDes= %s,
            FotoFech=%s,
            FotoHor=%s,
            FotoTipo=%s,
            Imagen=%s
        WHERE IdFoto =%s
        """,(IdServicio,FotoDes,FotoFech,FotoHor,FotoTipo,Imagen,id))
        mysql.connection.commit()
        flash('foto actualizada satisfactoriamente')
        return redirect(url_for('opfoto'))


#editar reportes
@app.route('/edit-reportes/<id>')
def edit_reportes(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM reportes_enviados WHERE IdReporte= {0}'.format(id))
    dataedit = cur.fetchall()
    cur2 = mysql.connection.cursor()
    cur2.execute('SELECT * FROM clientes')
    data2 = cur2.fetchall()
    return render_template('edit-reportes.html', reporte = dataedit[0], clientes=data2)

@app.route('/update-reportes/<id>', methods=['POST'])
def update_reportes(id):
    if request.method == 'POST':
        ahora = datetime.now()
        CliNumDoc = request.form['CliNumDoc']
        fecha_actual = date(ahora.year, ahora.month, ahora.day)
        RepFechEnvi = fecha_actual
        hora_actual = time(ahora.hour, ahora.minute, ahora.second)
        RepHorEnvi = hora_actual
        RepTipo = request.form['RepTipo']
        Estado = request.form['Estado']
        LinkDrive = request.form['LinkDrive']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE reportes_enviados
        SET CliNumDoc= %s,
            RepFechEnvi= %s,
            RepHorEnvi=%s,
            RepTipo=%s,
            LinkDrive= %s,
            Estado= %s
        WHERE IdReporte =%s
        """,(CliNumDoc,RepFechEnvi,RepHorEnvi,RepTipo,LinkDrive,Estado,id))
        mysql.connection.commit()
        flash('reporte actualizado satisfactoriamente')
        return redirect(url_for('oprepor'))


#editar servicios realizados
@app.route('/edit-servicios/<id>')
def edit_servicios(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM servicios WHERE IdServicio= {0}'.format(id))
    dataedit = cur.fetchall()
    cur2= mysql.connection.cursor()
    cur2.execute('SELECT * FROM clientes')
    dataedit2 = cur2.fetchall()
    cur3 = mysql.connection.cursor()
    cur3.execute('SELECT * FROM equipos_computo')
    dataedit3 = cur3.fetchall()
    cur4 = mysql.connection.cursor()
    cur4.execute('SELECT * FROM usuarios WHERE UsuTipo = "tecnico"')
    dataedit4 = cur4.fetchall()
    return render_template('edit-servicios.html', servicio = dataedit[0],clientes=dataedit2,equipos=dataedit3,tecnicos=dataedit4)

@app.route('/update-servicios/<id>', methods=['POST'])
def update_servicios(id):
    if request.method == 'POST':
        ahora = datetime.now()
        CliNumDoc = request.form['CliNumDoc']
        IdEquipo = request.form['IdEquipo']
        SerDes = request.form['SerDes']
        fecha_actual = date(ahora.year, ahora.month, ahora.day)
        SerFech = fecha_actual
        hora_actual = time(ahora.hour, ahora.minute, ahora.second)
        SerHora = hora_actual
        SerFechAsig = request.form['SerFechAsig']
        SerHorAsig = request.form['SerHorAsig']
        SerClasifica = request.form['SerClasifica']
        UsuNumDoc = request.form['UsuNumDoc']
        Estado = request.form['Estado']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE servicios
        SET CliNumDoc=%s,
            IdEquipo=%s,
            SerDes=%s,
            SerFech=%s,
            SerHora=%s,
            SerFechAsig=%s,
            SerHorAsig=%s,
            SerClasifica=%s,
            UsuNumDoc=%s,
            Estado=%s
        WHERE IdServicio=%s
        """,(CliNumDoc,IdEquipo,SerDes,SerFech,SerHora,SerFechAsig,SerHorAsig,SerClasifica,UsuNumDoc,Estado,id))
        mysql.connection.commit()
        flash('servicio actualizado satisfactoriamente')
        return redirect(url_for('opservicio'))


#editar usuarios
@app.route('/edit-usuarios/<id>')
def edit_usuarios(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios WHERE UsuNumDoc= {0}'.format(id))
    dataedit = cur.fetchall()
    cur2= mysql.connection.cursor()
    cur2.execute('SELECT * FROM empresa')
    dataedit2 = cur2.fetchall()
    return render_template('edit-user.html', usuario = dataedit[0], empresas= dataedit2)

@app.route('/update-usuarios/<id>', methods=['POST'])
def update_usuarios(id):
    if request.method == 'POST':
        ahora = datetime.now()
        UsuNom = request.form['UsuNom']
        UsuApe = request.form['UsuApe']
        UsuTipDoc = request.form['UsuTipDoc']
        UsuNumDoc = request.form['UsuNumDoc']
        UsuTipo = request.form['UsuTipo']
        UsuEstado = request.form['UsuEstado']
        UsuTel = request.form['UsuTel']
        UsuDir = request.form['UsuDir']
        UsuTipoContrat = request.form['UsuTipoContrat']
        fecha_actual = date(ahora.year, ahora.month, ahora.day)
        UsuFechRegist = fecha_actual
        hora_actual = time(ahora.hour, ahora.minute, ahora.second)
        UsuHorRegist = hora_actual
        UsuVenciContrat = request.form['UsuVenciContrat']
        UsuEstadoContrat = request.form['UsuEstadoContrat']
        Usupass =  request.form['Usupass']
        IdEmpresa =  request.form['IdEmpresa']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE usuarios 
        SET UsuNom= %s,
            UsuApe=%s,
            UsuTipDoc=%s,
            UsuNumDoc=%s,
            UsuTipo= %s,
            UsuEstado=%s,
            UsuTel=%s,
            UsuDir=%s,
            UsuTipoContrat= %s,
            UsuFechRegist=%s,
            UsuHorRegist=%s,
            UsuVenciContrat=%s,
            UsuEstadoContrat=%s,
            Usupass=%s,
            IdEmpresa=%s
        WHERE UsuNumDoc =%s
        """,(UsuNom,UsuApe,UsuTipDoc,UsuNumDoc,UsuTipo,UsuEstado,UsuTel,UsuDir,UsuTipoContrat,UsuFechRegist,UsuHorRegist,UsuVenciContrat,UsuEstadoContrat,Usupass,IdEmpresa,id))
        mysql.connection.commit()
        flash('usuario actualizado satisfactoriamente')
        return redirect(url_for('opuser'))

#verificamos si esta en la principal
#es decir si el archivo que empieza a ejecutar es app.py pues empieza a ejecutar nuestro servidor
if __name__ == '__main__':
    #le damos el puerto y debug
    app.run(port = 5500, debug = True)