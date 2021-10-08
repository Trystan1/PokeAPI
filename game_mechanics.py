import random
from collections import deque
from pokemon_database import *
from api_request import initialiseDatabase
from pokemon_types import PokemonTypes


def InitialiseDecks():
    Player1 = DataBase('Player1', ['name', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Player1.createTable()
    Player2 = DataBase('Player2', ['name', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Player2.createTable()
    return Player1, Player2


def InitialiseDeck(playerIndex):

    if playerIndex == 0:
        AttackingPlayer = DataBase('Player1', ['name', 'image', 'attack', 'defence', 'types'],
                           ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
        AttackingPlayer.createTable()
        DefendingPlayer = DataBase('Player2', ['name', 'image', 'attack', 'defence', 'types'],
                           ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
        DefendingPlayer.createTable()
    elif playerIndex == 1:
        AttackingPlayer = DataBase('Player2', ['name', 'image', 'attack', 'defence', 'types'],
                                   ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
        AttackingPlayer.createTable()
        DefendingPlayer = DataBase('Player1', ['name', 'image', 'attack', 'defence', 'types'],
                                   ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
        DefendingPlayer.createTable()

    return AttackingPlayer, DefendingPlayer


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
    if playno == 0:
        Player1.addData(player)
    elif playno == 1:
        Player2.addData(player)
    else:
        pass


def SelectAttackingPlayer(Player1, Player2):
    Players = [Player1, Player2]
    playerIndex = random.randint(0, 1)
    AttackingPlayer = Players[playerIndex]
    return AttackingPlayer, playerIndex


def SwitchAttackingPlayer(playerIndex):
    if playerIndex == 0:
        playerIndex = 1
    elif playerIndex == 1:
        playerIndex = 0
    else:
        playerIndex = None

    return playerIndex


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


def ComputeVictor(attackType, Player1, Player2, playerIndex):

    defenceTypes = GetDefenceTypes(Player1, Player2, playerIndex)
    # needs to call pokemonTypes, then workout how to define attacker and defender
    damageModifier = PokemonTypes(attackType, defenceTypes)

    if playerIndex == 0:
        AttackingPlayer = Player1
        attackingPlayer = AttackingPlayer.getAllData()
        DefendingPlayer = Player2
        defendingPlayer = DefendingPlayer.getAllData()
    elif playerIndex == 1:
        AttackingPlayer = Player2
        attackingPlayer = AttackingPlayer.getAllData()
        DefendingPlayer = Player1
        defendingPlayer = DefendingPlayer.getAllData()

    attackValue = int(attackingPlayer[0]['attack'])
    defenceValue = int(defendingPlayer[0]['defence'])
    modifiedAttack = damageModifier*attackValue
    attackResult = defenceValue - modifiedAttack

    if attackResult <= 0:
        print('attacker victory')
        # add defender's card to attacker
        AttackingPlayer.addData([defendingPlayer[0]])
        # delete card from defender
        DefendingPlayer.deleteLine(defendingPlayer[0]['name'])
        # rotate attacker's deck
        attackingPlayer = AttackingPlayer.getAllData()
        attackingPlayer = deque(attackingPlayer)
        attackingPlayer.rotate(-1)
        attackingPlayer = list(attackingPlayer)
        AttackingPlayer.destroyTable()
        AttackingPlayer, DefendingPlayer = InitialiseDeck(playerIndex)
        AttackingPlayer.addData(attackingPlayer)

    elif attackResult > 0:
        print('defender victory')
        # add attacker's card to defender
        DefendingPlayer.addData([attackingPlayer[0]])
        # delete card from attacker
        AttackingPlayer.deleteLine(attackingPlayer[0]['name'])
        # rotate defender's deck
        defendingPlayer = DefendingPlayer.getAllData()
        defendingPlayer = deque(defendingPlayer)
        defendingPlayer.rotate(-1)
        defendingPlayer = list(defendingPlayer)
        DefendingPlayer.destroyTable()
        AttackingPlayer, DefendingPlayer = InitialiseDeck(playerIndex)
        DefendingPlayer.addData(defendingPlayer)
        # defender and attacker switch roles
        playerIndex = SwitchAttackingPlayer(playerIndex)

    return playerIndex, attackResult


def EndGame(Player1, Player2):
    player1 = Player1.GetAllData()
    player2 = Player2.GetAllData()
    endFlag = False

    if len(player1) == 0 or len(player2) == 0:
        endFlag = True

    return endFlag

# --------------------- Lines for testing
# Player1, Player2 = InitialiseGame()
# Player1, Player2 = InitialiseDecks()
# player1 = Player1.getAllData()
# player2 = Player2.getAllData()
# print(f"Player 1: {player1[0]['name']}, attack: {player1[0]['attack']}, defence: {player1[0]['defence']}, types: {player1[0]['types']}")
# print(f"Player 2: {player2[0]['name']}, attack: {player2[0]['attack']}, defence: {player2[0]['defence']}, types: {player2[0]['types']}")
# AttackingPlayer, playerIndex = SelectAttackingPlayer(Player1, Player2)
# attackingPlayer = AttackingPlayer.getAllData()
# attackType = ComputerAttack(AttackingPlayer)
# print(f'Player {playerIndex+1} ({attackingPlayer[0]["name"]}) is attacking, using their {attackType} type')
# defendingTypes = GetDefenceTypes(Player1, Player2, playerIndex)
# print(f"The defender's types are {defendingTypes}")
# playerIndex, attackResult = ComputeVictor(attackType, Player1, Player2, playerIndex)
# print(f"The new attacker is Player: {playerIndex+1}")

# --------------------- All you actually need to put in web.py
Player1, Player2 = InitialiseDecks()
AttackingPlayer, playerIndex = SelectAttackingPlayer(Player1, Player2)   # not after game initialisation
attackType = ComputerAttack(AttackingPlayer)    # this is coming from the frontend?
playerIndex, attackResult = ComputeVictor(attackType, Player1, Player2, playerIndex)
