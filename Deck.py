import random

"""
Esqueleto para documentação de classes:

Classe(vars)
Descrição:
Campos:
Métodos:

"""



class Carta(object):
    """
    Classe Carta(valor, naipe)
    Descrição:
        Uma carta qualquer, com um valor e um naipe.
    Campos:
        self.naipe - Naipe da carta. Pertence ao conjunto {"o", "e", "c", "p"}, que significam Ouro, Espadas, Copas e
            Paus, respectivamente.

        self. valor - Valor numérico da carta, inteiro entre 1 e 13. 1 é Ás, 11, 12 e 13 são Valete, Dama e Rei,
            respectivamente.

        self.naipe_str e self.valor_str - Strings do valor e naipe, para impressão simplificada da carta.
    Métodos:
        print() - imprime o valor e naipe da carta de maneira simplificada (valor-naipe).

    """
    def __init__(self, valor, naipe):
        self.naipe = naipe
        self.valor = valor
        if (valor > 1 and valor < 11):
            self.valor_str = str(valor)
        elif (valor == 1):
            self.valor_str = "A"
        elif (valor == 11):
            self.valor_str = "J"
        elif (valor == 12):
            self.valor_str = "Q"
        elif (valor == 13):
            self.valor_str = "K"
        if (naipe == "o"):
            self.naipe_str = "♦"
        if (naipe == "e"):
            self.naipe_str = "♠"
        if (naipe == "c"):
            self.naipe_str = "♥"
        if (naipe == "p"):
            self.naipe_str = "♣"

    def __eq__(self, other):
        return (self.valor == other.valor) and (self.naipe == other.naipe)

    def __str__(self):
        return "{}{}".format(self.valor_str, self.naipe_str)

    def print(self):
        print("[{}{}] ".format(self.valor_str, self.naipe_str), end="", flush=True)


class Monte(object):
    """
    Classe Monte()
    Descrição: Um monte onde se pode inserir cartas, iniciado vazio.
    Campos:
        cartas [] - lista de cartas presentes no monte
    Métodos:

    """

    def __init__(self):
        self.cartas = []

    def __len__(self):
        return len(self.cartas)

    def print(self):
        for c in self.cartas:
            c.print()

    def embaralhar(self):
        for i in range(len(self.cartas)-1, 0, -1):
            rand = random.randint(0, i)
            self.cartas[i], self.cartas[rand] = self.cartas[rand], self.cartas[i]

    def tirar_topo(self):
        try:
            return self.cartas.pop()
        except IndexError:
            print("IndexError: Impossível tirar carta de monte vazio.")

    def tirar_random(self):
        if len(self.cartas) > 0:
            rand = random.randint(0, len(self.cartas))
            return self.cartas.pop(rand)
        else:
            raise IndexError("IndexError: Impossível tirar carta de monte vazio.")

    def inserir_topo(self, carta):
        self.cartas.append(carta)
        return len(self.cartas)

    def inserir_baixo(self, carta):
        self.cartas.insert(0, carta)
        return len(self.cartas)


class Baralho(Monte):
    """
    Classe Baralho() - Extende a classe Monte()
    Descrição: Um baralho de cartas, iniciado em 52 cartas padrão.
    Campos:
    Métodos:

    """

    def __init__(self):
        self.cartas = []
        self.construir()

    def construir(self):
        for np in ["o", "e", "c", "p"]:
            for val in range(1,14):
                self.cartas.append(Carta(val, np))


class Jogador(object):
    """
    Classe Jogador(nome)
    Descrição: Jogador em um jogo de cartas, possui um nome.
    Campos:
    Métodos:

    """

    def __init__(self,nome):
        self.nome = nome
        self.mao = []

    def __str__(self):
        return self.nome

    def sacar_topo(self, baralho):
        self.mao.append(baralho.tirar_topo())

    def print_mao(self):
        for carta in self.mao:
            carta.print()

    def descartar(self, index):
        try:
            return self.mao.pop(index)
        except:
            print("IndexError: Impossível tirar carta de mão vazia.")

    def descartar_carta(self, val, np):
        descarte = Carta(val, np)
        for i in range(0, len(self.mao)):
            if self.mao[i] == descarte:
                return self.mao.pop(i)
        return self.mao

    def qtd_cartas(self):
        return len(self.mao)

    def inserir_carta(self, carta):
        self.mao.append(carta)


class Mesa(object):
    """
    Classe Mesa(jogadores)
    Descrição: Estado atual da mesa de jogo. Possui jogadores e um baralho.
    Campos:
    Métodos:

    """
    def __init__(self, nomes_jogadores):
        self.jogadores = [Jogador(nome) for nome in nomes_jogadores]
        self.baralho = Baralho()
        self.montes = []

    def dar_cartas_inicio(self, num):
        self.baralho.embaralhar()
        for i in range(num):
            for player in self.jogadores:
                try:
                    player.sacar_topo(self.baralho)
                except IndexError:
                    print("Erro ao tentar sacar carta ao distribuir cartas, baralho vazio")

    def criar_monte(self):
        self.montes.append(Monte())
        return self
