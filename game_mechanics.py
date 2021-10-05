import random
from collections import deque
from pokemon_database import *
from api_request import initialiseDatabase


def InitialiseDecks():
    Player1 = DataBase('Player1', ['name', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Player1.createTable()
    Player2 = DataBase('Player2', ['name', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Player2.createTable()
    DiscardPile = DataBase('DiscardPile', ['name', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    DiscardPile.createTable()
    return Player1, Player2, DiscardPile


def DealCards(pokeDex, Player1, Player2):
    random.shuffle(pokeDex)
    Player1.addData(pokeDex[0:76])
    Player2.addData(pokeDex[76:151])


def InitialiseGame():
    Player1, Player2, DiscardPile = InitialiseDecks()
    Player1.destroyTable()
    Player2.destroyTable()
    DiscardPile.destroyTable()
    Player1, Player2, DiscardPile = InitialiseDecks()
    Pokedex = initialiseDatabase()
    pokeDex = Pokedex.getAllData()

    DealCards(pokeDex, Player1, Player2)

    return Player1, Player2, DiscardPile


def NextCard(Player1):
    # Put first card in player 'deck' to end
    player1 = Player1.getAllData()
    player1 = deque(player1)
    player1.rotate(-1)
    player1 = list(player1)
    Player1.destroyTable()
    Player1, Player2, DiscardPile = InitialiseDecks()
    Player1.addData(player1)


def PreviousCard(Player1):
    # Put first card in player 'deck' to end
    player1 = Player1.getAllData()
    player1 = deque(player1)
    player1.rotate(1)
    player1 = list(player1)
    Player1.destroyTable()
    Player1, Player2, DiscardPile = InitialiseDecks()
    Player1.addData(player1)

## Lines for testing
# Player1, Player2, DiscardPile = InitialiseGame()
# player1 = Player1.getAllData()
# player2 = Player2.getAllData()
# print('Player 1')
# # print(*player1, sep="\n")
# print('Player 2')
# print(*player2, sep="\n")
# print('Player1 rotated')
# NextCard(Player1)
# print('Player2 rotated')
# NextCard(Player2)


# recommend that the shown card is the first one in the list
# clicking NextCard resorts the player1/2 list and updates the player database to match
