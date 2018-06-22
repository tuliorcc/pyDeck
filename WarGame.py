import argparse

from Deck import *

class WarGame(object):
    """
    WarGame(mesa)
    Descrição:
    Campos:
    Métodos:
    """

    def __init__(self, mesa):
        self.mesa = mesa
        self.rodadas = 0
        self.batalha = []

        #configuração da mesa
        self.mesa.dar_cartas_inicio(26)
        self.mesa.criar_monte()         # Cria monte war

    def jogar(self, limite):
        while not self.fim and self.rodadas < limite:
            self.rodadas += 1
            # print_underline('Jogando rodada {}'.format(self.rodadas), '=')
            self.play_rodada()
            """print("Fim da rodada.\nCartas: {}: {} | {}: {}".format(str(self.mesa.jogadores[0]),\
                                                                     self.mesa.jogadores[0].qtd_cartas(),\
                                                                     str(self.mesa.jogadores[1]), \
                                                                     self.mesa.jogadores[1].qtd_cartas()))"""

        print_underline('FIM DE SIMULAÇÃO!', '=')
        print("Resultados:\n"
              "Rodadas jogadas: {}\n"
              "Cartas: {}: {}  x  {}: {}\n"
              "Restante no monte: {}".format(self.rodadas,
                                                 str(self.mesa.jogadores[0]),
                                                 self.mesa.jogadores[0].qtd_cartas(),
                                                 str(self.mesa.jogadores[1]),
                                                 self.mesa.jogadores[1].qtd_cartas(),
                                                 len(self.mesa.montes[0])))

        vencedor = str(self.calc_vencedor())
        print("Vencedor: {}".format(vencedor))

    def play_rodada(self):
        self.descartar_mao_battle()     # Manda topo da mão para o monte battle
        if not self.fim:
            self.battle()                   # Roda a batalha
        else:
            self.batalha_to_war()

    def descartar_mao_battle(self):
        for jogador in self.mesa.jogadores:
            self.batalha.append(jogador.descartar(0))     # Manda topo da mão para battle

    def battle(self):
        carta1 = self.batalha[0]
        carta2 = self.batalha[1]
        self.batalha_to_war()      # manda cartas da batalha para monte
        #print("Batalha: {} vs {}".format(str(carta1), str(carta2)))

        if carta1.valor == carta2.valor:        # caso empate
            # print("War!")
            if not self.fim:                       # caso ainda tenham cartas
                self.mao_to_war()                       # descarta mao > war
                self.play_rodada()

        elif carta1.valor > carta2.valor:    # caso jogador 1 ganhe
            # print("{} venceu a rodada!".format(self.mesa.jogadores[0]))
            self.win_rodada(self.mesa.jogadores[0])

        else:                               # caso jogador 2 ganhe
            # print("{} venceu a rodada!".format(self.mesa.jogadores[1]))
            self.win_rodada(self.mesa.jogadores[1])

    def mao_to_war(self):
        for jogador in self.mesa.jogadores:
            self.mesa.montes[0].inserir_topo(jogador.descartar(0)) # descarta 1 carta de cada jogador p/ war

    def batalha_to_war(self):
        for i in range(len(self.batalha)):
            self.mesa.montes[0].inserir_topo(self.batalha.pop(0)) # dá pop 2 vezes em batalha e envia para o monte war

    def win_rodada(self, jogador):
        for i in range(len(self.mesa.montes[0])):                     # para cada carta no monte war
            jogador.inserir_carta(self.mesa.montes[0].tirar_topo())   # inserir carta no fundo da mão

    def calc_vencedor(self):
        if self.mesa.jogadores[0].qtd_cartas() > self.mesa.jogadores[1].qtd_cartas():
            return str(self.mesa.jogadores[0])
        elif self.mesa.jogadores[0].qtd_cartas() < self.mesa.jogadores[1].qtd_cartas():
            return str(self.mesa.jogadores[1])
        else:
            return "Empate"

    @property
    def fim(self):
        return sum(bool(jogador.mao) for jogador in self.mesa.jogadores) == 1


def main():
    parser = argparse.ArgumentParser(description='Esse programa simula um jogo de War')
    parser.add_argument('-r', '--rodadas', help='Rodadas para se simular', default=100, type=int, required=False)
    args = parser.parse_args()

    # Inicia a mesa com 2 jogadores
    mesa = Mesa(["Bob", "Patrick"])

    wargame = WarGame(mesa)
    wargame.jogar(args.rodadas)


def print_underline(string, line):
    print('\n{}\n{}'.format(string, line * len(string)))


if __name__ == '__main__':
    main()