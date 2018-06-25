from Deck import *


class BJGame(object):

    def __init__(self):
        self.mesa = Mesa(["Jogador", "Casa"])
        self.rodadas = 0
        self.score = 100
        self.pot = 0
        self.winner = 0

        self.fim, self.stand, self.bust = False
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

        self.blind_bet()     # aposta inicial (10)

        self.deal_inicio()  # dá duas cartas para a casa e para o jogador
        self.bet()          # jogador escolhe a aposta

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

