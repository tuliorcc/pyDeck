# pyDeck

OOP study in python: Game simulations using a centralized Deck library of classes.

### Deck.py

  Library that contains all the classes used by the games. Classes are all documented in the file itself (in Portuguese).
  Contains card, stack, deck, player, table, etc.
  
  <br />
  
### WarGame.py

  Simulates the game of War between two players, using standard rules. 
  
  #### Usage
  `python WarGame.py -r`  
  - `-r` or `--rodadas`: number of maximum rounds to simulate (default is 100).

  #### Usage example:
  ```
  python WarGame.py -r 250

  FIM DE JOGO!
  ============
  Resultados:
  Rodadas jogadas: 250
  Cartas: Bob: 20  x  Patrick: 32
  Vencedor: Patrick

  ``` 
