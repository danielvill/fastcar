from flask import flash, Flask, render_template, request,Response ,jsonify, redirect, url_for
from controllers.basedatos import Conexion as dbase


db = dbase()

app = Flask(__name__)
app.secret_key = 'fastcar'

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
    render_template('/admin/in_admin.html') 

#*Vista Administradores
@app.route('/admin/admin',methods=['GET','POST'])
def admin():
    render_template('/admin/admin.html')
        

#* Editar y eliminar  administradores
    

#*Ingreso de cliente
@app.route('/admin/in_cliente',methods=['GET','POST'])
def incliente():
    render_template('/admin/in_cliente.html')

#*Vista de cliente
@app.route('/admin/cliente',methods=['GET','POST'])
def cliente():
    render_template('/admin/cliente.html')


#*Editar y eliminar cliente
    

#*Ingreso de usuarios
@app.route('/admin/in_usuario',methods=['GET','POST'])
def inusuario():
    render_template('/admin/in_usuario.html')

#*Vista de usuarios
@app.route('/admin/usuarios',methods=['GET','POST'])
def usuario():
    render_template('/admin/usuarios.html')    


#*Editar y eliminar usuarios


#*Ingreso de conductores
@app.route('/admin/in_conductores',methods=['GET','POST'])
def inconductores():
    render_template('/admin/in_conductores.html')

#*Vista de Conductores
@app.route('/admin/conductores',methods=['GET','POST'])
def conductores():
    render_template('/admin/conductores.html')    


#*Ingreso de unidades
@app.route('/admin/in_unidades',methods=['GET','POST'])
def inunidades():
    render_template('/admin/in_unidades.html')


        
     


#*********** Ingreso de Operadores ****************************





        
        


if __name__ == '__main__':
    app.run(debug=True, port=2000)
