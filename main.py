import tkinter                  #Biblioteca Tkinter
from PIL import Image, ImageTk  #Para tener más opciones de edición de imágenes
from random import choice       #Elecciones aleatorias para el bot
from copy import deepcopy       #Para diccionario anidados (pkDefaultStats y gameStats)

#|||Código para la aplicación|||

#|Variables globales|

IsPlayerTurn = True

listaPokemones = [
    "Don Elmer",
    "Rodrigo Chaves",
    "BB7",
    "Diego Garro",
    "Porcionzón",
    "Ignacio Santos",
    "Edgar Silva",
    "Jerry Alfaro",
    "Araya Vlogs",
    "Corney"
]

pkDefaultStats = {
    "Don Elmer": {
        "HP": 100,
        "ATQ": 50,
        "DEF": 30,
        "DEFEX": 0},
    "Rodrigo Chaves": {
        "HP": 120,
        "ATQ": 40,
        "DEF": 50,
        "DEFEX": 0},
    "BB7": {
        "HP": 80,
        "ATQ": 60,
        "DEF": 20,
        "DEFEX": 0},
    "Diego Garro": {
        "HP": 90,
        "ATQ": 55,
        "DEF": 25,
        "DEFEX": 0},
    "Porcionzón": {
        "HP": 110,
        "ATQ": 45,
        "DEF": 40,
        "DEFEX": 0},
    "Ignacio Santos": {
        "HP": 95,
        "ATQ": 65,
        "DEF": 15,
        "DEFEX": 0},
    "Edgar Silva": {
        "HP": 85,
        "ATQ": 70,
        "DEF": 10,
        "DEFEX": 0},
    "Jerry Alfaro": {
        "HP": 105,
        "ATQ": 35,
        "DEF": 45,
        "DEFEX": 0},
    "Araya Vlogs": {
        "HP": 115,
        "ATQ": 30,
        "DEF": 55,
        "DEFEX": 0},
    "Corney": {
        "HP": 75,
        "ATQ": 80,
        "DEF": 5,
        "DEFEX": 0}
}
gameStats = deepcopy(pkDefaultStats)    #Variable para almacenar las estadísticas de los pokemones durante la batalla, se modifica constantemente pero se restaura a los valores por defecto al finalizar o salir de la batalla.





#|Clases|

class registroClasificacion:
    
    """Clase para manejar la lectura y escritura de la clasificación en el archivo de texto"""

    def leerClasificacion(controller):

        """Función para leer la clasificación del archivo de texto y actualizar la tabla
        de clasificación en la ventana correspondiente"""

        tradTxt = []
        
        with open("Data/scoreboard.txt", "r") as file:  #Abrir el archivo de texto en modo lectura. Almacena cada linea en una lista, luego separa cada linea en avatar, nombre y puntos y almacena cada una en una lista dentro de tradTxt.
            lineas = file.readlines()
            for linea in lineas:
                avatar, nombre, puntos = linea.strip().split("-")
                tradTxt.append([avatar, nombre, puntos])
        
        tradTxt.sort(key=lambda x: int(x[2]), reverse=True) #ordenar tradTxt de mayor a menor puntaje en base a la posición 2 de cada lista (puntos)

        if not hasattr(controller, 'avtImgs'):  #Crear lista para guardar referencias persistentes a las imágenes.
           controller.avtImgs = []
        controller.avtImgs = [] #Limpiar la lista
        
        
        for i in range(10): #Actualizar tabla de clasificación con los datos del archivo de texto. Si falta algún puesto, rellenar con datos vacíos.
            if i < len(tradTxt):
                avatar, nombre, puntos = tradTxt[i]
                avtImg = img(f"{avatar}.png", 50, 50)
                controller.avtImgs.append(avtImg)  # Guardar referencia persistente
                controller.listaPuestos[i][0].delete("all")
                controller.listaPuestos[i][0].create_image(0, 0, anchor="nw", image=avtImg)
                controller.listaPuestos[i][1].configure(text=nombre)
                controller.listaPuestos[i][2].configure(text=puntos)
            else:
                controller.listaPuestos[i][0].delete("all")
                controller.listaPuestos[i][1].configure(text="")
                controller.listaPuestos[i][2].configure(text="")
    
    def escribirClasificacion(controller, ganador):

        """Función para escribir el ganador de la partida en el archivo de texto y actualizar la clasificación"""

        tradTxt = []

        Gnombre = ganador.nombre
        Gavatar = ganador.avatar
        Gpuntos = ganador.puntos


        with open("Data/scoreboard.txt", "r+") as file:
            lineas = file.readlines()

            for linea in lineas:    #Separar cada linea en avatar, nombre y puntos y almacenar cada una en una lista dentro de tradTxt IMPORTANTE: el formato del archivo de texto debe ser avatar-nombre-puntos, separados por guiones, sin espacios. Su posición en el archivo de texto determina su posición en la clasificación.
                avatar, nombre, puntos = linea.strip().split("-")
                tradTxt.append([avatar, nombre, puntos])

            tradTxt.append([Gavatar, Gnombre, str(Gpuntos)])

            tradTxt.sort(key=lambda x: int(x[2]), reverse=True) #Ordenar la clasificación de mayor a menor puntaje, en base a la posición 2 de cada lista (puntos)

            with open("Data/scoreboard.txt", "w") as file:  #Rescribir el archivo de texto con la nueva clasificación, limitando a los 10 primeros puestos.
                for avatar, nombre, puntos in tradTxt[:10]:
                    file.write(f"{avatar}-{nombre}-{puntos}\n") #Formato del archivo txt: avatar-nombre-puntos, separados por guiones, sin espacios. Su posición en el archivo de texto determina su posición en la clasificación.
    
        return

class bot:

    """Clase para representar al bot, con funciones para generar un nombre, avatar y equipo de pokemones aleatorios"""

    def __init__(self, nombre, avatar, equipo): #El nombre, avatar y equipo del bot se asignan al iniciar la partida, utilizando las funciones de la clase para generar valores aleatorios.
        self.nombre = nombre
        self.avatar = avatar
        self.pk = equipo
        self.currentPk

    def nombreBot(self):
        
        """Función para generar un nombre aleatorio para el bot, utilizando una lista de nombres predefinidos
        y agregando un número aleatorio para hacerlo único"""

        nombre = choice(["Alfa", "Beta", "Gamma", "Delta", "Epsilon"])
        nombre = nombre + str(choice(range(1, 100)))

        return nombre
    
    def avatarBot(self):
        
        """Función para generar un avatar aleatorio para el bot, utilizando una lista de nombres de archivos
        de imagen predefinidos y seleccionando uno al azar"""

        avt = choice(["av0", "av1", "av2", "av3", "av4"])

        return avt
    
    def equipoBot(self):
        
        """Función para generar un equipo de pokemones aleatorio para el bot, utilizando la lista de pokemones
        predefinida y seleccionando uno al azar, asegurándose de que no se repita ningún pokemon en el equipo
        del bot ni en el del jugador"""

        equipo = []
        for _ in range(3):
            pk = choice(listaPokemones)
            while pk in equipo or pk in jugador.pk: #Evalúa si ya tiene un Pokemon igual en su equipo o en el del jugador
                pk = choice(listaPokemones)
            equipo.append(pk)

        return equipo

class jugador:

    """Clase para representar al jugador, su nombre, avatar, equipo de pokemones y pokemon en uso"""

    def __init__(self, nombre, avatar, equipo, currentPk):
        self.nombre = nombre
        self.avatar = avatar
        self.pk = equipo
        self.currentPk = currentPk


#Para evitar problemas con la clasificación, se asignan puntos iniciales de 0 tanto al jugador como al bot, aunque no se utilice esta variable hasta el final de la partida, cuando se actualiza la clasificación.
jugador.puntos = 0
bot.puntos = 0





#|Funciones independientes|

def img(path, x, y):

    """Función para cargar y redimensionar imágenes, devuelve la imagen en formato compatible con Tkinter"""

    imagen = ImageTk.PhotoImage(Image.open(f"Img/{path}").resize((x, y)))

    return imagen

def TESTFUNCTION():

    """Función para probar el correcto funcionamiento de las clases y variables globales, imprimiendo los
    datos relevantes en la consola. No tiene ningún impacto en la aplicación, se puede eliminar o comentar
    sin afectar el funcionamiento del programa."""

    print("\n\n\n\n\n\n\n\n\n\n-------------PRUEBA-------------\n")
    print(f"Lista de pokemones del JUGADOR: {jugador.pk}")
    print(f"Pokemon en uso de JUGADOR: {jugador.currentPk}\n")
    
    print(f"Pokemon en uso de BOT: {bot.currentPk}")
    print(f"Lista de pokemones del BOT: {bot.pk}")
    
    
    print("DATOS POR DEFECTO-----\n")
    print(f"Estadisticas del Pokemon de JUGADOR por defecto: ATQ({pkDefaultStats[jugador.currentPk]['ATQ']})  DEF({pkDefaultStats[jugador.currentPk]['DEF']})  HP({pkDefaultStats[jugador.currentPk]['HP']})")
    print(f"Estadisticas del Pokemon BOT por defecto: ATQ({pkDefaultStats[bot.currentPk]['ATQ']})  DEF({pkDefaultStats[bot.currentPk]['DEF']})  HP({pkDefaultStats[bot.currentPk]['HP']})")
    print("\nDATOS EN BATALLA------\n")
    print(f"Estadisticas del Pokemon de JUGADOR en turno ATQ({gameStats[jugador.currentPk]['ATQ']})  DEF({gameStats[jugador.currentPk]['DEF']})  HP({gameStats[jugador.currentPk]['HP']})  +DEF({gameStats[jugador.currentPk]['DEFEX']})")
    print(f"Estadisticas del Pokemon de BOT en turno ATQ({gameStats[bot.currentPk]['ATQ']})  DEF({gameStats[bot.currentPk]['DEF']})  HP({gameStats[bot.currentPk]['HP']})  +DEF({gameStats[bot.currentPk]['DEFEX']})")

def intercambiarPK(ganador, perdedor, controller):

    """Función para intercambiar el Pokemon derrotado del perdedor al equipo del ganador, restaurar la vida
    del Pokemon añadido y actualizar la ventana de batalla. Si el perdedor se queda sin pokemones, muestra
    la ventana de clasificación y actualiza la clasificación con el ganador."""

    ganador.pk.append(perdedor.currentPk)       #Añadir el Pokemon derrotado al equipo del ganador
    perdedor.pk.remove(perdedor.currentPk)      #Remover el Pokemon derrotado del equipo del perdedor


    gameStats[ganador.pk[-1]]["HP"] = pkDefaultStats[ganador.pk[-1]]["HP"]      #Restaurar la vida del Pokemon añadido. Índice -1 para referirse al último Pokemon añadido al equipo del ganador, que es el Pokemon derrotado del perdedor.


    if len(perdedor.pk) == 0:       #Si el perdedor se queda sin pokemones, mostrar la ventana de clasificación y actualizar la clasificación con el ganador
        controller.mostrar_ventana(clasif)
        registroClasificacion.escribirClasificacion(controller, ganador)
        registroClasificacion.leerClasificacion(controller.ventanas[clasif])
        return

    perdedor.currentPk = perdedor.pk[0]     #Establecer el primer Pokemon del equipo del perdedor como Pokemon en uso.

def cambiarPk(JB):

    """Función para cambiar el Pokemon en uso del jugador o bot, dependiendo de quién sea el que llama a
    la función. Cambia al siguiente Pokemon en la lista de pokemones del jugador o bot, y si llega al final
    de la lista, vuelve al primer Pokemon."""

    lastIndex = len(JB.pk) - 1
    nextPk = JB.pk.index(JB.currentPk)
    nextPk += 1

    if nextPk > lastIndex:
        nextPk = 0

    JB.currentPk = JB.pk[nextPk] #Cambia el pokemon en uso al siguiente Pokemon en su equipo.

def calcularFortaleza(CurrentPk):
    
    """Función para calcular la fortaleza de un Pokemon, que es un aumento temporal de defensa que dura 1 turno.
    Se calcula como el 20% de la defensa base del Pokemon, redondeado al número entero más cercano."""

    #Fórmula: Fortaleza temporal = Defensa base del Pokemon * 0.2
    global gameStats
    fortaleza = pkDefaultStats[CurrentPk]["DEF"]
    fortaleza = round(fortaleza * 0.2)

    return fortaleza

def calcularDaño(CurrentPk, RivalCurrentPk):

    """Función para calcular el daño que un Pokemon le hace a otro al atacar, teniendo en cuenta la defensa base
    del rival, la fortaleza temporal del rival y el ataque del Pokemon en uso. El daño real se calcula como el
    ataque del Pokemon en uso menos la defensa base del rival y la fortaleza temporal del rival. Si el daño
    real es menor a 0, se considera que el ataque no hizo daño. Además, la fortaleza temporal del rival se reduce
    en la cantidad de ataque del Pokemon que ataca, y si la fortaleza temporal restante es menor a 0, se restaura a 0."""


    #Fórmula: Daño real = Ataque del Pokemon en uso - (Defensa base del rival + Fortaleza temporal del rival)
    CurrentPkAtq = gameStats[CurrentPk]["ATQ"]
    RivalCurrentPkDef = gameStats[RivalCurrentPk]["DEF"]

    DefExtra = gameStats[RivalCurrentPk]["DEFEX"]
    dañoReal = (CurrentPkAtq - DefExtra) - RivalCurrentPkDef
    DefExtraRestante = DefExtra - CurrentPkAtq

    if dañoReal < 0:
        dañoReal = 0
    
    if DefExtraRestante < 0:
        DefExtraRestante = 0

    gameStats[RivalCurrentPk]["DEFEX"] = DefExtraRestante

    return dañoReal
        

def calcularCura(currentPk):

    """Función para calcular la cantidad de vida que un Pokemon recupera al usar la acción de curar, que es el 20%
    de su vida máxima, redondeado al número entero más cercano."""

    #Fórmula: Vida a recuperar = Vida máxima del Pokemon * 0.2

    vidaMax = pkDefaultStats[currentPk]["HP"]
    cura =  round(vidaMax * 0.2)

    return cura



def turnoBot(controller):

    """Función para ejecutar el turno del bot, elige una acción aleatoria entre atacar, defender, curar o cambiar de Pokemon,
    y ejecuta la acción elegida. Después de ejecutar la acción, espera 2 segundos y luego permite el siguiente turno del jugador."""

    global IsPlayerTurn
    global gameStats

    game_frame = controller.ventanas[game]

    acc = choice(["DEF", "ATQ", "HP", "CH"]) #Elegir entre Defender, Atacar, Curar o Cambiar pokemon actual.

    def ejecutarAccion():

        """Función para ejecutar la acción elegida por el bot, dependiendo de la acción elegida, se ejecuta el código correspondiente
        para cada acción. Al finalizar la acción, espera 2 segundos y luego permite el siguiente turno del jugador."""

        nonlocal acc
        if acc == "CH":
            cambiarPk(bot)
            game_frame.C_PkBot.delete("all")
            game_frame.botPkImg = img(f"pk{listaPokemones.index(bot.currentPk)}.png", 200, 200)
            game_frame.C_PkBot.create_image(0, 0, anchor="nw", image=game_frame.botPkImg)
            game_frame.L_PkBotName.configure(text=f"{bot.nombre}:   {bot.currentPk}")
            Hp = gameStats[bot.currentPk]["HP"]
            Atq = gameStats[bot.currentPk]["ATQ"]
            Def = gameStats[bot.currentPk]["DEF"]
            DefEx = gameStats[bot.currentPk]["DEFEX"]
            game_frame.BcurrentPkHP.set(f"HP: {Hp}")
            game_frame.BcurrentPkATQ.set(f"ATQ: {Atq}")
            game_frame.BcurrentPkDEF.set(f"DEF: {Def}")
            game_frame.BcurrentPkDEFEx.set(f"+DEF: {DefEx}")
            game_frame.L_BotInfo.configure(text=f"{bot.nombre} cambió a {bot.currentPk}!")
            game_frame.after(2000, turnoBot, controller) #Después de cambiar de Pokemon, el bot ejecuta otra acción aleatoria, para evitar que el bot cambie de Pokemon y luego espere 2 segundos sin hacer nada. Al ejecutar otra acción después de cambiar de Pokemon, el bot ejecuta otra acción aleatoria.
            return
        
        currentPk = bot.currentPk
        
        if acc == "DEF":
            gameStats[currentPk]["DEFEX"] = calcularFortaleza(currentPk)
            DefEx = gameStats[currentPk]["DEFEX"]
            game_frame.PcurrentPkDEFEx.set(f"+DEF: {DefEx}")
            game_frame.L_BotInfo.configure(text=f"{bot.currentPk} ha incrementado su defensa! +{gameStats[bot.currentPk]['DEFEX']} DEF por 1 turno")
        
        elif acc == "ATQ":
            daño = calcularDaño(currentPk, jugador.currentPk)
            if daño == 0:
                game_frame.L_BotInfo.configure(text=f"{bot.currentPk} ha atacado a {jugador.currentPk} pero no le hizo daño!")
                gameStats[jugador.currentPk]["DEFEX"] = 0
                game_frame.PcurrentPkDEFEx.set(f"+DEF: {gameStats[jugador.currentPk]['DEFEX']}")
            else:
                HpRestante = gameStats[jugador.currentPk]["HP"] - daño
                if HpRestante <= 0:
                    gameStats[jugador.currentPk]["HP"] = 0
                    game_frame.L_BotInfo.configure(text=f"{bot.currentPk} ha derrotado a {jugador.currentPk}, {jugador.currentPk} ahora le pertenece a {bot.nombre}!")
                    bot.puntos += 1
                    game_frame.after(2000, lambda: finalizarBotAtaque(controller))
                    return
                else:
                    gameStats[jugador.currentPk]["HP"] = HpRestante
                    game_frame.L_BotInfo.configure(text=f"{bot.currentPk} ha atacado a {jugador.currentPk} causando {daño} de daño!")
                    game_frame.PcurrentPkHP.set(f"HP: {gameStats[jugador.currentPk]['HP']}")
        
        elif acc == "HP":
            cura = calcularCura(currentPk)
            vidaActual = gameStats[currentPk]["HP"]
            vidaMax = pkDefaultStats[currentPk]["HP"]
            curacionPk = vidaActual + cura
            if curacionPk > vidaMax:
                gameStats[currentPk]["HP"] = vidaMax
                game_frame.BcurrentPkHP.set(f"HP: {gameStats[currentPk]['HP']}")
                game_frame.L_BotInfo.configure(text=f"{bot.currentPk} se ha curado por completo!")
            else:
                gameStats[currentPk]["HP"] += cura
                game_frame.BcurrentPkHP.set(f"HP: {gameStats[currentPk]['HP']}")
                game_frame.L_BotInfo.configure(text=f"{bot.currentPk} se ha curado por {cura} HP!")
        
        gameStats[jugador.currentPk]["DEFEX"] = 0
        game_frame.PcurrentPkDEFEx.set(f"+DEF: {gameStats[jugador.currentPk]['DEFEX']}")
        game_frame.PcurrentPkHP.set(f"HP: {gameStats[jugador.currentPk]['HP']}")
        game_frame.PcurrentPkATQ.set(f"ATQ: {gameStats[jugador.currentPk]['ATQ']}")
        game_frame.PcurrentPkDEF.set(f"DEF: {gameStats[jugador.currentPk]['DEF']}")
        game_frame.after(2000, lambda: terminarTurnoBot(controller))
    
    game_frame.after(2000, ejecutarAccion)


def finalizarBotAtaque(controller):

    """Función que se ejecuta cuando el bot derrota el Pokemon del jugador, intercambia el Pokemon derrotado al equipo del bot,
    actualiza la ventana de batalla y luego permite el siguiente turno del jugador."""

    global gameStats
    game_frame = controller.ventanas[game]
    intercambiarPK(bot, jugador, controller)
    game_frame.puntosBot.set(f"PUNTOS: {bot.puntos}")
    game_frame.C_PkJugador.delete("all")
    game_frame.jugadorPkImg = img(f"pk{listaPokemones.index(jugador.currentPk)}.png", 200, 200)
    game_frame.C_PkJugador.create_image(0, 0, anchor="nw", image=game_frame.jugadorPkImg)
    game_frame.L_PkPlayerName.configure(text=f"{jugador.nombre}:   {jugador.currentPk}")
    game_frame.PcurrentPkHP.set(f"HP: {gameStats[jugador.currentPk]['HP']}")
    game_frame.PcurrentPkATQ.set(f"ATQ: {gameStats[jugador.currentPk]['ATQ']}")
    game_frame.PcurrentPkDEF.set(f"DEF: {gameStats[jugador.currentPk]['DEF']}")
    game_frame.PcurrentPkDEFEx.set(f"+DEF: {gameStats[jugador.currentPk]['DEFEX']}")
    game_frame.after(2000, lambda: terminarTurnoBot(controller))


def terminarTurnoBot(controller):

    """Función para terminar el turno del bot, permite el turno del jugador después de que el bot haya ejecutado su acción y
    esperado 2 segundos."""

    global IsPlayerTurn
    IsPlayerTurn = True


def turnoJugador(acc, controller):

    """Función para ejecutar el turno del jugador, dependiendo de la acción elegida por el jugador, se ejecuta el código
    correspondiente para cada acción. Al finalizar la acción, espera 2 segundos y luego ejecuta el turno del bot.
    Si el jugador intenta ejecutar una acción cuando no es su turno, la función no hace nada."""

    global IsPlayerTurn
    global gameStats
    
    game_frame = controller.ventanas[game]
    
    if not IsPlayerTurn:
        return
    
    if acc == "CH":
        cambiarPk(jugador)
        game_frame.C_PkJugador.delete("all")
        game_frame.jugadorPkImg = img(f"pk{listaPokemones.index(jugador.currentPk)}.png", 200, 200)
        game_frame.C_PkJugador.create_image(0, 0, anchor="nw", image=game_frame.jugadorPkImg)
        game_frame.L_PkPlayerName.configure(text=f"{jugador.nombre}:   {jugador.currentPk}")
        Hp = gameStats[jugador.currentPk]["HP"]
        Atq = gameStats[jugador.currentPk]["ATQ"]
        Def = gameStats[jugador.currentPk]["DEF"]
        DefEx = gameStats[jugador.currentPk]["DEFEX"]
        game_frame.PcurrentPkHP.set(f"HP: {Hp}")
        game_frame.PcurrentPkATQ.set(f"ATQ: {Atq}")
        game_frame.PcurrentPkDEF.set(f"DEF: {Def}")
        game_frame.PcurrentPkDEFEx.set(f"+DEF: {DefEx}")
        game_frame.L_PlayerInfo.configure(text=f"{jugador.nombre} cambió a {jugador.currentPk}!")
        return

    IsPlayerTurn = False #Desactivar el turno del jugador para evitar que ejecute otra acción antes de que el bot ejecute su turno después de esta acción.
    currentPk = jugador.currentPk
    
    if acc == "DEF":
        gameStats[currentPk]["DEFEX"] = calcularFortaleza(currentPk)
        DefEx = gameStats[currentPk]["DEFEX"]
        game_frame.PcurrentPkDEFEx.set(f"+DEF: {DefEx}")
        game_frame.L_PlayerInfo.configure(text=f"{jugador.currentPk} ha incrementado su defensa! +{gameStats[jugador.currentPk]['DEFEX']} DEF por 1 turno")
    
    elif acc == "ATQ":
        daño = calcularDaño(currentPk, bot.currentPk)
        if daño == 0:
            game_frame.L_PlayerInfo.configure(text=f"{jugador.currentPk} ha atacado a {bot.currentPk} pero no le hizo daño!")
            gameStats[bot.currentPk]["DEFEX"] = 0
            game_frame.BcurrentPkDEFEx.set(f"+DEF: {gameStats[bot.currentPk]['DEFEX']}")
            game_frame.after(2000, turnoBot, controller)
            return

        HpRestante = gameStats[bot.currentPk]["HP"] - daño
        if HpRestante <= 0:
            gameStats[bot.currentPk]["HP"] = 0
            game_frame.L_PlayerInfo.configure(text=f"{jugador.currentPk} ha derrotado a {bot.currentPk}, {bot.currentPk} ahora le pertenece a {jugador.nombre}!")
            jugador.puntos += 1
            game_frame.after(2000, lambda: finalizarJugadorAtaque(controller))
            return
        else:
            gameStats[bot.currentPk]["HP"] = HpRestante
            game_frame.L_PlayerInfo.configure(text=f"{jugador.currentPk} ha atacado a {bot.currentPk} causando {daño} de daño!")
    
    elif acc == "HP":
        cura = calcularCura(currentPk)
        vidaActual = gameStats[currentPk]["HP"]
        vidaMax = pkDefaultStats[currentPk]["HP"]
        curacionPk = vidaActual + cura
        if curacionPk > vidaMax:
            gameStats[currentPk]["HP"] = vidaMax
            game_frame.PcurrentPkHP.set(f"HP: {gameStats[currentPk]['HP']}")
            game_frame.L_PlayerInfo.configure(text=f"{jugador.currentPk} se ha curado por completo!")
        else:
            gameStats[currentPk]["HP"] += cura
            game_frame.PcurrentPkHP.set(f"HP: {gameStats[currentPk]['HP']}")
            game_frame.L_PlayerInfo.configure(text=f"{jugador.currentPk} se ha curado por {cura} HP!")

    gameStats[bot.currentPk]["DEFEX"] = 0
    game_frame.BcurrentPkDEFEx.set(f"+DEF: {gameStats[bot.currentPk]['DEFEX']}")
    game_frame.BcurrentPkHP.set(f"HP: {gameStats[bot.currentPk]['HP']}")
    game_frame.BcurrentPkATQ.set(f"ATQ: {gameStats[bot.currentPk]['ATQ']}")
    game_frame.BcurrentPkDEF.set(f"DEF: {gameStats[bot.currentPk]['DEF']}")
    game_frame.after(2000, turnoBot, controller)


def finalizarJugadorAtaque(controller):

    """Función que se ejecuta cuando el jugador derrota el Pokemon del bot, intercambia el Pokemon derrotado al equipo del jugador,"""

    global gameStats
    game_frame = controller.ventanas[game]
    intercambiarPK(jugador, bot, controller)
    game_frame.puntosJugador.set(f"PUNTOS: {jugador.puntos}")
    game_frame.C_PkBot.delete("all")
    game_frame.botPkImg = img(f"pk{listaPokemones.index(bot.currentPk)}.png", 200, 200)
    game_frame.C_PkBot.create_image(0, 0, anchor="nw", image=game_frame.botPkImg)
    game_frame.L_PkBotName.configure(text=f"{bot.nombre}:   {bot.currentPk}")
    game_frame.BcurrentPkHP.set(f"HP: {gameStats[bot.currentPk]['HP']}")
    game_frame.BcurrentPkATQ.set(f"ATQ: {gameStats[bot.currentPk]['ATQ']}")
    game_frame.BcurrentPkDEF.set(f"DEF: {gameStats[bot.currentPk]['DEF']}")
    game_frame.BcurrentPkDEFEx.set(f"+DEF: {gameStats[bot.currentPk]['DEFEX']}")
    game_frame.after(2000, turnoBot, controller)



        
    

    


























#|||UI de la aplicación|||

class root(tkinter.Tk):

    """Clase principal de la aplicación, hereda de tkinter.Tk, se encarga de crear la ventana principal, el contenedor para las
    ventanas y el diccionario para almacenar las ventanas. También tiene la función para mostrar las ventanas."""

    def __init__(self):
        super().__init__()
        self.title("TicoMon")
        self.state("zoomed")
        self.configure(bg="blue")
    
        #Contenedor dentro de root para mostrar las ventanas
        self.contenedor = tkinter.Frame(self, background="black")
        self.contenedor.pack(expand=True, fill="both")

        #Diccionario para almacenar las ventanas
        self.ventanas = {}

        #Bucle para crear las ventanas y almacenarlas en el diccionario
        for F in (main, selecAvt, selecPk, game, clasif):
            ventana = F(self.contenedor, self)
            self.ventanas[F] = ventana
            ventana.grid(row=0, column=0, sticky="nsew")
        
        # Configurar pesos para que el frame ocupe todo el espacio
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)
        
        #Mostrar la ventana inicial
        self.mostrar_ventana(main)

    def mostrar_ventana(self, ventana):

        """Función para mostrar una ventana, recibe como parámetro la clase de la ventana a mostrar, busca la ventana en el
        diccionario y la muestra utilizando tkraise()"""

        ventana = self.ventanas[ventana]
        ventana.tkraise()



#---------------------------------------------------------------------------------------

#                   VENTANA DE SELECCIÓN DE POKEMON

#---------------------------------------------------------------------------------------    



class main(tkinter.Frame):

    """Clase para la ventana principal de la aplicación, hereda de tkinter.Frame, se encarga de mostrar el título del juego,
    los botones para jugar y ver la clasificación, y el label inferior con los créditos."""

    def __init__(self, parent, controller):

        super().__init__(parent)

        #Imagenes utilizadas en el frame
        self.MainTitle = img("MainTitle.png", 800, 330)


        self.mainCont = tkinter.Label(self, bg="#C4EAFF", borderwidth=0)
        self.mainCont.pack(expand=True, fill="both") 
        self.mainCont.columnconfigure(0, weight=1)
        self.mainCont.rowconfigure(0, weight=1)
        self.mainCont.rowconfigure(1, weight=1)
        self.mainCont.rowconfigure(2, weight=1)
        self.mainCont.rowconfigure(3, minsize=100)

        self.C_Titulo = tkinter.Canvas(self.mainCont, bg="#C4EAFF", width=800, height=330, highlightthickness=0)
        self.C_Titulo.create_image(0, 0, anchor="nw", image=self.MainTitle)
        self.C_Titulo.grid(column=0, row=0, sticky="ns")

        self.B_BotonJugar = tkinter.Button(self.mainCont, text="¡Adelante!", bg="#54C3FF", fg="white", relief="flat", height=1, width=10, font=("", 50), padx=10, pady=10, cursor="hand2", command=lambda: controller.mostrar_ventana(selecAvt))
        self.B_BotonJugar.grid(column=0, row=1)

        self.B_BotonClasificacion = tkinter.Button(self.mainCont, text="Clasificación",  bg="#54C3FF", fg="white", relief="flat", height=1, width=10, font=("", 50), padx=10, pady=10, cursor="hand2", command=lambda: (controller.mostrar_ventana(clasif), registroClasificacion.leerClasificacion(controller.ventanas[clasif])))
        self.B_BotonClasificacion.grid(column=0, row=2)

        #Label inferior de la ventana principal
        self.L_LabelInferior = tkinter.Label(self.mainCont, bg="#fcef7d", borderwidth=0)
        self.L_LabelInferior.columnconfigure(0, weight=1)
        self.L_LabelInferior.columnconfigure(1, weight=1)
        self.L_LabelInferior.rowconfigure(0, weight=1)
        self.L_LabelInferior.grid(column=0, row=3, sticky="nswe")

        #Widgets dentro del label inferior
        self.L_Creditos = tkinter.Label(self.L_LabelInferior, text="Por: Jordanny Hernández", fg="white", font=("", 20), bg="#0059ff")
        self.L_Creditos.grid(column=0, row=0, sticky="nsw")



#---------------------------------------------------------------------------------------

#                   VENTANA DE SELECCIÓN DE AVATAR

#---------------------------------------------------------------------------------------

    

class selecAvt(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        #Imagenes utilizadas en el frame
        self.av0_Img = img("av0.png", 300, 300)
        self.av1_Img = img("av1.png", 300, 300)
        self.av2_Img = img("av2.png", 300, 300)
        self.av3_Img = img("av3.png", 300, 300)
        self.av4_Img = img("av4.png", 300, 300)

        self.mainCont = tkinter.Label(self, background="yellow", borderwidth=0)
        self.mainCont.pack(expand=True, fill="both")
        self.mainCont.columnconfigure(0, weight=1)
        self.mainCont.rowconfigure(0, minsize=100)
        self.mainCont.rowconfigure(1, weight=1)
        self.L_AvtCont = tkinter.Label(self.mainCont, bg="#8BC6FE", borderwidth=0)
        #self.L_AvtCont.pack_propagate(False)
        self.L_AvtCont.grid(column=0, row=0, sticky="nswe")

        #Botones de avatares
        self.B_Avt0 = tkinter.Button(self.L_AvtCont, text="AV0", bg="#fff79b", relief="flat", image=self.av0_Img, cursor="hand2", command=lambda: self.avatarSeleccionado("av0", self.av0_Img))
        self.B_Avt0.pack(side="left", fill="both", expand=True)
        self.B_Avt1 = tkinter.Button(self.L_AvtCont, text="AV1", bg="#75f5fe", relief="flat", image=self.av1_Img, cursor="hand2", command=lambda: self.avatarSeleccionado("av1", self.av1_Img))
        self.B_Avt1.pack(side="left", fill="both", expand=True)
        self.B_Avt2 = tkinter.Button(self.L_AvtCont, text="AV2", bg="#fccd81", relief="flat", image=self.av2_Img, cursor="hand2", command=lambda: self.avatarSeleccionado("av2", self.av2_Img))
        self.B_Avt2.pack(side="left", fill="both", expand=True)
        self.B_Avt3 = tkinter.Button(self.L_AvtCont, text="AV3", bg="#6efec0", relief="flat", image=self.av3_Img, cursor="hand2", command=lambda: self.avatarSeleccionado("av3", self.av3_Img))
        self.B_Avt3.pack(side="left", fill="both", expand=True)
        self.B_Avt4 = tkinter.Button(self.L_AvtCont, text="AV4", bg="#3e948f", relief="flat", image=self.av4_Img, cursor="hand2", command=lambda: self.avatarSeleccionado("av4", self.av4_Img))
        self.B_Avt4.pack(side="left", fill="both", expand=True)

        self.L_r1Cont = tkinter.Label(self.mainCont, bg="#554CFF", borderwidth=0)
        self.L_r1Cont.grid(column=0, row=1, sticky="nswe")

        self.C_AvtSeleccionado = tkinter.Canvas(self.L_r1Cont, width=300, height=300, bg="lightblue")
        self.C_AvtSeleccionado.pack(side="left", padx=20)

        self.L_NombreTitulo = tkinter.Label(self.L_r1Cont, text="Nombre del jugador", font=("", 20), fg="white", bg="#39BAFF")
        self.L_NombreTitulo.pack(anchor="center", side="left", padx=10, ipadx=10)

        self.E_NombreJugador = tkinter.Entry(self.L_r1Cont, width=20, font=("", 20))
        self.E_NombreJugador.pack(anchor= "center", side="left", padx=10)

        self.B_Volver = tkinter.Button(self.mainCont, text="Volver", font=("", 30), fg="white", bg="red", relief="flat", width=7, cursor="hand2", command=lambda: controller.mostrar_ventana(main))
        self.B_Volver.place(anchor="sw", rely=1, x=0, y=0)

        self.B_Siguiente = tkinter.Button(self.mainCont, text="Siguiente", font=("", 30), fg="white", bg="green", relief="flat", width=7, cursor="hand2", command=lambda: self.obtenerNombreJugador(self.E_NombreJugador, controller))
        self.B_Siguiente.place(anchor="se", relx=1, rely=1, x=0, y=0)

        

    def avatarSeleccionado(self, avt, img):

        """Función para seleccionar el avatar del jugador, recibe como parámetros el nombre del avatar seleccionado y la imagen
        del avatar seleccionado, asigna el avatar seleccionado al jugador y muestra la imagen del avatar seleccionado en el
        canvas correspondiente."""

        jugador.avatar = avt
        self.C_AvtSeleccionado.delete("all")
        self.C_AvtSeleccionado.create_image(0, 0, anchor="nw", image= img)

    def obtenerNombreJugador(self, event, controller):

        """Función para obtener el nombre del jugador, recibe como parámetros el campo de texto donde el jugador ingresa su
        nombre y el controlador para cambiar de ventana, asigna el nombre ingresado al jugador y cambia a la ventana de selección
        de Pokémon. Si el nombre ingresado contiene caracteres no válidos o está vacío, la función no hace nada."""

        unvalidChar = [" ", "-", "_", ".", ",", ";", ":", "!", "?", "/", "\\", "\"", "\'", "|", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "="]
        
        for char in unvalidChar:    #No hacer nada si el nombre contiene caracteres no válidos
            if char in event.get():
                return  

        if event.get() == "":  #No hacer nada si el campo de texto está vacío
            return 
        jugador.nombre = event.get()
        controller.mostrar_ventana(selecPk)  #Cambia a la ventana de selección de Pokémon



#---------------------------------------------------------------------------------------

#                   VENTANA DE SELECCIÓN DE POKEMON

#---------------------------------------------------------------------------------------



class selecPk(tkinter.Frame):

    """Clase para la ventana de selección de Pokémon, hereda de tkinter.Frame, se encarga de mostrar la lista de Pokémon disponibles para seleccionar"""

    def __init__(self, parent, controller):
        super().__init__(parent)

        #Las imagenes utilizadas se cargan al seleccionar el pokemon

        self.mainCont = tkinter.Label(self, background="#554CFF", borderwidth=0)
        self.mainCont.pack(expand=True, fill="both")

        #Contenedor para el equipo de pokemones
        self.L_ContPk0 = tkinter.Label(self.mainCont, bg="#ff7979", borderwidth=0, height=40)
        self.L_ContPk0.pack(side="left", fill="x", expand=True)
        self.L_ContPk0.pack_propagate(False)
        self.L_ContPk1 = tkinter.Label(self.mainCont, bg="#92ffaf", borderwidth=0, height=40)
        self.L_ContPk1.pack(side="left", fill="x", expand=True)
        self.L_ContPk1.pack_propagate(False)
        self.L_ContPk2 = tkinter.Label(self.mainCont, bg="#91fff9", borderwidth=0, height=40)
        self.L_ContPk2.pack(side="left", fill="x", expand=True)
        self.L_ContPk2.pack_propagate(False)
        

        self.C_Pk0 = tkinter.Canvas(self.L_ContPk0, width=300, height=300, bg="lightblue")
        self.C_Pk0.pack(side="top", pady=20)
        self.LB_Pk0 = tkinter.Listbox(self.L_ContPk0, height=5, listvariable=tkinter.StringVar(value=listaPokemones))
        self.LB_Pk0.bind("<<ListboxSelect>>", lambda event: self.pkSeleccionado(event, 0))
        self.LB_Pk0.pack(side="top", fill="x", padx=20)

        self.C_Pk1 = tkinter.Canvas(self.L_ContPk1, width=300, height=300, bg="lightblue")
        self.C_Pk1.pack(side="top", pady=20)
        self.LB_Pk1 = tkinter.Listbox(self.L_ContPk1, height=5, listvariable=tkinter.StringVar(value=listaPokemones))
        self.LB_Pk1.bind("<<ListboxSelect>>", lambda event: self.pkSeleccionado(event, 1))
        self.LB_Pk1.pack(side="top", fill="x", padx=20)

        self.C_Pk2 = tkinter.Canvas(self.L_ContPk2, width=300, height=300, bg="lightblue")
        self.C_Pk2.pack(side="top", pady=20)
        self.LB_Pk2 = tkinter.Listbox(self.L_ContPk2, height=5, listvariable=tkinter.StringVar(value=listaPokemones))
        self.LB_Pk2.bind("<<ListboxSelect>>", lambda event: self.pkSeleccionado(event, 2))
        self.LB_Pk2.pack(side="top", fill="x", padx=20)

        #Nombre del Pokemon seleccionado y sus stats

        self.L_ContNombreStatsPk0 = tkinter.Label(self.L_ContPk0, bg="red", borderwidth=0, height=8)
        self.L_ContNombreStatsPk0.pack(side="bottom", fill="x")
        self.L_ContNombreStatsPk0.pack_propagate(False)

        self.L_NombrePk0 = tkinter.Label(self.L_ContNombreStatsPk0, text="NOMBRE DE POKEMON", font=("", 15), height=2, bg="#f6ff47")
        self.L_NombrePk0.pack(side="top", fill="x")

        self.L_ContStatsPk0 = tkinter.Label(self.L_ContNombreStatsPk0, bg="lightgray", borderwidth=0)
        self.L_ContStatsPk0.pack(side="top", fill="both", expand=True)
        self.L_HPPk0 = tkinter.Label(self.L_ContStatsPk0, text="HP:0", font=("", 12), bg="lightblue")
        self.L_HPPk0.pack(side="left", expand=True)
        self.L_AttPk0 = tkinter.Label(self.L_ContStatsPk0, text="ATQ: 0", font=("", 12), bg="lightblue")
        self.L_AttPk0.pack(side="left", expand=True)
        self.L_DefPk0 = tkinter.Label(self.L_ContStatsPk0, text="DEF: 0", font=("", 12), bg="lightblue")
        self.L_DefPk0.pack(side="left", expand=True)



        self.L_ContNombreStatsPk1 = tkinter.Label(self.L_ContPk1, bg="red", borderwidth=0, height=8)
        self.L_ContNombreStatsPk1.pack(side="bottom", fill="x")
        self.L_ContNombreStatsPk1.pack_propagate(False)

        self.L_NombrePk1 = tkinter.Label(self.L_ContNombreStatsPk1, text="NOMBRE DE POKEMON", font=("", 15), height=2, bg="#f6ff47")
        self.L_NombrePk1.pack(side="top", fill="x")

        self.L_ContStatsPk1 = tkinter.Label(self.L_ContNombreStatsPk1, bg="lightgray", borderwidth=0)
        self.L_ContStatsPk1.pack(side="top", fill="both", expand=True)
        self.L_HPPk1 = tkinter.Label(self.L_ContStatsPk1, text="HP: 0", font=("", 12), bg="lightblue")
        self.L_HPPk1.pack(side="left", expand=True)
        self.L_AttPk1 = tkinter.Label(self.L_ContStatsPk1, text="ATQ: 0", font=("", 12), bg="lightblue")
        self.L_AttPk1.pack(side="left", expand=True)
        self.L_DefPk1 = tkinter.Label(self.L_ContStatsPk1, text="DEF: 0", font=("", 12), bg="lightblue")
        self.L_DefPk1.pack(side="left", expand=True)



        self.L_ContNombreStatsPk2 = tkinter.Label(self.L_ContPk2, bg="red", borderwidth=0, height=8)
        self.L_ContNombreStatsPk2.pack(side="bottom", fill="x")
        self.L_ContNombreStatsPk2.pack_propagate(False)

        self.L_NombrePk2 = tkinter.Label(self.L_ContNombreStatsPk2, text="NOMBRE DE POKEMON", font=("", 15), height=2, bg="#f6ff47")
        self.L_NombrePk2.pack(side="top", fill="x")

        self.L_ContStatsPk2 = tkinter.Label(self.L_ContNombreStatsPk2, bg="lightgray", borderwidth=0)
        self.L_ContStatsPk2.pack(side="top", fill="both", expand=True)
        self.L_HPPk2 = tkinter.Label(self.L_ContStatsPk2, text="HP: 100", font=("", 12), bg="lightblue")
        self.L_HPPk2.pack(side="left", expand=True)
        self.L_AttPk2 = tkinter.Label(self.L_ContStatsPk2, text="ATQ: 50", font=("", 12), bg="lightblue")
        self.L_AttPk2.pack(side="left", expand=True)
        self.L_DefPk2 = tkinter.Label(self.L_ContStatsPk2, text="DEF: 30", font=("", 12), bg="lightblue")
        self.L_DefPk2.pack(side="left", expand=True)



        self.B_Volver = tkinter.Button(self.mainCont, text="Volver", font=("", 30), fg="white", bg="red", relief="flat", width=7, cursor="hand2", command=lambda: controller.mostrar_ventana(selecAvt))
        self.B_Volver.place(anchor="sw", rely=1, x=0, y=0)

        self.B_Siguiente = tkinter.Button(self.mainCont, text="Siguiente", font=("", 30), fg="white", bg="green", relief="flat", width=7, cursor="hand2", command=lambda: self.iniciarPartida(controller))
        self.B_Siguiente.place(anchor="se", relx=1, rely=1, x=0, y=0)
    
    def pkSeleccionado(self, event, pkIndex):

        """Función para seleccionar el Pokémon del jugador, recibe como parámetros el evento de selección en la lista de Pokémon y el
        índice del Pokémon seleccionado (0, 1 o 2), asigna el Pokémon seleccionado al equipo del jugador dependiendo del índice y muestra
        la imagen y los stats del Pokémon seleccionado en el canvas y labels correspondientes."""

        seleccion = event.widget.get(event.widget.curselection())
        imagen = img(f"pk{listaPokemones.index(seleccion)}.png", 300, 300)
        
        if pkIndex == 0:
            self.L_NombrePk0.config(text=seleccion)
            self.L_HPPk0.config(text=f"HP: {pkDefaultStats[seleccion]['HP']}")
            self.L_AttPk0.config(text=f"ATQ: {pkDefaultStats[seleccion]['ATQ']}")
            self.L_DefPk0.config(text=f"DEF: {pkDefaultStats[seleccion]['DEF']}")
            
            self.img0 = imagen  # Mantener referencia persistente
            self.C_Pk0.delete("all")
            self.C_Pk0.create_image(0, 0, anchor="nw", image=self.img0)
        elif pkIndex == 1:
            self.L_NombrePk1.config(text=seleccion)
            self.L_HPPk1.config(text=f"HP: {pkDefaultStats[seleccion]['HP']}")
            self.L_AttPk1.config(text=f"ATQ: {pkDefaultStats[seleccion]['ATQ']}")
            self.L_DefPk1.config(text=f"DEF: {pkDefaultStats[seleccion]['DEF']}")
            
            self.img1 = imagen  # Mantener referencia persistente
            self.C_Pk1.delete("all")
            self.C_Pk1.create_image(0, 0, anchor="nw", image=self.img1)
        elif pkIndex == 2:
            self.L_NombrePk2.config(text=seleccion)
            self.L_HPPk2.config(text=f"HP: {pkDefaultStats[seleccion]['HP']}")
            self.L_AttPk2.config(text=f"ATQ: {pkDefaultStats[seleccion]['ATQ']}")
            self.L_DefPk2.config(text=f"DEF: {pkDefaultStats[seleccion]['DEF']}")
            
            self.img2 = imagen  # Mantener referencia persistente
            self.C_Pk2.delete("all")
            self.C_Pk2.create_image(0, 0, anchor="nw", image=self.img2)
    

    def iniciarPartida(self, controller):

        """Función para iniciar la partida, asigna el equipo seleccionado al jugador y al bot, reinicia los stats de los pokemones,
        actualiza los gráficos de la ventana de batalla y muestra la ventana de batalla. Si no se han seleccionado los pokemones o se
        han seleccionado pokemones repetidos, la función no hace nada."""

        # No iniciar la partida si no se han seleccionado los pokemones
        if (self.L_NombrePk0.cget("text") == "NOMBRE DE POKEMON" or
            self.L_NombrePk1.cget("text") == "NOMBRE DE POKEMON" or
            self.L_NombrePk2.cget("text") == "NOMBRE DE POKEMON"):
            return 
        
        # No iniciar la partida si se han seleccionado pokemones repetidos
        if (self.L_NombrePk0.cget("text") == self.L_NombrePk1.cget("text") or
            self.L_NombrePk0.cget("text") == self.L_NombrePk2.cget("text") or
            self.L_NombrePk1.cget("text") == self.L_NombrePk2.cget("text")):
            return  
        
        #Asignar el equipo seleccionado al jugador
        jugador.pk = [self.L_NombrePk0.cget("text"), self.L_NombrePk1.cget("text"), self.L_NombrePk2.cget("text")]
        jugador.currentPk = jugador.pk[0]
        jugador.puntos = 0

        #Asignar el equipo del bot aleatoriamente
        bot.nombre = bot.nombreBot(bot)
        bot.avatar = bot.avatarBot(bot)
        bot.pk = bot.equipoBot(bot)
        bot.currentPk = bot.pk[0]
        bot.puntos = 0

        global IsPlayerTurn
        IsPlayerTurn = True

        #Reiniciar diccionarios de stats para el nuevo juego
        global gameStats
        gameStats = deepcopy(pkDefaultStats)

        
        #Cambios gráficos para game
        game_frame = controller.ventanas[game]
        
        game_frame.C_PkJugador.delete("all")
        game_frame.C_PkBot.delete("all")

        self.jugadorAvtImg = img(f"{jugador.avatar}.png", 375, 375)
        game_frame.C_AvtJugador.create_image(0, 0, anchor="nw", image=self.jugadorAvtImg)

        self.jugadorPkImg = img(f"pk{listaPokemones.index(jugador.currentPk)}.png", 200, 200)
        game_frame.C_PkJugador.create_image(0, 0, anchor="nw", image=self.jugadorPkImg)

        self.botAvtImg = img(f"{bot.avatar}.png", 375, 375)
        game_frame.C_Bot.create_image(0, 0, anchor="nw", image=self.botAvtImg)

        self.botPkImg = img(f"pk{listaPokemones.index(bot.currentPk)}.png", 200, 200)
        game_frame.C_PkBot.create_image(0, 0, anchor="nw", image=self.botPkImg)

        game_frame.L_PkPlayerName.configure(text=f"{jugador.nombre}:   {jugador.currentPk}")
        game_frame.L_PkBotName.configure(text=f"{bot.nombre}:   {bot.currentPk}")

        #Stats del jugador
        game_frame.PcurrentPkHP.set(f"HP: {gameStats[jugador.currentPk]['HP']}")
        game_frame.PcurrentPkATQ.set(f"ATQ: {gameStats[jugador.currentPk]['ATQ']}")
        game_frame.PcurrentPkDEF.set(f"DEF: {gameStats[jugador.currentPk]['DEF']}")
        game_frame.PcurrentPkDEFEx.set(f"+DEF: {gameStats[jugador.currentPk]['DEFEX']}")
        #Stats del bot
        game_frame.BcurrentPkHP.set(f"HP: {gameStats[bot.currentPk]['HP']}")
        game_frame.BcurrentPkATQ.set(f"ATQ: {gameStats[bot.currentPk]['ATQ']}")
        game_frame.BcurrentPkDEF.set(f"DEF: {gameStats[bot.currentPk]['DEF']}")
        game_frame.BcurrentPkDEFEx.set(f"+DEF: {gameStats[bot.currentPk]['DEFEX']}")
        TESTFUNCTION()
        controller.mostrar_ventana(game)



#---------------------------------------------------------------------------------------

#                   VENTANA DE BATALLA

#---------------------------------------------------------------------------------------



class game(tkinter.Frame):

    """Clase para la ventana de batalla, hereda de tkinter.Frame, se encarga de mostrar la información de ambos jugadores, los pokemones actuales,
    sus stats, la información de las acciones realizadas y los puntos de cada jugador."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.PcurrentPkHP = tkinter.StringVar()
        self.PcurrentPkDEF = tkinter.StringVar()
        self.PcurrentPkATQ = tkinter.StringVar()
        self.PcurrentPkDEFEx = tkinter.StringVar()
        self.PcurrentPkHP.set("HP: 0")
        self.PcurrentPkDEF.set("DEF: 0")
        self.PcurrentPkATQ.set("ATQ: 0")
        self.PcurrentPkDEFEx.set("+DEF: 0")

        self.BcurrentPkHP = tkinter.StringVar()
        self.BcurrentPkDEF = tkinter.StringVar()
        self.BcurrentPkATQ = tkinter.StringVar()
        self.BcurrentPkDEFEx = tkinter.StringVar()
        self.BcurrentPkHP.set("HP: 0")
        self.BcurrentPkDEF.set("DEF: 0")
        self.BcurrentPkATQ.set("ATQ: 0")
        self.BcurrentPkDEFEx.set("+DEF: 0")

        self.puntosJugador = tkinter.StringVar()
        self.puntosBot = tkinter.StringVar()
        self.puntosJugador.set(f"PUNTOS: {jugador.puntos}")
        self.puntosBot.set(f"PUNTOS: {bot.puntos}")



        self.mainCont = tkinter.Label(self, background="#554CFF", borderwidth=0)
        self.mainCont.pack(expand=True, fill="both")

        #Información de ambos jugadores
        self.L_InfoBot = tkinter.Label(self.mainCont, width=80, bg="red", height=15, borderwidth=0)
        self.L_InfoBot.place(x=20, y=10)
        self.L_InfoBot.pack_propagate(False)

        self.L_InfoPlayer = tkinter.Label(self.mainCont, width=80, bg="green", height=15, borderwidth=0)
        self.L_InfoPlayer.place(anchor="se", relx=1, rely=1, x=-10, y=-20)
        self.L_InfoPlayer.pack_propagate(False)

        self.L_PkPlayerName = tkinter.Label(self.L_InfoPlayer, text="nombre", font=("", 15), height=2, bg="lightgray")
        self.L_PkPlayerName.pack(side="top", anchor="nw", fill="x")

        self.L_PkPlayerDescCont = tkinter.Label(self.L_InfoPlayer, bg="gray")
        self.L_PkPlayerDescCont.pack(side="bottom", anchor="nw", expand=True, fill="both")
        
        #Contenedor para stats actuales del jugador
        
        self.L_PkStatsCont = tkinter.Label(self.L_PkPlayerDescCont)
        self.L_PkStatsCont.pack(side="top", fill="x")

        #Labels de stats para el jugador
        self.L_PkPlayerHP = tkinter.Label(self.L_PkStatsCont, textvariable=self.PcurrentPkHP, font=("", 12), bg="lightblue")
        self.L_PkPlayerHP.pack(side="left", padx=5, expand=True)
        self.L_PkPlayerATQ = tkinter.Label(self.L_PkStatsCont, textvariable=self.PcurrentPkATQ, font=("", 12), bg="lightblue")
        self.L_PkPlayerATQ.pack(side="left", padx=5, expand=True)
        self.L_PkPlayerDEF = tkinter.Label(self.L_PkStatsCont, textvariable=self.PcurrentPkDEF, font=("", 12), bg="lightblue")
        self.L_PkPlayerDEF.pack(side="left", padx=5, expand=True)
        self.L_PkPlayerDEFEx = tkinter.Label(self.L_PkStatsCont, textvariable=self.PcurrentPkDEFEx, font=("", 12), bg="lightblue")
        self.L_PkPlayerDEFEx.pack(side="left", padx=5, expand=True)

        #Informacion de accion
        self.L_PlayerInfo = tkinter.Label(self.L_PkPlayerDescCont, bg="black", fg="white", font=("", 12))
        self.L_PlayerInfo.pack(side="top", fill="both", expand=True)

        self.L_PkBotName = tkinter.Label(self.L_InfoBot, text="nombre", font=("", 15), height=2, bg="lightgray")
        self.L_PkBotName.pack(side="top", fill="x")

        self.L_PkBotDescCont = tkinter.Label(self.L_InfoBot, bg="gray")
        self.L_PkBotDescCont.pack(side="top", expand=True, fill="both")

        #Contenedor para stats actuales del bot
        self.L_PkBotStatsCont = tkinter.Label(self.L_PkBotDescCont)
        self.L_PkBotStatsCont.pack(side="top", fill="x")

        #Labels de stats para el bot
        self.L_PkBotHP = tkinter.Label(self.L_PkBotStatsCont, textvariable=self.BcurrentPkHP, font=("", 12), bg="lightblue")
        self.L_PkBotHP.pack(side="left", padx=5, expand=True)
        self.L_PkBotATQ = tkinter.Label(self.L_PkBotStatsCont, textvariable=self.BcurrentPkATQ, font=("", 12), bg="lightblue")
        self.L_PkBotATQ.pack(side="left", padx=5, expand=True)
        self.L_PkBotDEF = tkinter.Label(self.L_PkBotStatsCont, textvariable=self.BcurrentPkDEF, font=("", 12), bg="lightblue")
        self.L_PkBotDEF.pack(side="left", padx=5, expand=True)
        self.L_PkBotDEFEx = tkinter.Label(self.L_PkBotStatsCont, textvariable=self.BcurrentPkDEFEx, font=("", 12), bg="lightblue")
        self.L_PkBotDEFEx.pack(side="left", padx=5, expand=True)

        #Informacion de accion
        self.L_BotInfo = tkinter.Label(self.L_PkBotDescCont, bg="black", fg="white", font=("", 12))
        self.L_BotInfo.pack(side="top", fill="both", expand=True)

        #Opciones del jugador
        self.L_ContOpciones = tkinter.Label(self.mainCont, width=100, bg="yellow", height=4)
        self.L_ContOpciones.place(anchor="sw", rely=1, x=0, y=0)
        self.L_ContOpciones.pack_propagate(False)

        self.B_Salir = tkinter.Button(self.L_ContOpciones, text="Salir", bg="red", width=8, font=("", 15), cursor="hand2", command=lambda: controller.mostrar_ventana(main))
        self.B_Salir.pack(side="right", fill="y")

        self.B_Cambiar = tkinter.Button(self.L_ContOpciones, text="Cambiar Ticomon", font=("", 15), bg="#ffcb46",cursor="hand2", command=lambda: turnoJugador("CH", controller))
        self.B_Cambiar.pack(side="right", expand=True, fill="both")

        self.B_Atacar = tkinter.Button(self.L_ContOpciones, text="ATACAR", font=("", 15), bg="#ff4e4e", cursor="hand2", command=lambda: turnoJugador("ATQ", controller))
        self.B_Atacar.pack(side="right", expand=True, fill="both")

        self.B_Defender = tkinter.Button(self.L_ContOpciones, text="DEFENDER", font=("", 15), bg="#97fff3", cursor="hand2", command=lambda: turnoJugador("DEF", controller))
        self.B_Defender.pack(side="right", expand=True, fill="both")

        self.B_Curar = tkinter.Button(self.L_ContOpciones, text="CURAR", font=("", 15), bg="#77ff87", cursor="hand2", command=lambda: turnoJugador("HP", controller))
        self.B_Curar.pack(side="right", expand=True, fill="both")

        self.L_PuntosJugador = tkinter.Label(self.L_ContOpciones, textvariable=self.puntosJugador, font=("", 15))
        self.L_PuntosJugador.pack(side="left", expand=True, fill="both")

        #Sprites de avatares y pokemones
        self.L_ContJugador = tkinter.Label(self.mainCont, width=105, height=25)
        self.L_ContJugador.place(anchor="sw", rely=1, x=10, y=-80)
        self.L_ContJugador.pack_propagate(False)

        self.L_ContBot = tkinter.Label(self.mainCont, width=105, height=25)
        self.L_ContBot.place(anchor="ne", relx=1, x=-10, y=80)
        self.L_ContBot.pack_propagate(False)

        self.L_PuntosBot = tkinter.Label(self.mainCont, width=12, height=2, textvariable=self.puntosBot, font=("", 15))
        self.L_PuntosBot.place(anchor="ne",relx=1, x=0, y=0)

        self.C_AvtJugador = tkinter.Canvas(self.L_ContJugador, width=375, bg="blue")
        self.C_AvtJugador.pack(side="left", fill="y")

        self.C_PkJugador = tkinter.Canvas(self.L_ContJugador, width=200, height= 200, bg="lightblue")
        self.C_PkJugador.pack(side="bottom")

        self.C_Bot = tkinter.Canvas(self.L_ContBot, width=375, bg="blue")
        self.C_Bot.pack(side="right", fill="y")

        self.C_PkBot = tkinter.Canvas(self.L_ContBot, width=200, height=200, bg="lightblue")
        self.C_PkBot.pack(side="bottom")



#---------------------------------------------------------------------------------------

#                   VENTANA DE CLASIFICACION

#---------------------------------------------------------------------------------------



class clasif(tkinter.Frame):

    """Clase para la ventana de clasificación, hereda de tkinter.Frame, se encarga de mostrar la tabla de clasificación con los 10
    mejores puntajes de los jugadores."""

    def __init__(self, parent, controller):
        super().__init__(parent)



        self.mainCont = tkinter.Label(self, background="lightgreen", borderwidth=0)
        self.mainCont.pack(expand=True, fill="both")

        #Tabla de clasificaciones
        self.L_TablaClasificacion = tkinter.Label(self.mainCont, width=100, height=45, bg="green")
        self.L_TablaClasificacion.place(relx=0.5, rely=0.5, anchor="center")
        self.L_TablaClasificacion.pack_propagate(False)

        self.L_Titulo = tkinter.Label(self.L_TablaClasificacion, text="Top 10 Mejores", font=("", 20))
        self.L_Titulo.pack(side="top", fill="x", pady=(0, 10))

        self.L_P0Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="1", font=("", 20), justify="left", padx=20, bg="yellow")
        self.L_P0Cont.pack(side="top", expand=True, fill="both")
        self.C_P0AvImg = tkinter.Canvas(self.L_P0Cont, width=50, height=50, bg="lightblue")
        self.C_P0AvImg.pack(side="left", padx=10)
        self.L_P0Name = tkinter.Label(self.L_P0Cont, text="----", font=("", 20), bg="yellow")
        self.L_P0Name.pack(side="left", padx=10)
        self.L_P0Points = tkinter.Label(self.L_P0Cont, text="--", font=("", 20), bg="yellow")
        self.L_P0Points.pack(side="right", padx=10)

        self.L_P1Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="2", font=("", 20), justify="left", padx=20, bg="blue")
        self.L_P1Cont.pack(side="top", expand=True, fill="both")
        self.C_P1AvImg = tkinter.Canvas(self.L_P1Cont, width=50, height=50, bg="lightblue")
        self.C_P1AvImg.pack(side="left", padx=10)
        self.L_P1Name = tkinter.Label(self.L_P1Cont, text="----", font=("", 20), bg="blue", fg="white")
        self.L_P1Name.pack(side="left", padx=10)
        self.L_P1Points = tkinter.Label(self.L_P1Cont, text="--", font=("", 20), bg="blue", fg="white")
        self.L_P1Points.pack(side="right", padx=10)

        self.L_P2Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="3", font=("", 20), justify="left", padx=20, bg="yellow")
        self.L_P2Cont.pack(side="top", expand=True, fill="both")
        self.C_P2AvImg = tkinter.Canvas(self.L_P2Cont, width=50, height=50, bg="lightblue")
        self.C_P2AvImg.pack(side="left", padx=10)
        self.L_P2Name = tkinter.Label(self.L_P2Cont, text="----", font=("", 20), bg="yellow")
        self.L_P2Name.pack(side="left", padx=10)
        self.L_P2Points = tkinter.Label(self.L_P2Cont, text="--", font=("", 20), bg="yellow")
        self.L_P2Points.pack(side="right", padx=10)

        self.L_P3Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="4", font=("", 20), justify="left", padx=20, bg="blue")
        self.L_P3Cont.pack(side="top", expand=True, fill="both")
        self.C_P3AvImg = tkinter.Canvas(self.L_P3Cont, width=50, height=50, bg="lightblue")
        self.C_P3AvImg.pack(side="left", padx=10)
        self.L_P3Name = tkinter.Label(self.L_P3Cont, text="----", font=("", 20), bg="blue", fg="white")
        self.L_P3Name.pack(side="left", padx=10)
        self.L_P3Points = tkinter.Label(self.L_P3Cont, text="--", font=("", 20), bg="blue", fg="white")
        self.L_P3Points.pack(side="right", padx=10)

        self.L_P4Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="5", font=("", 20), justify="left", padx=20, bg="yellow")
        self.L_P4Cont.pack(side="top", expand=True, fill="both")
        self.C_P4AvImg = tkinter.Canvas(self.L_P4Cont, width=50, height=50, bg="lightblue")
        self.C_P4AvImg.pack(side="left", padx=10)
        self.L_P4Name = tkinter.Label(self.L_P4Cont, text="----", font=("", 20), bg="yellow")
        self.L_P4Name.pack(side="left", padx=10)
        self.L_P4Points = tkinter.Label(self.L_P4Cont, text="--", font=("", 20), bg="yellow")
        self.L_P4Points.pack(side="right", padx=10)

        self.L_P5Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="6", font=("", 20), justify="left", padx=20, bg="blue")
        self.L_P5Cont.pack(side="top", expand=True, fill="both")
        self.C_P5AvImg = tkinter.Canvas(self.L_P5Cont, width=50, height=50, bg="lightblue")
        self.C_P5AvImg.pack(side="left", padx=10)
        self.L_P5Name = tkinter.Label(self.L_P5Cont, text="----", font=("", 20), bg="blue", fg="white")
        self.L_P5Name.pack(side="left", padx=10)
        self.L_P5Points = tkinter.Label(self.L_P5Cont, text="--", font=("", 20), bg="blue", fg="white")
        self.L_P5Points.pack(side="right", padx=10)

        self.L_P6Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="7", font=("", 20), justify="left", padx=20, bg="yellow")
        self.L_P6Cont.pack(side="top", expand=True, fill="both")
        self.C_P6AvImg = tkinter.Canvas(self.L_P6Cont, width=50, height=50, bg="lightblue")
        self.C_P6AvImg.pack(side="left", padx=10)
        self.L_P6Name = tkinter.Label(self.L_P6Cont, text="----", font=("", 20), bg="yellow")
        self.L_P6Name.pack(side="left", padx=10)
        self.L_P6Points = tkinter.Label(self.L_P6Cont, text="--", font=("", 20), bg="yellow")
        self.L_P6Points.pack(side="right", padx=10)

        self.L_P7Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="8", font=("", 20), justify="left", padx=20, bg="blue")
        self.L_P7Cont.pack(side="top", expand=True, fill="both")
        self.C_P7AvImg = tkinter.Canvas(self.L_P7Cont, width=50, height=50, bg="lightblue")
        self.C_P7AvImg.pack(side="left", padx=10)
        self.L_P7Name = tkinter.Label(self.L_P7Cont, text="----", font=("", 20), bg="blue", fg="white")
        self.L_P7Name.pack(side="left", padx=10)
        self.L_P7Points = tkinter.Label(self.L_P7Cont, text="--", font=("", 20), bg="blue", fg="white")
        self.L_P7Points.pack(side="right", padx=10)

        self.L_P8Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="9", font=("", 20), justify="left", padx=20, bg="yellow")
        self.L_P8Cont.pack(side="top", expand=True, fill="both")
        self.C_P8AvImg = tkinter.Canvas(self.L_P8Cont, width=50, height=50, bg="lightblue")
        self.C_P8AvImg.pack(side="left", padx=10)
        self.L_P8Name = tkinter.Label(self.L_P8Cont, text="----", font=("", 20), bg="yellow")
        self.L_P8Name.pack(side="left", padx=10)
        self.L_P8Points = tkinter.Label(self.L_P8Cont, text="--", font=("", 20), bg="yellow")
        self.L_P8Points.pack(side="right", padx=10)

        self.L_P9Cont = tkinter.Label(self.L_TablaClasificacion, anchor="w", text="10", font=("", 20), justify="left", padx=20, bg="blue")
        self.L_P9Cont.pack(side="top", expand=True, fill="both")
        self.C_P9AvImg = tkinter.Canvas(self.L_P9Cont, width=50, height=50, bg="lightblue")
        self.C_P9AvImg.pack(side="left", padx=10)
        self.L_P9Name = tkinter.Label(self.L_P9Cont, text="----", font=("", 20), bg="blue", fg="white")
        self.L_P9Name.pack(side="left", padx=10)
        self.L_P9Points = tkinter.Label(self.L_P9Cont, text="--", font=("", 20), bg="blue", fg="white")
        self.L_P9Points.pack(side="right", padx=10)

        #Esta lista 
        self.listaPuestos = [(self.C_P0AvImg, self.L_P0Name, self.L_P0Points), (self.C_P1AvImg, self.L_P1Name, self.L_P1Points), (self.C_P2AvImg, self.L_P2Name, self.L_P2Points), (self.C_P3AvImg, self.L_P3Name, self.L_P3Points), (self.C_P4AvImg, self.L_P4Name, self.L_P4Points), (self.C_P5AvImg, self.L_P5Name, self.L_P5Points), (self.C_P6AvImg, self.L_P6Name, self.L_P6Points), (self.C_P7AvImg, self.L_P7Name, self.L_P7Points), (self.C_P8AvImg, self.L_P8Name, self.L_P8Points), (self.C_P9AvImg, self.L_P9Name, self.L_P9Points)]

        self.B_Volver = tkinter.Button(self.mainCont, text="Volver", font=("", 30), bg="red", width=7, height=2, relief="flat", cursor="hand2", command=lambda: controller.mostrar_ventana(main))
        self.B_Volver.place(anchor="sw",rely=1, x=0, y=0)

#Ejecutar la aplicación
if __name__ == "__main__":
    root().mainloop()

