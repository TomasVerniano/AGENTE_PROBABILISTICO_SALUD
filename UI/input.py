from datetime import date
import string

class Usuario:

    def ingresarDatos(self):

        while True:
            dni = input("\nDNI: ")
            dni = "".join(car for car in str(dni) if car in string.digits)

            if not len(dni) < 7:
                break
            else:
                print("\nDNI inválido \n Intente denuevo.")
        
        while True:
            nombre = input("\nNombre: ").strip()
            
            if nombre.replace(" ", "").isalpha():
                break
            else:
                print("\nEl nombre no debe contener ningun caracter especial")
            
        while True:
            apellido = input("\nApellido: ").strip() # '  Del Real  ' <- 'Del Real'
            
            if apellido.replace(' ', '').isalpha(): # Del Real <- DelReal
                break
            else:
                print('\nel apellido no debe de contener ningun caracter especial')

        while True:
            fec_nac = input("\nNacimiento (dd/mm/aaaa): ")
            
            try:
                fecha_validada = date.strptime(fec_nac, '%d/%m/%Y')

                if fecha_validada <= date.today():
                    fecha_validada = str(fecha_validada)
                    break
                
                else:
                    print('\n\nFormato incorrecto o fecha inválida. Por favor, usa el formato indicado (ej: 15/05/1998).')
                
            except ValueError:
                print("\nFormato incorrecto o fecha inválida. Por favor, usa el formato indicado (ej: 15/05/1998).")
        
        while True:
            genero = input("\nSexo: ").upper()
            
            if genero == "M" or genero == "F":
                break
            else:
                print("\nIngrese una opcion valida.")

        return (dni, nombre, apellido, fecha_validada, genero)

    def consultar(self, nombre):
        print(f"\nHola {nombre}, soy tu asistente virtual")
        consulta = input('\n-')
        return consulta
