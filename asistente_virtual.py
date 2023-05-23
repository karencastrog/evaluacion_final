import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
from datetime import datetime
import wikipedia
import cv2

# inicia motor de texto a voz
motor = pyttsx3.init()

# Configura la velocidad de lectura
velocidad = motor.getProperty("rate")
motor.setProperty("rate", velocidad - 10)

# Nombre del asistente
nombre = "lucas"
print("""
    Estas son las opciones disponibles: 
    1. Lucas reproduce ___ (en youtube)
    2. Lucas dame la hora
    3. Lucas busca en wikipedia ___
    4. Lucas abre google
    5. Lucas toma una foto
    6. Lucas detente
    """)

def hablar(contenido):
    motor.say(contenido)
    motor.runAndWait()

def escuchar():
    escuchar = sr.Recognizer()
    try:
        with sr.Microphone() as source: 
            hablar("Hola, soy Lucas, ¿qué necesitas?")
            escuchar.adjust_for_ambient_noise(source)
            audio = escuchar.listen(source)
            audio = escuchar.recognize_google(audio, language="es")
            info = audio.lower()
            print("Dijiste: {}".format(info))
    except sr.UnknownValueError:
        hablar("Lo siento, no te entendí")
    return info

def dar_hora():
    ahora = datetime.now()
    current_time = ahora.strftime("%H:%M:%S")
    print(f"La hora actual es {current_time}")
    hablar(f"La hora actual es {current_time}")

def buscar_wikipedia(consulta):
    wikipedia.set_lang("es")
    resultado = wikipedia.summary(consulta, sentences=2, auto_suggest=False)
    print(resultado)
    hablar(resultado)
    

def abrir_google():
    webbrowser.open_new_tab("https://www.google.com")

def tomar_foto():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        cv2.imwrite('foto.png', frame)
    cam.release()
    if ret:
        hablar("Foto tomada.")
    else:
        hablar("Lo siento, no pude tomar una foto.")

def reproducir_youtube(video):
    pywhatkit.playonyt(video)
    hablar(f"Reproduciendo {video}.")

def ejecutar_asistente():
    while True:
        try:
            info = escuchar()
        except UnboundLocalError:
            hablar("Intenta de nuevo, por fa")
            continue
        if nombre in info:
            info = info.replace(nombre, '').strip()
            if 'reproduce' in info:
                video = info.replace('reproduce', '').strip()
                reproducir_youtube(video)
            elif 'dame la hora' in info:
                dar_hora()
            elif 'busca en wikipedia' in info:
                consulta = info.replace('busca en wikipedia', '').strip()
                buscar_wikipedia(consulta)
            elif 'abre google' in info:
                abrir_google()
            elif 'toma una foto' in info:
                tomar_foto()
            elif 'detente' in info:
                hablar("ok, Me detendré ahora.")
                break

ejecutar_asistente()