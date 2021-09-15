# Importar Bibliotecas
from tkinter import *
from tkinter import messagebox
from tkinter import ttk 
import sqlite3

# Desarrollo de la Interfaz grafica
root=Tk()
root.title("Aplicación CRUD con Base de Datos")
root.geometry("600x350")

miId=StringVar()
N_empleado=StringVar()
producto=StringVar()
costo=StringVar()

def conexionBBDD():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()

	try:
		miCursor.execute('''
			CREATE TABLE empleado (
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			NOMBRE VARCHAR(50) NOT NULL,
			PRODUCTO VARCHAR(50) NOT NULL,
			COSTO INT NOT NULL)
			''')
		messagebox.showinfo("CONEXION","Base de Datos Creada exitosamente")
	except:
		messagebox.showinfo("CONEXION", "Conexión exitosa con la base de datos")

def eliminarBBDD():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	if messagebox.askyesno(message="¿Los Datos se perderan definitivamente, Desea continuar?", title="ADVERTENCIA"):
		miCursor.execute("DROP TABLE empleado")
	else:
		pass
	limpiarCampos()
	mostrar()

def salirAplicacion():
	valor=messagebox.askquestion("Salir","¿Está seguro que desea salir de la Aplicación?")
	if valor=="yes":
		root.destroy()

def limpiarCampos():
	miId.set("")
	N_empleado.set("")
	producto.set("")
	costo.set("")

def mensaje():
	acerca='''
	Aplicación CRUD
	Version 1.0
	Tecnología Python Tkinter
	Nos pone un 100? 

	░▐▓█▀▀▀▀▀▀▀▀▀█▓▌
	░▐▓█░░▄▀▄▀▄░░█▓▌
	░▐▓█░░▀▄─▄▀░░█▓▌
	░▐▓█▄▄▄▄█▄▄▄▄█▓▌
	░░░░░▄▄███▄▄░░░░
	'''
	messagebox.showinfo(title="INFORMACION", message=acerca)

################################ Métodos CRUD ##############################

def crear():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	try:
		datos=N_empleado.get(),producto.get(),costo.get()
		miCursor.execute("INSERT INTO empleado VALUES(NULL,?,?,?)", (datos))
		miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA","Ocurrió un error al crear el registro, verifique conexión con BBDD")
		pass
	limpiarCampos()
	mostrar()

def mostrar():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	registros=tree.get_children()
	for elemento in registros:
		tree.delete(elemento)

	try:
		miCursor.execute("SELECT * FROM empleado")
		for row in miCursor:
			tree.insert("",0,text=row[0], values=(row[1],row[2],row[3]))
	except:
		pass

                ################################## Tabla ################################
tree=ttk.Treeview(height=10, columns=('#0','#1','#2'))
tree.place(x=0, y=130)
tree.column('#0',width=100)
tree.heading('#0', text="ID", anchor=CENTER)
tree.heading('#1', text="N.Empleado", anchor=CENTER)
tree.heading('#2', text="Producto", anchor=CENTER)
tree.column('#3', width=100)
tree.heading('#3', text="Costo", anchor=CENTER)

def seleccionarUsandoClick(event):
	item=tree.identify('item',event.x,event.y)
	miId.set(tree.item(item,"text"))
	N_empleado.set(tree.item(item,"values")[0])
	producto.set(tree.item(item,"values")[1])
	costo.set(tree.item(item,"values")[2])

tree.bind("<Double-1>", seleccionarUsandoClick)



def actualizar():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	try:
		datos=N_empleado.get(),producto.get(),costo.get()
		miCursor.execute("UPDATE empleado SET NOMBRE=?, PRODUCTO=?, COSTO=? WHERE ID="+miId.get(), (datos))
		miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA","Ocurrió un error al actualizar el registro")
		pass
	limpiarCampos()
	mostrar()

def borrar():
	miConexion=sqlite3.connect("base")
	miCursor=miConexion.cursor()
	try:
		if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
			miCursor.execute("DELETE FROM empleado WHERE ID="+miId.get())
			miConexion.commit()
	except:
		messagebox.showwarning("ADVERTENCIA","Ocurrió un error al tratar de eliminar el registro")
		pass
	limpiarCampos()
	mostrar()

###################### Colocar widgets en la VISTA ######################
########## Creando Los menus ###############
menubar=Menu(root)
menubasedat=Menu(menubar,tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command=conexionBBDD)
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu=Menu(menubar,tearoff=0)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=mensaje)
menubar.add_cascade(label="Ayuda",menu=ayudamenu)

############## Creando etiquetas y cajas de texto ###########################
e1=Entry(root, textvariable=miId)

l2=Label(root, text="N.Empleado")
l2.place(x=20,y=10)
e2=Entry(root, textvariable=N_empleado, width=50)
e2.place(x=100, y=10)

l3=Label(root, text="Producto")
l3.place(x=30,y=40)
e3=Entry(root, textvariable=producto)
e3.place(x=100, y=40)

l4=Label(root, text="Costo")
l4.place(x=280,y=40)
e4=Entry(root, textvariable=costo, width=10)
e4.place(x=320, y=40)

l5=Label(root, text="USD")
l5.place(x=380,y=40)

################# Creando botones ###########################

b1=Button(root, text="Crear Registro", command=crear)
b1.place(x=50, y=90)
b2=Button(root, text="Modificar Registro", command=actualizar)
b2.place(x=180, y=90)
b3=Button(root, text="Mostrar Lista", command=mostrar)
b3.place(x=320, y=90)
b4=Button(root, text="Eliminar Registro",bg="red", command=borrar)
b4.place(x=450, y=90)


root.config(menu=menubar)


root.mainloop()