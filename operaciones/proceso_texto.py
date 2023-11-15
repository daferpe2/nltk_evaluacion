from tkinter import *
from tkinter import ttk,Tk
from tkinter import scrolledtext as st
import sqlite3
import datetime
from tkinter import filedialog
from tkinter import messagebox
from .op_texto import ProcesoTexto


class Aplicacion_texto:
    def __init__(self) -> None:
        self.formulario()


    def formulario(self):
        self.root=Tk()
        self.root.title('Texto')
        self.root.geometry("930x550")
        self.root.resizable(width=True,height=True)

        self.barramenu=Menu(self.root)
        self.root.config(menu=self.barramenu,width=400,height=400)
        self.bdmenu=Menu(self.barramenu,tearoff=0)
        self.bdmenu.add_command(label="Abrir Carpeta",command=self.abrir_carpeta)
        self.bdmenu.add_command(label="ngramas",command=self.ngramas)
        self.bdmenu.add_command(label="ngramas2",command=self.ngramas_apli2)
        self.bdmenu.add_command(label="colocaciones",command=self.colocaciones)
        # bdmenu.add_command(label="matriz ic",command=porspec)
        self.bdmenu.add_command(label="sentimientos", command=self.sentimientos)
        self.bdmenu.add_command(label="nube palabras",command=self.nube_l)

        self.barramenu.add_cascade(label="Proceso de texto especializado",menu=self.bdmenu)    

        self.frame=LabelFrame(self.root, text='Proceso texto')
        self.frame.grid(column=0,row=0)

        self.pkentry = Entry(self.frame,width=25)
        self.pkentry.grid(row=0,column=1)
        self.pkentrylabel=Label(self.frame,text='Pk: ')
        self.pkentrylabel.grid(row=0, column=0,sticky='w')

        self.lista_titulo = ["pendiente modificar"]
        self.titulo_documento = ttk.Combobox(self.frame,width=21,values=self.lista_titulo)
        self.titulo_documento.grid(row=1,column=1)
        self.titulo_documentoentry=Label(self.frame,text='Título: ')
        self.titulo_documentoentry.grid(row=1, column=0,sticky='w')

        self.tiempo = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.fecha = Entry(self.frame,width=25)
        self.fecha.grid(row=2,column=1)
        self.fecha.insert(0,self.tiempo)
        self.fechalabel=Label(self.frame,text='Fecha: ')
        self.fechalabel.grid(row=2, column=0,sticky='w')

        self.lista_temas=['Sin Tema','Propósitos','Medios','Método','Riesgos','Estrategia Adversario', 'Entorno']
        self.label_tema = Label(self.frame,text="Tema")
        self.label_tema.grid(row=3,column=0,sticky="w")
        self.tema = ttk.Combobox(self.frame,width=21,values=self.lista_temas)
        self.tema.insert(0,self.lista_temas[0])
        self.tema.grid(row=3, column=1)

        self.lista_variables = ["pendiente cambiar"]
        self.temalabel=Label(self.frame,text='Tema: ')
        self.variable = ttk.Combobox(self.frame,width=21,values=self.lista_variables)
        self.variable.grid(row=4,column=1)
        self.variable.insert(0,'Ingrese Variable')
        self.variablelabel=Label(self.frame,text='Variable: ')
        self.variablelabel.grid(row=4, column=0,sticky='w')

        self.lista_variables2 = ["pendiente modificar"]
        self.variable_1 = ttk.Combobox(self.frame,width=21,values=self.lista_variables2)
        self.variable_1.grid(row=5,column=1)
        self.variable_1.insert(0,'Ingrese Variable')
        self.variable_1label=Label(self.frame,text='Variable_1: ')
        self.variable_1label.grid(row=5, column=0,sticky='w')


        self.influencia = ttk.Spinbox(self.frame, from_=0, to=3, increment=1,width=23)
        self.influencia.grid(row=6,column=1)
        self.influencia.insert(0,0)
        self.influencia_label = Label(self.frame, text='Influencia: ')
        self.influencia_label.grid(row=6,column=0, sticky='w')
        
        self.dependencia = ttk.Spinbox(self.frame, from_=0, to=3, increment=1,width=23)
        self.dependencia.grid(row=7,column=1)
        self.dependencia.insert(0,0)
        self.dependencia_label = Label(self.frame, text='Dependecia: ')
        self.dependencia_label.grid(row=7,column=0, sticky='w')    

        self.anotacion_label = Label(self.frame, text='Anotación: ',padx=5,pady=5)
        self.anotacion_label.grid(row=8,column=0, sticky='w')     
        self.anotacion = Text(self.frame,width=25, height=10)
        self.anotacion.grid(row=8,column=1,padx=5,pady=5)
        self.anotacion.insert(END,'Ingrese Información')
        self.anotacion_scroll_texto=ttk.Scrollbar(self.frame,command=self.anotacion.yview)
        self.anotacion_scroll_texto.grid(row=9,column=2,sticky='nsew')
        self.anotacion.config(yscrollcommand=self.anotacion_scroll_texto.set)

        self.frame_botones = LabelFrame(self.root,text='Botones')
        self.frame_botones.grid(column=0,row=2)
        self.boton_buscar=Button(self.frame_botones,text='Abrir Documento',width=15)
        self.boton_buscar.grid(row=0,column=0, padx=5,pady=5,sticky="w")
        self.boton_limpiar=Button(self.frame_botones,text='Limpiar Documento',width=15)
        self.boton_limpiar.grid(row=0,column=1, padx=5,pady=5,sticky="w")
        self.boton_guardar=Button(self.frame_botones,text='Guardar Información',width=15)
        self.boton_guardar.grid(row=1,column=0, padx=5,pady=5,sticky="w")
        self.boton_ins_bbdd = Button(self.frame_botones,text="Base Datos",width=15)
        self.boton_ins_bbdd.grid(row=1,column=1,padx=5,pady=5,sticky="w")
        self.boton_proceso_texto=Button(self.frame_botones,text='Proceso Texto',width=15)
        self.boton_proceso_texto.grid(row=1,column=3, padx=5,pady=5,sticky="w")
        self.boton_proceso_texto2=Button(self.frame_botones,text='Ingresar Excel',width=15)
        self.boton_proceso_texto2.grid(row=0,column=3, padx=5,pady=5,sticky="w")   

        #boton_guardar_archivo=Button(frame,text='Guardar Archivo')
        #boton_guardar_archivo.grid(row=1,column=2, padx=5,pady=5)

        self.frame_texto=LabelFrame(self.root,text='Texto')
        self.frame_texto.grid(column=1,row=0)

        self.texto_encontrado = Text(self.frame_texto, width=30,height=25)
        self.texto_encontrado.grid(row=0,column=1,padx=5,pady=5)
        self.text_scroll_texto=ttk.Scrollbar(self.frame_texto,command=self.texto_encontrado.yview)
        self.text_scroll_texto.grid(row=0,column=2,sticky='nsew')
        #texto_label=Label(frame_texto,text='Texto Encontrado')
        #texto_label.grid(row=0,column=0,padx=5,pady=5)
        self.texto_encontrado.config(yscrollcommand=self.text_scroll_texto.set)

        self.frame_proceso_texto = LabelFrame(self.root,text="Proceso texto")
        self.frame_proceso_texto.grid(column=2,row=0)

        self.texto_procesado = Text(self.frame_proceso_texto, width=30,height=25)
        self.texto_procesado.grid(row=0,column=1,padx=5,pady=5)
        self.texto_procesado_scroll = ttk.Scrollbar(self.frame_proceso_texto, command=self.texto_procesado.yview)
        self.texto_procesado_scroll.grid(row=0,column=2,sticky='nsew')
        self.texto_procesado.config(yscrollcommand=self.texto_procesado_scroll.set)


    def abrir_carpeta(self):
        self.filenames = filedialog.askdirectory()
        texto = ProcesoTexto.abrir_muchos_archivos(ProcesoTexto,self.filenames)
        print(len(texto))
        self.texto_encontrado.insert("1.0",texto[::])


    def ngramas(self):
        texto = self.texto_encontrado.get("1.0",END)
        return ProcesoTexto.ngramas(texto)


    def visualizacion(self):
        self.root.mainloop()


    def ngramas_apli2(self):
        texto = self.texto_encontrado.get("1.0",END)
        return ProcesoTexto.ngramas2(texto)


    def colocaciones(self):
        texto = self.texto_encontrado.get("1.0",END)
        resultado2 = ProcesoTexto.coloc2(texto)
        self.texto_procesado.delete("1.0",END)
        self.texto_procesado.insert("1.0",resultado2)
        return ProcesoTexto.colocaciones(texto)


    def sentimientos(self):
        texto = self.texto_encontrado.get("1.0",END)
        return ProcesoTexto.sentimientos_v(texto)


    def nube_l(self):
        texto = self.texto_encontrado.get("1.0",END)
        return ProcesoTexto.nube(texto) 


def main():
    apli = Aplicacion_texto()
    apli.visualizacion()


if __name__=="__main__":
    main()

