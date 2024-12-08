from tkinter import *
from tkinter import ttk,messagebox
import ttkbootstrap as tp 
#importar la libreria para conectar la base de datos
import sqlite3
class ventana(tp.Window):
    def __init__(self):
        super().__init__()
        self.ventana_login()
    def ventana_login(self):
        self.frame_login=Frame(self)
        self.frame_login.pack()
        
        self.lblframe_login=LabelFrame(self.frame_login,text='Acceso')
        self.lblframe_login.pack(padx=10,pady=10)

        lbltitulo=ttk.Label(self.lblframe_login,text='Inicio de sesion',font=('Arial',22))
        lbltitulo.pack(padx=10 , pady=35)

        self.txt_usuario=ttk.Entry(self.lblframe_login,width=40,justify=CENTER)
        self.txt_usuario.pack(padx=10, pady=10)
        self.txt_clave=ttk.Entry(self.lblframe_login,width=40,justify=CENTER)
        self.txt_clave.pack(padx=10, pady=10)
        self.txt_clave.configure(show='*')
        btn_acceso=ttk.Button(self.lblframe_login,text='Log in',command=self.logueo)
        btn_acceso.pack(padx=10, pady=10)
    def ventana_menu(self):
        self.frame_left=Frame(self,width=200)
        self.frame_left.grid(row=0,column=0,sticky=NSEW)
        self.frame_center=Frame(self)
        self.frame_center.grid(row=0,column=1,sticky=NSEW)
        self.frame_rigth=Frame(self,width=400)
        self.frame_rigth.grid(row=0,column=2,sticky=NSEW)

        btn_productos=ttk.Button(self.frame_left,text='PRODUCTOS',width=15,command=self.ventana_lista_productos)
        btn_productos.grid(row=0,column=0,padx=10,pady=10)
        btn_ventas=ttk.Button(self.frame_left,text='VENTAS',width=15,command=self.ventana_lista_ventas)
        btn_ventas.grid(row=1,column=0,padx=10,pady=10)
        btn_cliente=ttk.Button(self.frame_left,text='CLIENTES',width=15)
        btn_cliente.grid(row=2,column=0,padx=10,pady=10)
        btn_compras=ttk.Button(self.frame_left,text='COMPRAS',width=15)
        btn_compras.grid(row=3,column=0,padx=10,pady=10)
        btn_usuario=ttk.Button(self.frame_left,text='USUARIO',width=15,command=self.ventana_lista_usuarios)
        btn_usuario.grid(row=4,column=0,padx=10,pady=10)
        btn_reportes=ttk.Button(self.frame_left,text='REPORTES',width=15)
        btn_reportes.grid(row=5,column=0,padx=10,pady=10) 
        btn_restaurar=ttk.Button(self.frame_left,text='RESTAURAR',width=15)
        btn_restaurar.grid(row=7,column=0,padx=10,pady=10) 
    def logueo(self):
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()
            
            nombre_usuario=self.txt_usuario.get()
            clave_usuario=self.txt_clave.get()

            #consultamos la base de datos 
            micursor.execute("SELECT * FROM Usuarios WHERE Nombre=? AND Clave=?",(nombre_usuario,clave_usuario))
            #con esto traigo todos los registros y lo guardo en datos
            datos_logueo=micursor.fetchall()
            if datos_logueo!="":
                for row in datos_logueo:
                    cod_usu=row[0]
                    nom_usu=row[1]
                    cla_usu=row[2]
                    rol_usu=row[3]
                if (nom_usu==self.txt_usuario.get() and cla_usu==self.txt_clave.get()):
                    self.frame_login.pack_forget()#ocultamos la ventana login
                    self.ventana_menu()#abrimos nuestra ventana menu

            #aplicamos cambios 
            miconexion.commit()
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("Acceso","El usuario o clave son incorrectos")
#============================USUARIOS=========================
    def ventana_lista_usuarios(self):
        self.borrar_frames()
        self.frame_lista_usuarios=Frame(self.frame_center)
        self.frame_lista_usuarios.grid(row=0,column=0,columnspan=2,sticky=NSEW)

        self.lblframe_botones_listusu=LabelFrame(self.frame_lista_usuarios)
        self.lblframe_botones_listusu.grid(row=0,column=0,padx=10,pady=10,sticky=NSEW)

        btn_nuevo_usuario=tp.Button(self.lblframe_botones_listusu,text='NUEVO',width=15
                                    ,bootstyle="success",command=self.ventana_nuevo_usuario)
        btn_nuevo_usuario.grid(row=0,column=0,padx=5,pady=5)
        
        btn_modificar_usuario=tp.Button(self.lblframe_botones_listusu,text='MODIFICAR',width=15,bootstyle="warnig",command=self.ventana_modificar_usuario)
        btn_modificar_usuario.grid(row=0,column=1,padx=5,pady=5)

        btn_eliminar_usuario=tp.Button(self.lblframe_botones_listusu,text='ELIMINAR',width=15,bootstyle="danger",command=self.eliminar_usuarios)
        btn_eliminar_usuario.grid(row=0,column=2,padx=5,pady=5)

        self.lblframe_busqueda_listusu=LabelFrame(self.frame_lista_usuarios)
        self.lblframe_busqueda_listusu.grid(row=1,column=0,sticky=NSEW)

        self.busqueda_usuarios=ttk.Entry(self.lblframe_busqueda_listusu,width=50)
        self.busqueda_usuarios.grid(row=0,column=0,padx=5,pady=5)
        self.busqueda_usuarios.bind('<Key>',self.buscar_usuarios)
    
        #==========================================Treeview=========================================
        
        self.lblframe_tree_listusu=LabelFrame(self.frame_lista_usuarios)
        self.lblframe_tree_listusu.grid(row=2,column=0,padx=10,pady=10,sticky=NSEW)

        #crear columnas
        columnas=("codigo","nombre","clave","rol")
        
        self.tree_lista_usuarios=tp.Treeview(self.lblframe_tree_listusu,column=columnas,
                                        height=17,show='headings',bootstyle='dark')
        self.tree_lista_usuarios.grid(row=0,column=0)

        #cabeceras del treeview
        self.tree_lista_usuarios.heading("codigo",text="Codigo",anchor=W)
        self.tree_lista_usuarios.heading("nombre",text="Nombre",anchor=W)
        self.tree_lista_usuarios.heading("clave",text="Clave",anchor=W)
        self.tree_lista_usuarios.heading("rol",text="Rol",anchor=W)

        #Para ocultar clave solo aparece codigo , nombre, rol
        self.tree_lista_usuarios['displaycolumns']=("codigo","nombre","rol") 

        #CREAR BARRA DE DESPLAZAMIENTO
        tree_scroll_listausu=tp.Scrollbar(self.frame_lista_usuarios,bootstyle='round success')                           
        tree_scroll_listausu.grid(row=2,column=1)

        #CONFIGURACION  DE BARRA 
        tree_scroll_listausu.config(command=self.tree_lista_usuarios.yview)    

        ##llamamos a nuestra funcion mostrar usuarios
        self.mostrar_usuarios()  
    def mostrar_usuarios(self):

        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()
            #limpiamos nuestro treeview
            registros=self.tree_lista_usuarios.get_children()
            #recorer cada registro
            for elementos in registros:
                self.tree_lista_usuarios.delete(elementos)
            #consultamos la base de datos 
            micursor.execute("SELECT * FROM Usuarios")
            #con esto traigo todos los registros y lo guardo en datos
            datos=micursor.fetchall()
            #recorrer cada fila encontrada
            for row in datos:
                #Llenamos nuetro treeview
                self.tree_lista_usuarios.insert("",0,text=row[0],values=(row[0],row[1],row[2],row[3]))
            #aplicamos cambios 
            miconexion.commit()
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("lista de usuarios","ocurrior un error al mostrar la lista de usuarios")
    def ventana_nuevo_usuario(self):

        self.frame_nuevo_usuario=Toplevel(self)#ventana por encima de la lista de usuarios
        self.frame_nuevo_usuario.title('Nuevo Usuario')#titulo de la ventana
        self.centrar_ventana_nuevo_usuario(400,300)#tamaño
        self.frame_nuevo_usuario.resizable(0,0)#para que no se pueda maximizar ni minimizar
        self.frame_nuevo_usuario.grab_set()#para que no permita ninguna otra accion hasta que cierre la ventana

        lblframe_nuevo_usuario=LabelFrame(self.frame_nuevo_usuario)
        lblframe_nuevo_usuario.grid(row=0,column=0,sticky=NSEW,padx=25,pady=35)

        lbl_codigo_nuevo_usuario=Label(lblframe_nuevo_usuario,text='Codigo')
        lbl_codigo_nuevo_usuario.grid(row=0,column=0,padx=10,pady=10,sticky=E)
        self.txt_codigo_nuevo_usuario=ttk.Entry(lblframe_nuevo_usuario,width=40)
        self.txt_codigo_nuevo_usuario.grid(row=0,column=1,padx=10,pady=10)

        lbl_nombre_nuevo_usuario=Label(lblframe_nuevo_usuario,text='Nombre')
        lbl_nombre_nuevo_usuario.grid(row=1,column=0,padx=10,pady=10,sticky=E)
        self.txt_nombre_nuevo_usuario=ttk.Entry(lblframe_nuevo_usuario,width=40)
        self.txt_nombre_nuevo_usuario.grid(row=1,column=1,padx=10,pady=10)

        lbl_clave_nuevo_usuario=Label(lblframe_nuevo_usuario,text='Clave')
        lbl_clave_nuevo_usuario.grid(row=2,column=0,padx=10,pady=10,sticky=E)
        self.txt_clave_nuevo_usuario=ttk.Entry(lblframe_nuevo_usuario,width=40)
        self.txt_clave_nuevo_usuario.grid(row=2,column=1,padx=10,pady=10)

        lbl_rol_nuevo_usuario=Label(lblframe_nuevo_usuario,text='Rol')
        lbl_rol_nuevo_usuario.grid(row=3,column=0,padx=10,pady=10,sticky=E)
        self.txt_rol_nuevo_usuario=ttk.Combobox(lblframe_nuevo_usuario,values=('Administrador','Bodega','Vendedor'),width=38,state='readonly')
        self.txt_rol_nuevo_usuario.grid(row=3,column=1,padx=10,pady=10)
        self.txt_rol_nuevo_usuario.current(0)#Aqui colocamos el valor que aparece por defecto

        btn_guardar_nuevo_usuario=ttk.Button(lblframe_nuevo_usuario,text='Guardar',width=38,command=self.guardar_usuario)
        btn_guardar_nuevo_usuario.grid(row=4,column=1,padx=10,pady=10)

        #llamamos a la funcion ultimo usuario 
        self.ultimo_usuario()
        #Programamos el foco en el nombre usuario
        self.txt_nombre_nuevo_usuario.focus()
    def guardar_usuario(self):
        #validamos para que no queden vacios los campos
        if self.txt_codigo_nuevo_usuario.get()=="" or self.txt_nombre_nuevo_usuario.get()=="" or self.txt_clave_nuevo_usuario.get()=="":
            messagebox.showwarning("Guardando Usuarios","Algun campo no es valido revisar")
            return
        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()

            datos_guardar_usuario=self.txt_codigo_nuevo_usuario.get(),self.txt_nombre_nuevo_usuario.get(),self.txt_clave_nuevo_usuario.get(),self.txt_rol_nuevo_usuario.get()
            #consultamos la base de datos 
            micursor.execute("INSERT INTO Usuarios VALUES(?,?,?,?)",(datos_guardar_usuario))
            messagebox.showinfo('Guardando Usuarios',"Usuario Guardado Correctamente")
            #aplicamos cambios 
            miconexion.commit()
            self.frame_nuevo_usuario.destroy()#cerramos ventana,guardar nuevo usuario
            self.ventana_lista_usuarios()#cargamos nuevamente la ventana para ver los cambios 
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("Guardando Usuarios","Ocurrio un error al Guardar  Usuario") 
    def ultimo_usuario(self):
    
        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()
            
            #consultamos la base de datos 
            micursor.execute("SELECT MAX (Codigo) FROM Usuarios")
            #con esto traigo todos los registros y lo guardo en datos
            datos=micursor.fetchone()#solo necesitamos un dato
            for codusu in datos:
                if codusu == None:
                    self.ultusu=(int(1))
                    self.txt_codigo_nuevo_usuario.config(state=NORMAL)
                    self.txt_codigo_nuevo_usuario.insert(0,self.ultusu)
                    self.txt_codigo_nuevo_usuario.config(state='readonly')
                    break
                if codusu=="":
                    self.ultusu=(int(1))
                    self.txt_codigo_nuevo_usuario.config(state=NORMAL)
                    self.txt_codigo_nuevo_usuario.insert(0,self.ultusu)
                    self.txt_codigo_nuevo_usuario.config(state='readonly')
                    break

                else:
                    self.ultusu=(int(codusu)+1)
                    self.txt_codigo_nuevo_usuario.config(state=NORMAL)
                    self.txt_codigo_nuevo_usuario.insert(0,self.ultusu)
                    self.txt_codigo_nuevo_usuario.config(state='readonly')

            #aplicamos cambios 
            miconexion.commit()
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("lista de usuarios","ocurrio un error al mostrar la lista de usuarios")
    def centrar_ventana_nuevo_usuario(self,ancho,alto):
        ventana_ancho=ancho
        ventana_alto=alto

        pantalla_ancho=self.frame_rigth.winfo_screenwidth()
        pantalla_alto=self.frame_rigth.winfo_screenheight()

        cordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        cordenadas_y=int((pantalla_alto/2)-(ventana_ancho/2))
        self.frame_nuevo_usuario.geometry("{}x{}+{}+{}".format(ventana_ancho,ventana_alto,cordenadas_x,cordenadas_y))
    def buscar_usuarios(self,event):
        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()
            #limpiamos nuestro treeview
            registros=self.tree_lista_usuarios.get_children()
            #recorer cada registro
            for elementos in registros:
                self.tree_lista_usuarios.delete(elementos)
            #consultamos la base de datos 
            micursor.execute("SELECT * FROM Usuarios WHERE Nombre LIKE ?",(self.busqueda_usuarios.get()+'%',))
            #con esto traigo todos los registros y lo guardo en datos
            datos=micursor.fetchall()
            #recorrer cada fila encontrada
            for row in datos:
                #Llenamos nuetro treeview
                self.tree_lista_usuarios.insert("",0,text=row[0],values=(row[0],row[1],row[2],row[3]))
            #aplicamos cambios 
            miconexion.commit()
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("Busqueda de usuarios","ocurrio un error al buscar en la lista de usuarios")
    def ventana_modificar_usuario(self):
        #con esto estamos validando que se abra la ventana solamente si hay algun valor seleccionado
        self.usuario_seleccionado=self.tree_lista_usuarios.focus()
        
        self.val_mod_usu=self.tree_lista_usuarios.item(self.usuario_seleccionado,'values')

        if self.val_mod_usu!='':

            self.frame_modificar_usuario=Toplevel(self)#ventana por encima de la lista de usuarios
            self.frame_modificar_usuario.title('Nuevo Usuario')#titulo de la ventana
            self.frame_modificar_usuario.geometry('400x300')
            #self.centrar_ventana_modificar_usuario(400,300)#tamaño
            self.frame_modificar_usuario.resizable(0,0)#para que no se pueda maximizar ni minimizar
            self.frame_modificar_usuario.grab_set()#para que no permita ninguna otra accion hasta que cierre la ventana

            lblframe_modificar_usuario=LabelFrame(self.frame_modificar_usuario)
            lblframe_modificar_usuario.grid(row=0,column=0,sticky=NSEW,padx=25,pady=35)

            lbl_codigo_modificar_usuario=Label(lblframe_modificar_usuario,text='Codigo')
            lbl_codigo_modificar_usuario.grid(row=0,column=0,padx=10,pady=10,sticky=E)
            self.txt_codigo_modificar_usuario=ttk.Entry(lblframe_modificar_usuario,width=40)
            self.txt_codigo_modificar_usuario.grid(row=0,column=1,padx=10,pady=10)

            lbl_nombre_modificar_usuario=Label(lblframe_modificar_usuario,text='Nombre')
            lbl_nombre_modificar_usuario.grid(row=1,column=0,padx=10,pady=10,sticky=E)
            self.txt_nombre_modificar_usuario=ttk.Entry(lblframe_modificar_usuario,width=40)
            self.txt_nombre_modificar_usuario.grid(row=1,column=1,padx=10,pady=10)

            lbl_clave_modificar_usuario=Label(lblframe_modificar_usuario,text='Clave')
            lbl_clave_modificar_usuario.grid(row=2,column=0,padx=10,pady=10,sticky=E)
            self.txt_clave_modificar_usuario=ttk.Entry(lblframe_modificar_usuario,width=40)
            self.txt_clave_modificar_usuario.grid(row=2,column=1,padx=10,pady=10)

            lbl_rol_modificar_usuario=Label(lblframe_modificar_usuario,text='Rol')
            lbl_rol_modificar_usuario.grid(row=3,column=0,padx=10,pady=10,sticky=E)
            self.txt_rol_modificar_usuario=ttk.Combobox(lblframe_modificar_usuario,values=('Administrador','Bodega','Vendedor'),width=38)
            self.txt_rol_modificar_usuario.grid(row=3,column=1,padx=10,pady=10)
        
            btn_guardar_modificar_usuario=ttk.Button(lblframe_modificar_usuario,text='Guardar',width=38,bootstyle='warning',command=self.modificar_usuarios)
            btn_guardar_modificar_usuario.grid(row=4,column=1,padx=10,pady=10)

            self.llenar_entrys_modificar_usuario()
            #Programamos el foco en el nombre usuario
            self.txt_nombre_modificar_usuario.focus()
    def llenar_entrys_modificar_usuario(self):
        #Liampiaremos todos los entry
        self.txt_codigo_modificar_usuario.delete(0,END)    
        self.txt_nombre_modificar_usuario.delete(0,END)
        self.txt_clave_modificar_usuario.delete(0,END)
        self.txt_rol_modificar_usuario.delete(0,END)
        #llenamos los entres
        self.txt_codigo_modificar_usuario.insert(0,self.val_mod_usu[0])
        self.txt_codigo_modificar_usuario.config(state='readonly')    
        self.txt_nombre_modificar_usuario.insert(0,self.val_mod_usu[1])
        self.txt_clave_modificar_usuario.insert(0,self.val_mod_usu[2])
        self.txt_rol_modificar_usuario.insert(0,self.val_mod_usu[3])
        self.txt_rol_modificar_usuario.config(state='readonly') 
    def modificar_usuarios(self):
         #validamos para que no queden vacios los campos
        if self.txt_codigo_modificar_usuario.get()=="" or self.txt_nombre_modificar_usuario.get()=="" or self.txt_clave_modificar_usuario.get()=="":
            messagebox.showwarning("Modificar Usuarios","Algun campo no es valido revisar")
            return
        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()

            datos_modificar_usuario=self.txt_nombre_modificar_usuario.get(),self.txt_clave_modificar_usuario.get(),self.txt_rol_modificar_usuario.get()
            
            #consultamos la base de datos 
            micursor.execute("UPDATE Usuarios SET Nombre=?,Clave=?,Rol=? WHERE Codigo="+self.txt_codigo_modificar_usuario.get(),(datos_modificar_usuario))
            messagebox.showinfo('Modificar Usuarios',"Usuario Modificado Correctamente")
            #aplicamos cambios 
            miconexion.commit()
            self.val_mod_usu=self.tree_lista_usuarios.item(self.usuario_seleccionado,text='',values=(self.txt_codigo_modificar_usuario.get(),self.txt_nombre_modificar_usuario.get(),self.txt_clave_modificar_usuario.get(),self.txt_rol_modificar_usuario.get()))
            self.frame_modificar_usuario.destroy()#cerramos ventana,guardar nuevo usuario
            self.ventana_lista_usuarios()#cargamos nuevamente la ventana para ver los cambios 
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("Modificando Usuarios","Ocurrio un error al Modificar  Usuario")
    def eliminar_usuarios(self):
            usuario_selec_eliminar=self.tree_lista_usuarios.focus()
            valor_usuario_selec_eliminar=self.tree_lista_usuarios.item(usuario_selec_eliminar,'values')
            if valor_usuario_selec_eliminar!='':
                respuesta=messagebox.askquestion('Elimando usuarios','¿Estas seguro de eliminar?')
                if respuesta=='yes':
                   #establecer la conexion
                   miconexion=sqlite3.connect('ventas.db')
                   #creamos el cursor
                   micursor=miconexion.cursor()
                   #consultamos la base de datos 
                   micursor.execute("DELETE FROM Usuarios WHERE Codigo="+str(valor_usuario_selec_eliminar[0]))

                   #aplicamos cambios 
                   miconexion.commit()
                   messagebox.showinfo('Eliminado Usuarios','Eliminado correctamente')
                   self.mostrar_usuarios()
                   #cerramos la conexion
                   miconexion.close()
            else:
                messagebox.showerror('Eliminado Usuario','Eliminacion cancelada')
    def correlativo_usuarios(self):

        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()
            #consultamos la base de datos 
            micursor.execute("SELECT MAX(codigo) FROM Usuario")
            #con esto traigo todos los registros y lo guardo en datos
            correlativo_usuarios=micursor.fetchone()
            #recorrer cada fila encontrada
            for datos in correlativo_usuarios:
                if datos==None:
                    self.nuevo_correlativo_usuario=(int(1))
                    self.txt_codigo_nuevo_usuario.config(state=NORMAL)
                    self.txt_codigo_nuevo_usuario.insert(0,self.nuevo_correlativo_usuario)
                    self.txt_codigo_nuevo_usuario.config(state='readonly')
                else:
                    self.nuevo_correlativo_usuario=(int(datos)+1)
                    self.txt_codigo_nuevo_usuario.config(state=NORMAL)
                    self.txt_codigo_nuevo_usuario.insert(0,self.nuevo_correlativo_usuario)
                    self.txt_codigo_nuevo_usuario.config(state='readonly')   
                    
            #aplicamos cambios 
            miconexion.commit()
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("Correlativo Usuario","ocurrio un error")
#==================================PRODUCTOS====================
    def ventana_lista_productos(self):
        self.borrar_frames()
        self.frame_lista_productos=Frame(self.frame_center)
        self.frame_lista_productos.grid(row=0,column=0,columnspan=2,sticky=NSEW)

        self.lblframe_botones_productos=LabelFrame(self.frame_lista_productos)
        self.lblframe_botones_productos.grid(row=0,column=0,padx=10,pady=10,sticky=NSEW)

        btn_nuevo_productos=tp.Button(self.lblframe_botones_productos,text='NUEVO',width=15
                                       ,bootstyle="success",command=self.ventana_nuevo_productos)
        btn_nuevo_productos.grid(row=0,column=0,padx=5,pady=5)
        
        btn_modificar_productos=tp.Button(self.lblframe_botones_productos,text='MODIFICAR',width=15,bootstyle="warnig",command=self.ventana_modificar_productos)
        btn_modificar_productos.grid(row=0,column=1,padx=5,pady=5)

        btn_eliminar_productos=tp.Button(self.lblframe_botones_productos,text='ELIMINAR',width=15,bootstyle="danger",command=self.eliminar_producto)
        btn_eliminar_productos.grid(row=0,column=2,padx=5,pady=5)

        self.lblframe_busqueda_productos=LabelFrame(self.frame_lista_productos)
        self.lblframe_busqueda_productos.grid(row=1,column=0)

        self.busqueda_productos=ttk.Entry(self.lblframe_busqueda_productos,width=50)
        self.busqueda_productos.grid(row=0,column=0,padx=5,pady=5)
        self.busqueda_productos.bind('<Key>')
    
        #==========================================Treeview=========================================
        
        self.lblframe_tree_productos=LabelFrame(self.frame_lista_productos)
        self.lblframe_tree_productos.grid(row=2,column=0,padx=10,pady=10,sticky=NSEW)

        #crear columnas
        columnas=("codigo","producto","costo","precio","stock","minimo",)
        
        self.tree_lista_productos=tp.Treeview(self.lblframe_tree_productos,column=columnas,
                                        height=17,show='headings',bootstyle='dark')
        self.tree_lista_productos.grid(row=0,column=0)

        #cabeceras del treeview
        self.tree_lista_productos.heading("codigo",text="codigo",anchor=W)
        self.tree_lista_productos.heading("producto",text="producto",anchor=W)
        self.tree_lista_productos.heading("costo",text="costo",anchor=W)
        self.tree_lista_productos.heading("precio",text="precio",anchor=W)
        self.tree_lista_productos.heading("stock",text="stock",anchor=W)
        self.tree_lista_productos.heading("minimo",text="minimo",anchor=W)
        #Para ocultar clave solo aparece codigo , nombre, rol
        self.tree_lista_productos['displaycolumns']=("codigo","producto","precio","stock") 

        #CREAR BARRA DE DESPLAZAMIENTO
        tree_scroll_productos=tp.Scrollbar(self.frame_lista_productos,bootstyle='round success')                           
        tree_scroll_productos.grid(row=2,column=1)

        #CONFIGURACION  DE BARRA 
        tree_scroll_productos.config(command=self.tree_lista_productos.yview)    
        self.buscar_productos('')
    def ventana_nuevo_productos(self):
        self.frame_nuevo_productos=Toplevel(self)#ventana por encima de la lista de usuarios
        self.frame_nuevo_productos.title('Nuevo producto')#titulo de la ventana
        self.centrar_ventana_nuevo_productos(500,400)#tamaño
        self.frame_nuevo_productos.resizable(0,0)#para que no se pueda maximizar ni minimizar
        self.frame_nuevo_productos.grab_set()#para que no permita ninguna otra accion hasta que cierre la ventana

        lblframe_nuevo_productos=LabelFrame(self.frame_nuevo_productos)
        lblframe_nuevo_productos.pack(padx=15,pady=15)

        lbl_codigo_nuevo_productos=Label(lblframe_nuevo_productos,text='codigo')
        lbl_codigo_nuevo_productos.grid(row=0,column=0,padx=10,pady=10)
        self.txt_codigo_nuevo_productos=tp.Entry(lblframe_nuevo_productos,width=40)
        self.txt_codigo_nuevo_productos.grid(row=0,column=1,padx=10,pady=10)

        lbl_producto_nuevo_productos=Label(lblframe_nuevo_productos,text='producto')
        lbl_producto_nuevo_productos.grid(row=1,column=0,padx=10,pady=10)
        self.txt_producto_nuevo_productos=tp.Entry(lblframe_nuevo_productos,width=40)
        self.txt_producto_nuevo_productos.grid(row=1,column=1,padx=10,pady=10)

        lbl_costo_nuevo_productos=Label(lblframe_nuevo_productos,text='costo')
        lbl_costo_nuevo_productos.grid(row=2,column=0,padx=10,pady=10)
        self.txt_costo_nuevo_productos=tp.Entry(lblframe_nuevo_productos,width=40)
        self.txt_costo_nuevo_productos.grid(row=2,column=1,padx=10,pady=10)

        lbl_precio_nuevo_productos=Label(lblframe_nuevo_productos,text='precio')
        lbl_precio_nuevo_productos.grid(row=3,column=0,padx=10,pady=10)
        self.txt_precio_nuevo_productos=tp.Entry(lblframe_nuevo_productos,width=40)
        self.txt_precio_nuevo_productos.grid(row=3,column=1,padx=10,pady=10)

        lbl_stock_nuevo_productos=Label(lblframe_nuevo_productos,text='stock')
        lbl_stock_nuevo_productos.grid(row=4,column=0,padx=10,pady=10)
        self.txt_stock_nuevo_productos=tp.Entry(lblframe_nuevo_productos,width=40)
        self.txt_stock_nuevo_productos.grid(row=4,column=1,padx=10,pady=10)

        lbl_minimo_nuevo_productos=Label(lblframe_nuevo_productos,text='minimo')
        lbl_minimo_nuevo_productos.grid(row=5,column=0,padx=10,pady=10)
        self.txt_minimo_nuevo_productos=tp.Entry(lblframe_nuevo_productos,width=40)
        self.txt_minimo_nuevo_productos.grid(row=5,column=1,padx=10,pady=10)
        
        btn_guardar_nuevo_productos=tp.Button(lblframe_nuevo_productos,text='Guardar',width=38,command=self.guardar_productos)
        btn_guardar_nuevo_productos.grid(row=6,column=1,padx=10,pady=10)

        self.txt_producto_nuevo_productos.focus()
        self.correlativo_productos()
    def centrar_ventana_nuevo_productos(self,ancho,alto):
        ventana_ancho=ancho
        ventana_alto=alto

        pantalla_ancho=self.frame_rigth.winfo_screenwidth()
        pantalla_alto=self.frame_rigth.winfo_screenheight()

        cordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        cordenadas_y=int((pantalla_alto/2)-(ventana_ancho/2))
        self.frame_nuevo_productos.geometry("{}x{}+{}+{}".format(ventana_ancho,ventana_alto,cordenadas_x,cordenadas_y))
    def guardar_productos(self):
        #validamos para que no queden vacios los campos "codigo","producto","costo","precio","stock","minimo",
        if (self.txt_codigo_nuevo_productos.get()=="" or self.txt_producto_nuevo_productos.get()=="" or self.txt_costo_nuevo_productos.get()==""or self.
         txt_precio_nuevo_productos.get()=="" or self.txt_stock_nuevo_productos.get()=="" or self.txt_minimo_nuevo_productos.get()=="" ):
            messagebox.showwarning("Guardando Producto","Algun campo no es valido revisar")
            return
        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()

            datos_guardar_productos=(self.txt_codigo_nuevo_productos.get(),self.txt_producto_nuevo_productos.get(),self.txt_costo_nuevo_productos.get(),self.
            txt_precio_nuevo_productos.get(),self.txt_stock_nuevo_productos.get(),self.txt_minimo_nuevo_productos.get()=="" )
            #consultamos la base de datos 
            micursor.execute("INSERT INTO Productos VALUES(?,?,?,?,?,?)",(datos_guardar_productos))
            messagebox.showinfo('Guardando Producto',"Producto Guardado Correctamente")
            #aplicamos cambios 
            miconexion.commit()
            self.frame_nuevo_productos.destroy()#cerramos ventana,guardar nuevo usuario
            self.ventana_lista_productos()#cargamos nuevamente la ventana para ver los cambios 
            #cerramos la conexion
            miconexion.close()
            self.buscar_productos('')

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("Guardando Productos","Ocurrio un error al Guardar Producto")
    def buscar_productos(self,event):
        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()
            #limpiamos nuestro treeview
            registros=self.tree_lista_productos.get_children()
            #recorer cada registro
            for elementos in registros:
                self.tree_lista_productos.delete(elementos)
            #consultamos la base de datos 
            micursor.execute("SELECT * FROM productos WHERE producto LIKE ?",(self.busqueda_productos.get()+'%',))
            #con esto traigo todos los registros y lo guardo en datos
            datos=micursor.fetchall()
            #recorrer cada fila encontrada
            for row in datos:
                #Llenamos nuetro treeview
                self.tree_lista_productos.insert("",0,text=row[0],values=(row[0],row[1],row[2],row[3],row[4],row[5]))
            #aplicamos cambios 
            miconexion.commit()
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("Busqueda de productos","ocurrio un error")
    def correlativo_productos(self):

        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()
            #consultamos la base de datos 
            micursor.execute("SELECT MAX(codigo) FROM Productos")
            #con esto traigo todos los registros y lo guardo en datos
            correlativo_productos=micursor.fetchone()
            #recorrer cada fila encontrada
            for datos in correlativo_productos:
                if datos==None:
                    self.nuevo_correlativo_productos=(int(1))
                    self.txt_codigo_nuevo_productos.config(state=NORMAL)
                    self.txt_codigo_nuevo_productos.insert(0,self.nuevo_correlativo_productos)
                    self.txt_codigo_nuevo_productos.config(state='readonly')
                else:
                    self.nuevo_correlativo_productos=(int(datos)+1)
                    self.txt_codigo_nuevo_productos.config(state=NORMAL)
                    self.txt_codigo_nuevo_productos.insert(0,self.nuevo_correlativo_productos)
                    self.txt_codigo_nuevo_productos.config(state='readonly')   
                    
            #aplicamos cambios 
            miconexion.commit()
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("Correlativo producto","ocurrio un error")
    def ventana_modificar_productos(self):
         self.productos_seleccionado=self.tree_lista_productos.focus()
        
         self.val_mod_prod=self.tree_lista_productos.item(self.productos_seleccionado,'values')

         if self.val_mod_prod!='':

           self.frame_modificar_productos=Toplevel(self)#ventana por encima de la lista de usuarios
           self.frame_modificar_productos.title('Modificar producto')#titulo de la ventana
           #self.centrar_ventana_modificar_productos(500,400)#tamaño
           self.frame_modificar_productos.resizable(0,0)#para que no se pueda maximizar ni minimizar
           self.frame_modificar_productos.grab_set()#para que no permita ninguna otra accion hasta que cierre la ventana

           lblframe_modificar_productos=LabelFrame(self.frame_modificar_productos,text='Modificar Producto')
           lblframe_modificar_productos.pack(padx=15,pady=15)

           lbl_codigo_modificar_productos=Label(lblframe_modificar_productos,text='codigo')
           lbl_codigo_modificar_productos.grid(row=0,column=0,padx=10,pady=10)
           self.txt_codigo_modificar_productos=tp.Entry(lblframe_modificar_productos,width=40)
           self.txt_codigo_modificar_productos.grid(row=0,column=1,padx=10,pady=10)

           lbl_producto_modificar_productos=Label(lblframe_modificar_productos,text='producto')
           lbl_producto_modificar_productos.grid(row=1,column=0,padx=10,pady=10)
           self.txt_producto_modificar_productos=tp.Entry(lblframe_modificar_productos,width=40)
           self.txt_producto_modificar_productos.grid(row=1,column=1,padx=10,pady=10)

           lbl_costo_modificar_productos=Label(lblframe_modificar_productos,text='costo')
           lbl_costo_modificar_productos.grid(row=2,column=0,padx=10,pady=10)
           self.txt_costo_modificar_productos=tp.Entry(lblframe_modificar_productos,width=40)
           self.txt_costo_modificar_productos.grid(row=2,column=1,padx=10,pady=10)

           lbl_precio_modificar_productos=Label(lblframe_modificar_productos,text='precio')
           lbl_precio_modificar_productos.grid(row=3,column=0,padx=10,pady=10)
           self.txt_precio_modificar_productos=tp.Entry(lblframe_modificar_productos,width=40)
           self.txt_precio_modificar_productos.grid(row=3,column=1,padx=10,pady=10)

           lbl_stock_modificar_productos=Label(lblframe_modificar_productos,text='stock')
           lbl_stock_modificar_productos.grid(row=4,column=0,padx=10,pady=10)
           self.txt_stock_modificar_productos=tp.Entry(lblframe_modificar_productos,width=40)
           self.txt_stock_modificar_productos.grid(row=4,column=1,padx=10,pady=10)

           lbl_minimo_modificar_productos=Label(lblframe_modificar_productos,text='minimo')
           lbl_minimo_modificar_productos.grid(row=5,column=0,padx=10,pady=10)
           self.txt_minimo_modificar_productos=tp.Entry(lblframe_modificar_productos,width=40)
           self.txt_minimo_modificar_productos.grid(row=5,column=1,padx=10,pady=10)
        
           btn_guardar_modificar_productos=tp.Button(lblframe_modificar_productos,text='Guardar',width=38,bootstyle='warning',command=self.modificar_productos)
           btn_guardar_modificar_productos.grid(row=6,column=1,padx=10,pady=10)
           self.llenar_entrys_modificar_productos()
           self.txt_producto_modificar_productos.focus()
    def centrar_ventana_modificar_productos(self,ancho,alto):
        ventana_ancho=ancho
        ventana_alto=alto

        pantalla_ancho=self.frame_rigth.winfo_screenwidth()
        pantalla_alto=self.frame_rigth.winfo_screenheight()

        cordenadas_x=int((pantalla_ancho/2)-(ventana_ancho/2))
        cordenadas_y=int((pantalla_alto/2)-(ventana_ancho/2))
        self.frame_modificar_productos.geometry("{}x{}+{}+{}".format(ventana_ancho,ventana_alto,cordenadas_x,cordenadas_y))
    def llenar_entrys_modificar_productos(self):
        #Liampiaremos todos los entry
        self.txt_codigo_modificar_productos.delete(0,END)    
        self.txt_producto_modificar_productos.delete(0,END)
        self.txt_costo_modificar_productos.delete(0,END)
        self.txt_precio_modificar_productos.delete(0,END)
        self.txt_stock_modificar_productos.delete(0,END)
        self.txt_minimo_modificar_productos.delete(0,END)
        #llenamos los entrys
        self.txt_codigo_modificar_productos.config(state=NORMAL) 
        self.txt_codigo_modificar_productos.insert(0,self.val_mod_prod[0]) 
        self.txt_codigo_modificar_productos.config(state='readonly')    
        self.txt_producto_modificar_productos.insert(0,self.val_mod_prod[1])
        self.txt_costo_modificar_productos.insert(0,self.val_mod_prod[2])
        self.txt_precio_modificar_productos.insert(0,self.val_mod_prod[3])
        self.txt_codigo_modificar_productos.config(state=NORMAL) 
        self.txt_stock_modificar_productos.insert(0,self.val_mod_prod[4])
        self.txt_codigo_modificar_productos.config(state='readonly') 
        self.txt_minimo_modificar_productos.insert(0,self.val_mod_prod[5])
    def modificar_productos(self):
        if (self.txt_codigo_modificar_productos.get()==""or self.txt_producto_modificar_productos.get()=="" or self.txt_costo_modificar_productos.get()==""or self.txt_precio_modificar_productos.get()=="" or self.txt_stock_modificar_productos.get()=="" or self.txt_minimo_modificar_productos.get()==""):
          messagebox.showwarning("Guardando Productos","Algun campo no es valido revisar")
          return
        #capturador de error
        try:
            #establecer la conexion
            miconexion=sqlite3.connect('ventas.db')
            #creamos el cursor
            micursor=miconexion.cursor()

            datos_modificar_productos=(self.txt_producto_modificar_productos.get() ,self.txt_costo_modificar_productos.get(),self.txt_precio_modificar_productos.get(),self.txt_stock_modificar_productos.get(),self.txt_minimo_modificar_productos.get())
            
            #consultamos la base de datos 
            micursor.execute("UPDATE productos SET producto=?,costo=?,precio=?,stock=?,minimo=? WHERE codigo="+self.txt_codigo_modificar_productos.get(),(datos_modificar_productos))
            messagebox.showinfo('Modificar Productos',"Productos Modificado Correctamente")
            miconexion.commit()
            self.val_mod_prod=self.tree_lista_productos.item(self.productos_seleccionado,text='',values=(self.txt_codigo_modificar_productos.get(),self.txt_producto_modificar_productos.get(), self.txt_costo_modificar_productos.get(),self.txt_precio_modificar_productos.get(), self.txt_stock_modificar_productos.get(), self.txt_minimo_modificar_productos.get()))
            
            self.frame_modificar_productos.destroy()#cerramos ventana,guardar nuevo usuario
            self.ventana_lista_productos()#cargamos nuevamente la ventana para ver los cambios 
            #cerramos la conexion
            miconexion.close()

        except:
            #mensaje si ocurre algun error
            messagebox.showerror("Modificando Productos","Ocurrio un error al Modificar Productos")
    def eliminar_producto(self):
            productos_selec_eliminar=self.tree_lista_productos.focus()
            valor_productos_selec_eliminar=self.tree_lista_productos.item(productos_selec_eliminar,'values')
            if valor_productos_selec_eliminar!='':
                respuesta=messagebox.askquestion('Elimando Producto ','¿Estas seguro de eliminar?')
                if respuesta=='yes':
                   #establecer la conexion
                   miconexion=sqlite3.connect('ventas.db')
                   #creamos el cursor
                   micursor=miconexion.cursor()
                   #consultamos la base de datos 
                   micursor.execute("DELETE FROM productos WHERE codigo="+str(valor_productos_selec_eliminar[0]))

                   #aplicamos cambios 
                   miconexion.commit()
                   messagebox.showinfo('Eliminado productos','Eliminado correctamente')
                #    self.mostrar_productos()
                   #cerramos la conexion
                   miconexion.close()
            else:
                messagebox.showerror('Eliminado Productos','Eliminacion cancelada')
    def borrar_frames(self):
        for frames in self.frame_center.winfo_children():
            frames.destroy()        
    #=================VENTAS==================
    def ventana_lista_ventas(self):
        self.borrar_frames()
        self.frame_lista_ventas=Frame(self.frame_center)
        self.frame_lista_ventas.grid(row=0,column=0,columnspan=2,sticky=NSEW)

        self.lblframe_botones_ventas=LabelFrame(self.frame_lista_ventas)
        self.lblframe_botones_ventas.grid(row=0,column=0,padx=10,pady=10,sticky=NSEW)

        btn_detalle_ventas=tp.Button(self.lblframe_botones_ventas,text='DETALLE',width=15
                                       ,bootstyle="success")
        btn_detalle_ventas.grid(row=0,column=0,padx=5,pady=5)
        
        btn_cantidad_ventas=tp.Button(self.lblframe_botones_ventas,text='CANTIDAD',width=15,bootstyle="warnig")
        btn_cantidad_ventas.grid(row=0,column=1,padx=5,pady=5)

        btn_descuento_ventas=tp.Button(self.lblframe_botones_ventas,text='DESCUENTO',width=15,bootstyle="danger")
        btn_descuento_ventas.grid(row=0,column=2,padx=5,pady=5)

        btn_pagar_ventas=tp.Button(self.lblframe_botones_ventas,text='PAGAR',width=15,bootstyle="danger")
        btn_pagar_ventas.grid(row=0,column=3,padx=5,pady=5)

        btn_credito_ventas=tp.Button(self.lblframe_botones_ventas,text='CREDITO',width=15,bootstyle="danger")
        btn_credito_ventas.grid(row=0,column=4,padx=5,pady=5)

        btn_eliminar_ventas=tp.Button(self.lblframe_botones_ventas,text='ELIMINAR',width=15,bootstyle="danger")
        btn_eliminar_ventas.grid(row=0,column=5,padx=5,pady=5)

        self.lblframe_busqueda_ventas=LabelFrame(self.frame_lista_ventas)
        self.lblframe_busqueda_ventas.grid(row=1,column=0)

        self.busqueda_ventas=ttk.Entry(self.lblframe_busqueda_ventas,width=50)
        self.busqueda_ventas.grid(row=0,column=0,padx=5,pady=5)
        #self.busqueda_ventas.bind('<Key>')
    
        #==========================================Treeview=========================================
        
        self.lblframe_tree_ventas=LabelFrame(self.frame_lista_ventas)
        self.lblframe_tree_ventas.grid(row=2,column=0,padx=10,pady=10,sticky=NSEW)

        #crear columnas
        columnas=("codigo","detalle","cantidad","descuento","costo","pagar","credito","subtotal")
        
        self.tree_lista_ventas=tp.Treeview(self.lblframe_tree_ventas,column=columnas,
                                        height=17,show='headings',bootstyle='dark')
        self.tree_lista_ventas.grid(row=0,column=0)

        #cabeceras del treeview
        self.tree_lista_ventas.heading("codigo",text="Codigo",anchor=W)
        self.tree_lista_ventas.heading("detalle",text="Detalle",anchor=W)
        self.tree_lista_ventas.heading("cantiadad",text="Cantiadad",anchor=W)
        self.tree_lista_ventas.heading("descuento",text="Descuento",anchor=W)
        self.tree_lista_ventas.heading("costo",text="Costo",anchor=W)
        self.tree_lista_ventas.heading("pagar",text="Pagar",anchor=W)
        self.tree_lista_ventas.heading("credito",text="Credito",anchor=W)
        self.tree_lista_ventas.heading("subtotal",text="Subtotal",anchor=W)

        #Configurar las columnas que quiero que se muestren
        self.tree_lista_ventas['displaycolumns']=("codigo","detalle","cantidad","descuento","pagar","subtotal") 

        #CREAR BARRA DE DESPLAZAMIENTO
        tree_scroll_ventas=tp.Scrollbar(self.frame_lista_ventas,bootstyle='round success')                           
        tree_scroll_ventas.grid(row=2,column=1)

        #CONFIGURACION  DE BARRA 
        tree_scroll_ventas.config(command=self.tree_lista_ventas.yview)    
        #self.buscar_ventas('')
        self.busqueda_ventas.focus()

def main():
    app=ventana()
    app.title('sistema de ventas')
    app.state('zoomed')
    tp.Style('superhero')
    app.mainloop()
if __name__=='__main__':
    main()