#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ttk
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
import MySQLdb
import os
#Codigo escrito por Guillermo Gimenez 2015
#DATOS DB = 
HOST = 'localhost'
USUARIO = 'root'
PASS = ''
NOMBREDB = 'l2jdb'
DIRECTORIO_SERVER = ''
DIRECTORIO_L2 = ''
print "[+]L2TEU Iniciado:::::::::::::::"
def consultar(query=''): 
		datos = [HOST, USUARIO, PASS, NOMBREDB] 
		conn = MySQLdb.connect(*datos)  
		cursor = conn.cursor()         
		cursor.execute(query)          
		dat = []
		if query.upper().startswith('SELECT'): 
			data = cursor.fetchall()  # Traer los resultados de un select 
			dat = data
		else:conn.commit()              # Hacer efectiva la escritura de datos 
		cursor.close()               
		conn.close
		return dat
def conseguir(nombre_tabla,que_cosa):#SELECT id FROM characters
	#NOMBRE DE LA TABLA, ID DE COLUMNA , CABEZAL DE GUARDADO,DONDE
	donde_guardar = {}
	consulta = "SELECT %s FROM %s" %(que_cosa,nombre_tabla)
	return consultar(consulta)
def actualizar(tabla,verificacion,dato):
		consulta = "UPDATE %s set %s WHERE %s" % (tabla,dato,verificacion)
		consultar(consulta)
#INICIALIZACION DE VARIABLES BASICAS Y GLOBALES
armaduras = {}
armas = {}
items = {}
npc = []
teleport = {}
tablas_lista= ["account_data","accounts","armor","armorsets","auction","auction_bid","auction_watch","auto_announcements","auto_chat","auto_chat_text","boxaccess","boxes","castle","characters","clan_data","npc","teleport","weapon"]
###############################################
codigo_actual = []
NOMBRE_GEN = "indef"#Nombre global de "Nombre"
ID_GEN = 0#ID Global aun no definida
TIPO_GEN = 0#Tipo global no definido
elegido ="indefinido"
ACTUAL = []
INDICE_PROCESO = 1
productos = {} #ALMACENAMIENTO TEMPORAL
archivo_html = 0
PUNTERO_AUX  = 0
temporal_copia =0
muestra = 0
muestra0 = 0
archivo_actual_xml = 0
macros_lista = {
	"Nivel GM":["characters","char_name","accesslevel"],
	"Nombre de PJ":["characters","char_name","char_name"],
	"Nivel de PJ":["characters","char_name","level"],
	"Nivel de PJ":["characters","char_name","level"],
	"ID de cuenta":["accounts","login","login"],
	"ID de cuenta en PJ":["characters","account_name","account_name"]}
tipos = [
		"L2Npc",
		"L2RaidBoss",
		"L2Monster",
		"L2SiegeSummon",
		"L2NpcBuffer",
		"L2ClanHallManager",
		"L2Guard",
		"L2VillageMaster",
		"L2Merchant",
		"L2Teleporter",
		"L2Warehouse",
		"L2Trainer",
		"L2Adventurer",
		"L2Minion",
		"L2ManorManager",
		"L2Pet",
		"L2CastleTeleporter",
		"L2Doormen",
		"L2SiegeGuard",
		"L2MercManager",
		"L2TamedBeast",
		"L2CastleChamberlain",
		"L2FestivalMonster",
		"L2GrandBoss",
		"L2FriendlyMob",
		"L2WyvernManager",
		"L2FestivalGuide",
		"L2SignsPriest",
		"L2CabaleBuffer",
		"L2CastleWarehouse",
		"L2CastleBlacksmith",
		"L2SymbolMaker",
		"L2RiftInvader",
		"L2Chest",
		"L2FeedableBeast",
		"L2OlympiadManager"]
def Acerca_de(x):
	f = Toplevel()
	f.title("Acerca de L2JTEU Alpha")
	f.iconbitmap("icon.ico")
	f.geometry("400x257+350+250")
	f.resizable(width=FALSE,height=FALSE)
	foto = PhotoImage(file="logo.gif")
	f0 = Label(f,image=foto)
	f0.pack()
	f.transient(x)
	f.grab_set()
	x.wait_window()
estilor = {"Normal":"texto",
					"Especial 1":""" width=204 height=14 back="sek.cbui36" fore="sek.cbui72\"""",
					"Estilo 2": """"width=204 height=14 back="sek.cbui55" fore="sek.cbui55\"""",
					"Boton Azul normal":""" width=75 height=21 back="L2UI_ch3.Btn1_normalOn" fore="L2UI_ch3.Btn1_normal\""""
					}
def procesar_sql_normal():#Abrir y procesar SQL para ser reconocido normalmente
		try:npc.append(consultar("SELECT * FROM npc"))
		except:showerror("Error","Problema al cargar la tabla 'npc' correspondientes en la Database\n Revisar datos de conexion o existencias de las tablas")
		print "[+]Lista de NPC Procesado Correctamente"
def procesar_sql(nombre,lugar_almacenamiento):#Abrir y procesar SQL para ser reconocido por XML
			cabezal = "SELECT * FROM %s"%(nombre)
			consulta = consultar(cabezal)
			for i in consulta:
					lugar_almacenamiento[int(i[0])] = i[0:8]
			print "[+]"+nombre+".sql Procesado Correctamente"
################FIN DE INICIALIZACION COMIENZO DE PROGRAMA
def buscar_item(x):#BUSCAR ITEM POR ID Y DEVOLVER NOMBRE
		if x in armaduras:return ((armaduras[int(x)])[1])
		if x in armas:return (armas[int(x)])[1]
		if x in items:return (items[int(x)])[1]
def buscar(x,com,vv):#BUSCAR EN COMBOX DE XML POR ID
			coincidencias = []
			for i in armaduras:
				d = buscar_item(i)
				if x in (armaduras[int(i)])[1]:coincidencias.append(d)
			for i in armas:	
				d = buscar_item(i)
				if x in (armas[int(i)])[1]:coincidencias.append(d)
			for i in items:	
				d = buscar_item(i)
				if x in (items[int(i)])[1]:coincidencias.append(d)	
			if coincidencias == []:showinfo("No encontrado!","No se han encontrado coincidencias.")
			else:
				for i in coincidencias:
					if i == com.get():
						com.set(i)
						break
				coincidencias.sort()
				mini = Toplevel()
				mini.geometry("300x300+350+250")
				mini.title("Coincidencias:")
				barra = Scrollbar(mini,orient=VERTICAL)
				caja = Listbox(mini,width=40,height=60,yscrollcommand=barra.set)
				barra.config(command=caja.yview)
				barra.pack(side=RIGHT,fill=Y)
				caja.pack()
				for i in coincidencias:caja.insert(END,i)
				def seleccionar_coincidencia(object):
					com.set(caja.get(caja.curselection()[0]))
					mini.destroy()
				caja.bind("<Double-Button-1>",seleccionar_coincidencia)
				mini.transient(vv)
				mini.grab_set()
				vv.wait_window(mini)
def buscar_general(x,com,vv,que):#BUSCAR EN COMBOX EN NPC
			coincidencias = []
			for e in que:
					try:
						for i in e: 
							st = ((i[2]).replace("\"","").replace("'","").replace("\s","'s"))
							if x in st[1:len(st)-1]:coincidencias.append(st[0:len(st)])
					except:
						if x in e:coincidencias.append(e)
			if coincidencias == []:showinfo("No encontrado!","No se han encontrado coincidencias.")
			else:
				for i in list(set(coincidencias)):
					if i == com.get():
						com.set(i)
						break
				coincidencias.sort()
				mini = Toplevel()
				mini.geometry("300x300+350+250")
				mini.title("Coincidencias:")
				barra = Scrollbar(mini,orient=VERTICAL)
				caja = Listbox(mini,width=40,height=60,yscrollcommand=barra.set)
				barra.config(command=caja.yview)
				barra.pack(side=RIGHT,fill=Y)
				caja.pack()
				for i in list(set(coincidencias)):caja.insert(END,i)
				def seleccionar_coincidencia(object):
					com.set(caja.get(caja.curselection()[0]))
					mini.destroy()
				caja.bind("<Double-Button-1>",seleccionar_coincidencia)
				mini.transient(vv)
				mini.grab_set()
				vv.wait_window(mini)
bien,go = 0,0
def AIO_Creador(x):
	#Codeado el 18/05/15
	personajes = {}
	skilles_a_agregar = []
	skilles_a_agregar_final = {}
	aio =  Toplevel()
	aio.iconbitmap("icon.ico")
	aio.title("Skill Administrador")
	aio.geometry("400x240+350+250")
	aio.resizable(width=False,height=False)
	Label(aio,text="Seleccionar opcion de skilles:").pack()
	barra = Scrollbar(aio,orient=VERTICAL)
	lista_personajes = Listbox(aio,width=58,yscrollcommand=barra.set)
	lista_personajes.pack()
	barra.config(command=lista_personajes.yview)
	barra.place(rely=0.09,relx=0.94,height=165)
	#Carga los personajes con sus ID unicos en el diccionario personajes
	consulta =  consultar("SELECT * FROM characters")
	def procesar_agregado(x):
		global bien,go
		for uuu in skilles_a_agregar:
			temp = []
			skill = consultar("SELECT name FROM skill_trees where skill_id=%s"%uuu)
			skill2 = consultar("SELECT level FROM skill_trees where skill_id=%s"%uuu)
			uu = consultar("SELECT skill_id FROM skill_trees where skill_id=%s"%uuu)
			try:ii = uu[0]
			except:ii = uu
			mayor  = 0
			for i in skill2:
				temp.append(i)
			m = 0
			for m1 in temp:
				if m1>m:m=m1
			if skill == ():skilles_a_agregar_final["Skill Desconocido"] = [uuu,(1)]
			else:skilles_a_agregar_final[skill[0]] = [uuu,m]	
		for i in skilles_a_agregar_final:
			ide = (skilles_a_agregar_final[i])[0]
			nombre = i[0]
			if nombre == "S":nombre = "Skill Desconocido"
			nivel = (skilles_a_agregar_final[i])[1]
			try:s = "INSERT INTO character_skills VALUES (%s, %s, %s, '%s', 0)"%(x,ide,nivel[0],nombre)
			except:s = "INSERT INTO character_skills VALUES (%s, %s, %s, '%s', 0)"%(x,ide,nivel,nombre)
			try:
				consultar(s)
				go +=1
			except:pass
	for i in consulta:
		for e in i:personajes[i[2]] = int(i[1])
	#Los carga en la lista
	def funcion_cargar_skilles():
		global bien,go
		persona = personajes[lista_personajes.get(lista_personajes.curselection()[0])]
		archivo_skilles = askopenfile(title="Cargar archivo con los ID skiles")
		n = archivo_skilles.read().split(" ")
		for i in n[0].split("\n"):
			if i == "":pass
			else:
				try:skilles_a_agregar.append(i.split("#")[0].replace("\n",""))
				except:pass
		skilles_a_agregar
		showinfo("Información","Archivo cargado correctamente! %s skilles encontrados y cargados en la memoria."%len(list(set(skilles_a_agregar))))
		confirmacion = askokcancel("Confirmación","Seguro queres darle esos skilles a %s?"%lista_personajes.get(lista_personajes.curselection()[0]))
		if confirmacion == True:procesar_agregado(persona)
		showinfo("Eureka!","Se han agregado %s skilles correctamente! "%go)
	def funcion_dar_skill():
		personaje_actual = personajes[lista_personajes.get(lista_personajes.curselection()[0])]
		nm = lista_personajes.get(lista_personajes.curselection()[0])
		dar = Toplevel()
		dar.iconbitmap("icon.ico")
		Label(dar,text="Seleccionar el skill (enter para buscar)").pack()
		dar.geometry("200x90+300+150")
		dar.title("Dar Skill")
		skilles0 = []
		sk = consultar("SELECT name FROM skill_trees")
		for i in sk:skilles0.append(i[0])
		skill = ttk.Combobox(dar,values=list(set(skilles0)))
		skill.set("Seleccionar skill")
		skill.pack()
		skill.bind("<Return>",lambda c:buscar_general(skill.get(),skill,aio,skilles0))
		def aceptar():
					sk = consultar("SELECT skill_id FROM skill_trees where name='%s'"%skill.get())
					skilles_a_agregar.append(int((sk[0])[0]))
					procesar_agregado(str(personaje_actual))
					showinfo("Confirmación","Se ah agregado el skill %s a %s correctamente"%(skill.get(),nm))
					dar.destroy()
		c = Button(dar,text="Aceptar",width=23,command=aceptar)
		c.place(relx=0.08,rely=0.6)
		dar.transient(aio)
		dar.grab_set()
		aio.wait_window(aio)
	def funcion_ver_skills():
		nm = lista_personajes.get(lista_personajes.curselection()[0])
		personaje_actual = personajes[lista_personajes.get(lista_personajes.curselection()[0])]
		print nm,personaje_actual
		ver = Toplevel()
		ver.iconbitmap("icon.ico")
		ver.geometry("300x300+350+250")
		ver.title("Lista skilles")
		barra = Scrollbar(ver,orient=VERTICAL)
		caja = Listbox(ver,width=50,height=60,yscrollcommand=barra.set)
		barra.config(command=caja.yview)
		barra.pack(side=RIGHT,fill=Y)
		caja.pack()
		skilles_char = []
		sk = consultar("SELECT skill_name FROM character_skills where char_obj_id=%s"%personaje_actual)
		for i in sk:skilles_char.append(str(i[0]))
		for i in skilles_char:caja.insert(END,i)
		skilles_char.sort()
		def eliminar(x):
			el = askokcancel("Confirmación","Seguro que deseas eliminar este skill de %s?"%nm)
			if el == True:
				try:
					s = "DELETE FROM character_skills where skill_name='%s' and char_obj_id=%s"%(x,personaje_actual)
					con = consultar(s)
					caja.delete(caja.index(caja.curselection()[0]))
				except:showerror("Error","Se produjo un error desconocido")
		caja.bind("<Delete>",lambda c:eliminar( caja.get(  caja.curselection()[0]   )))
		ver.transient(aio)
		ver.grab_set()
		aio.wait_window(ver)
	for i in personajes:lista_personajes.insert(END,i)
	boton1 = Button(aio,text="Desde Archivo",width=15,command=funcion_cargar_skilles)
	boton1.place(rely=0.8,relx=0.06)
	boton2 = Button(aio,text="Un Skill",width=15,command=funcion_dar_skill)
	boton2.place(rely=0.8,relx=0.356)
	boton3 = Button(aio,text="Ver/Del Skills",width=15,command=funcion_ver_skills)
	boton3.place(rely=0.8,relx=0.65)
	aio.transient(x)
	aio.grab_set()
	x.wait_window(aio)
def XML_EDITOR():#EDITOR XML
	ventana0 = Tk()
	ventana0.title("Shop XML Editor L2J")
	ventana0.resizable(width=FALSE,height=FALSE)
	ventana0.geometry("600x400+300+200")
	ventana0.iconbitmap("icon.ico")
	DIRECTORIO_XML = DIRECTORIO_SERVER+"\gameserver\data\multisell\\"
	def abrir_xml():#Abrir un XML
		global archivo_actual_xml
		archivo  = askopenfile(initialdir=DIRECTORIO_XML,mode="r",defaultextension="xml",filetypes=[(".XML L2J","*.xml")])
		archivo_actual_xml = archivo
		xml_obtenido = []
		for i in archivo:
			xml_obtenido.append(i)
		actualizar_lista_productos(xml_obtenido)
	#Fin Menu Cascada
	barra_scroll = Scrollbar(ventana0,orient=VERTICAL)
	lista_productos = Listbox(ventana0,height=23,width=96,yscrollcommand=barra_scroll.set)
	barra_scroll.config(command=lista_productos.yview)
	barra_scroll.pack(side=RIGHT,fill=Y)
	lista_productos.place(relx=0.0,rely=0.0)
	def procesar_xml_sell(x):#Abrir y clasificar por orden un xml
		elemento_inicial,temp = 1,[]
		for i in x:
			inte = i.replace("\n","").replace("\t","")
			if "</item>" in inte:
				productos[elemento_actual] = "\n".join(str(u) for u in temp)
				temp=[]
			else:
				if "<item id=" in inte:
					uno,uno0 = [],inte.split(" ")
					for i in uno0:
						if i == "":pass
						else:uno.append(i)
					elemento_actual = int(uno[1].replace("id=\"","").replace("\">","").replace("\"",""))
				elif "production" in inte:temp.append(inte)
				elif "ingredient"  in inte:temp.append(inte)
	def clasificar_productos():#NOMBRE/PRECIO/ITEM A CAMBIO/ENCHANT/ID DE ITEM DE VENTA/CANTIDAD/ENCHANT_OBJETO
		productos_finales = {}
		def ordenar(orden,en):
			NOMBRE_PRODUCTO = 0
			#Ingrediente
			NUMERO_ORDEN = orden
			PRECIO = 0
			ITEM_PRECIO = 0
			ENCHANT = 0
			ENCHANT_PRODUCTO = 0
			#Producto
			ID_ITEM = 0
			CANTIDAD = 0
			cortado = en.split(">")
			
			for i in cortado:
				if "<ingredient" in i:
					cortado0 =  i.split(" ")
					for e in cortado0:
						NUMERO_ORDEN = int(orden)
						if "count=" in e:PRECIO  = int(e.replace("count="+"\"","").replace("/","").replace("\"",""))
						if "id=" in e:ITEM_PRECIO = int(e.replace("id="+"\"","").replace("\"",""))
						if "enchant=" in e:ENCHANT = int(e.replace("enchant="+"\"","").replace("\"","").replace("/",""))
				if "<production" in i:
					cortado0 = i.split(" ")
					for i in cortado0:
					
						if "enchant=" in i:ENCHANT_PRODUCTO =   int(i.replace("enchant="+"\"","").replace("\"","").replace("/",""))
						if "id=" in i:ID_ITEM =   int(i.replace("id="+"\"","").replace("\"",""))
						if "count=" in i:CANTIDAD =  int(i.replace("count="+"\"","").replace("\"","").replace("/",""))
			if ID_ITEM == -1:
				productos_finales[NUMERO_ORDEN] = ["Desconocido",PRECIO,ITEM_PRECIO,ENCHANT,ID_ITEM,CANTIDAD]
				return productos_finales	
			else:
				if ID_ITEM in armaduras:
					NOMBRE_PRODUCTO = (armaduras[ID_ITEM])[0]
			 
					
				if ID_ITEM in armas:
					NOMBRE_PRODUCTO = (armas[ID_ITEM])[0]

				if ID_ITEM in items:
					NOMBRE_PRODUCTO = (items[ID_ITEM])[0]
					
			productos_finales[NUMERO_ORDEN] = [NOMBRE_PRODUCTO,PRECIO,ITEM_PRECIO,ENCHANT,ID_ITEM,CANTIDAD,ENCHANT_PRODUCTO]
			return productos_finales
		for i in productos:
			ordenar(int(i),productos[int(i)])
		return productos_finales
	def actualizar_lista_productos(x):#Actualizar Lista actual de la listbox de productos
		global productos
		lista_productos.delete(0,END)
		productos = {}
		procesar_xml_sell(x)
		productos  = clasificar_productos()
		for i in productos:
			espacio = "                            "
			fila = str(i )+"  "+str(buscar_item((productos[i])[0])) +espacio+"Precio:   "+str((productos[i])[1])
			lista_productos.insert(END,fila)
	def actualizar_final():
		global productos
		lista_productos.delete(0,END)
		for i in productos:
			nombre = "<Desconocido>"
			espacios = "                            "
			try:
				if int((productos[i])[4]) in armaduras: nombre =  buscar_item((armaduras[int((productos[int(i)])[4])])[0])
				if int((productos[i])[4]) in armas: nombre =      buscar_item((armas[int((productos[int(i)])[4])])[0])
				if int((productos[i])[4]) in items: nombre =      buscar_item((items[int((productos[int(i)])[4])])[0])
				try:fila =    str(str(i)+"  "+str(nombre)  +espacios   +  "Precio   :"+str((productos[i])[1]))
				except:fila = str(str(i)+"  "+str(nombre)  +espacios   +  "Precio   :"+str((productos[i])[1]))
				lista_productos.insert(END,fila)
			except:
				productos  = clasificar_productos()
				for i in productos:
					espacios = " "* (48-len((productos[i])[0])+6)
					fila = str(str(i)+"  "+(productos[i])[0])+espacios+"Precio:   "+str((productos[i])[1])
					lista_productos.insert(END,fila)
		lista_productos.activate(SELECCION_ACTUAL)
	def cambiar(primero,segundo,diccionario):#Intercambiar valores en un diccionario
		global productos
		elemento_uno,elemento_dos,cache = diccionario[primero],diccionario[segundo],[]
		cache.append(diccionario[primero])
		diccionario[primero] , diccionario[segundo]= diccionario[segundo],cache[0]
		productos = diccionario	
	SELECCION_ACTUAL = 0
	def mover_hacia_abajo(x):
		try:
			cambiar(x,x+1,productos)
			lista_productos.itemconfig(x,background="#042A93",fg="#FFFFFF")
			actualizar_final()
			lista_productos.activate(x-1)
		except:showerror("Error","No se puede mover mas el objeto")
	def doubles(x):
			cambiar(x,x+1,productos)
			lista_productos.itemconfig(x,background="#042A93",fg="#FFFFFF")
	def mover_hacia_arriba(x):
		try:
			cambiar(x,x-1,productos)
			lista_productos.itemconfig(x,background="#042A93",fg="#FFFFFF")
			actualizar_final()
			lista_productos.activate(x-1)
		except:showerror("Error","No se puede mover mas el objeto")
	items_lista2 = {}
	for i in armaduras:items_lista2[(armaduras[int(i)])[1]] = i
	for i in armas:items_lista2[(armas[int(i)])[1]] = i
	for i in items:items_lista2[(items[int(i)])[1]] = i
	items_lista =  list(set(items_lista2)) #LISTA DE ITEMS PARA UNA COMBOX
	def buscar_item_nombre(x):#BUSCAR ITEM POR NOMBRE
		if x in items_lista2:	return items_lista2[x]
	def propiedades_producto(x):
		global productos
		SELECCION_ACTUAL = lista_productos.index(lista_productos.curselection()[0])+1
		ventana1 = Toplevel()
		ventana1.title("Propiedades")
		ventana1.geometry("260x250+350+250")
		ventana1.resizable(width=FALSE,height=FALSE)
		Label(ventana1,text="Propiedades del producto seleccionado:").pack()
		pre = Label(ventana1,text="Item:")
		pre.place(relx=0.0,rely=0.09)
		item = ttk.Combobox(ventana1,values=items_lista,width=20)
		item.place(relx=0.25,rely=0.1)
		item.bind("<Return>",lambda c:buscar(item.get(),item,ventana1))
		pre = Label(ventana1,text="Cantidad:")
		pre.place(relx=0.0,rely=0.21)
		cantidad = Entry(ventana1)
		cantidad.place(relx=0.25,rely=0.22)
		pre1 = Label(ventana1,text="Enchant:")
		pre1.place(relx=0.0,rely=0.3)
		enchant1 = Entry(ventana1)
		enchant1.place(relx=0.25,rely=0.3)
		pre = Label(ventana1,text="Precio:")
		pre.place(relx=0.0,rely=0.39)
		precio = Entry(ventana1)
		precio.place(relx=0.25,rely=0.39)
		pre = Label(ventana1,text="Objeto:")
		pre.place(relx=0.0,rely=0.5)
		objeto = ttk.Combobox(ventana1,values=items_lista,width=20)
		objeto.place(relx=0.25,rely=0.5)
		objeto.bind("<Return>",lambda c:buscar(objeto.get(),objeto,ventana1))
		pre = Label(ventana1,text="Enchant:")
		pre.place(relx=0.0,rely=0.6)
		enchant = Entry(ventana1)
		enchant.place(relx=0.25,rely=0.6)
		producto = productos[SELECCION_ACTUAL]
		cantidad.insert(END,producto[5])
		precio.insert(END,producto[1])
		item.insert(END,buscar_item(producto[4]))
		enchant.insert(END,producto[3])
		objeto.insert(END,buscar_item(producto[2]))
		enchant1.insert(END,producto[6])
		def guardar():
			global productos
			producto = productos[SELECCION_ACTUAL]
			try:resultado = [producto[0],int(precio.get()),buscar_item_nombre(objeto.get()),int(enchant.get()),buscar_item_nombre(item.get()),int(cantidad.get()),int(enchant1.get())]
			except:showerror("Error","Revisa bien los parametros")
			productos[SELECCION_ACTUAL] = resultado
			if None in resultado:showerror("Error","Error al guardar el cambio, revise los cambios")
			else:
				actualizar_final()
				ventana1.destroy()
		boton = Button(ventana1,text="Guardar Cambios Aplicados",command=guardar)
		boton.place(rely=0.8,relx=0.18)
		ventana1.transient(ventana0)
		ventana1.grab_set()
		ventana0.wait_window(ventana1)
	actualizar_lista_productos("pruebas/20072.xml")
	########################MENU ELEMENTOS
	menu_d = Menu(ventana0,tearoff=0)
	def eliminar():
		SELECCION_ACTUAL = lista_productos.index(lista_productos.curselection()[0])+1
		confirmacion_eliminacion = askokcancel("Confirmacion","Seguro que desea eliminar este producto?")
		if confirmacion_eliminacion  == True:
				for i in range(0,len(productos)):
					try:
						doubles(SELECCION_ACTUAL)
						SELECCION_ACTUAL+=1 
					except:pass
				del productos[len(productos)]
				actualizar_final()
	menu_d.add_command(label="Editar",command=lambda :propiedades_producto( lista_productos.curselection()[0]     )  )
	menu_d.add_command(label="Eliminar  (Supr)",command=eliminar)
	menu_d.add_command(label="Mover Arriba  (Tecla Arriba)",command=lambda :mover_hacia_arriba(lista_productos.index(lista_productos.curselection()[0])+1))
	menu_d.add_command(label="Mover Abajo  (Tecla Abajo)",command=lambda :mover_hacia_abajo(lista_productos.index(lista_productos.curselection()[0])+1))
	def men(event):#Menu de opciones desplegable
		try:menu_d.tk_popup(event.x_root,event.y_root)
		except:menu_d.grab_release()
	lista_productos.bind("<Button-3>",men)#menu desplegable
	lista_productos.bind("<Key-Up>",lambda c:mover_hacia_arriba(lista_productos.index(lista_productos.curselection()[0])+1))
	lista_productos.bind("<Key-Down>",lambda c:mover_hacia_abajo(lista_productos.index(lista_productos.curselection()[0])+1))
	lista_productos.bind("<Delete>",lambda c:eliminar())
	#######################################
	def seleccion_actual(object):lista_productos.config(selectbackground="#000000")
	lista_productos.bind("<Button-1>",seleccion_actual)
	def agregar_producto():
		ventana2 = Toplevel()
		ventana2.geometry("300x300+350+350")
		ventana2.iconbitmap("icon.ico")
		t = Label(ventana2,text="Item a comprar=====================")
		t.place(relx=0.02,rely=0.05)
		t = Label(ventana2,text="Item:")
		t.place(relx=0.0,rely=0.15)
		entrad = ttk.Combobox(ventana2,values=items_lista,width=25)
		entrad.set("Item")
		entrad.place(relx=0.3,rely=0.15)
		entrad.bind("<Return>",lambda c:buscar(entrad.get(),entrad,ventana2))
		t = Label(ventana2,text="Cantidad:")
		t.place(relx=0.0,rely=0.25)
		cantidad = Entry(ventana2,width=25)
		cantidad.place(relx=0.3,rely=0.25)
		t = Label(ventana2,text="Item de intercambio:================")
		t.place(relx=0.02,rely=0.45)
		t = Label(ventana2,text="Objeto:")
		t.place(relx=0.0,rely=0.55)
		objeto = ttk.Combobox(ventana2,values=items_lista,width=25)
		objeto.place(relx=0.3,rely=0.55)
		objeto.set("Adena")
		objeto.bind("<Return>",lambda c:buscar(objeto.get(),objeto,ventana2))
		t = Label(ventana2,text="Precio:")
		t.place(relx=0.0,rely=0.65)
		precio = Entry(ventana2,width=25)
		precio.place(relx=0.3,rely=0.65)
		def agregar():
				global productos
				cajas = [entrad.get(),cantidad.get(),objeto.get(),precio.get(),cantidad.get()]
				errores = []
				for i in cajas:
					if i == "":errores.append(i)
					if entrad == "Item":errores.append("x")
					if objeto == "Adena":errores.append("asd")
				if errores == []:
					ide = buscar_item_nombre(entrad.get())
					if ide == None:ide = "Desconocido"
					objetoo = buscar_item_nombre(objeto.get())
					try:item = [entrad.get(),int(precio.get()),objetoo,0,int(ide),int(cantidad.get()),0]
					except:showerror("Error","Revisa bien los parametros")
					productos[len(productos)+1] = item
					actualizar_final()
					ventana2.destroy()
				else:showerror("ERROR","Rellena todos los campos.")			
		boton = Button(ventana2,text="Agregar",width=40,command=agregar)
		boton.place(relx=0.02,rely=0.85)
		ventana2.transient(ventana0)
		ventana2.grab_set()
		ventana0.wait_window(ventana2)
	menu_superior = Menu(ventana0)
	menu1 = Menu(menu_superior,tearoff=0)
	menu2 = Menu(menu_superior,tearoff=0)
	menu3 = Menu(menu_superior,tearoff=0)
	def ayuda():
		showinfo("Ayuda","Controles:\n Eliminar Producto:Tecla Supr\n Mover de lugar:Tecla arriba/Tecla Abajo\n")
	menu_superior.add_cascade(label="Archivo",menu=menu1)
	menu_superior.add_cascade(label="Edicion",menu=menu2)
	menu_superior.add_cascade(label="Ayuda",menu=menu3)
	menu3.add_command(label="Ayuda..",command=ayuda)
	menu3.add_separator()
	menu3.add_command(label="Acerca de..",command=lambda :Acerca_de(ventana0))
	def guardar_actual():
		generar_codigo()
		global archivo_actual_xml
		if archivo_actual_xml == 0:guardar_como()
		else:
			try:
				j = str(archivo_actual_xml)
				u = j.split(" ")
				p = str(u[2])+str(u[3])
				p7 = p.replace("u'","").replace("',","").replace("'","")
				o = p7.split("/")
				a  = open(o[len(o)-1],"w")
			except:
				a = open(archivo_actual_xml,"w")
			for i in codigo_actual:a.writelines(i)
			a.close()
	def guardar_como():
		global archivo_actual_xml
		generar_codigo()
		nombre0 = str(len(productos))
		direccion = asksaveasfilename(initialdir=DIRECTORIO_XML,initialfile=nombre0,title="Guardar XML",defaultextension="xml",filetypes=[("XML de L2J","*.xml")])
		archivo = open(direccion,"w")
		for i in codigo_actual:
			archivo.writelines(i)
		archivo.close()
		archivo_actual_xml = direccion
	def nuevo():
		global codigo_actual
		codigo_actual = []
		global archivo_actual_xml
		lista_productos.delete(0,END)
		archivo_actual_xml = 0
		lista_productos.insert(END,"")
	menu1.add_command(label="Nuevo",command=nuevo)
	menu1.add_command(label="Abrir",command=abrir_xml)
	menu1.add_command(label="Guardar",command=guardar_actual)
	menu1.add_command(label="Guardar Como",command=guardar_como)
	def salir():
		conf = askyesno("Confirmacion:","Esta seguro que quieres salir del programa?")
		if conf == True:ventana0.destroy()
		else:pass
	menu1.add_separator()
	def salir_a_menu():
		
		conf = askokcancel("Confirmacion","Salir?")
		if conf == True:
			ventana0.destroy()
			Interfaz()
	menu1.add_command(label="Salir..",command=salir_a_menu)
	def generar_codigo():
		global codigo_actual,productos
		try:productos  = clasificar_productos()
		except:pass
		codigo_actual = []
		codigo_actual.append("<?xml version='1.0' encoding='utf-8'?>\n")
		codigo_actual.append("<!-- Editado con L2JTEU -->\n")
		codigo_actual.append(" <list>\n")
		for i in productos:
			cabezal = "<!-- " + str(buscar_item((productos[i])[4])) + " -->\n" 
			codigo_actual.append(cabezal)
			codigo_actual.append("<item id=\""+str(i)+"\">\n")
			codigo_actual.append(" <ingredient id=\""+str((productos[i])[2])+"\" count=\""+str((productos[i])[1])+"\" enchant=\""+str((productos[i])[3])+ "\"/>\n")
			codigo_actual.append(" <production id=\""+str((productos[i])[4])+"\" count=\""+str((productos[i])[5])+"\" enchant=\""+str((productos[i])[6])+ "\"/>\n")
			codigo_actual.append("</item>\n")
			codigo_actual.append("\n")
		codigo_actual.append("</list>\n")
	def ver_codigo_fuente():
		generar_codigo()
		ventan = Toplevel()
		ventan.title("CODIGO FUENTE")
		ventan.geometry("500x500")
		barrita = Scrollbar(ventan,orient=VERTICAL)
		caja = Text(ventan,width=100,height=100,yscrollcommand=barrita.set)
		barrita.config(command=caja.yview)
		barrita.pack(side=RIGHT,fill=Y)
		barrita.set(1,2)
		caja.pack()
		for i in codigo_actual:caja.insert(END,i)
		caja.yview(END)
		ventan.transient(ventana0)
		ventan.grab_set()
		ventana0.wait_window(ventan)
	menu2.add_command(label="Ver codigo Fuente",command=ver_codigo_fuente)
	menu2.add_command(label="Agregar Producto",command=agregar_producto)
	ventana0.config(menu=menu_superior)
	ventana0.mainloop()
def HTML_editor(x,y):#Editor de HTML	
		global elegido,archivo_html,ACTUAL,title_v
		historial = []
		if x == "existente":
			"""
			confirmacion = askokcancel("Confirmaciòn","Abrir archivo existente?")
			if confirmacion == True:
				archivo  = askopenfile(mode="r",defaultextension="htm",filetypes=[("HTM de L2J","*htm"),("HTML de L2J","*html")])
				archivo_html = archivo
				ACTUAL = []
				for i in archivo_html:ACTUAL.append(i)
				ventana0.destroy()
			else:
			"""
			ACTUAL = ["\n","<html><body>","<head>","\n","</head>","\n","\n","\n","\n","\n","\n","\n","\n","\n","</body></html>","\n"]
		ventana  = Toplevel()
		ventana.geometry("800x500+20+32")
		titulo_ventana = "NPC HTML Editor"
		ventana.title(titulo_ventana)
		ventana.iconbitmap("icon.ico")
		ventana.resizable(width=FALSE,height=FALSE)
		sss = "Proceda a editar su Html correspondiente al NPC %s" %(NOMBRE_GEN)
		linea_actual = StringVar()
		barra = Scrollbar(ventana,orient=VERTICAL)
		caja = Listbox(ventana,width=102,height=28,yscrollcommand=barra.set)
		barra.config(command=caja.yview)
		caja.place(rely=0.0,relx=0.00)
		barra.place(rely=0.0,relx=0.78,relheight=1)
		PUNTERO = 1
		def actualizar():
			temp = []
			for i in ACTUAL:temp.append(i)
			historial.append(temp)
			caja.delete(0,END)
			for i in ACTUAL:caja.insert(END,i)
			caja.config(selectbackground="#76FFA5")
		#INICIALIZACION
		actualizar()
		def ac(object):
			global PUNTERO_AUX
			caja.config(selectbackground="#76FFA5")
			actualizar_actual()
			asd = caja.curselection()[0]
			PUNTERO_AUX  = asd
			linea_actual.set(asd-1)
			l = "Linea:"+str(linea_actual.get())
			linea_actual.set(l)
		def ac2(object):
			global PUNTERO_AUX
			caja.config(selectbackground="#EEFFF4")
			PUNTERO_AUX = None
		def editar():
				PUNTERO = caja.index(caja.curselection()[0])
				v = Toplevel()
				v.title("Editar")
				v.geometry("300x300+350+200")
				v.iconbitmap("icon.ico")
				v.resizable(width=FALSE,height=FALSE)
				tex = Text(v,width=40,height=15)
				tex.pack()
				an=  ACTUAL[int(caja.curselection()[0])]
				if an =="":pass
				else:tex.insert(END,ACTUAL[int(caja.curselection()[0])])
				def listo():
					ACTUAL[int(PUNTERO)] = tex.get(1.0,END)
					actualizar()
					v.destroy()
				Button(v,text="Guardar Cambios",command=listo).pack()
				v.transient(ventana)
				v.grab_set()
				ventana.wait_window(v)
		def elim():
			del ACTUAL[int(caja.curselection()[0])]
			actualizar()
		caja.bind("<Delete>",lambda c:elim())
		def insertar(x):
			if PUNTERO_AUX == None:showerror("Advertencia!","Selecciona primer el elemento antes de proceder (Doble click)")
			else:
				ACTUAL.insert(int(PUNTERO_AUX),x)
				actualizar()
		caja.bind("<Key-e>",lambda c:editar())
		def texto():
		  if PUNTERO_AUX == None:showerror("Advertencia!","Selecciona primer el elemento antes de proceder (Doble click)")
		  else:
			ventan = Toplevel()
			ventan.title("Msg")
			ventan.iconbitmap("icon.ico")
			ventan.resizable(width=FALSE,height=FALSE)
			ventan.geometry("300x100+719+26")
			Label(ventan,text="Texto/Mensaje:").pack()
			texto = Entry(ventan,width=39)
			texto.pack()
			Label(ventan,text="___________Propiedades___________").pack()
			colores = {"Normal":"FFFFFF","Blanco":"FFFFFF","Negro":"000000","Azul":"75759B","Celeste":"6FD8DB","Rojo":"FF1C00","Purpura":"A847A2","Verde":"05D92B","Amarillo":"FFFF00","Verde Claro":"90EE90","Naranja":"FB8600"}	
			clr =list(set(colores))
			a = Label(ventan,text="Color:")
			a.place(rely=0.7,relx=0.0)
			b = ttk.Combobox(ventan,values=clr)
			b.place(rely=0.7,relx=0.13)
			b.insert(END,"Normal")
			def generar():
				if texto.get() == "":showerror(title="Error",message="Inserta un texto!")
				else:
					st = "<font color=\"%s\">%s</font>"%(colores[b.get()],texto.get())
					insertar(st)
					ventan.destroy()
			w = Button(ventan,text="Listo!",command=generar)
			w.place(rely=0.7,relx=0.8)
			ventan.transient(ventana)
			ventan.grab_set()
			ventana.wait_window(ventan)
		titulo = Button(ventana,text="Titulo",width=14,command=lambda:insertar("\n<title>Titulo</title>\n"))
		titulo.place(rely=0.0,relx=0.81)
		mensaje = Button(ventana,text="Mensaje",width=14,command=texto)
		mensaje.place(rely=0.0500,relx=0.81)
		def boton():
		  if PUNTERO_AUX == None:showerror("Advertencia!","Selecciona primer el elemento antes de proceder (Doble click)")
		  else:
				ven = Toplevel()
				ven.resizable(width=FALSE,height=FALSE)
				ven.title("Boton Editor")
				ven.iconbitmap("icon.ico")
				ven.geometry("500x200+350+200")
				text = Label(ven,text="Texto del botón:").pack()
				texto = Entry(ven,width=30)
				#text2 = Label(ven,text="Tamaño:")
				#text2.place(relx=0.8,rely=0.0)
				#taman = ["32x32","72x72","75x21"]
				#tam = Combobox(ven,values=taman,width=8)
				#tam.place(relx=0.8,rely=0.11)
				texto = Entry(ven,width=30)
				estilos = list(set(estilor))
				est = Label(ven,text="Estilo:")
				est.place(relx=0.0,rely=0.4)
				estilo = ttk.Combobox(ven,values=estilos)
				estilo.place(relx=0.077,rely=0.4)
				estilo.set("Normal")
				posicione  = {"Centro":"center"}
				asd = IntVar()
				posicionv = Checkbutton(ven,text="Centrado",var=asd)
				posicionv.place(relx=0.0,rely=0.55)
				asd1 = IntVar()
				obj = Checkbutton(ven,text="Objeto de tabla",var=asd1)
				obj.place(relx=0.0,rely=0.65)
				valuess = {"Ir a HTML":"Chat", "Quest/Script":"Quest","Cerrar ventana":"Close", "Ir a Multisell":"multisell", "Vender":"Sell", "Comprar":"Buy", "Ir a Localizacion":"goto","Guardar en Ware":"Deposit","Sacar de Ware":"Withdraw"}
				vu = list(set(valuess))
				valor = Label(ven,text="Acción:")
				valor.place(relx=0.5,rely=0.4)
				value = ttk.Combobox(ven,values=vu)
				value.place(relx=0.6,rely=0.4)
				value.set("Acción a realizar")
				dond = Label(ven,text="N° Direccion:")
				dond.place(relx=0.4,rely=0.7)
				donde = Entry(ven,width=30)
				donde.place(relx=0.3,rely=0.8)
				def genera():
				 st = []
				 errores = []
				 if value.get() == "Acción a realizar": errores.append("Accion")
				 if texto.get() == "": errores.append("Texto")
				 if donde.get() == "":errores.append("Direccion de accion")
				 def aplicar(x):
					 atributos0 = []
					 atributos1 = []
					 if asd == 1:
						 atributos0.append("<center>")
						 atributos1.append("</center>")
					 if asd1 == 1:
						 atributos0.append("<td>")
						 atributos1.append("</td>")
					 return str("".join(str(y)for y in atributos0) + x + "".join(str(u)for u in atributos1))
				 if errores == []:
					 if estilo.get() == "Normal":
								 st = "<a action="+"\"" + "bypass -h npc_%objectId%_" + valuess[value.get()]  + " " +donde.get() + "\"" +">" +texto.get()+"</a>"
								 st0 = aplicar(st)
								 insertar(st0)
								 ven.destroy()
					 else:
								 st = """<button value=""" +"\""+texto.get()+"\"" + " action=" +"\""+"bypass -h npc_%objectId%_" + valuess[value.get()]+ " " + donde.get() + "\"" + estilor[estilo.get()]+">"
								 st0 = "   "+aplicar(st)
								 insertar(st0)
								 ven.destroy()

				 else:
					st = "Los siguientes parametros no fueron correctamente definidos:\n"+ "\n".join(str(u)for u in errores)
					showerror(title="Error",message=st)
				boton = Button(ven,text="Generar Botón!",command=genera)
				boton.place(relx=0.7,rely=0.78)
				texto.pack()
				ven.transient(ventana)
				ven.grab_set()
				ventana.wait_window(ventana)
		boton = Button(ventana,text="Boton",width=14,command=boton)
		boton.place(rely=0.1,relx=0.81)
		barra = Button(ventana,text="Barra",width=14,command=lambda:insertar(""" <img src="L2UI_CH3.herotower_deco" width=256 height=32> """))
		barra.place(rely=0.1500,relx=0.81)
		espacio = Button(ventana,text="Espacio",width=14,command=lambda:insertar("<br>"))
		espacio.place(rely=0.2,relx=0.81)
		caja.bind("<space>",lambda c:insertar("<br>"))
		cent = Button(ventana,text="Centrado<",width=14,command=lambda:insertar("<center>"))
		cent.place(rely=0.3,relx=0.81)
		cent = Button(ventana,text="Centrado>",width=14,command=lambda:insertar("</center>"))
		cent.place(rely=0.3500,relx=0.81)
		tabla = Button(ventana,text="Tabla<",width=14,command=lambda:insertar("<table width=220> <!-- INICIO DE TABLA -->"))
		tabla.place(rely=0.4,relx=0.81)
		tabla = Button(ventana,text="Tabla>",width=14,command=lambda:insertar("</table>  <!-- FIN DE TABLA -->"))
		tabla.place(rely=0.4500,relx=0.81)
		tabla = Button(ventana,text="Fila Tabla<",width=14,command=lambda:insertar("<tr>"))
		tabla.place(rely=0.5,relx=0.81)
		tabla = Button(ventana,text="Fila Tabla>",width=14,command=lambda:insertar("</tr>"))
		tabla.place(rely=0.5500,relx=0.81)
		tabla = Button(ventana,text="Obj Tabla<",width=14,command=lambda:insertar("<td>"))
		tabla.place(rely=0.6,relx=0.81)
		tabla = Button(ventana,text="Obj Tabla>",width=14,command=lambda:insertar("</td>"))
		tabla.place(rely=0.6500,relx=0.81)
		tabla = Button(ventana,text="Comentario",width=14,command=lambda:insertar("<!-- Aca va el comentario -->"))
		tabla.place(rely=0.7500,relx=0.81)
		def insertm(x):
			res = []
			for  i in x.split(" "):
				if i == "-":ACTUAL.insert(int(PUNTERO_AUX),"\n")
				else:ACTUAL.insert(int(PUNTERO_AUX),i)
			actualizar()
		act = StringVar()
		nm_linea = Label(textvar=linea_actual)
		nm_linea.place(rely=0.95,relx=0.0)
		archivo_actual = Label(textvar=act)
		archivo_actual.place(rely=0.95,relx=0.1)
		def actualizar_actual():
				if "<open" in str(archivo_html):
					j = str(archivo_html)
					u = j.split(" ")
					p = str(u[2])+str(u[3])
					p7 = p.replace("u'","")
					l0 = "Actual:"+p7
					act.set(l0)		
				else:
					l0 = "Actual:"+str(archivo_html)
					act.set(l0)
		def ayuda():showinfo(title="Ayuda!",message="Controles:\n\n *Eliminar elemento:Supr\n\n*Selecciona Elemento:Click\n\n\n* X <: *Etiqueta abierta\n* X >:Etiqueta cerrada\n\nDesplazamiento con la ruedita, ASEGURATE DE TENER SELECCIONADO EL ITEM CON DOBLE CLICK PARA MAS PRECISION ;)")
		def guardar(x1):
					global elegido,archivo_html	,ID_GEN, ACTUAL,title_v,DIRECTORIO_HTML
					DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\\"
					if TIPO_GEN == "L2Merchant":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\merchant\\"
					if TIPO_GEN == "L2Npc":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\default\\"
					if TIPO_GEN == "L2Guard":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\guard\\"
					if TIPO_GEN == "L2Siege":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\siege\\"
					if TIPO_GEN == "L2ClanHallManager":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\clanHallManager\\"
					if TIPO_GEN == "L2VillageMaster":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\villagemaster\\"
					if TIPO_GEN == "L2Teleporter":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\teleporter\\"
					if TIPO_GEN == "L2Warehouse":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\warehouse\\"
					if TIPO_GEN == "L2Trainer":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\trainer\\"
					if TIPO_GEN == "L2Adventurer":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\adventurer_guildsman\\"
					if TIPO_GEN == "L2CastleWarehouse":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\castlewarehouse\\"
					if TIPO_GEN == "L2ManorManager":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\manormanager\\"
					if TIPO_GEN == "L2NpcBuffer":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\npcbuffer\\"
					if TIPO_GEN == "L2MercManager":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\mercmanager\\"
					if TIPO_GEN == "L2CastleBlacksmith":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\castleblacksmith\\"
					if TIPO_GEN == "L2SignsPriest":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\seven_signs\\"
					if TIPO_GEN == "L2SymbolMaker":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\symbolmaker\\"
					if TIPO_GEN == "L2OlympiadManager":DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\olympiad\\"
					if TIPO_GEN == 0:DIRECTORIO_HTML = DIRECTORIO_SERVER+"\gameserver\data\html\\"
					actualizar_actual()
					if x1 == 2:
						if x  =="existente":
							ACTUAL = ["<html><body>","<head>","\n","</head>","\n","\n","\n","\n","\n","\n","\n","\n","\n","</body></html>","\n","\n"]
							actualizar()
							archivo_html = 0
							actualizar_actual()
					if x =="existente" and x1 == 0:
						if archivo_html == 0:
								lol = asksaveasfilename(initialdir=DIRECTORIO_HTML,defaultextension="htm",filetypes=[("HTM de L2J","*.htm")])
								l =  str(lol).split("/")
								l0 = l[len(l)-1]
								ID_GEN = l0.replace(".htm","")
								archivo = open(lol,"w")
								archivo_html = lol
								for i in ACTUAL:
									am = i
									archivo.writelines(am)	
								actualizar_actual()
								showinfo("Guardado!","El archivo ah sido correctamente guardado")
						else:
							lol = asksaveasfilename(initialdir=DIRECTORIO_HTML,defaultextension="htm",filetypes=[("HTM de L2J","*.htm")])
							l =  str(lol).split("/")
							l0 = l[len(l)-1]
							ID_GEN = l0.replace(".htm","")
							archivo = open(lol,"w")
							archivo_html = lol
							actualizar_actual()
							for i in ACTUAL:
									am = i
									archivo.writelines(am)		
					if x =="existente" and x1 == 1:
						if archivo_html == 0:
								lol = asksaveasfilename(initialdir=DIRECTORIO_HTML,defaultextension="htm",filetypes=[("HTM de L2J","*.htm")])
								l =  str(lol).split("/")
								l0 = l[len(l)-1]
								ID_GEN = l0.replace(".htm","")
								archivo = open(lol,"w")
								archivo_html = lol
								for i in ACTUAL:
									am = i+"\n"
									archivo.writelines(am)		
						else:
							if x  == "existente":
								 if x1 == 1:
									try:
										dire = str( archivo_html).split("'")
										arci = open(dire[1],"w")
									except:arci  = open(archivo_html,"w")
									for i in ACTUAL:
										am = i+"\n"
										arci.writelines(am)				
		def abrir():
			global ACTUAL,title_v,archivo_html
			directorio_html = DIRECTORIO_SERVER+"\gameserver\data\html\\"
			archivo_html0 = askopenfile(initialdir = directorio_html ,mode="r",filetypes=[("HTM de L2J","*htm"),("HTML de L2J","*html")],defaultextension="htm")
			archivo_html = archivo_html0
			ACTUAL=[]
			for i in archivo_html:ACTUAL.append(i)
			actualizar()
			actualizar_actual()
		def borrar():
			del ACTUAL[0:]
			ACTUAL.append("\n")
			actualizar()
		def salir():ventana.destroy()
		def ver_codigo_fuente():
			mini = Toplevel()
			mini.title("Codigo Fuente Actual")
			barra = Scrollbar(mini,orient=VERTICAL)
			barra.pack(side=RIGHT,fill=Y)
			caja = Text(mini,yscrollcommand=barra.set)
			caja.pack()
			barra.config(command=caja.yview)
			for i in ACTUAL:
				caja.insert(END,i)
			caja.yview(END)
			mini.transient(ventana)
			mini.grab_set()
			ventana.wait_window(ventana)
		def filtrar_espacios():
		  global ACTUAL
		  s = []
		  for i in ACTUAL:
			  if i == "\n" :pass
			  else: s.append(i)
		  ACTUAL = s
		  actualizar()
		menu0 = Menu(ventana)
		menu1 = Menu(menu0,tearoff=0)
		menu2 = Menu(menu0,tearoff=0)
		menu0.add_cascade(label="Archivo",menu=menu1)
		menu2.add_command(label="Ver codigo fuente",command=ver_codigo_fuente)
		menu0.add_cascade(label="Edición",menu=menu2)
		menu2.add_command(label="Eliminar espacios",command=filtrar_espacios)
		def tipo():
			global TIPO_GEN
			g = Toplevel()
			g.iconbitmap("icon.ico")
			g.geometry("0x40+350+250")
			l = ttk.Combobox(g,values=tipos)
			l.pack()
			if TIPO_GEN == 0:
				l.set("L2Npc")
			else:l.set(str(TIPO_GEN))
			def c():
				global TIPO_GEN
				TIPO_GEN = l.get()
				g.destroy()
			Button(g,text="Aceptar",command=c).pack()
			l.bind("<Return>",lambda:c())
			g.transient(ventana)
			g.grab_set()
			ventana.wait_window(g)
		menu2.add_command(label="Tipo de NPC",command=tipo)
		menu3 = Menu(menu0,tearoff=0)
		menu0.add_cascade(label="Ayuda",menu=menu3)
		menu3.add_command(label="Ayuda",command=ayuda)
		menu3.add_separator()
		menu3.add_command(label="Acerca de..",command=lambda : Acerca_de(ventana))
		menu1.add_command(label="Nuevo",command=lambda:guardar(2))
		menu1.add_command(label="Abrir",command=abrir)
		menu1.add_command(label="Guardar",command=lambda:guardar(1))
		menu1.add_command(label="Guardar como..",command=lambda:guardar(0))
		def salir_a_menu():
			conf = askokcancel("Confirmacion","Salir?")
			if conf == True:
				ventana.destroy()
				Interfaz()
		menu1.add_separator()
		menu1.add_command(label="Salir a menu",command=lambda :ventana.destroy())
		mn = Menu(ventana,tearoff=0)
		def copiar():
			global temporal_copia
			if PUNTERO_AUX == None:showerror("Advertencia!","Selecciona primer el elemento antes de proceder (Doble click)")
			else:temporal_copia = caja.get(PUNTERO_AUX)
		def pegar():
			global temporal_copia
			if PUNTERO_AUX == None:showerror("Advertencia!","Selecciona primer el elemento antes de proceder (Doble click)")
			else:
				if temporal_copia== 0:pass
				else:insertar(temporal_copia)
		mn.add_command(label="Editar (E)",command=editar)
		mn.add_command(label="Eliminar (SUPR)",command=elim)
		mn.add_command(label="Copiar",command=copiar)
		mn.add_command(label="Pegar",command=pegar)
		def menu_desplegable(event):
			try:mn.tk_popup(event.x_root,event.y_root)
			except:pass
		caja.bind("<Double-1>",ac)
		caja.bind("<Button-1>",ac2)
		caja.bind("<Button-3>",menu_desplegable)
		menu2.add_command(label="Borrar todo",command=borrar)
		ventana.config(menu=menu0)
		ventana.transient(y)
		ventana.grab_set()
		y.wait_window(ventana)
def NPC_Creator():#EDITOR NPC 
	#Inicializacion de interfaz grafica general
	ventana0  = Tk()
	ventana0.transient()
	ventana0.title("L2J NPC Creador")
	ventana0.geometry("400x300+400+200")
	ventana0.iconbitmap("icon.ico")
	ventana0.resizable(width=FALSE,height=FALSE)
	#Tipos de NPC
	cln = []
	facciones_lista = ['goblin_clan', 'demonic_clan', 'orc_clan', 'lizardman_clan', 'werewolf_clan', 'elemental1_clan', 'skeleton_clan', 'elemental2_clan', 'wererat_clan', 'ol_mahum_clan', 'bugbear_clan', 'scropio_clan', 'ant_clan', 'elemental3_clan', 'elemental4_clan', 'croc_clan2', 'undead_clan', 'dragon_clan', 'mandragora_clan', 'stakato_clan', 'neer_crawler_clan', 'oel_mahum_clan', 'serpent_clan', 'silenos_clan', 'tyrant_clan', 'wolf_clan', 'porta_clan', 'beast_clan', 'torfe_clan', 'giant_leech_clan', 'cave_servant_clan', 'succubus_clan', 'ghost_clan', 'kirunak_clan', 'monster_eye_clan', 'elemental_clan', 'kobold_clan', 'malruk_clan', 'mirrorforest_clan', 'giant_clan', 'hatar_clan', 'doom_clan', 'partisan_clan', 'lizardman_clan1', 'lienrik_clan', 'croc_clan', 'theeder_clan', 'tower_ghost_clan', 'hallate_clan', 'tower_guard_clan', 'undead_clan1', 'zaken_clan', 'kel_mahum_clan', 'hatu_clan', 'green_clan', 'bloody_clan', 'kinpin_clan', 'c_dungeon_clan', 'animal_clan', 'eye_clan', 'divine_clan', 'ketra_orc_clan', 'varka_silenos_clan', 'fire_clan', 'tomb_clan', 'nonpet_clan', 'pet_clan', 'saint_clan', 'necro_clan', 'vampire_clan', 'ssq_clan', 'timiniel_clan', 'abyss_jewel_clan', 'grave_guard_clan', 'grave_keeper_clan', 'q421_tree_clan', 'guard_of_secrets_clan', 'gludio_siege_clan','queen_ant_clan', 'curma_core_clan', 'all_elemental_clan', 'all_elemental2_clan', 'dion_siege_clan', 'giran_siege_clan', 'orfen_clan', 'oren_siege_clan', 'aden_siege_clan', 'mercenary_siege_clan', 'gustav_clan', 'innadril_siege_clan', 'goddard_siege_clan', 'null', 'valakas_clan', 'tomb1_clan', 'tomb2_clan', 'tomb3_clan', 'tomb4_clan', 'tomb5_clan']
	clases = {}
	nm = 0
	clanes = {}
	for i in facciones_lista:clanes[i] = i
	clanes["(Ninguno)"] = ""
	for i in npc[0]:clases[(i[2])] = i
	clasa = list(set(clases))
	clasa.sort()
	clans = list(set(clanes))
	clans.sort()
	def Iniciar_Interfaz():#Interfaces del editor
		global ID_GEN
		Label(ventana0,text="Crear NPC:").pack()
		idev = Label(ventana0,text="ID:")
		idev.place(relx = 0.02, rely = 0.1)
		ide = Entry(ventana0)
		ide.place(relx = 0.1500,rely = 0.11)
		ID_GEN = ide.get()
		for i in clases:
			objeto_ultimo = consultar("SELECT * FROM npc ORDER BY id DESC LIMIT 1")
			break
		ide.insert(END, int((objeto_ultimo[0])[0])+1  )
		htmlv = Label(ventana0,text="Plantilla:")
		htmlv.place(relx = 0.02,rely=0.22)
		clasev = ttk.Combobox(ventana0,values=clasa)
		clasev.config(width=40)
		clasev.place(relx = 0.1500,rely = 0.22)
		clasev.set("Seleccionar Skin/Modelo")
		nombrev = Label(ventana0,text="Nombre:")
		nombrev.place(relx=0.02,rely = 0.33)
		nombre = Entry(ventana0)
		nombre.place(relx = 0.1500,rely = 0.33)
		nombre0 = IntVar()
		checknombre = Checkbutton(ventana0,text="Visible en el server",variable = nombre0)
		checknombre.place(relx = 0.5,rely = 0.33)
		titlev = Label(ventana0,text="Titulo:")
		titlev.place(relx=0.02,rely = 0.44)
		title = Entry(ventana0)
		title.place(relx= 0.1500, rely=0.44)
		check0 = IntVar()
		check = Checkbutton(ventana0,text="Visible en el server",variable=check0)
		check.place(relx = 0.5,rely=0.43)
		######################################
		sexov = Label(ventana0,text="Sexo:")
		sexov.place(relx = 0.02,rely=0.55)
		sexo = Menu(ventana0)
		sexoo = ttk.Combobox(ventana0,values=["male","female"])
		sexoo.set("Sexo")
		sexoo.place(relx=0.1500,rely=.55)
		tipov = Label(ventana0,text="Tipo:")
		tipov.place(relx=0.02,rely=0.66)
		tipo = ttk.Combobox(ventana0,values=tipos)
		tipo.place(relx=0.1500,rely=0.66)
		tipo.set("L2Npc")
		clan = ttk.Combobox(ventana0,values=clans)
		clan.place(relx=0.6,rely=0.66)
		clan.set("Facción")
		def on():buscar_general(clasev.get(),clasev,ventana0,npc)
		ll = Button(ventana0,text="Buscar",command=lambda :on())
		ll.place(relx=0.82,rely = 0.22)
		def se(object):
				con = False
				for i in clasa:
					if clasev.get() == i:
						clasev.set(i)
						con=False
						break
					elif clasev.get().lower() in i.lower():
						clasev.set(i)
						con=False
						break
				if con == True:
					showerror(title="Error",message="Ninguna coincidencia :(")
					clasev.set("")
		clasev.bind("<Return>",lambda c:buscar_general(clasev.get(),clasev,ventana0,npc))
		def generar():#Generar y guardar sql correspondiente
			global ID_GEN,NOMBRE_GEN,TIPO_GEN
			idd = ide.get()
			ID_GEN = idd
			htm = (clases[clasev.get()])[1]
			name = nombre.get()
			NOMBRE_GEN = name
			nombr_visible = nombre0.get()
			titulo = title.get()
			titulo_visible = check0.get()
			collision_radius = (clases[clasev.get()])[7]
			collision_height = (clases[clasev.get()])[8]
			level = (clases[clasev.get()])[9]
			sex = sexoo.get()
			typ =  tipo.get()
			TIPO_GEN = typ
			clas = (clases[clasev.get()])[6]
			attackrange = (clases[clasev.get()])[12]
			hp = (clases[clasev.get()])[13]
			mp = (clases[clasev.get()])[14]
			hpreg = (clases[clasev.get()])[15]
			mpreg = (clases[clasev.get()])[16]
			strr = (clases[clasev.get()])[17]
			con = (clases[clasev.get()])[18]
			dex = (clases[clasev.get()])[19]
			intt = (clases[clasev.get()])[20]
			wit = (clases[clasev.get()])[21]
			men = (clases[clasev.get()])[22]
			exp = (clases[clasev.get()])[23]
			sp = (clases[clasev.get()])[24]
			patk = (clases[clasev.get()])[25]
			pdef = (clases[clasev.get()])[26]
			matk = (clases[clasev.get()])[27]
			mdef = (clases[clasev.get()])[28]
			atkspd = (clases[clasev.get()])[29]
			aggro = (clases[clasev.get()])[30]
			matkspd = (clases[clasev.get()])[31]
			rhand =(clases[clasev.get()])[32]#
			lhand = (clases[clasev.get()])[33]
			armor = (clases[clasev.get()])[34]
			walkspd = (clases[clasev.get()])[35]
			runspd = (clases[clasev.get()])[36]
			faction_id = clan.get()
			if faction_id == "(Ninguna)":faction_id = ""
			faction_range = (clases[clasev.get()])[38]
			isUndead = (clases[clasev.get()])[39]
			absorb_level = (clases[clasev.get()])[40]
			ss = (clases[clasev.get()])[41]
			bss = (clases[clasev.get()])[42]
			ss_rate = (clases[clasev.get()])[43]
			sql =[ idd,htm,name,nombr_visible,titulo,titulo_visible,clas,collision_radius,collision_height,level,sex,typ,attackrange,hp,mp,
			hpreg,mpreg,strr,con,dex,intt,wit,men,exp,sp,patk,pdef,matk,mdef,atkspd,aggro,matkspd,rhand,lhand,armor,
			walkspd,runspd,faction_id,faction_range,isUndead,absorb_level,ss,bss,ss_rate]
			stats_dic  = { "id":idd,"idTemplate":htm,"name":name,"ServerSideName":nombr_visible,"title":titulo,"serverSideName":titulo_visible,"class":clas,"collision_radius":collision_radius,"collision_height":collision_height,"level":level,"sex":sex,"type":typ,"attackrange":attackrange,"hp":hp,"mp":mp,
				"hpreg":hpreg,"mpreg":mpreg,"str":strr,"con":con,"dex":dex,"int":intt,"wit":wit,"men":men,"exp":exp,"sp":sp,"patk":patk,"pdef":pdef,"matk":matk,"mdef":mdef,"atkspd":atkspd,"aggro":aggro,"matkspd":matkspd,"rhand":rhand,"lhand":lhand,"armor":armor,
				"walkspd":walkspd,"runspd":runspd,"faction_id":faction_id,"faction_range":faction_range,"isUndead":isUndead,"absorb_level":absorb_level,"ss":ss,"bss":bss,"ss_rate":ss_rate}
			final_sql = []
			for t in sql:final_sql.append("'"+str(t).replace("\"","")+"'")
			return "("+",".join(str(e)for e in final_sql)+")"
		def iniciar(x):
				conf = 0
				errores = []
				abc = "qwertyuiopasdfgghhjkklzxccvbnm"
				for i in abc:
					if i in ide.get():
						errores.append("El ID tiene que contener solo numeros")
						break
				if nombre.get() == "":errores.append("Nombre")
				if sexoo.get() == "Sexo":errores.append("Sexo")
				if ide.get() == "":errores.append("ID")
				if clan.get() == "Facción" or clan.get() == "":errores.append("Clan")
				if clasev.get() == "Seleccionar Skin/Modelo":errores.append("Skin")
				if errores == []:
					SQL_ACTUAL_GENERADO = generar()
					if x == "save":
						archivo = asksaveasfilename(title="Donde guardar el SQL",initialfile=ID_GEN,defaultextension="sql",filetypes=[("SQL de L2J","*.sql")])
						archivos = open(archivo,"w")
						archivos.writelines(SQL_ACTUAL_GENERADO)
						archivos.close()
						showinfo(title="Eureka!",message="El SQL ah sido creado y guardado correctamente.")
					
					if x == "db":
							con = "INSERT INTO npc VALUES"+SQL_ACTUAL_GENERADO
							try:
								consultar(con)
								showinfo("Eureka!","NPC Inyectado correctamente y listo para usar :D")
							except:showerror("ERROR","ERROR AL INYECTAR SQL EN LA BASE DE DATOS\n Revisar configuraciones o datos del NPC")
				else:
					msj = "Falta definir las variables para: \n\n"+"\t\n".join(str(u)for u in errores)
					showerror(title="ATENCIÓN",message=msj)
		menu9 = Menu(ventana0,bg="#F0F0F0")
		menu1 = Menu(menu9,tearoff=0)
		menu2 = Menu(menu9,tearoff=0)
		def iniciar_html():
			ventana0.destroy()
			HTML_editor("existente")
		menu9.add_cascade(label="Archivo",menu=menu1)
		menu9.add_cascade(label="Ayuda",menu=menu2)
		menu1.add_command(label="Generar y Guardar SQL",command=lambda :iniciar("save") )
		menu1.add_command(label="Generar e Inyectar SQL",command=lambda :iniciar("db")     )
		menu1.add_command(label="Crear un HTML",command=lambda:iniciar_html())
		def salir_a_menu():
			conf = askokcancel("Confirmacion","Salir?")
			if conf == True:
				ventana0.destroy()
				Interfaz()
		menu1.add_separator()
		menu1.add_command(label="Salir a menu",command=salir_a_menu)
		menu2.add_command(label="Acerca de..",command=lambda : Acerca_de(ventana0))
		ventana0.config(menu=menu9)
	Iniciar_Interfaz()
	ventana0.mainloop()
def macros(x):
		ventana3 = Toplevel()
		ventana3.title("Menu Macros")
		ventana3.geometry("300x300+350+250")
		ventana3.iconbitmap("icon.ico")
		menualto = Menu(ventana3,tearoff=0)
		menu_op = Menu(menualto,tearoff=0)
		menualto.add_cascade(label="Opciones",menu=menu_op)
		def archivo_macros():
			ar = open("macros.ini","w")
			for i in macros_lista:
				strs = i,macros_lista[i]
				ar.writelines(str(strs)+"\n")
		def crear_macro():
			f = Toplevel()
			f.title("Creacion de Macro")
			f.geometry("228x150+350+250")
			f.resizable(width=FALSE,height=FALSE)
			#Label(f,text="Para crear un macro recuerda que la estructura es\n tabla+referencia+lo que se quiere modificar.\n Quiere decir que el macro tomara la tabla donde esta el valor,encontrara \nlo que quiere cambiar por el valor de referencia y cambiara el valor especificado.").pack()
			v = Label(f,text="Tabla:")
			v.place(relx=0.0,rely=0.0)
			tabla = ttk.Combobox(f,values=tablas_lista,width=20)
			tabla.set("Elegir tabla")
			tabla.place(relx=0.3,rely=0.0)
			v1 = Label(f,text="Referencia:")
			v1.place(relx=0.0,rely=0.15)
			referencia = Entry(f,width=23)
			referencia.place(relx=0.3,rely=0.15)
			v2 = Label(f,text="Valor:")
			v2.place(relx=0.0,rely=0.30)
			valor = Entry(f,width=23)
			valor.place(relx=0.3,rely=0.30)
			n = Label(f,text="Nombre:")
			n.place(relx=0.0,rely=0.45)
			nombre = Entry(f,width=23)
			nombre.place(relx=0.3,rely=0.45)
			def gener():
				st = tabla.get(),referencia.get(),valor.get()
				asd = "El macro sera: "+str(st)+"\n Esta seguro?"
				conf = askokcancel("Confirmación",asd)
				if conf == True:
					macros_lista[nombre.get()] = [tabla.get(),referencia.get(),valor.get()]
					f.destroy()
					showinfo("Eureka!","Macro creado y agregado a la lista")
					actualiza()
					archivo_macros()
			g = Button(f,text="Guardar",command=gener,width=31)
			g.place(relx=0.0,rely=0.60)
			f.transient(ventana3)
			f.grab_set()
			ventana3.wait_window(f)
		menu_op.add_command(label="Crear un macro",command=crear_macro)
		Label(ventana3,text="Lista de accesos directos para\n una rapida configuracion del servidor.").pack()
		sc = Scrollbar(ventana3,orient=VERTICAL)
		lista = Listbox(ventana3,width=50,height=30,yscrollcommand=sc.set)
		sc.config(command=lista.yview)
		sc.pack(side=RIGHT,fill=Y)
		def eliminar(x):
				conf = askyesno("Confirmación","Deseas eliminar este macro?")
				if conf == True:
					del macros_lista[x]
					actualiza()
					archivo_macros()
		def ejecutar_macro(x):
			try:
				m = Toplevel()
				m.transient(ventana3)
				m.geometry("228x150+350+250")
				m.iconbitmap("icon.ico")
				m.resizable(width=FALSE,height=FALSE)
				Label(m,text="Modificar valores:").pack()
				scrolll = Scrollbar(m,orient=VERTICAL)
				ca = Listbox(m,width=32,yscrollcommand=scrolll.set)
				scrolll.config(command=ca.yview)
				scrolll.pack(side=RIGHT,fill=Y)
				ca.pack()
				sen = macros_lista[x]
				def actualizar0():
					lis =  conseguir(sen[0],sen[1])
					ca.delete(0,END)
					try:
						for i in lis:ca.insert(END,i)
					except:m.destroy()
				actualizar0()
				m.grab_set()
				def cmd(x1):
					g = Toplevel()
					g.title("Editar valor")
					g.iconbitmap("icon.ico")
					g.geometry("300x80+350+250")
					testo = IntVar()
					st = "Modificacion de variable '%s' en '%s'" %(sen[2],x1[0])
					testo.set(st)
					k = Label(g,textvar=testo)
					k.pack()
					valor = Entry(g,width=30)
					valor.pack()
					def guardar():
						try:
							try:
								actualizar(sen[0],sen[1]+"="+"'"+x1[0]+"'",sen[2]+"="+valor.get())
								g.destroy()
								actualizar0()
							except:
								actualizar(sen[0],sen[1]+"="+"'"+x1[0]+"'",sen[2]+"="+"'"+valor.get()+"'")
								g.destroy()
								actualizar0()
						except:showerror("Error","Algo ocurrio y no se pudo modificar nada.\nRevisa que el valor tenga que ser numeral o de caracteres.")
					Button(g,text="Guardar Cambio",command=guardar).pack()
					g.transient(m)
					g.grab_set()
					m.wait_window(g)
				ca.bind("<Double-1>",lambda c:cmd(ca.get(ca.curselection()[0])))
				ventana3.wait_window(m)
			except:pass
		def actualiza():
			lista.delete(0,END)
			for i in macros_lista:lista.insert(END,i)
		def edit(x,y):
			v = Toplevel()
			v.title("Editar")
			v.geometry("228x150+350+250")
			v.iconbitmap("icon.ico")
			actual  = macros_lista[x]
			v1 = Label(v,text="Tabla:")
			v1.place(relx=0.0,rely=0.0)
			tabla = ttk.Combobox(v,values=tablas_lista,width=20)
			tabla.set((actual[0]))
			tabla.place(relx=0.3,rely=0.0)
			v1 = Label(v,text="Referencia:")
			v1.place(relx=0.0,rely=0.15)
			referencia = Entry(v,width=23)
			referencia.place(relx=0.3,rely=0.15)
			referencia.insert(END,(actual[1]))
			v2 = Label(v,text="Valor:")
			v2.place(relx=0.0,rely=0.30)
			valor = Entry(v,width=23)
			valor.place(relx=0.3,rely=0.30)
			valor.insert(END,(actual[2]))
			def gc():
				macros_lista[x] = [tabla.get(),referencia.get(),valor.get()]
				actualiza()
				archivo_macros()
				showinfo("Aviso","Se guardaron correctamente todos los cambios :)")
			g = Button(v,text="Guardar Cambio",command=lambda :gc())
			g.place(relx=0.0,rely=0.60)
			v.transient(ventana3)
			v.grab_set()
			ventana3.wait_window(v)
		minu = Menu(ventana3,tearoff=0)
		menu_op.add_command(label="Editar macro",command=lambda :edit(lista.get(lista.curselection()[0]),ventana3))
		minu.add_command(label="Editar",command=lambda :edit(lista.get(lista.curselection()[0]),ventana3))
		minu.add_command(label="Eliminar",command=lambda :eliminar(lista.get(lista.curselection()[0])))
		def menu_pop(event):
				try:minu.tk_popup(event.x_root,event.y_root)
				except:pass
		lista.bind("<Button-3>",menu_pop)
		actualiza()
		lista.bind("<Delete>",lambda c:eliminar(lista.get(lista.curselection()[0])))
		try:lista.bind("<Double-1>",lambda c: ejecutar_macro(lista.get(lista.curselection()[0])))
		except:pass
		lista.pack()
		ventana3.config(menu=menualto)
		ventana3.transient(x)
		ventana3.grab_set()
		x.wait_window(x)
def Interfaz():
	global HOST,USUARIO,PASS,NOMBREDB,DIRECTORIO_SERVER,DIRECTORIO_L2
	archivo_configuracion = {
	"Host":'localhost',
	"Usuario":'root',
	"Pass":'',
	"Base de datos":'l2jdb',
	"Directorio Server":'',
	"Directorio L2":''}
	def crear_archivo():
		config = open("configuracion.ini","w")
		for i in archivo_configuracion:config.writelines((i+"="+archivo_configuracion[i]+"\n"))
	configuraciones_encontradas = {}
	try:
		conf = open("configuracion.ini","r")
		for i in conf:
			o = i.replace("\n","").split("=")
			configuraciones_encontradas[o[0]] = o[1]
		HOST = configuraciones_encontradas["Host"]
		USUARIO = configuraciones_encontradas["Usuario"]
		PASS = configuraciones_encontradas["Pass"]
		NOMBREDB = configuraciones_encontradas["Base de datos"]
		DIRECTORIO_SERVER = configuraciones_encontradas["Directorio Server"]
		DIRECTORIO_L2 =configuraciones_encontradas["Directorio L2"]
	except:crear_archivo()
	ventana54 = Tk()
	ventana54.title("L2J TEU Alpha ")
	ventana54.geometry("384x320+350+240")
	ventana54.resizable(width=FALSE,height=FALSE)
	ventana54.iconbitmap("icon.ico")
	men_superior = Menu(ventana54)
	menu_herramientas = Menu(men_superior,tearoff=0)
	menu_op = Menu(men_superior,tearoff=0)
	menus = Menu(men_superior,tearoff=0)
	men_superior.add_cascade(label="Archivo",menu=menus)
	men_superior.add_cascade(label="Herramientas",menu=menu_herramientas)
	men_superior.add_cascade(label="Opciones",menu=menu_op)
	l = Label(ventana54,text="Control de servidor:")
	menus.add_separator()
	#Estructura macro, Identificador, que se va a modificar,referencia
	def cargar_macros():
		try:ap = open("macros.ini","r")
		except:
			 open("macros.ini","w")
			 ap = open("macros.ini","r")
		for i in ap:
			al = i.split(",")
			temp = []
			for m in al:temp.append(m.replace(")","").replace("\n","").replace("(","").replace("[","").replace("]","").replace("'",""))
			macros_lista[temp[0]] = temp[1:]
	cargar_macros()
	l1 = Label(ventana54,text="Tweaks:")
	l1.place(relx=0.8,rely=0.05)
	def salir():
		c = askokcancel("Salir?","Seguro que desea salir del programa?")
		if c == True:
			os.system("TASKKILL /F /IM \"TEU L2J.exe\"")
			ventana54.destroy()
	menus.add_command(label="Salir",command=lambda :salir())
	l.place(relx=0.0,rely=0.05)
	def iniciar_server():
		adh = intentar_conexion()
		if adh == True:
				comando = "cd /D \""+DIRECTORIO_SERVER+"\gameserver\" & start startGameServer.bat"
				com  = os.system(comando)
	def iniciar_login():
		adh = intentar_conexion()
		if adh == True:
				comando = "cd /D \""+DIRECTORIO_SERVER+"\login\" & start startLoginServer.bat"
				os.system(comando)
	def matar():os.system("TASKKILL /F /IM java.exe & TASKKILL /F /IM cmd.exe")
	iniciar = Button(ventana54,text="Iniciar Game Server",command=iniciar_server)
	iniciar.place(relx=0.0,rely=0.22)
	login = Button(ventana54,text="Iniciar Login Server",command=iniciar_login)
	login.place(relx=0.0,rely=0.12)
	d = Button(ventana54,text="Detener Todo",command=matar,bg="#FF7E7E")
	d.place(relx=0.03,rely=0.32)
	def intentar_conexion():
		datos = [HOST, USUARIO, PASS, NOMBREDB] 
		try:
			conn = MySQLdb.connect(*datos)
			conn.close()
			return True
		except:
			showerror("Error","Error de conexión a la base de datos,verifique que el host se encuentra activa o haya configurado correctamente los parametros \nde conexion en el menu de Configuraciòn")
			return False
	def iniciar_npc():
		
		cn = intentar_conexion()
		if cn == True:
			ventana54.title("-------CARGANDO-------")
			procesar_sql_normal()
			ventana54.destroy()
			NPC_Creator()
	def iniciar_html():
		cn = intentar_conexion()
		if cn == True:HTML_editor("existente",ventana54)
	def iniciar_xml():
		cn = intentar_conexion()
		if cn == True:
			ventana54.title("-------CARGANDO-------")
			procesar_sql("armor",armaduras)
			procesar_sql("weapon",armas)
			procesar_sql("etcitem",items)
			ventana54.destroy()
			XML_EDITOR()
	def iniciar_macros():
		adh = intentar_conexion()
		if adh == True:macros()
	def iniciar_aio():
		adh = intentar_conexion()
		if adh == True:AIO_Creador(ventana54)
	menu_herramientas.add_cascade(label="Creador de NPC",command=iniciar_npc)
	menu_herramientas.add_cascade(label="Editor de Html",command=iniciar_html)
	menu_herramientas.add_cascade(label="Editor de Shops (Multisell)",command=iniciar_xml)
	menu_herramientas.add_cascade(label="Dar Skilles",command=iniciar_aio)
	vert = Button(ventana54,text="DB  Macros",command=lambda : macros(ventana54))
	vert.place(relx=0.8,rely=0.12)
	def iniciar_l2():
			comando = "cd /D \""+DIRECTORIO_L2+"\" & start l2.exe"
			os.system(comando)
	ver = Button(ventana54,text=" Iniciar  L2  ",command=lambda: iniciar_l2())
	ver.place(relx=0.8,rely=0.22)
	def configuracion():
		vent = Toplevel()
		vent.title("Menu Configuraciones")
		vent.iconbitmap("icon.ico")
		vent.geometry("300x300+350+250")
		Label(vent,text="Menu de parametros para iniciar conexion y\n fijar directorio de gameserver").pack()
		re = Label(vent,text="Hostname:")
		re.place(relx=0.0,rely=0.2)
		host = Entry(vent,width=30)
		host.place(relx=0.25,rely=0.2)
		host.insert(END,HOST)
		re = Label(vent,text="Usuario:")
		re.place(relx=0.0,rely=0.3)
		user = Entry(vent,width=30)
		user.place(relx=0.25,rely=0.3)
		user.insert(END,USUARIO)
		re = Label(vent,text="Contraseña:")
		re.place(relx=0.0,rely=0.4)
		pas = Entry(vent,width=30)
		pas.place(relx=0.25,rely=0.4)
		pas.insert(END,PASS)
		re = Label(vent,text="Nombre DB:")
		re.place(relx=0.0,rely=0.5)
		db = Entry(vent,width=30)
		db.place(relx=0.25,rely=0.5)
		db.insert(END,NOMBREDB)
		re = Label(vent,text="Directorio:")
		re.place(relx=0.0,rely=0.6)
		di = Entry(vent,width=30)
		di.place(relx=0.25,rely=0.6)
		di.insert(END,DIRECTORIO_SERVER)
		rere = Label(vent,text="Dir. L2:")
		rere.place(relx=0.0,rely=0.7)
		ri = Entry(vent,width=30)
		ri.insert(END,DIRECTORIO_L2)
		ri.place(relx=0.25,rely=0.7)
		def guardar_cambios():
			global HOST,USUARIO,PASS,NOMBREDB,DIRECTORIO_SERVER,DIRECTORIO_L2
			HOST = host.get()
			USUARIO = user.get()
			PASS = pas.get()
			NOMBREDB = db.get()
			DIRECTORIO_SERVER = di.get()
			DIRECTORIO_L2 = ri.get()
			archivo_configuracion = {
			"Host":HOST,
			"Usuario":USUARIO,
			"Pass":PASS,
			"Base de datos":NOMBREDB,
			"Directorio Server":DIRECTORIO_SERVER,
			"Directorio L2":DIRECTORIO_L2
			}
			conf = open("configuracion.ini","w")
			for i in archivo_configuracion:
				o = i+"="+archivo_configuracion[i]+"\n"
				conf.writelines(o)
			vent.destroy()
		boton = Button(vent,text="Guardar Cambios",width=35,command=guardar_cambios)
		boton.place(relx=0.07,rely=0.9)
		vent.transient(ventana54)
		vent.grab_set()
		ventana54.wait_window(vent)
	menu_op.add_command(label="Configuracion",command=configuracion)
	menu_op.add_separator()
	menu_op.add_command(label="Acerca de..",command=lambda : Acerca_de(ventana54))
	im = PhotoImage(file="logo.gif")
	lab  = Label(ventana54,image=im)
	lab.place(relx=-0.004,rely=0.45)
	ventana54.config(menu=men_superior)
	ventana54.mainloop()
Interfaz()
