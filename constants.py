import os

if os.getcwd().endswith('tests'):
    DATABASE = '../pokemon_library.db'
else:
    DATABASE = 'pokemon_library.db'
