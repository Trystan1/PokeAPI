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


def SelectAttackingPlayer(Player1, Player2):
    Players = [Player1, Player2]
    playerIndex = random.randint(0, 1)
    AttackingPlayer = Players[playerIndex]
    return AttackingPlayer, playerIndex


def SwitchAttackingPlayer(Player1, Player2, playerIndex):
    if playerIndex == 0:
        playerIndex = 1
    elif playerIndex == 1:
        playerIndex = 0
    else:
        playerIndex = None

    Players = [Player1, Player2]
    AttackingPlayer = Players[playerIndex]
    return AttackingPlayer, playerIndex


def ComputerAttack(AttackingPlayer):
    attackingPlayer = AttackingPlayer.getAllData()
    attackingTypeString = attackingPlayer[0]['types']
    attackingTypes = attackingTypeString.split(",")
    attackingType = random.choice(attackingTypes)

    return attackingType


def GetDefenceTypes(Player1, Player2, playerIndex):
    if playerIndex == 0:
        DefendingPlayer = Player2
    elif playerIndex == 1:
        DefendingPlayer = Player1
    defendingPlayer = DefendingPlayer.getAllData()
    defendingTypeString = defendingPlayer[0]['types']
    defendingTypes = defendingTypeString.split(",")
    return defendingTypes


def ComputeVictor():
    # don't call me Shirley
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
Player1, Player2 = InitialiseGame()
# player1 = Player1.getAllData()
# player2 = Player2.getAllData()
# print(player1)
# print(player2)
AttackingPlayer, playerIndex = SelectAttackingPlayer(Player1, Player2)
attackingPlayer = AttackingPlayer.getAllData()
# print(playerIndex)
# print(attackingPlayer)
attackingType = ComputerAttack(AttackingPlayer)
# print(attackingType)
defendingTypes = GetDefenceTypes(Player1, Player2, playerIndex)
# print(defendingTypes)


# NextCard(Player1)
# NextCard(Player2)
# PlayCard(Player1)

