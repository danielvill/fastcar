from flask import flash, Flask, session, render_template, request,Response ,jsonify, redirect, url_for,send_file
from controllers.basedatos import Conexion as dbase
from modules.admin import Admin
from modules.carreras import Carreras
from modules.clientes import Clientes
from modules.conductores import Conductores
from modules.unidades import Unidades
from modules.usuarios import Usuario
from modules.guardias import Guardias
from modules.media import Media
from reportlab.pdfgen import canvas # *pip install reportlab
from reportlab.lib.pagesizes import letter #* pip install reportlab 
from markupsafe import escape
from modules.comentario import Comentario
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer ,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
#* Este codigo lo reemplazas con la ip de la pc y el puerto que deseas que se abra pero en la linea de comando
#* Correr el servidor flask run --host=0.0.0.0 --port=4848 

db = dbase()

app = Flask(__name__)
app.secret_key = 'fastcar'


@app.route('/',methods=['GET','POST'])
def run():
    return redirect(url_for('index'))


@app.route('/admin/home',methods=['GET','POST'])
def home():
    # Verifica si el usuario está en la sesión
    if 'username' in session:
        return render_template('admin/home.html')
    else:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))  # Redirige al usuario al inicio si no está en la sesión

@app.route('/logout')
def logout():
    # Elimina el usuario de la sesión si está presente
    session.pop('username', None)
    return redirect(url_for('index'))

#* Ingreso al sistema

@app.route('/index',methods=['GET','POST'])
def index():
    
    if request.method == 'POST':
        usuario = request.form['nombre']
        password = request.form['clave']
        usuario_fo = db.admin.find_one({'nombre':usuario,'clave':password})
        operador = db.usuarios.find_one({'nombre':usuario,'clave':password})
        if usuario_fo:
            session["username"]= usuario
            return redirect(url_for('home'))
        elif operador:
            session["username"]= usuario
            return redirect(url_for('opercarrera'))
        else:
            flash("Contraseña incorrecta")
            return redirect(url_for('index'))
    else:
        return render_template('index.html')

#*Ingreso Administradores
@app.route('/admin/in_admin',methods=['GET','POST'])
def inadmin():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))  # Redirige al usuario al inicio si no está en la sesión

    if request.method == 'POST':
        admin = db['admin']
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        rol = request.form['rol']
        email = request.form['email']
        clave = request.form['clave']
        
        
        exist_nombre = admin.find_one({'nombre':nombre})
        exist_cedula = admin.find_one({'cedula':cedula })

        if exist_nombre:
            flash("Ya existe un Administrador con ese nombre ")
            return redirect(url_for('inadmin'))
        
        elif exist_cedula:
            flash("Ya existe un Administrador con ese cedula ")
            return redirect(url_for('inadmin'))
        
        else:
                # Si no existe, inserta el nuevo administrador
                regis = Admin(cedula, nombre, rol ,email, clave)
                admin.insert_one(regis.AdmDBCollection())
                flash("Enviado a la base de datos ")
                return redirect(url_for('inadmin')) # Direccionamiento para la pagina que es /admin/in_admin
    else:
        return render_template('admin/in_admin.html') #* Cargado de la pagina 

#*Vista Administradores
@app.route('/admin/admin',methods=['GET','POST'])
def admin():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    # Redirige al usuario al inicio si no está en la sesión
    admin =db ['admin'].find()
    return render_template('/admin/admin.html',admin=admin)#* Vista para los administradores
    
        

#* Editar y eliminar administradores
@app.route('/delete_adm/<string:ad_name>')
def elitad(ad_name):
    ad = db['admin']
    ad.delete_one({'nombre':ad_name})
    return redirect(url_for('admin'))

@app.route('/edit_ad/<string:ad_name>', methods=['GET', 'POST'])
def editad(ad_name):
    ad = db['admin']
    cedula = request.form['cedula']
    nombre = request.form['nombre']
    rol = request.form['rol']
    email = request.form['email']
    clave = request.form['clave']

    if cedula and nombre and rol and email and clave:
        ad.update_one({'cedula':ad_name},{'$set':{'cedula':cedula,'nombre':nombre,'rol':rol,'email':email,'clave':clave}})
        print("nada")
        return redirect(url_for('admin'))

    else:
        return render_template("admin/admin.html")

#*Ingreso de cliente
@app.route('/admin/in_cliente',methods=['GET','POST'])
def incliente():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))  # Redirige al usuario al inicio si no está en la sesión
    
    if request.method == 'POST':
        cliente = db['clientes']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        coordenadas = request.form['coordenadas']
        cedula = request.form['cedula']
        referencia = request.form['referencia']
        comentario = request.form['comentario']
        
        exist_nombre = cliente.find_one({'nombre':nombre})
        exist_cedula = cliente.find_one({'cedula':cedula })
        
        if exist_nombre:
            flash("Ya existe un cliente con ese nombre ")
            return redirect(url_for('incliente'))
        
        elif exist_cedula:
            flash("Ya existe un cliente con ese cedula ")
            return redirect(url_for('incliente'))
        
        else:
            regis = Clientes(nombre, telefono, direccion, coordenadas, cedula, referencia, comentario)
            cliente.insert_one(regis.CliDBCollection())
            flash("Enviado a la base de datos ")
            return redirect(url_for('incliente'))
        
    else: 
        return render_template('/admin/in_cliente.html') #* Cargado de la pagina 
    

def generar_pdf_clientes(datos):
    pagesize = (2000, 2000)
    doc = SimpleDocTemplate("clientes.pdf", pagesize=pagesize)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading3']
    left_aligned_style.alignment = 0  # 1 = TA_CENTER

    # Agrega la imagen
    imagen = Image('static/img/fas.jpeg', width=100, height=50)
    imagen.hAlign = 'LEFT'
    story.append(imagen)
    

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    

    # Agrega el título
    title = Paragraph("<h3>Compañia de Taxi</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    
    title2 = Paragraph("<h1>TRANSNEWFASTCAR S.A.</h1>", left_aligned_style)
    story.append(title2)

    # Agrega otro salto de línea
    
    title3 = Paragraph("<h3>Machala - EL ORO -  Ecuador</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))
    # Prepara los datos para la tabla
    data = [["Nombre", "Telefono", "Direccion", "Coordenadas", "Cedula", "Referencia", "Comentario"]]  # Encabezados

    for dato in datos:
        row = [dato['nombre'], dato['telefono'], dato['direccion'], dato['coordenadas'], dato['cedula'], dato['referencia'], dato['comentario']]
        data.append(row)

    # Crea la tabla
    table = Table(data, colWidths=[300, 200, 200, 300]) 

    # Formatea la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    # Agrega la tabla al documento
    story.append(table)

    doc.build(story)

#* Filtrar por nombre del cliente 
@app.route('/admin/reporte/r_clientes_nombre', methods=['GET'])
def r_cliente_nombre():
    pagesize = (1000, 1000)
    doc = SimpleDocTemplate("clientes.pdf", pagesize=pagesize)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading3']
    left_aligned_style.alignment = 0  # 1 = TA_CENTER

    # Agrega la imagen
    imagen = Image('static/img/fas.jpeg', width=100, height=50)
    imagen.hAlign = 'LEFT'
    story.append(imagen)
    

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    

    # Agrega el título
    title = Paragraph("<h3>Compañia de Taxi</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    

    title2 = Paragraph("<h1>TRANSNEWFASTCAR S.A.</h1>", left_aligned_style)
    story.append(title2)

    # Agrega otro salto de línea
    
    title3 = Paragraph("<h3>Machala - EL ORO -  Ecuador</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))

    nombre = request.args.get('cedula', default=None, type=str)
    
    if nombre:
        clie = db['clientes'].find({'cedula': nombre})
    else:
        clie = db['clientes'].find()

    generar_pdf_clientes(clie)
    return send_file('clientes.pdf', as_attachment=True)



@app.route('/admin/cliente',methods=['GET','POST'])
def cliente():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    clie = db['clientes'].find()
    return render_template('/admin/cliente.html', clientes=clie)


@app.route('/admin/reporte/r_clientes', methods=['GET'])
def r_cliente():
    clie = db['clientes'].find()
    generar_pdf_clientes(clie)
    return send_file('clientes.pdf', as_attachment=True)
    
#*Editar y eliminar cliente
@app.route('/delete_cli/<string:cli_name>')
def elitcli(cli_name):
    cli = db['clientes']
    cli.delete_one({'nombre':cli_name})
    return redirect(url_for('cliente'))

@app.route('/edit_cli/<string:cli_name>', methods=['GET', 'POST'])
def editcli(cli_name):
    cli = db['clientes']

    nombre = request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    coordenadas = request.form['coordenadas']
    cedula = request.form['cedula']
    referencia = request.form['referencia']
    comentario = request.form['comentario']
    
    if  nombre and telefono and direccion and coordenadas and cedula and referencia and comentario:
        cli.update_one({'cedula':cli_name},{'$set':{'nombre':nombre,'telefono':telefono,'direccion':direccion,'coordenadas':coordenadas,'cedula':cedula,'referencia':referencia,'comentario':comentario}})
        return redirect(url_for('cliente'))
    else:
        return render_template("admin/cliente.html")

#*Ingreso de usuarios
@app.route('/admin/in_usuario',methods=['GET','POST'])
def inusuario():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        usuario = db['usuarios']
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        rol = request.form['rol']
        email = request.form['email']
        clave = request.form['clave']
        
        exist_nombre = usuario.find_one({'nombre':nombre})
        exist_cedula = usuario.find_one({'cedula':cedula })
        
        if exist_nombre:
            flash("Ya existe un usuario con ese nombre ")
            return redirect(url_for('inusuario'))
        
        elif exist_cedula:
            flash("Ya existe un usuario con ese cedula ")
            return redirect(url_for('inusuario'))

        else:
            regis = Usuario(cedula, nombre, rol,email, clave)
            usuario.insert_one(regis.UsuDBCollection())
            return redirect(url_for('inusuario')) # Direccionamiento para la pagina que es /admin/in_usuario
        
    else:
        return render_template('/admin/in_usuario.html') #* Cargado de la pagina
    
#*Vista de usuarios
@app.route('/admin/usuarios',methods=['GET','POST'])
def usuario():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    usua = db['usuarios'].find()
    return render_template('/admin/usuarios.html',usuarios=usua)# Vista para usuarios

#*Editar y eliminar usuarios
@app.route('/delete_usu/<string:usu_name>')
def elitusu(usu_name):
    usu = db['usuarios']
    usu.delete_one({'nombre':usu_name})
    return redirect(url_for('usuario'))

@app.route('/edit_usu/<string:usu_name>', methods=['GET', 'POST'])
def editusu(usu_name):
    usu = db['usuarios']
    cedula = request.form['cedula']
    nombre = request.form['nombre']
    rol = request.form['rol']
    email = request.form['email']
    clave = request.form['clave']
    
    if cedula and nombre and rol and email and clave:
        usu.update_one({'cedula':usu_name},{'$set':{'cedula':cedula,'nombre':nombre,'rol':rol,'email':email,'clave':clave}})
        return redirect(url_for('usuario'))
    else:
        return render_template("admin/usuarios.html")
    

#*Ingreso de conductores
@app.route('/admin/in_conductores',methods=['GET','POST'])
def inconductores():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        conductor = db['conductores']
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        em_nombre = request.form['em_nombre']
        em_telefono = request.form['em_telefono']
        em_relacion = request.form['em_relacion']
        clave = request.form['clave']
        licencia = request.form['licencia']

        exist_nombre = conductor.find_one({'nombre':nombre})
        exist_cedula = conductor.find_one({'cedula':cedula })
        
        if exist_nombre:
            flash("Ya existe un conductor con ese nombre ")
            return redirect(url_for('inconductores'))
        
        elif exist_cedula:
            flash("Ya existe un conductor con esa cedula ")
            return redirect(url_for('inconductores'))
        
        if cedula and nombre and email and telefono and direccion and em_nombre and em_relacion and clave and licencia:
            regis = Conductores(cedula, nombre, email, telefono, direccion, em_nombre, em_telefono, em_relacion, clave, licencia)
            conductor.insert_one(regis.CondDBCollection())
            flash("Enviado a la base de datos ")
            return redirect(url_for('inconductores')) # Direccionamiento para la pagina que es /admin/in_conductores
    else: 
        return render_template('/admin/in_conductores.html') #* Cargado de la pagina

#*Vista de Conductores
@app.route('/admin/conductores',methods=['GET','POST'])
def conductores():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    condu = db['conductores'].find()
    return render_template('/admin/conductores.html',conductores=condu)# Vista para conductores

# * Editar y Eliminar Conductores
@app.route('/delete_cond/<string:cond_name>')
def elitcondu(cond_name):
    cond = db['conductores']
    cond.delete_one({'nombre':cond_name})
    return redirect(url_for('conductores'))

@app.route('/edit_cond/<string:cond_name>', methods=['GET', 'POST'])
def editcondu(cond_name):
    cond = db['conductores']
    cedula = request.form['cedula']
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    em_nombre = request.form['em_nombre']
    em_telefono = request.form['em_telefono']
    em_relacion = request.form['em_relacion']
    clave = request.form['clave']
    licencia = request.form['licencia']
    
    if cedula and nombre  and email and telefono and direccion and em_nombre and em_relacion and clave and licencia:
        cond.update_one({'cedula':cond_name},{'$set':{'cedula':cedula,'nombre':nombre,'email':email,'telefono':telefono,'direccion':direccion,'em_nombre':em_nombre,'em_telefono':em_telefono,'em_relacion':em_relacion,'clave':clave,'licencia':licencia}})
        return redirect(url_for('conductores'))
    else:
        return render_template("admin/conductores.html")

#*Ingreso de unidades
@app.route('/admin/in_unidades',methods=['GET','POST'])
def inunidades():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        uni = db['unidades']
        unidad =request.form['unidad']
        placa = request.form['placa']
        modelo = request.form['modelo']
        marca = request.form['marca']
        color = request.form['color']
        observacion = request.form['observacion']
        
        es_fecha = request.form['es_fecha']

        exist_unidad = uni.find_one({'unidad':unidad})
        exist_placa = uni.find_one({'placa':placa })
        if exist_unidad:
            flash("Ya existe esa unidad ")
            return redirect(url_for('inunidades'))
        elif exist_placa:
            flash("Ya existe esa placa ")
            return redirect(url_for('inunidades'))
        if unidad and placa and modelo and marca and color  and observacion  and es_fecha:
            regis = Unidades( unidad,placa, modelo, marca, color, observacion, es_fecha)
            uni.insert_one(regis.UniDBCollection())
            flash("Enviado a la base de datos ")
            return redirect(url_for('inunidades')) # Direccionamiento para la pagina que es /admin/in_unidades
    else: #
        return render_template('/admin/in_unidades.html') #* Cargado de la pagina

#*Vista de unidades
@app.route('/admin/unidades',methods=['GET','POST'])
def unidades(): 
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    uni = db['unidades'].find()
    return render_template('/admin/unidades.html',unidades=uni)# Vista de unidades

#*Editar y eliminar unidades
@app.route('/delete_uni/<string:uni_name>')
def elituni(uni_name):
    uni = db['unidades']
    uni.delete_one({'placa':uni_name})
    return redirect(url_for('unidades'))

@app.route('/edit_uni/<string:uni_name>', methods=['GET', 'POST'])
def edituni(uni_name):
    uni = db['unidades']
    unidad = request.form['unidad']
    placa = request.form['placa']
    modelo = request.form['modelo']
    marca = request.form['marca']
    color = request.form['color']
    observacion = request.form['observacion']
    es_fecha = request.form['es_fecha']
    
    if unidad and placa and modelo and marca and color  and observacion  and es_fecha:
        uni.update_one({'unidad':uni_name},{'$set':{'unidad':unidad,'placa':placa,'modelo':modelo,'marca':marca,'color':color,'observacion':observacion,'es_fecha':es_fecha}})
        return redirect(url_for('unidades'))
    else:
        return render_template("admin/unidades.html")


#*  Ingresar de Carreras
@app.route('/admin/in_carreras',methods=['GET','POST'])
def incarreras():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        carrera = db ['carreras']
        media = db['media']
        cliente = request.form['cliente']
        unidad =request.form['unidad']
        comentario = request.form['comentario']
        fecha = request.form['fecha']
        hora = request.form['hora']

        if cliente and unidad and comentario and fecha and hora:
            regis = Carreras(cliente, unidad ,comentario,fecha, hora) 
            carrera.insert_one(regis.CareDBCollection())
            media.delete_one({'unidad':unidad})
            flash("Guardado exitosamente")
            return redirect(url_for('incarreras')) # Direccionamiento para la pagina que es /admin/in_carreras
    else: #
        return render_template('/admin/in_carreras.html',clientes=cliu(),unidades=uni(),media=med()) #* Cargado de la pagina
        
# *Estadistica
def preparar_datos(results):
    labels = []
    data = []
    for result in results:
        labels.append(result['_id'])
        data.append(result['count'])
    return labels, data

db, results = dbase() 
labels, data = preparar_datos(results)




@app.route('/admin/carreras',methods=['GET','POST'])
def carreras():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    # Obtén los resultados de la agregación y prepara los datos para Chart.js
    db, results = dbase()
    labels, data = preparar_datos(results)

    carre = db['carreras'].find()
    return render_template('/admin/carreras.html',carreras=carre, labels=labels, data=data)

#* Editar y Eliminar Carreras
@app.route('/delete_car/<string:car_name>')
def elitcarre(car_name):
    carre = db['carreras']
    carre.delete_one({'cliente':car_name})
    return redirect(url_for('carreras'))

@app.route('/edit_car/<string:car_name>', methods=['GET', 'POST'])
def editcarre(car_name):
    carre = db['carreras']
    cliente = request.form['cliente']
    unidad =request.form['unidad']
    comentario = request.form['comentario']
    fecha = request.form['fecha']
    hora = request.form['hora']

    if cliente and unidad and comentario and fecha and hora:
        carre.update_one({'cliente':car_name},{'$set':{'cliente':cliente,"unidad":unidad,"comentario":comentario,"fecha":fecha,"hora":hora}})
        return redirect(url_for('carreras'))
    else:
        return render_template("admin/carreras.html")


#* Reportes de Carreras
# * Registra la fuente
def generar_pdf_carreras(datos):
    doc = SimpleDocTemplate("carreras.pdf", pagesize=letter)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading3']
    left_aligned_style.alignment = 0  # 1 = TA_CENTER

    # Agrega la imagen
    imagen = Image('static/img/fas.jpeg', width=100, height=50)
    imagen.hAlign = 'LEFT'
    story.append(imagen)
    

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    
    # Agrega el título
    title = Paragraph("<h3>Compañia de Taxi</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    
    title2 = Paragraph("<h1>TRANSNEWFASTCAR S.A.</h1>", left_aligned_style)
    story.append(title2)

    # Agrega otro salto de línea

    title3 = Paragraph("<h3>Machala - EL ORO -  Ecuador</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))

    # Prepara los datos para la tabla
    data = [["Cliente", "Unidad", "Comentario", "Fecha", "Hora"]]  # Encabezados

    for dato in datos:
        row = [dato['cliente'], dato['unidad'], dato['comentario'], dato['fecha'], dato['hora']]
        data.append(row)

    # Crea la tabla
    table = Table(data, colWidths=[100, 150, 100, 100]) 

    # Formatea la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    # Agrega la tabla al documento
    story.append(table)

    doc.build(story)


#* Filtrar por unidad 
@app.route('/admin/reporte/r_carreras_unidad', methods=['GET'])
def r_carreras_unidad():
    doc = SimpleDocTemplate("carreras.pdf", pagesize=letter)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading1']
    left_aligned_style.alignment = 0  # 1 = TA_CENTER


    # Agrega la imagen
    imagen = Image('static/img/fas.jpeg', width=100, height=50)
    imagen.hAlign = 'LEFT'
    story.append(imagen)
    story.append(Spacer(1, 12))

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    


    # Agrega el título
    title = Paragraph("<h3>Compañia de Taxi</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    

    title2 = Paragraph("<h1>TRANSNEWFASTCAR S.A.</h1>", left_aligned_style)
    story.append(title2)

    # Agrega otro salto de línea
    

    title3 = Paragraph("<h3>Machala - EL ORO -  Ecuador</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))

    # Prepara los datos no como tabla
    client = request.args.get('hora', default=None, type=str)
    
    
    if client is not None:
        clie = db['carreras'].find({'hora': client})
    else:
        clie = db['carreras'].find()

    generar_pdf_carreras(clie)
    return send_file('carreras.pdf', as_attachment=True)




@app.route('/admin/reporte/r_carreras', methods=['GET'])
def r_carreras():
    carre = db['carreras'].find()
    generar_pdf_carreras(carre)
    return send_file('carreras.pdf', as_attachment=True)

# * Select para carreras
def cliu():
    clientes = db.clientes.find({},{"nombre":1})
    return [clientes["nombre"]for clientes in clientes]

def uni():
    unidades = db.unidades.find({},{"unidad":1})
    return [unidades["unidad"]for unidades in unidades]
def con():
    conductores = db.conductores.find({},{"nombre":1})
    return [conductores["nombre"]for conductores in conductores]

def med():
    medias = db.media.find({},{"unidad":1})
    return [medias["unidad"]for medias in medias]
    
#* Ingreso de guardias
@app.route('/admin/in_guardias',methods=['GET','POST'])
def inguardia():
    if request.method == 'POST':
        carrera = db ['guardias']
        unidad =request.form['unidad']

        if  unidad  :
            regis = Guardias( unidad  )
            carrera.insert_one(regis.GuardDBCollection())
            return redirect(url_for('inguardia')) 
    else: 
        return render_template('/admin/in_guardias.html',unidades=uni(),conductores=con()) #* Cargado de la pagina
    

@app.route('/admin/guardias',methods=['GET','POST'])
def guardia():
    # * Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        media = db['media']
        guar= db['guardias']
        unidad =request.form['unidad']
        if unidad :
            registro = Media( unidad )
            media.insert_one(registro.MediaDBCollection())
            
            guar.delete_one({'unidad':unidad})
            return redirect(url_for('incarreras'))
    else: 
        guardia = db['guardias'].find()
        return render_template('/admin/guardias.html',guardias=guardia)


# * Reordenamiento 
@app.route('/admin/guardias/reorder', methods=['POST'])
def handle_reorder():
    data = request.get_json()
    from_index = data['from']
    to_index = data['to']

    # Aquí es donde debes actualizar tus datos en la base de datos.
    # Por ejemplo, podrías reordenar tus datos y luego guardarlos.
    # Este es solo un ejemplo, necesitarás adaptarlo a tus necesidades específicas.

    guardias = list(db['guardias'].find())
    guardia_to_move = guardias[from_index]
    guardias.remove(guardia_to_move)
    guardias.insert(to_index, guardia_to_move)

    for i, guardia in enumerate(guardias):
        db['guardias'].update_one({'_id': guardia['_id']}, {'$set': {'order': i}})

    return 'Reorder successful!', 200

# * Delete de Guardias

@app.route('/delete_gua/<string:gua_name>')
def elitguardia(gua_name):
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    guardia = db['guardias']
    guardia.delete_one({'unidad':gua_name})
    return redirect(url_for('guardia'))


#* Comentario
@app.route('/admin/comentario',methods=['GET','POST'])
def comentario():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        guar= db['comentario']
        unidad =request.form['unidad']
        comentario = request.form['comentario']
        fecha = request.form['fecha']
        hora = request.form['hora']


        if unidad and comentario and fecha and hora:
            registro = Comentario( unidad , comentario , fecha , hora)
            guar.insert_one(registro.ComeDBCollection())
            return redirect(url_for('comentario'))
    else: 
        return render_template('/admin/comentario.html',unidades=uni())

# * Comentarios
#* Reportes de Comentarios
# * Registra la fuente
def generar_pdf_comentarios(datos):
    doc = SimpleDocTemplate("comentarios.pdf", pagesize=letter)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading3']
    left_aligned_style.alignment = 0  # 0 = TA_LEFT


    
    # Agrega la imagen
    imagen = Image('static/img/fas.jpeg', width=100, height=50)
    imagen.hAlign = 'LEFT'
    story.append(imagen)
    #story.append(Spacer(1, 12))

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    #story.append(Spacer(1, 12))
    
    # Agrega el título
    title = Paragraph("<h3>Compañia de Taxi</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    #story.append(Spacer(1, 12))

    title2 = Paragraph("<h1>TRANSNEWFASTCAR S.A.</h1>", left_aligned_style)
    story.append(title2)

    # Agrega otro salto de línea
    #story.append(Spacer(1, 12))

    title3 = Paragraph("<h3>Machala - EL ORO -  Ecuador</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))
    
    # Prepara los datos para la tabla
    data = [["Unidad", "Comentario", "Fecha", "Hora"]]  # Encabezados

    for dato in datos:
        row = [dato['unidad'], dato['comentario'], dato['fecha'], dato['hora']]
        data.append(row)

    # Crea la tabla
    table = Table(data, colWidths=[100, 150, 100, 100]) 

    # Formatea la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    # Agrega la tabla al documento
    story.append(table)

    doc.build(story)

# * Registro de comentario
#* Filtrar por unidad 
@app.route('/admin/reporte/r_comentarios_unidad', methods=['GET'])
def r_comentarios_unidad():
    doc = SimpleDocTemplate("comentarios.pdf", pagesize=letter)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading3']
    left_aligned_style.alignment = 0  # 1 = TA_CENTER

    # Agrega la imagen
    imagen = Image('static/img/fas.jpeg', width=100, height=50)
    imagen.hAlign = 'LEFT'
    story.append(imagen)
    story.append(Spacer(1, 12))

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    
    
    
    # Agrega el título
    title = Paragraph("<h3>Compañia de Taxi</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    

    title2 = Paragraph("<h1>TRANSNEWFASTCAR S.A.</h1>", left_aligned_style)
    #story.append(title2)

    # Agrega otro salto de línea
    

    title3 = Paragraph("<h3>Machala - EL ORO -  Ecuador</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))

    # Prepara los datos no como tabla
    client = request.args.get('hora', default=None, type=str)
    
    
    if client is not None:
        clie = db['comentario'].find({'hora': client})
    else:
        clie = db['comentario'].find()

    generar_pdf_comentarios(clie)
    return send_file('comentarios.pdf', as_attachment=True)



#* Vista comentarios
@app.route('/admin/vi_comentario',methods=['GET','POST'])
def vi_comentario():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    come = db['comentario'].find()
    return render_template('/admin/vi_comentario.html',comentario=come)# Vista de carreras

#* Editar y Eliminar Comentario
@app.route('/delete_come/<string:come_name>')
def elitcome(come_name):
    come = db['comentario']
    come.delete_one({'unidad':come_name})
    return redirect(url_for('vi_comentario'))

@app.route('/edit_come/<string:come_name>', methods=['GET', 'POST'])
def editcome(come_name):
    come = db['comentario']
    unidad =request.form['unidad']
    comentario = request.form['comentario']
    fecha = request.form['fecha']
    hora = request.form['hora']

    if  unidad and comentario and fecha and hora:
        come.update_one({'unidad':come_name},{'$set':{"unidad":unidad,"comentario":comentario,"fecha":fecha,"hora":hora}})
        return redirect(url_for('comentario'))
    else:
        return render_template("admin/vi_comentario.html")




#*************** Ingreso de Operadores ****************************


#* Bienvenida
@app.route('/operador/home',methods=['GET','POST'])
def casa():
    # Verifica si el usuario está en la sesión
    if 'username' in session:
        return render_template('operador/home.html')
    else:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))

#* Operadores Carreras
@app.route('/operador/in_carreras',methods=['GET','POST'])
def opercarrera():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        carrera = db ['carreras']
        media = db['media']
        cliente = request.form['cliente']
        unidad =request.form['unidad']
        comentario = request.form['comentario']
        fecha = request.form['fecha']
        hora = request.form['hora']

        if cliente and unidad and comentario and fecha and hora:
            regis = Carreras(cliente, unidad ,comentario,fecha, hora) 
            carrera.insert_one(regis.CareDBCollection())
            media.delete_one({'unidad':unidad})
            flash("Guardado exitosamente")
            return redirect(url_for('operacarrera')) # Direccionamiento para la pagina que es /admin/in_carreras
    else: #
        return render_template('/operador/in_carreras.html',clientes=cliu(),unidades=uni(),media=med()) #* Cargado de la pagina

#* Editar y Eliminar Carreras
@app.route('/deleteop_car/<string:car_name>')
def elitopcarre(car_name):
    carre = db['carreras']
    carre.delete_one({'cliente':car_name})
    return redirect(url_for('operacarrera'))

@app.route('/edit_opcar/<string:car_name>', methods=['GET', 'POST'])
def editopcarre(car_name):
    carre = db['carreras']
    cliente = request.form['cliente']
    unidad =request.form['unidad']
    comentario = request.form['comentario']
    fecha = request.form['fecha']
    hora = request.form['hora']

    if cliente and unidad and comentario and fecha and hora:
        carre.update_one({'cliente':car_name},{'$set':{'cliente':cliente,"unidad":unidad,"comentario":comentario,"fecha":fecha,"hora":hora}})
        return redirect(url_for('operacarrera'))
    else:
        return render_template("operador/carreras.html")


#* Vista de Carreras Operadores
@app.route('/operador/carreras',methods=['GET','POST'])
def operacarrera():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    # Obtén los resultados de la agregación y prepara los datos para Chart.js
    db, results = dbase()
    labels, data = preparar_datos(results)

    carre = db['carreras'].find()
    return render_template('/operador/carreras.html',carreras=carre, labels=labels, data=data)# Vista de carreras    


#* Clientes
@app.route('/operador/in_clientes',methods=['GET','POST'])
def opcliente():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        cliente = db['clientes']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        coordenadas = request.form['coordenadas']
        cedula = request.form['cedula']
        referencia = request.form['referencia']
        comentario = request.form['comentario']
        
        exist_nombre = cliente.find_one({'nombre':nombre})
        exist_cedula = cliente.find_one({'cedula':cedula })

        if exist_nombre:
            flash("Ya existe un cliente con ese nombre ")
            return redirect(url_for('opcliente'))
        elif exist_cedula:
            flash("Ya existe un cliente con ese cedula ")
            return redirect(url_for('opcliente'))
        else:
            regis = Clientes(nombre, telefono, direccion, coordenadas, cedula, referencia, comentario)
            cliente.insert_one(regis.CliDBCollection())
            flash("Enviado a la base de datos ")
            return redirect(url_for('opcliente')) 
    else: 
        return render_template('/operador/in_clientes.html') #* Cargado de la pagina    

#*Vista de clientes
@app.route('/operador/clientes',methods=['GET','POST'])
def opercliente():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    clie = db['clientes'].find()
    return render_template('/operador/clientes.html', clientes=clie)    

#*Editar y eliminar cliente
@app.route('/delete_opcli/<string:cli_name>')
def elitopcli(cli_name):
    cli = db['clientes']
    cli.delete_one({'nombre':cli_name})
    return redirect(url_for('opercliente'))

@app.route('/edit_opcli/<string:cli_name>', methods=['GET', 'POST'])
def editopcli(cli_name):
    cli = db['clientes']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    coordenadas = request.form['coordenadas']
    cedula = request.form['cedula']
    referencia = request.form['referencia']
    comentario = request.form['comentario']
    
    if nombre and telefono and direccion and coordenadas and cedula and referencia and comentario:
        cli.update_one({'cedula':cli_name},{'$set':{'nombre':nombre,'telefono':telefono,'direccion':direccion,'coordenadas':coordenadas,'cedula':cedula,'referencia':referencia,'comentario':comentario}})
        return redirect(url_for('opercliente'))
    else:
        return render_template("/operador/clientes.html")

#* Guardias Operadores
@app.route('/operador/in_guardias',methods=['GET','POST'])
def opguardia():
    if request.method == 'POST':
        carrera = db ['guardias']
        unidad =request.form['unidad']
        if  unidad  :
            regis = Guardias( unidad  )
            carrera.insert_one(regis.GuardDBCollection())
            return redirect(url_for('opguardia')) 
    else: #
        return render_template('/operador/in_guardias.html',unidades=uni(),conductores=con()) #* Cargado de la pagina


#*Vista de Guardias Operadores 
@app.route('/operador/guardias',methods=['GET','POST'])
def opeguardia():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        media = db['media']
        guar= db['guardias']
        unidad =request.form['unidad']
        if unidad :
            registro = Media( unidad )
            media.insert_one(registro.MediaDBCollection())
            
            guar.delete_one({'unidad':unidad})
            return redirect(url_for('opercarrera'))
    else: 
        guardia = db['guardias'].find()
        return render_template('/operador/guardias.html',guardias=guardia)


# * Delete de Guardias de Operadores

@app.route('/delete_opgua/<string:gua_name>')
def elitopguardia(gua_name):
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    guardia = db['guardias']
    guardia.delete_one({'unidad':gua_name})
    return redirect(url_for('opeguardia'))



#* Operadores Unidades
@app.route('/operador/in_unidades',methods=['GET','POST'])
def inopunidades():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        uni = db['unidades']
        unidad =request.form['unidad']
        placa = request.form['placa']
        modelo = request.form['modelo']
        marca = request.form['marca']
        color = request.form['color']
        observacion = request.form['observacion']
        es_fecha = request.form['es_fecha']
        
        exist_unidad = uni.find_one({'unidad':unidad})
        exist_placa = uni.find_one({'placa':placa })
        if exist_unidad:
            flash("Ya existe esa unidad")
            return redirect(url_for('inopunidades'))
        elif exist_placa:
            flash("Ya existe esa placa")
            return redirect(url_for('inopunidades'))

        if unidad and placa and modelo and marca and color  and observacion  and es_fecha:
            regis = Unidades( unidad,placa, modelo, marca, color, observacion, es_fecha)
            uni.insert_one(regis.UniDBCollection())
            flash("Enviado a la base de datos ")
            return redirect(url_for('inopunidades')) # Direccionamiento para la pagina que es /admin/in_unidades
    else: #
        return render_template('/operador/in_unidades.html') #* Cargado de la pagina

#*Vista de unidades Operadores
@app.route('/operador/unidades',methods=['GET','POST'])
def op_unidades():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    uni = db['unidades'].find()
    return render_template('/operador/unidades.html',unidades=uni)# Vista de unidades

#*Editar y eliminar unidades Operadores
@app.route('/delete_uniop/<string:uni_name>')
def elituniop(uni_name):
    uni = db['unidades']
    uni.delete_one({'placa':uni_name})
    return redirect(url_for('op_unidades'))

@app.route('/edit_uniop/<string:uni_name>', methods=['GET', 'POST'])
def edituniop(uni_name):
    uni = db['unidades']
    unidad = request.form['unidad']
    placa = request.form['placa']
    modelo = request.form['modelo']
    marca = request.form['marca']
    color = request.form['color']
    observacion = request.form['observacion']
    es_fecha = request.form['es_fecha']
    
    if unidad and placa and modelo and marca and color  and observacion and  es_fecha:
        uni.update_one({'unidad':uni_name},{'$set':{'unidad':unidad,'placa':placa,'modelo':modelo,'marca':marca,'color':color,'observacion':observacion,'es_fecha':es_fecha}})
        return redirect(url_for('op_unidades'))
    else:
        return render_template("operador/unidades.html")


#* Ingresar Comentario Operadores
    
@app.route('/operador/comentario',methods=['GET','POST'])
def opcomentario():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        guar= db['comentario']
        unidad =request.form['unidad']
        comentario = request.form['comentario']
        fecha = request.form['fecha']
        hora = request.form['hora']


        if unidad and comentario and fecha and hora:
            registro = Comentario( unidad , comentario , fecha , hora)
            guar.insert_one(registro.ComeDBCollection())
            flash("Guardado exitosamente")
            return redirect(url_for('opcomentario'))
    else: 
        return render_template('/operador/comentario.html',unidades=uni())



#* Vista comentarios
@app.route('/operador/vi_comentario',methods=['GET','POST'])
def op_comentario():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    come = db['comentario'].find()
    return render_template('/operador/vi_comentario.html',comentario=come)# Vista de carreras


# * Operadores Conductores

@app.route('/operador/in_conductores',methods=['GET','POST'])
def inopconductores():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    if request.method == 'POST':
        conductor = db['conductores']
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        em_nombre = request.form['em_nombre']
        em_telefono = request.form['em_telefono']
        em_relacion = request.form['em_relacion']
        clave = request.form['clave']
        licencia = request.form['licencia']

        exist_nombre = conductor.find_one({'nombre':nombre})
        exist_cedula = conductor.find_one({'cedula':cedula })
        
        if exist_nombre:
            flash("Ya existe un conductor con ese nombre ")
            return redirect(url_for('inopconductores'))
        
        elif exist_cedula:
            flash("Ya existe un conductor con esa cedula ")
            return redirect(url_for('inopconductores'))
        
        if cedula and nombre and email and telefono and direccion and em_nombre and em_relacion and clave and licencia:
            regis = Conductores(cedula, nombre, email, telefono, direccion, em_nombre, em_telefono, em_relacion, clave, licencia)
            conductor.insert_one(regis.CondDBCollection())
            flash("Enviado a la base de datos ")
            return redirect(url_for('inopconductores')) # Direccionamiento para la pagina que es /admin/in_conductores

    else: 
        return render_template('/operador/in_conductores.html') #* Cargado de la pagina

#*Vista de Conductores
@app.route('/operador/conductores',methods=['GET','POST'])
def opconductores():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index')) 
    
    condu = db['conductores'].find()
    return render_template('/operador/conductores.html',conductores=condu)# Vista para conductores

# * Editar y Eliminar Conductores
@app.route('/delete_condop/<string:cond_name>')
def elitconduop(cond_name):
    cond = db['conductores']
    cond.delete_one({'nombre':cond_name})
    return redirect(url_for('opconductores'))

@app.route('/edit_condop/<string:cond_name>', methods=['GET', 'POST'])
def editconduop(cond_name):
    cond = db['conductores']
    cedula = request.form['cedula']
    nombre = request.form['nombre']
    email = request.form['email']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    em_nombre = request.form['em_nombre']
    em_telefono = request.form['em_telefono']
    em_relacion = request.form['em_relacion']
    clave = request.form['clave']
    licencia = request.form['licencia']
    
    if cedula and nombre  and email and telefono and direccion and em_nombre and em_relacion and clave and licencia:
        cond.update_one({'cedula':cond_name},{'$set':{'cedula':cedula,'nombre':nombre,'email':email,'telefono':telefono,'direccion':direccion,'em_nombre':em_nombre,'em_telefono':em_telefono,'em_relacion':em_relacion,'clave':clave,'licencia':licencia}})
        return redirect(url_for('opconductores'))
    else:
        return render_template("operador/conductores.html")


if __name__ == '__main__':
    app.run(debug=True, port=2000)
