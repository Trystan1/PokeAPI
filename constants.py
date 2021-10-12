import os

if os.getcwd().endswith('tests'):
    DATABASE = '../pokemon_library.db'
else:
    DATABASE = 'pokemon_library.db'


PLAYERCHOICES = {
    0: ['CPU 1', 'CPU 2'],
    1: ['Player', 'CPU'],
    2: ['Player 1', 'Player 2']
}
