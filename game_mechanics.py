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

    return Player1, Player2


def NextCard(Player, playno):
    # Put first card in player 'deck' to end
    player = Player.getAllData()
    player = deque(player)
    player.rotate(-1)
    player = list(player)
    Player.destroyTable()
    Player1, Player2 = InitialiseDecks()
    if playno == 1:
        Player1.addData(player)
    elif playno == 2:
        Player2.addData(player)
    else:
        pass


def PlayCard(Player1):
    # when function is called, the first item in the player deck table is deleted ('played')
    # the same card is then added to the discard pile
    # you may want to add 'cardPlayed' as an output of this function?
    player1 = Player1.getAllData()
    cardPlayed = [player1[0]]
    player1.pop(0)
    Player1.destroyTable()
    Player1, Player2 = InitialiseDecks()
    # DiscardPile.addData(cardPlayed)
    Player1.addData(player1)


# Lines for testing
# Player1, Player2 = InitialiseGame()
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
# PlayCard(Player1)