from gtts import gTTS


"""
    this use the library GTTS from goole that generates audio 
"""
def guardarAudios():
    frase= "eres menor de edad, no se te permite ingresar"
    myobj = gTTS(text=frase, lang="es", slow=False)
    myobj.save("menorEdad.mp3")

    frase= "su temperatura es elevada. no tiene permitido el ingreso, le recomendamos consultar a un médico"
    myobj = gTTS(text=frase, lang="es", slow=False)
    myobj.save("temperaturaElevada.mp3")

    frase= "lo sentimos. Hoy no tienes permitido ingresar. Te esperamos mañana"
    myobj = gTTS(text=frase, lang="es", slow=False)
    myobj.save("diaNoIngreso.mp3")

    frase= "Bienvenido"
    myobj = gTTS(text=frase, lang="es", slow=False)
    myobj.save("bienvenido.mp3")

    frase= "Bienvenida"
    myobj = gTTS(text=frase, lang="es", slow=False)
    myobj.save("bienvenida.mp3")

    frase= "bienvenida. por favor acérquese al sensor"
    myobj = gTTS(text=frase, lang="es", slow=False)
    myobj.save("introMujer.mp3")

    frase= "bienvenido. por favor acérquese al sensor"
    myobj = gTTS(text=frase, lang="es", slow=False)
    myobj.save("introHombre.mp3")