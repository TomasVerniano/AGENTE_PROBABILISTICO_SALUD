import spacy
from spacy.lang.es.stop_words import STOP_WORDS
from sklearn import svm
import os
import json
import numpy as np
import ejemplos as ejemplos

if os.path.exists("respuestas.json"):
    with open("respuestas.json", "r", encoding="utf-8") as archivo:
        TEXTOS = json.load(archivo)
else:
    raise FileNotFoundError(f"Falta el archivo de configuración de respuestas: {"respuestas.json"}")

#python -m spacy download es_coore_news_sm
nlp=spacy.load('es_core_news_lg')

def limpiar(texto):
    doc = nlp(texto.lower())
    limpio = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(limpio)

class Agente():
    
    def clasificar(self, consulta):

        class Clasificaciones:
            secretaria = "secretaria"
            guardia = "guardia"
            urgencias = "urgencias"

        entrenamiento_x = ejemplos.secretaria + \
                ejemplos.guardia + \
                    ejemplos.urgencias 

        x_sin_sw = [limpiar(t) for t in entrenamiento_x]
        consulta_sin_stopwords = limpiar(consulta)

        entrenamiento_y = [Clasificaciones.secretaria] * len(ejemplos.secretaria) + \
                [Clasificaciones.guardia] * len(ejemplos.guardia) + \
                    [Clasificaciones.urgencias] * len(ejemplos.urgencias) 

        sw = list(STOP_WORDS)
        sw.append("mucha")

        entren_x_vector = np.array([nlp(t).vector for t in x_sin_sw])
        consulta_vector = np.array([nlp(consulta_sin_stopwords).vector])

        clasificador_svm_wv = svm.SVC(kernel="linear")
        clasificador_svm_wv.fit(entren_x_vector, entrenamiento_y)

        clase = clasificador_svm_wv.predict(consulta_vector)

        return clase[0]

    def priorizar(self, dpto):
        
        resultado = ""

        if dpto == "secretaria":
            
            print('\nVeo que esta queriendo contactarse con Secretaria. \nPor favor digame en que puedo ayudar o si quiere contactarse directamente con un operador.')
            
            while True:
                try:
                    print("\n1: Consulta \n2: Sacar turno \n3: Reclamo \n4: Operador")
                    opcion = int(input("\n-"))

                    if opcion==1:
                        return 'Baja'
                        break
                    
                    elif opcion==2:
                        return 'Media'
                        break
                    
                    elif opcion==3:
                        return 'Alta'
                        break
                    
                    elif opcion==4:
                        print("\nYa lo estamos contactando, por favor espere")
                        return "Baja"
                        break
                    
                    else:
                        print("\nIngrese una opción válida")

                except ValueError:
                    print("\nIngrese una opción válida")

        if dpto == "guardia":
            return "Media"
             
        if dpto == "urgencias":
            return "Alta"

    def sugerir(self, dpto, prioridad):
    
        if "secretaria" in dpto:
        
            if prioridad =='Baja':

                print("\nPreguntas frecuentes:")

                while True:
                    try:
                        print("\n1: ¿Atienden por Obra Social? \n2: ¿Donde se Ubican? \n3: ¿En que Horario atienden? \n4: Otro.")
                    
                        opcion = int(input("\n-"))
                    
                        if opcion==1:
                            print('\nActualmente trabajamos con: PAMI, Swiss Medical, Apres, IOMA y OSDE.')
                            return "Actualmente trabajamos con: PAMI, Swiss Medical, Apres, IOMA y OSDE."
                            break
                        
                        elif opcion==2:
                            print('\nContamos con múltiples sedes en: Avellaneda, CABA, Lanús, Quilmes')
                            return "Contamos con múltiples sedes en: Avellaneda, CABA, Lanús, Quilmes"
                            break
                        
                        elif opcion==3:
                            print('\nAtendemos de 8hs a 18hs')
                            return "Atendemos de 8hs a 18hs"
                            break
                        
                        elif opcion==4:
                            print('\nPor favor contactese a través de este número: 11-4889-3239 \nO también via Email: email@inventado.com')
                            return 'Por favor contactese a través de este número: 11-4889-3239 \nO también via Email: email@inventado.com'
                            break

                        else:
                            print("\nIngrese una opción válida")

                    except ValueError:
                        print("\nIngrese una opción válida")

            elif prioridad =='Media':
            
                print("\nÁreas:")

                while True:
                    try:
                        print("\n1: Radiología \n2: Pediatría")
                        opcion = int(input('\n-'))
                    
                        if opcion in [1,2]:
                            print('\nNo hay turnos disponibles en este momento. Por favor consulte más tarde')
                            return "No hay turnos disponibles en este momento. Por favor consulte más tarde"
                            break
                    
                        else:
                            print("\nIngrese una opción válida")  

                    except ValueError:
                        print("\nIngrese una opción válida")
        
            else:
                while True:
                    
                    print('\nLamentamos que haya sufrido inconvenientes bajo nuestros servicios.\nIndique el motivo:')
                    print('\n1: Mala atención \n2: Mala práxis \n3: Otro')
                    
                    try:
                        opcion = int(input("\n-"))
                        
                        if opcion==1:
                            reclamo = input('Asunto del reclamo: ')
                            print("Gracias por comunicarte con nosotros. Estaremos trabajando en mejorarlo")
                            return f"reclamo: {reclamo}"
                            break
                        
                        elif opcion==2:
                            reclamo = input("Asunto del reclamo: ")
                            print("Gracias por comunicarte con nosotros. Estaremos trabajando en mejorarlo")
                            return f"reclamo: {reclamo}"
                            break   
                        
                        elif opcion==3:
                            reclamo = input('Asunto del reclamo: ')
                            print("Gracias por comunicarte con nosotros. Estaremos trabajando en mejorarlo")
                            return f"reclamo: {reclamo}"
                            break
                         
                        else:
                            print("Ingrese una opción válida")

                    except ValueError:
                        print("Ingrese una opción válida")

        if "guardia" in dpto:
            print("\nPor favor acerquese al centro médico más cercano.")
            print("\nAvellaneda: Av. Bartolomé Mitre 3420 \n\nCABA: Lavalle 1546 \n\nLanús: Av. Hipólito Yrigoyen 4278 \n\nQuilmes: Sarmiento 766 \n")
            return "Por favor acerquese al centro médico más cercano."
    
        if "urgencias" in dpto:
            print("\nLa ambulancia ya está en camino, por favor aguarde.")
            return "La ambulancia ya está en camino, por favor aguarde." 
