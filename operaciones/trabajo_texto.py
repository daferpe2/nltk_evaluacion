from tkinter import *
from tkinter import ttk,Tk
from tkinter import scrolledtext as st
import sqlite3
import datetime
from tkinter import filedialog
from tkinter import messagebox
from operaciones.proceso_texto import ProcesoTexto
from operaciones.prosp import Consultas_Base
import pandas as pd
import numpy as np
from three_viwe_prosp import Arbol_prosp
from operaciones.conexion import Conexion
import plotly.express as px



def proceso_texto():
    
    def abrirdoc():
        root.filename = filedialog.askopenfilename(initialdir='./',title='Selecciona Documento',
                                                   filetypes=(("txt files", "*.txt"),("all files","*.*")))
        
        texto = root.filename

        with open(texto,'r',encoding='utf-8') as f:
            doc=f.read()
            texto_encontrado.delete("1.0",END)
            texto_encontrado.insert(END,doc)
            f.close()
            
    def limpiar_campos():
        pkentry.delete(0,END)
        titulo_documento.delete(0,END)
        fecha.delete(0,END)
        tema.delete(0,END)
        variable.delete(0,END)
        variable_1.delete(0,END)
        anotacion.delete('1.0',END) 
        influencia.delete(0,END)
        dependencia.delete(0,END)
        #texto_encontrado.delete('1.0',END)
        
        tiempo = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fecha.insert(0,tiempo)

    def update():
        try:
            conn = sqlite3.connect('reporte_diario.db')
            #crear la conexion
            c = conn.cursor()
            c.execute("SELECT * FROM proceso_texto GROUP BY varible ORDER BY varible DESC LIMIT 20")
            records = c.fetchall()
        
            p_record=[]
            for i in records:
                p_record.append(i[4])
            conn.commit
            conn.close()
            return p_record
        except:
            messagebox.showwarning('Base de Datos','No existe la tabla')

    def update2():
        try:
            conn = sqlite3.connect('reporte_diario.db')
            #crear la conexion
            c = conn.cursor()
            c.execute("SELECT * FROM proceso_texto GROUP BY variable_rel ORDER BY variable_rel DESC LIMIT 20")
            records = c.fetchall()
        
            p_record=[]
            for i in records:
                p_record.append(i[5])
            conn.commit
            conn.close()
            return p_record
        except:
            messagebox.showwarning('Base de Datos','No existe la tabla')        


    def titulo():
        try:
            conn = sqlite3.connect('reporte_diario.db')
            #crear la conexion
            c = conn.cursor()
            c.execute("SELECT numero_document,anotacion FROM reporte ORDER BY pk DESC LIMIT 1")
            records = c.fetchall()
            conn.close
            lista_documento = [i for i in records]
            return lista_documento[0]
            
        except:
            messagebox.showwarning('Base de Datos','No existe la tabla')
            
    def update3():
        
        conn = sqlite3.connect('reporte_diario.db')
        #crear la conexion
        seleccion = titulo_documento.get()
        c = conn.cursor()
        c.execute("SELECT * FROM reporte WHERE numero_document =" + "'" + seleccion + "'")
        records = c.fetchall()
        #texto_encontrado.delete("1.0",END)
        #records_lista = [i for i in records]
        #texto_encontrado.insert(END,f"{records_lista[0][1:7]}")
           
        for item,valor in enumerate(records):
            count=0
            #item +=2
            for y in valor:
                texto_encontrado.insert(END,"\n"+ str(y) + "\n")
                count +=1
            
        conn.commit()
        conn.close()
   
    def submit():
        if titulo_documento.get() != '':
            conn = sqlite3.connect('reporte_diario.db')
            #crear la conexion
            c = conn.cursor()
            datos = (titulo_documento.get().capitalize(),fecha.get(),tema.get(),variable.get(), variable_1.get(), anotacion.get('1.0',END),influencia.get(),dependencia.get())
                    
            c.execute("INSERT INTO proceso_texto VALUES(NULL,?,?,?,?,?,?,?,?)",(datos))
                    
            conn.commit()
            conn.close()
                    
            limpiar = limpiar_campos() 
                    
            messagebox.showinfo('Ingreso Información','Se ingreso la información exitosamente')
        
        else:
            messagebox.showerror('Información','Diligencie todos los espacios')
       
    def proceso_texto():
        texto = texto_encontrado.get('1.0',END)
        proceso = ProcesoTexto.lista_documentos(texto)
        conteo_texto = ProcesoTexto.estadistica_lenguaje(proceso)
        texto_procesado.delete("1.0",END)
        for item,valor in conteo_texto.items():
            texto_procesado.insert(END,f"{item} | {valor} \n")

        
        messagebox.showinfo('Información','CSV creado correctamente')

    def ngramas_apli():
        texto = texto_encontrado.get('1.0',END)
        resultado = ProcesoTexto.ngramas(texto)
        return resultado

    def ngramas_apli2():
        texto = texto_encontrado.get('1.0',END)
        resultado = ProcesoTexto.ngramas2_2(texto)
        return resultado

    def colocaciones():
        texto = texto_encontrado.get('1.0',END)
        resultado = ProcesoTexto.colocaciones(texto)
        resultado2 = ProcesoTexto.coloc2(texto)
        texto_procesado.delete("1.0",END)
        texto_procesado.insert("1.0",resultado2)
        return resultado
    
    def sentimientos():
        texto = texto_encontrado.get('1.0',END)
        sent = ProcesoTexto.sentimientos_v(texto)
        return sent


    def nube_l():
        texto = texto_encontrado.get('1.0',END)
        sent = ProcesoTexto.nube(texto)
        return sent   


    def porspec():
        tit = titulo_documento.get()
        
        conn = Conexion.conexion2()
        c = conn.cursor()
        df = pd.read_sql_query(f"SELECT titulo_documento,fecha,tema,varible,variable_rel,anotacion,sum(influencia) as con_influencia,sum(dependencia) as con_dependencia FROM proceso_texto WHERE titulo_documento='{tit}' GROUP BY varible ORDER BY con_influencia DESC",conn)
        #df = pd.read_sql_query(f"SELECT * FROM proceso_texto WHERE titulo_documento = '{text_buscado}' GROUP BY varible ORDER BY pk",conn)

        df["cuadrado_influencia"]=np.sqrt((df["con_influencia"]))
        df["cuadrado_dependencia"]=np.sqrt((df["con_dependencia"]))
        
        conn.close()
        
        df.to_excel("matriz_influencia_dependencia.xlsx",index=False)
        
        fig = px.scatter(x = df['cuadrado_dependencia'].values, y = df['cuadrado_influencia'].values, color = df['cuadrado_influencia'], 
                        size = (df['cuadrado_dependencia']+df['cuadrado_dependencia']).values, 
                        hover_name = df['varible'].values, width = 600, height = 600, labels = {'x': 'cuadrado_dependencia', 'y': 'cuadrado_influencia'})
            
        return fig.show()

    def top():
        def clear_tree():
            my_tree.delete(*my_tree.get_children())

        def open_file():
            clear_tree()
            root.filename = filedialog.askopenfilename(initialdir='./',title='Selecciona Documento',
                                                    filetypes=(("xlsx files", "*.xlsx"),("all files","*.*")))
            
            texto = root.filename

            if texto:
                try:
                    texto = r"{}".format(texto)
                    df = pd.read_excel(texto)
                except ValueError as e:
                    my_label.config(text='No se pudo abrir el archivo')
                except FileNotFoundError:
                    my_label.config(text='No se pudo abrir el archivo')

            
            my_tree['column']= list(df.columns)
            my_tree['show'] = "headings"
            for column in my_tree['column']:
                my_tree.heading(column,text=column)
            
            #convertir data frame en una lista de python
            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                my_tree.insert("","end",values=row)
                
            my_tree.pack()
        
        
            return df_rows
       
        def guardar_base_datos():
            my_data = open_file()
            try:
                conn=Conexion.conexion2()
                c = conn.cursor()

                for i in my_data:
                    titulo_documento = i[0]
                    fecha = i[1]
                    tema = i[2]
                    variable=i[3]
                    variable_rel=i[4]
                    anotacion=i[5]
                    influencia=i[6]
                    dependencia = i[7]
                    query = "INSERT INTO proceso_texto VALUES(NULL,?,?,?,?,?,?,?,?)"
                    c.execute(query,(titulo_documento,fecha,tema,variable,variable_rel,anotacion,influencia,dependencia))     

                conn.commit()
                conn.close()
                
            
                messagebox.showinfo("Información",'Se guardo la información con exito')
                
                clear_tree()

            except ValueError as e:
                print(e)       
 
        root_top_label = Toplevel()
        root_top_label.title("Ingreso Información")
        root_top_label.geometry("700x600")
        label_ds = LabelFrame(root_top_label,text='Hoja de Calculo')
        label_ds.pack()
        my_tree = ttk.Treeview(label_ds)
        
        my_label = Label(label_ds,text='')
        my_label.pack(pady=10)
        
        boton_abrir= Button(my_label,text="Abrir Excel",command=open_file)
        boton_abrir.pack(side=LEFT, padx=3,pady=3)
        boton_ingresar= Button(my_label,text="Guardar Información",command=guardar_base_datos)
        boton_ingresar.pack(side=RIGHT, padx=3,pady=3)

  
    root=Tk()
    root.title('Texto')
    root.geometry("900x600")
    root.resizable(width=True,height=True)
    
    barramenu=Menu(root)
    root.config(menu=barramenu,width=400,height=400)
    bdmenu=Menu(barramenu,tearoff=0)
    bdmenu.add_command(label="ngramas",command=ngramas_apli)
    bdmenu.add_command(label="ngramas2",command=ngramas_apli2)
    bdmenu.add_command(label="colocaciones",command=colocaciones)
    bdmenu.add_command(label="matriz ic",command=porspec)
    bdmenu.add_command(label="sentimientos", command=sentimientos)
    bdmenu.add_command(label="nube palabras",command=nube_l)

    barramenu.add_cascade(label="Proceso de texto especializado",menu=bdmenu)    
    
    frame=LabelFrame(root, text='Proceso texto')
    frame.grid(column=0,row=0)
    
    pkentry = Entry(frame,width=25)
    pkentry.grid(row=0,column=1)
    pkentrylabel=Label(frame,text='Pk: ')
    pkentrylabel.grid(row=0, column=0,sticky='w')
    
    lista_titulo = titulo()
    titulo_documento = ttk.Combobox(frame,width=21,values=lista_titulo)
    titulo_documento.grid(row=1,column=1)
    titulo_documentoentry=Label(frame,text='Título: ')
    titulo_documentoentry.grid(row=1, column=0,sticky='w')
    
    tiempo = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fecha = Entry(frame,width=25)
    fecha.grid(row=2,column=1)
    fecha.insert(0,tiempo)
    fechalabel=Label(frame,text='Fecha: ')
    fechalabel.grid(row=2, column=0,sticky='w')
    
    lista_temas=['Sin Tema','Propósitos','Medios','Método','Riesgos','Estrategia Adversario', 'Entorno']
    tema = ttk.Combobox(frame,width=21,values=lista_temas)
    tema.grid(row=3,column=1,padx=5,pady=5)
    tema.insert(0,lista_temas[0])
    temalabel=Label(frame,text='Tema: ', padx=5,pady=5)
    temalabel.grid(row=3, column=0,sticky='w')

    lista_variables = update()
    variable = ttk.Combobox(frame,width=21,values=lista_variables)
    variable.grid(row=4,column=1)
    variable.insert(0,'Ingrese Variable')
    variablelabel=Label(frame,text='Variable: ')
    variablelabel.grid(row=4, column=0,sticky='w')
    
    lista_variables2 = update2()
    variable_1 = ttk.Combobox(frame,width=21,values=lista_variables2)
    variable_1.grid(row=5,column=1)
    variable_1.insert(0,'Ingrese Variable')
    variable_1label=Label(frame,text='Variable_1: ')
    variable_1label.grid(row=5, column=0,sticky='w')
    
    
    influencia = ttk.Spinbox(frame, from_=0, to=3, increment=1,width=23)
    influencia.grid(row=6,column=1,padx=5,pady=5)
    influencia.insert(0,0)
    influencia_label = Label(frame, text='Influencia: ',padx=5,pady=5)
    influencia_label.grid(row=6,column=0, sticky='w')
    
    dependencia = ttk.Spinbox(frame, from_=0, to=3, increment=1,width=23)
    dependencia.grid(row=7,column=1,padx=5,pady=5)
    dependencia.insert(0,0)
    dependencia_label = Label(frame, text='Dependecia: ',padx=5,pady=5)
    dependencia_label.grid(row=7,column=0, sticky='w')    

    anotacion_label = Label(frame, text='Anotación: ',padx=5,pady=5)
    anotacion_label.grid(row=8,column=0, sticky='w')     
    anotacion = Text(frame,width=25, height=10)
    anotacion.grid(row=8,column=1,padx=5,pady=5)
    anotacion.insert(END,'Ingrese Información')
    anotacion_scroll_texto=ttk.Scrollbar(frame,command=anotacion.yview)
    anotacion_scroll_texto.grid(row=9,column=2,sticky='nsew')
    anotacion.config(yscrollcommand=anotacion_scroll_texto.set)
  
    
    frame_botones = LabelFrame(root,text='Botones')
    frame_botones.grid(column=0,row=2)
    boton_buscar=Button(frame_botones,text='Abrir Documento',command=abrirdoc,width=15)
    boton_buscar.grid(row=0,column=0, padx=5,pady=5,sticky="w")
    boton_limpiar=Button(frame_botones,text='Limpiar Documento',command=limpiar_campos,width=15)
    boton_limpiar.grid(row=0,column=1, padx=5,pady=5,sticky="w")
    boton_guardar=Button(frame_botones,text='Guardar Información',command=submit,width=15)
    boton_guardar.grid(row=1,column=0, padx=5,pady=5,sticky="w")
    boton_ins_bbdd = Button(frame_botones,text="Base Datos", command=update3,width=15)
    boton_ins_bbdd.grid(row=1,column=1,padx=5,pady=5,sticky="w")
    boton_proceso_texto=Button(frame_botones,text='Proceso Texto',command=proceso_texto,width=15)
    boton_proceso_texto.grid(row=1,column=3, padx=5,pady=5,sticky="w")
    boton_proceso_texto2=Button(frame_botones,text='Ingresar Excel',command=top,width=15)
    boton_proceso_texto2.grid(row=0,column=3, padx=5,pady=5,sticky="w")   

    #boton_guardar_archivo=Button(frame,text='Guardar Archivo')
    #boton_guardar_archivo.grid(row=1,column=2, padx=5,pady=5)
    
    frame_texto=LabelFrame(root,text='Texto')
    frame_texto.grid(column=1,row=0)
    
    texto_encontrado = Text(frame_texto, width=30,height=25)
    texto_encontrado.grid(row=0,column=1,padx=5,pady=5)
    text_scroll_texto=ttk.Scrollbar(frame_texto,command=texto_encontrado.yview)
    text_scroll_texto.grid(row=0,column=2,sticky='nsew')
    #texto_label=Label(frame_texto,text='Texto Encontrado')
    #texto_label.grid(row=0,column=0,padx=5,pady=5)
    texto_encontrado.config(yscrollcommand=text_scroll_texto.set)
    
    frame_proceso_texto = LabelFrame(root,text="Proceso texto")
    frame_proceso_texto.grid(column=2,row=0)
    
    texto_procesado = Text(frame_proceso_texto, width=30,height=25)
    texto_procesado.grid(row=0,column=1,padx=5,pady=5)
    texto_procesado_scroll = ttk.Scrollbar(frame_proceso_texto, command=texto_procesado.yview)
    texto_procesado_scroll.grid(row=0,column=2,sticky='nsew')
    texto_procesado.config(yscrollcommand=texto_procesado_scroll.set)
    

    
    root.mainloop()
    

if __name__=='__main__':
    proceso_texto()
    
