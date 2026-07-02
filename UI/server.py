from flask import Flask, render_template, request, jsonify
import os
import json
from modelo import Agente

app = Flask(__name__)
agente = Agente()

NOMBRE_ARCHIVO_TICKETS = 'tickets.json'
NOMBRE_ARCHIVO_RESPUESTAS = 'respuestas.json'

if os.path.exists(NOMBRE_ARCHIVO_RESPUESTAS):
    
    with open(NOMBRE_ARCHIVO_RESPUESTAS, "r", encoding="utf-8") as archivo:
        TEXTOS = json.load(archivo)

else:
    raise FileNotFoundError(f"Falta el archivo de respuestas: {NOMBRE_ARCHIVO_RESPUESTAS}")

def guardar_ticket(datos_front, dpto, prioridad, resultado):

    lista_usuarios = []
    if os.path.exists(NOMBRE_ARCHIVO_TICKETS):
        with open(NOMBRE_ARCHIVO_TICKETS, "r", encoding="utf-8") as archivo:
            
            try:
                lista_usuarios = json.load(archivo)
            
            except json.JSONDecodeError:
                lista_usuarios = []

    nuevo_usuario = {
        "dni": datos_front.get("dni"),
        "nombre": datos_front.get("nombre"),
        "apellido": datos_front.get("apellido"),
        "fecha_nacimiento": datos_front.get("fecha_nacimiento"),
        "sexo": datos_front.get("sexo"),
        "consulta": datos_front.get("consulta"),
        "dpto": dpto,
        "prioridad": prioridad,
        "resultado": resultado
    }

    lista_usuarios.append(nuevo_usuario)
    with open(NOMBRE_ARCHIVO_TICKETS, 'w', encoding='utf-8') as archivo:
        json.dump(lista_usuarios, archivo, indent=4, ensure_ascii=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/inicial', methods=['POST'])
def procesamiento_inicial():
    data = request.json
    consulta = data.get('consulta', '')

    dpto = agente.clasificar(consulta)

    if dpto == "guardia":
        config = TEXTOS["guardia"]
        guardar_ticket(data, dpto, config["prioridad"], config["resultado"])
        return jsonify({"status": "finalizado", "mensaje": config["mensaje"]})

    elif dpto == "urgencias":
        config = TEXTOS["urgencias"]
        guardar_ticket(data, dpto, config["prioridad"], config["resultado"])
        return jsonify({"status": "finalizado", "mensaje": config["mensaje"]})

    elif dpto == "secretaria":
        config = TEXTOS["secretaria"]
        return jsonify({
            "status": "opciones_prioridad",
            "mensaje": config["mensaje"],
            "opciones": config["opciones_principales"]
        })

@app.route('/api/secretaria/siguiente', methods=['POST'])
def siguiente_paso_secretaria():
    data = request.json
    opcion_id = str(data.get('opcion_id'))
    user_info = data.get('user_data')
    
    config_pasos = TEXTOS["secretaria"]["pasos"]

    if opcion_id == "1":
        return jsonify({
            "status": "opciones_faq",
            "prioridad": "Baja",
            "mensaje": config_pasos["1"]["mensaje"],
            "opciones": config_pasos["1"]["opciones"]
        })
    elif opcion_id == "2":
        return jsonify({
            "status": "opciones_areas",
            "prioridad": "Media",
            "mensaje": config_pasos["2"]["mensaje"],
            "opciones": config_pasos["2"]["opciones"]
        })
    elif opcion_id == "3":
        return jsonify({
            "status": "opciones_motivo_reclamo",
            "prioridad": "Alta",
            "mensaje": config_pasos["3"]["mensaje"],
            "opciones": config_pasos["3"]["opciones"]
        })
    elif opcion_id == "4":
        respuesta = config_pasos["4"]["mensaje"]
        guardar_ticket(user_info, "secretaria", "Baja", respuesta)
        return jsonify({"status": "finalizado", "mensaje": respuesta})

@app.route('/api/secretaria/reclamo_texto', methods=['POST'])
def reclamo_texto():
    return jsonify({
        "status": "formulario_reclamo",
        "mensaje": "Asunto del reclamo: "
    })

@app.route('/api/secretaria/finalizar', methods=['POST'])
def finalizar_secretaria():
    data = request.json
    tipo = data.get('tipo')
    sub_opcion = str(data.get('sub_opcion_id'))
    texto_reclamo = data.get('texto_reclamo')
    prioridad = data.get('prioridad')
    user_info = data.get('user_data')

    config_finales = TEXTOS["secretaria"]["respuestas_finales"]
    respuesta = ""
    resultado_guardar = ""
    
    if tipo == "faq":
        respuesta = config_finales["faq"].get(sub_opcion, "")
        resultado_guardar = respuesta
    elif tipo == "areas":
        respuesta = config_finales["areas"]
        resultado_guardar = respuesta
    elif tipo == "reclamo":
        respuesta = config_finales["reclamo"]
        # Respetando la regla de negocio para la respuesta formateada de reclamos
        resultado_guardar = f"Reclamo: '{texto_reclamo}'"
        
    guardar_ticket(user_info, "secretaria", prioridad, resultado_guardar)
    return jsonify({"status": "finalizado", "mensaje": respuesta})

if __name__ == '__main__':
    app.run(debug=True, port=5000)