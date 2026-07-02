from modelo import Agente
from input import Usuario
import os
import json

def main():

    agente = Agente()
    usuario = Usuario()

    #<USUARIO>
    datos = usuario.ingresarDatos()
    consultado = usuario.consultar(datos[1])
    #</USUARIO>

    #<AGENTE>
    dpto = agente.clasificar(consultado)
    prioridad = agente.priorizar(dpto)
    sugerencia = agente.sugerir(dpto, prioridad)
    #</AGENTE>
    
    #</ALMACENAR>
    nombre_archivo ='tickets.json'

    nuevo_usuario={
        "dni" : datos[0],
        'nombre': datos[1], 
        'apellido': datos[2], 
        'fecha_nacimiento': datos[3], 
        'genero': datos[4],
        'consulta':consultado,
        'dpto':dpto,
        'prioridad':prioridad,
        'resultado':sugerencia
    }

    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        
            try:
                lista_usuarios = json.load(archivo)
        
            except json.JSONDecodeError:
                lista_usuarios=[]

    else:
        lista_usuarios = [] 

    lista_usuarios.append(nuevo_usuario)

    with open(nombre_archivo,'w',encoding='utf-8') as archivo:
        json.dump(lista_usuarios,archivo, indent=4, ensure_ascii=False)
    #</ALMACENAR>

if __name__ == '__main__':
    main()