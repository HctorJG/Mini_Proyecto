import random


class Carta(object):
    def __init__(self, nombre, valor, palo, simbolo):
        self.valor = valor
        self.palo = palo
        self.nombre = nombre
        self.simbolo = simbolo
        self.showing = False

    def __repr__(self):
        if self.showing:
            return self.simbolo
        else:
            return "Carta"


class Mazo(object):
    def shuffle(self, times=1):
        random.shuffle(self.cartas)
        print("Mazo barajeado")

    def deal(self):
        return self.cartas.pop(0)


class Baraja_Estandar(Mazo):
    def __init__(self):
        self.cartas = []
        palos = {"Corazones": "♡", "Picas": "♠", "Diamantes": "♢", "Treboles": "♣"}
        valores = {"Dos": 2,
                  "Tres": 3,
                  "Cuatro": 4,
                  "Cinco": 5,
                  "Seis": 6,
                  "Siete": 7,
                  "Ocho": 8,
                  "Nueve": 9,
                  "Diez": 10,
                  "Valet": 11,
                  "Dama": 12,
                  "Rey": 13,
                  "Az": 14}

        for nombre in valores:
            for palo in palos:
                icono = palos[palo]
                if valores[nombre] < 11:
                    simbolo = str(valores[nombre]) + icono
                else:
                    simbolo = nombre[0] + icono
                self.cartas.append(Carta(nombre, valores[nombre], palo, simbolo))

    def __repr__(self):
        return "Baraja:{0} restantes".format(len(self.cartas))


class Jugador(object):
    def __init__(self):
        self.cartas = []

    def cardCount(self):
        return len(self.cartas)

    def addCarta(self, carta):
        self.cartas.append(carta)


class Puntuacion(object):
    def __init__(self, cartas):
        # Numero de cartas
        if not len(cartas) == 5:
            return "Error: Cantidad incorrecta de cartas"

        self.cartas = cartas

    def flush(self):
        palos = [carta.palo for carta in self.cartas]
        if len(set(palos)) == 1:
            return True
        return False

    def straight(self):
        valores = [carta.valor for carta in self.cartas]
        valores.sort()

        if not len(set(valores)) == 5:
            return False

        if valores[4] == 14 and valores[0] == 2 and valores[1] == 3 and valores[2] == 4 and valores[3] == 5:
            return 5

        else:
            if not valores[0] + 1 == valores[1]: return False
            if not valores[1] + 1 == valores[2]: return False
            if not valores[2] + 1 == valores[3]: return False
            if not valores[3] + 1 == valores[4]: return False

        return valores[4]

    def highCard(self):
        values = [carta.valor for carta in self.cartas]
        highCard = None
        for carta in self.cartas:
            if highCard is None:
                highCard = carta
            elif highCard.valor < carta.valor:
                highCard = carta

        return highCard

    def highestCount(self):
        count = 0
        valores = [carta.valor for carta in self.cartas]
        for valor in valores:
            if valores.count(valor) > count:
                count = valores.count(valor)

        return count

    def pairs(self):
        pairs = []
        valores = [carta.valor for carta in self.cartas]
        for valor in valores:
            if valores.count(valor) == 2 and valor not in pairs:
                pairs.append(valor)

        return pairs

    def fourKind(self):
        valores = [carta.valor for carta in self.cartas]
        for valor in valores:
            if valores.count(valor) == 4:
                return True

    def fullHouse(self):
        two = False
        three = False

        valores = [carta.valor for carta in self.cartas]
        if valores.count(valores) == 2:
            two = True
        elif valores.count(valores) == 3:
            three = True

        if two and three:
            return True

        return False


def Juego():
    jugador = Jugador()

    # Intial Amount
    points = 100

    # Cost per hand
    handCost = 5

    end = False
    while not end:
        print("Usted tiene {0} puntos".format(points))
        print()

        points -= 5

        ## Hand Loop
        mazo = Baraja_Estandar()
        mazo.shuffle()

        # Deal Out
        for i in range(5):
            jugador.addCarta(mazo.deal())

        # Make them visible
        for carta in jugador.cartas:
            carta.showing = True
        print(jugador.cartas)

        validInput = False
        while not validInput:
            print("Que cartas deseas descartar de tu mano? ( ie. 1, 2, 3 )")
            print("*Escribe 'salir' para finalizar el juego")
            inputStr = input()

            if inputStr == "salir":
                end = True
                break

            try:
                inputList = [int(inp.strip()) for inp in inputStr.split(",") if inp]

                for inp in inputList:
                    if inp > 6:
                        continue
                    if inp < 1:
                        continue

                for inp in inputList:
                    jugador.cartas[inp - 1] = mazo.deal()
                    jugador.cartas[inp - 1].showing = True

                validInput = True
            except:
                print("Input Error: use comas para separar las cartas que desee descartar")

        print(jugador.cartas)
        # Score
        score = Puntuacion(jugador.cartas)
        straight = score.straight()
        flush = score.flush()
        highestCount = score.highestCount()
        pairs = score.pairs()

        # Royal flush
        if straight and flush and straight == 14:
            print("Flor Imperial!!!")
            print("+2000")
            points += 2000

        # Straight flush
        elif straight and flush:
            print("Escalera de color!")
            print("+250")
            points += 250

        # 4 of a kind
        elif score.fourKind():
            print("Poquer!")
            print("+125")
            points += 125

        # Full House
        elif score.fullHouse():
            print("Full!")
            print("+40")
            points += 40

        # Flush
        elif flush:
            print("Color!")
            print("+25")
            points += 25

        # Straight
        elif straight:
            print("Escalera!")
            print("+20")
            points += 20

        # 3 of a kind
        elif highestCount == 3:
            print("Tercia!")
            print("+15")
            points += 15

        # 2 pair
        elif len(pairs) == 2:
            print("Dos pares!")
            print("+10")
            points += 10

        # Jacks or better
        elif pairs and pairs[0] > 10:
            print("Par!")
            print("+5")
            points += 5

        jugador.cartas = []

        print()
        print()
        print()


Juego()




