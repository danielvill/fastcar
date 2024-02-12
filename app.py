from flask import flash, Flask, render_template, request,Response ,jsonify, redirect, url_for
from controllers.basedatos import Conexion as dbase
from modules.admin import Admin
from modules.carreras import Carreras
from modules.clientes import Clientes
from modules.conductores import Conductores
from modules.unidades import Unidades
from modules.usuarios import Usuario


db = dbase()

app = Flask(__name__)
app.secret_key = 'fastcar'


@app.route('/',methods=['GET','POST'])
def run():
    return redirect(url_for('index'))



#* Ingreso al sistema

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        usuario = request.form['user']
        password = request.form['contraseña']
        usuario_fo = db.admin.find_one({'user':usuario,'contraseña':password})
        if usuario_fo:
            return redirect(url_for('registro'))
    else:
        return render_template('index.html')

#*Ingreso Administradores
@app.route('/admin/in_admin',methods=['GET','POST'])
def inadmin():
    if request.method == 'POST':
        admin = db['admin']
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        rol = request.form['rol']
        email = request.form['email']
        clave = request.form['clave']
        
        if cedula and nombre and rol and email and clave:
            regis = Admin(cedula, nombre, rol ,email, clave)
            admin.insert_one(regis.AdmDBCollection())
            return redirect(url_for('inadmin')) # Direccionamiento para la pagina que es /admin/in_admin
    else:
        return render_template('/admin/in_admin.html') #* Cargado de la pagina 

#*Vista Administradores
@app.route('/admin/admin',methods=['GET','POST'])
def admin():
    admin =db ['admin'].find()
    return render_template('/admin/admin.html',admin=admin)#* Vista para los administradores
    
        

#* Editar y eliminar  administradores
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
        ad.update_one({'nombre':ad_name},{'$set':{'cedula':cedula,'nombre':nombre,'rol':rol,'email':email,'clave':clave}})
        return redirect(url_for('admin'))
    else:
        return render_template("admin/admin.html")

#*Ingreso de cliente
@app.route('/admin/in_cliente',methods=['GET','POST'])
def incliente():
    if request.method == 'POST':
        cliente = db['clientes']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        provincia = request.form['provincia']
        canton = request.form['canton']
        referencia = request.form['referencia']
        comentario = request.form['comentario']
        
        if nombre and telefono and direccion and provincia and canton and referencia and comentario:
            regis = Clientes(nombre, telefono, direccion, provincia, canton, referencia, comentario)
            cliente.insert_one(regis.CliDBCollection())
            return redirect(url_for('incliente')) # Direccionamiento para la pagina que es /admin/in_cliente
    else: 
        return render_template('/admin/in_cliente.html') #* Cargado de la pagina 
    

#*Vista de cliente
@app.route('/admin/cliente',methods=['GET','POST'])
def cliente():
    clie = db['clientes'].find()
    return render_template('/admin/cliente.html',clientes=clie)# Vista para cliente 
    


#*Editar y eliminar cliente
@app.route('/delete_cli/<string:cli_name>')
def elitcli(cli_name):
    cli = db['clientes']
    cli.delete_one({'nombre':cli_name})
    return redirect(url_for('admin'))

@app.route('/edit_cli/<string:cli_name>', methods=['GET', 'POST'])
def editcli(cli_name):
    cli = db['clientes']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    provincia = request.form['provincia']
    canton = request.form['canton']
    referencia = request.form['referencia']
    comentario = request.form['comentario']
    
    if nombre and telefono and direccion and provincia and canton and referencia and comentario:
        cli.update_one({'nombre':cli_name},{'$set':{'nombre':nombre,'telefono':telefono,'direccion':direccion,'provincia':provincia,'canton':canton,'referencia':referencia,'comentario':comentario}})
        return redirect(url_for('cliente'))
    else:
        return render_template("admin/cliente.html")


#*Ingreso de usuarios
@app.route('/admin/in_usuario',methods=['GET','POST'])
def inusuario():
    if request.method == 'POST':
        usuario = db['usuarios']
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        rol = request.form['rol']
        email = request.form['email']
        clave = request.form['clave']
        
        if cedula and nombre and rol and email and clave:
            regis = Usuario(cedula, nombre, rol,email, clave)
            usuario.insert_one(regis.UsuDBCollection())
            return redirect(url_for('inusuario')) # Direccionamiento para la pagina que es /admin/in_usuario
    else:
        return render_template('/admin/in_usuario.html') #* Cargado de la pagina
    

#*Vista de usuarios
@app.route('/admin/usuarios',methods=['GET','POST'])
def usuario():
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
        usu.update_one({'nombre':usu_name},{'$set':{'cedula':cedula,'nombre':nombre,'rol':rol,'email':email,'clave':clave}})
        return redirect(url_for('usuario'))
    else:
        return render_template("admin/usuarios.html")
    


#*Ingreso de conductores
@app.route('/admin/in_conductores',methods=['GET','POST'])
def inconductores():
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

        if cedula and nombre and email and telefono and direccion and em_nombre and em_telefono and em_relacion and clave and licencia:
            regis = Conductores(cedula, nombre, email, telefono, direccion, em_nombre, em_telefono, em_relacion, clave, licencia)
            conductor.insert_one(regis.CondDBCollection())
            return redirect(url_for('inconductores')) # Direccionamiento para la pagina que es /admin/in_conductores

    else: 
        return render_template('/admin/in_conductores.html') #* Cargado de la pagina

#*Vista de Conductores
@app.route('/admin/conductores',methods=['GET','POST'])
def conductores():
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
    
    if cedula and nombre and email and telefono and direccion and em_nombre and em_telefono and em_relacion and clave and licencia:
        cond.update_one({'nombre':cond_name},{'$set':{'cedula':cedula,'nombre':nombre,'email':email,'telefono':telefono,'direccion':direccion,'em_nombre':em_nombre,'em_telefono':em_telefono,'em_relacion':em_relacion,'clave':clave,'licencia':licencia}})
        return redirect(url_for('conductores'))
    else:
        return render_template("admin/conductores.html")


#*Ingreso de unidades
@app.route('/admin/in_unidades',methods=['GET','POST'])
def inunidades():
    if request.method == 'POST':
        unidad = db['unidades']
        placa = request.form['placa']
        modelo = request.form['modelo']
        marca = request.form['marca']
        codigo = request.form['codigo']
        kilometraje = request.form['kilometraje']
        observacion = request.form['observacion']
        orden = request.form['orden']
        es_codigo = request.form['es_codigo']
        es_tipo = request.form['es_tipo']
        es_fecha = request.form['es_fecha']

        if placa and modelo and marca and codigo and kilometraje and observacion and orden and es_codigo and es_tipo and es_fecha:
            regis = Unidades(placa, modelo, marca, codigo, kilometraje, observacion, orden, es_codigo, es_tipo, es_fecha)
            unidad.insert_one(regis.UniDBCollection())
            return redirect(url_for('inunidades')) # Direccionamiento para la pagina que es /admin/in_unidades
    else: #
        return render_template('/admin/in_unidades.html') #* Cargado de la pagina

#*Vista de unidades
@app.route('/admin/unidades',methods=['GET','POST'])
def unidades():
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
    placa = request.form['placa']
    modelo = request.form['modelo']
    marca = request.form['marca']
    codigo = request.form['codigo']
    kilometraje = request.form['kilometraje']
    observacion = request.form['observacion']
    orden = request.form['orden']
    es_codigo = request.form['es_codigo']
    es_tipo = request.form['es_tipo']
    es_fecha = request.form['es_fecha']
    
    if placa and modelo and marca and codigo and kilometraje and observacion and orden and es_codigo and es_tipo and es_fecha:
        uni.update_one({'placa':uni_name},{'$set':{'placa':placa,'modelo':modelo,'marca':marca,'codigo':codigo,'kilometraje':kilometraje,'observacion':observacion,'orden':orden,'es_codigo':es_codigo,'es_tipo':es_tipo,'es_fecha':es_fecha}})
        return redirect(url_for('unidades'))
    else:
        return render_template("admin/unidades.html")


#* Carreras
@app.route('/admin/in_carreras',methods=['GET','POST'])
def incarreras():
    if request.method == 'POST':
        carrera = db ['carreras']
        cliente = request.form['cliente']
        provincia =request.form['provincia']
        canton = request.form['canton']
        lugar = request.form['lugar']
        referencia = request.form['referencia']
        tipo = request.form['tipo']
        fecha_inicio = request.form['fecha_inicio']
        comentario = request.form['comentario']
        fecha_fin = request.form['fecha_fin']
        estado = request.form['estado']
        operador = request.form['operador']
        if cliente and provincia and canton and lugar and referencia and tipo and fecha_inicio and comentario and fecha_fin and estado and operador:
            regis = Carreras(cliente, provincia, canton, lugar, referencia, tipo, fecha_inicio, comentario, fecha_fin, estado, operador)
            carrera.insert_one(regis.CareDBCollection())
            return redirect(url_for('incarreras')) # Direccionamiento para la pagina que es /admin/in_carreras
    else: #
        return render_template('/admin/in_carreras.html') #* Cargado de la pagina
        

#*Vista de carreras
@app.route('/admin/carreras',methods=['GET','POST'])
def carreras():
    carre = db['carreras'].find()
    return render_template('/admin/carreras.html',carreras=carre)# Vista de carreras

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
    provincia =request.form['provincia']
    canton = request.form['canton']
    lugar = request.form['lugar']
    referencia = request.form['referencia']
    tipo = request.form['tipo']
    fecha_inicio = request.form['fecha_inicio']
    comentario = request.form['comentario']
    fecha_fin = request.form['fecha_fin']
    estado = request.form['estado']
    operador = request.form['operador']
    
    if cliente and provincia and canton and lugar and referencia and tipo and fecha_inicio and comentario and fecha_fin and estado and operador:
        carre.update_one({'cliente':car_name},{'$set':{'cliente':cliente,'provincia':provincia,'canton':canton,'lugar':lugar,'referencia':referencia,'tipo':tipo,'fecha_inicio':fecha_inicio,'comentario':comentario,'fecha_fin':fecha_fin,'estado':estado,'operador':operador}})
        return redirect(url_for('carreras'))
    else:
        return render_template("admin/carreras.html")





#*********** Ingreso de Operadores ****************************





        
        


if __name__ == '__main__':
    app.run(debug=True, port=2000)
