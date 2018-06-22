import random

class Carta(object):
    def __init__(self, valor, naipe):
        self.naipe = naipe
        self.valor = valor
        if (valor > 1 and valor < 11):
            self.valor_str = str(valor)
        elif (valor == 1):
            self.valor_str = "As"
        elif (valor == 11):
            self.valor_str = "Valete"
        elif (valor == 12):
            self.valor_str = "Dama"
        elif (valor == 13):
            self.valor_str = "Rei"
        if (naipe == "o"):
            self.naipe_str = "Ouros"
        if (naipe == "e"):
            self.naipe_str = "Espadas"
        if (naipe == "c"):
            self.naipe_str = "Copas"
        if (naipe == "p"):
            self.naipe_str = "Paus"

    def __eq__(self, other):
        return (self.valor == other.valor) and (self.naipe == other.naipe)

    def print(self):
        print("{} de {}".format(self.valor_str, self.naipe_str))


class Baralho(object):
    def __init__(self):
        self.cartas = []
        self.construir()

    def construir(self):
        for np in ["o", "e", "c", "p"]:
            for val in range(1,14):
                self.cartas.append(Carta(val, np))

    def print(self):
        for c in self.cartas:
            c.print()

    def embaralhar(self):
        for i in range(len(self.cartas)-1, 0, -1):
            rand = random.randint(0, i)
            self.cartas[i], self.cartas[rand] = self.cartas[rand], self.cartas[i]

    def tirar_topo(self):
        return self.cartas.pop()


class Jogador(object):
    def __init__(self,nome):
        self.nome = nome
        self.mao = []

    def sacar_topo(self, baralho):
        self.mao.append(baralho.tirar_topo())

    def print_mao(self):
        for carta in self.mao:
            carta.print()

    def descartar(self, index):
        return self.mao.pop(index)

    def descartar_carta(self, val, np):
        descarte = Carta(val, np)
        for i in range(0, len(self.mao)):
            if self.mao[i] == descarte:
                return self.mao.pop(i)
        return self.mao