import os
from Deck import *


class BJGame(object):

    def __init__(self):
        self.mesa = Mesa(["Jogador", "Casa"])
        self.rodadas = 0
        self.score = 100
        self.pot = 0
        self.winner = 0
        self.hidden = True # Carta da casa está oculta?
        self.fim, self.stand, self.bust = False, False, False
        """ 
            fim = jogador optou por terminar o jogo
            stand = jogador optou por jogar
            bust = jogador/mesa estourou 21
        """


    def jogar(self):

        while not self.fim:
            self.rodadas += 1

            self.play_rodada()      # joga uma rodada

            self.quit()             # jogador escolhe jogar novamente/sair (perda automática caso score < 10)

    def play_rodada(self):

        self.bet(10)     # aposta inicial (10)

        self.deal_inicio()  # dá duas cartas para a casa e para o jogador
        while True:
            try:
                aposta = input("Digite o quanto quer apostar: ")
                self.bet(int(aposta))          # jogador escolhe a aposta
            except:
                continue
            else:
                break

        while not self.stand and not self.bust:       # enquanto o jogador quiser ou não estourar
            self.player_action()                      # ele toma ações (hit ou stand)

        if not self.bust:
            self.dealer_action()        # dealer hit/stand

        if not self.bust:
            self.cards_compare()        # compara cartas
            self.score()                # dá/tira pontos do jogador (1:1 vitoria normal, 3:2 blackjack)

        self.reset_mesa()               # reseta estados

    def reset_mesa(self):
        self.stand, self.bust = False
        self.winner = 0
        self.pot = 0
        self.hidden = True

    def bet(self, bet):
        if self.score > bet:
            self.score -= bet
            self.pot += bet
        else:
            print('Aposta inválida - sem dinheiro suficiente')
            raise ValueError

    def deal_inicio(self):
        self.mesa.dar_cartas_inicio(2)
        self.print_status()

    def print_status(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_underline(">> CASA:", '-')
        if self.hidden:
            print("Cartas: [{}] - [OCULTA]".format(str(self.mesa.jogadores[1].mao[0])), end="", flush=True)
        else:
            print("Cartas: ")
            self.mesa.jogadores[1].print_mao()
        print("\nPontos: {}".format(self.pontos(self.mesa.jogadores[1])))

        print_underline(">> JOGADOR:", '-')
        print("Cartas: ", end="", flush=True)
        self.mesa.jogadores[0].print_mao()
        print("\nPontos: {}\n".format(self.pontos(self.mesa.jogadores[0])))

    def pontos(self, jogador):
        return 0

def print_underline(string, line):
    print('\n{}\n{}'.format(string, line * len(string)))

def main():

    bjgame = BJGame()
    bjgame.jogar()

if __name__ == '__main__':
    main()