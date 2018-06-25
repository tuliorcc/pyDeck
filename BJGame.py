import os
from Deck import *


class BJGame(object):

    def __init__(self):
        self.mesa = Mesa(["Jogador", "Casa"])
        self.rodadas = 0
        self.score = 100
        self.pot = 0
        self.winner, self.tie = False, False  # Jogador ganhou? Empatou?
        self.hidden = True  # Carta da casa está oculta?
        self.fim, self.stand, self.bust, self.vinteum = False, False, False, False
        """ 
            fim = jogador optou por terminar o jogo
            stand = jogador optou por jogar
            bust = jogador/mesa estourou 21
            vinteum = jogador conseuiu um blackjack
        """


    def jogar(self):

        while not self.fim:
            self.rodadas += 1

            self.play_rodada()      # joga uma rodada
            input("\nPressione Enter para continuar..")
            self.quit()             # jogador escolhe jogar novamente/sair (perda automática caso score < 10)

    def play_rodada(self):

        self.bet(10)     # aposta inicial (10)

        # Dá as cartas iniciais
        self.mesa.dar_cartas_inicio(2)
        self.print_status()

        while not self.stand and not self.bust and not self.vinteum:       # enquanto o jogador quiser ou não estourar
            self.player_action()                      # ele toma ações (hit ou stand)

        if not self.bust:
            self.dealer_action()        # dealer hit/stand

        if not self.bust:               # se nenhum dos dois der bust
            self.hidden = False
            self.cards_compare()        # compara cartas

        self.reset_mesa()               # reseta estados

    # Reinicia variáveis
    def reset_mesa(self):
        self.pot = 0
        self.hidden = True
        self.tie, self.vinteum, self.winner, self.stand, self.bust = False, False, False, False, False

        for carta in range(self.mesa.jogadores[0].qtd_cartas()):
            self.mesa.baralho.inserir_topo(self.mesa.jogadores[0].descartar(0))
        for carta in range(self.mesa.jogadores[1].qtd_cartas()):
            self.mesa.baralho.inserir_topo(self.mesa.jogadores[1].descartar(0))

    # Aposta
    def bet(self, bet):
        if self.score > bet:
            self.score -= bet
            self.pot += bet
        else:
            print('Aposta inválida - sem dinheiro suficiente')
            raise ValueError

    # Imprime o status do jogo (cartas e pontos)
    def print_status(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print_underline(">> CASA:", '-')
        if self.hidden:
            print("Cartas: [{}] - [OCULTA]".format(str(self.mesa.jogadores[1].mao[0])), end="", flush=True)
        else:
            print("Cartas: ")
            self.mesa.jogadores[1].print_mao()
            print("\nPontos: {}".format(self.pontos(self.mesa.jogadores[1])))

        print_underline("\n>> JOGADOR:", '-')
        print("Cartas: ", end="", flush=True)
        self.mesa.jogadores[0].print_mao()
        print("\nPontos: {}".format(self.pontos(self.mesa.jogadores[0])))
        print("\nSCORE: {}   Aposta atual: {}".format(self.score, self.pot))

    # calcula e retorna a quantidade de pontos de um jogador
    def pontos(self, jogador):
        pontos = 0
        num_ases = 0
        for carta in jogador.mao:
            if carta.valor == 1:
                num_ases += 1
        # calcula pontuação soft
        for carta in jogador.mao:
            if 1 < carta.valor < 11:
                # carta normal
                pontos += carta.valor
            elif carta.valor > 10:
                # J, Q ou K
                pontos += 10
            elif carta.valor == 1:
                # Ás
                pontos += 11
        # verifica se é possivel um hard value menor que 21 caso hajam ases na mao
        while num_ases > 0:
            if pontos > 21:
                pontos -= 10
                num_ases -= 1
            else:
                break
        return pontos

    # determina ação do jogador (hit ou stand)
    def player_action(self):
        valid = False
        while not valid:
            self.print_status()
            print("\nOpções: [1]Hit [2]Stand [3]Apostar")
            opt = input("> ")

            if opt == '1':
                self.player_hit()
                valid = True
            elif opt == '2':
                self.stand = True
                valid = True
            elif opt == '3':
                while True:
                    self.print_status()
                    try:
                        aposta = input("Digite o quanto quer apostar: ")
                        self.bet(int(aposta))  # jogador escolhe a aposta
                    except:
                        continue
                    else:
                        break

    def player_hit(self):
        self.mesa.jogadores[0].sacar_topo(self.mesa.baralho)
        if self.pontos(self.mesa.jogadores[0]) > 21:
            self.print_status()
            print("BUST! Você perdeu.\n")
            self.bust = True
        elif self.pontos(self.mesa.jogadores[0]) == 21:
            self.vinteum = True

    # determina ação do dealer (hit ou stand)
    def dealer_action(self):
        while self.pontos(self.mesa.jogadores[1]) < 17:
            self.mesa.jogadores[1].sacar_topo(self.mesa.baralho)
        if self.pontos(self.mesa.jogadores[1]) > 21:
            self.bust = True
            self.winner = True

    # compara pontos e determina vencedor
    def cards_compare(self):
        pts_jogador = self.pontos(self.mesa.jogadores[0])
        pts_dealer = self.pontos(self.mesa.jogadores[1])
        self.print_status()

        if pts_jogador > pts_dealer:
            self.winner = True
            print("Jogador venceu!")
            self.pagar(
                self.pontos(self.mesa.jogadores[0]))  # dá/tira pontos do jogador (1:1 vitoria normal, 3:2 blackjack)
        elif pts_jogador == pts_dealer:
            self.tie = True
            print("Empate!")
            self.pagar(
                self.pontos(self.mesa.jogadores[0]))  # dá/tira pontos do jogador (1:1 vitoria normal, 3:2 blackjack)
        else:
            print("A Casa venceu!")


    # dá pontos pro jogador - 1:1 vitoria normal, 3:2 blackjack
    def pagar(self, pontuacao):
        if self.winner:
            if pontuacao == 21:
                self.score += (self.pot + (self.pot *1.5))
                print("Blackjack! Prêmio: {}".format((self.pot *1.5)))
            else:
                self.score += 2*self.pot
                print("Prêmio: {}".format(self.pot))
        elif self.tie:
            self.score += self.pot



    # prompt continua/para
    def quit(self):
        valid = False
        if self.score < 10:
            self.fim = True
            self.valid = True
        while not valid:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Rodadas jogadas: {}".format(self.rodadas))
            print("Pontuação atual: {}".format(self.score))
            print("\n[1]Continuar [2]Parar")
            opt = input("> ")
            if opt == '2':
                self.fim = True
                valid = True
            elif opt == '1':
                valid = True



def print_underline(string, line):
    print('\n{}\n{}'.format(string, line * len(string)))

def main():

    bjgame = BJGame()
    bjgame.jogar()

if __name__ == '__main__':
    main()