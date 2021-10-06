import random
from pokemon_database import *
from api_request import initialiseDatabase


def InitialiseDecks():
    Player1 = DataBase('Player1', ['name', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Player1.createTable()
    Player2 = DataBase('Player2', ['name', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Player2.createTable()
    return Player1, Player2


def DealCards(pokeDex, Player1, Player2):
    random.shuffle(pokeDex)
    Player1.addData(pokeDex[0:76])
    Player2.addData(pokeDex[76:151])


def InitialiseGame():
    Player1, Player2 = InitialiseDecks()
    Player1.destroyTable()
    Player2.destroyTable()
    Player1, Player2 = InitialiseDecks()
    Pokedex = initialiseDatabase()
    pokeDex = Pokedex.getAllData()

    DealCards(pokeDex, Player1, Player2)
    player1 = Player1.getAllData()
    player2 = Player2.getAllData()

    print('Player 1')
    print(*player1, sep="\n")
    print('Player 2')
    print(*player2, sep="\n")


InitialiseGame()
