import random
from collections import deque
from pokemon_database import *
from api_request import InitialiseDatabase
from pokemon_types import PokemonTypes


def InitialiseDecks():
    Player1 = DataBase('Player1', ['name', 'evolution_path', 'image', 'max_hp', 'current_hp', 'attack', 'defence', 'types'],
                                  ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'TEXT'])
    Player1.CreateTable()
    Player2 = DataBase('Player2', ['name', 'evolution_path', 'image', 'max_hp', 'current_hp', 'attack', 'defence', 'types'],
                                  ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'TEXT'])
    Player2.CreateTable()
    return Player1, Player2


def InitialiseDeck(playerIndex):

    AttackingPlayer = None
    DefendingPlayer = None

    if playerIndex == 0:
        AttackingPlayer = DataBase('Player1', ['name', 'evolution_path', 'image', 'max_hp', 'current_hp', 'attack', 'defence', 'types'],
                                              ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'TEXT'])
        AttackingPlayer.CreateTable()
        DefendingPlayer = DataBase('Player2', ['name', 'evolution_path', 'image', 'max_hp', 'current_hp', 'attack', 'defence', 'types'],
                                              ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'TEXT'])
        DefendingPlayer.CreateTable()
    elif playerIndex == 1:
        AttackingPlayer = DataBase('Player2', ['name', 'evolution_path', 'image', 'max_hp', 'current_hp', 'attack', 'defence', 'types'],
                                              ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'TEXT'])
        AttackingPlayer.CreateTable()
        DefendingPlayer = DataBase('Player1', ['name', 'evolution_path', 'image', 'max_hp', 'current_hp', 'attack', 'defence', 'types'],
                                              ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'TEXT'])
        DefendingPlayer.CreateTable()

    return AttackingPlayer, DefendingPlayer


def GetEvolution(pokeDex):

    evolutions = []
    for individualPokemon in pokeDex:
        newEvolutions = individualPokemon['evolution_path'].split(",")
        for newEvolution in newEvolutions:
            evolutions.append(newEvolution)

    firstEvolutionPokedex = []
    for individualPokemon in pokeDex:
        if individualPokemon['name'] not in evolutions:
            firstEvolutionPokedex.append(individualPokemon)

    return firstEvolutionPokedex


def DealCards(pokeDex, Player1, Player2):
    deckLength = len(pokeDex)
    if deckLength % 2 == 0:
        handOneLength = int(deckLength / 2)
    else:
        handOneLength = int(deckLength // 2)

    random.shuffle(pokeDex)
    Player1.AddData(pokeDex[0:handOneLength])
    Player2.AddData(pokeDex[handOneLength:deckLength])


def InitialiseGame():
    Player1, Player2 = InitialiseDecks()
    Player1.DestroyTable()
    Player2.DestroyTable()
    Player1, Player2 = InitialiseDecks()
    Pokedex = InitialiseDatabase()
    pokeDex = Pokedex.GetAllData()
    firstEvolutionPokedex = GetEvolution(pokeDex)

    DealCards(firstEvolutionPokedex, Player1, Player2)

    return Player1, Player2


def NextCard(Player, playno):
    # Put first card in player 'deck' to end
    player = Player.GetAllData()
    player = deque(player)
    player.rotate(-1)
    player = list(player)
    Player.DestroyTable()
    Player1, Player2 = InitialiseDecks()
    if playno == 0:
        Player1.AddData(player)
    elif playno == 1:
        Player2.AddData(player)
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
    attackingPlayer = AttackingPlayer.GetAllData()
    attackingTypeString = attackingPlayer[0]['types']
    attackingTypes = attackingTypeString.split(",")
    attackingType = random.choice(attackingTypes)

    return attackingType


def GetDefenceTypes(Player1, Player2, playerIndex):
    DefendingPlayer = None
    if playerIndex == 0:
        DefendingPlayer = Player2
    elif playerIndex == 1:
        DefendingPlayer = Player1
    defendingPlayer = DefendingPlayer.GetAllData()
    defendingTypeString = defendingPlayer[0]['types']
    defendingTypes = defendingTypeString.split(",")
    return defendingTypes


def ComputeVictor(attackType, Player1, Player2, playerIndex):

    defenceTypes = GetDefenceTypes(Player1, Player2, playerIndex)
    # needs to call pokemonTypes, then workout how to define attacker and defender
    damageModifier = PokemonTypes(attackType, defenceTypes)

    attackingPlayer = None
    defendingPlayer = None
    AttackingPlayer = None
    DefendingPlayer = None

    if playerIndex == 0:
        AttackingPlayer = Player1
        attackingPlayer = AttackingPlayer.GetAllData()
        DefendingPlayer = Player2
        defendingPlayer = DefendingPlayer.GetAllData()
    elif playerIndex == 1:
        AttackingPlayer = Player2
        attackingPlayer = AttackingPlayer.GetAllData()
        DefendingPlayer = Player1
        defendingPlayer = DefendingPlayer.GetAllData()

    attackValue = int(attackingPlayer[0]['attack'])
    defenceValue = int(defendingPlayer[0]['defence'])
    modifiedAttack = damageModifier*attackValue
    attackResult = defenceValue - modifiedAttack

    if attackResult <= 0:
        # add defender's card to attacker
        AttackingPlayer.AddData([defendingPlayer[0]])
        # delete card from defender
        DefendingPlayer.DeleteLine(defendingPlayer[0]['name'])
        # rotate attacker's deck
        attackingPlayer = AttackingPlayer.GetAllData()
        attackingPlayer = deque(attackingPlayer)
        attackingPlayer.rotate(-1)
        attackingPlayer = list(attackingPlayer)
        AttackingPlayer.DestroyTable()
        AttackingPlayer, DefendingPlayer = InitialiseDeck(playerIndex)
        AttackingPlayer.AddData(attackingPlayer)

    elif attackResult > 0:
        # add attacker's card to defender
        DefendingPlayer.AddData([attackingPlayer[0]])
        # delete card from attacker
        AttackingPlayer.DeleteLine(attackingPlayer[0]['name'])
        # rotate defender's deck
        defendingPlayer = DefendingPlayer.GetAllData()
        defendingPlayer = deque(defendingPlayer)
        defendingPlayer.rotate(-1)
        defendingPlayer = list(defendingPlayer)
        DefendingPlayer.DestroyTable()
        AttackingPlayer, DefendingPlayer = InitialiseDeck(playerIndex)
        DefendingPlayer.AddData(defendingPlayer)
        # defender and attacker switch roles
        playerIndex = SwitchAttackingPlayer(playerIndex)

    return playerIndex, attackResult


def ComputeAttack(attType, Player1, Player2, playerIndex):

    winFlag = 0

    defenceTypes = GetDefenceTypes(Player1, Player2, playerIndex)

    if '[' in attType:
        print(f'the defender is shown and we are making an informed choice')
        # delete square brackets from either end
        attType = attType[:-1]
        attType = attType[1:]
        attType = attType.split(",")
        for i in range(0, len(attType)):
            # remove space in formatting for all but first in list
            if i > 0:
                attType[i] = attType[i][1:]
            # delete quotation marks from either side
            attType[i] = attType[i][:-1]
            attType[i] = attType[i][1:]

        print(attType)

        # pick the best option
        damage = []
        for typeAI in attType:
            damageModifier = PokemonTypes(typeAI, defenceTypes)
            damage.append(damageModifier)

        print(damage)
        highestIndex = damage.index(max(damage))

        attackType = str(attType[highestIndex])
    else:
        attackType = attType

    # needs to call pokemonTypes, then workout how to define attacker and defender
    damageModifier = PokemonTypes(attackType, defenceTypes)

    attackingPlayer = None
    defendingPlayer = None
    DefendingPlayer = None

    if playerIndex == 0:
        AttackingPlayer = Player1
        attackingPlayer = AttackingPlayer.GetAllData()
        DefendingPlayer = Player2
        defendingPlayer = DefendingPlayer.GetAllData()
    elif playerIndex == 1:
        AttackingPlayer = Player2
        attackingPlayer = AttackingPlayer.GetAllData()
        DefendingPlayer = Player1
        defendingPlayer = DefendingPlayer.GetAllData()

    attackValue = int(attackingPlayer[0]['attack'])
    defenceValue = int(defendingPlayer[0]['defence'])

    damageDealt = int((attackValue/defenceValue)*damageModifier*30)

    # modify defender's current hitpoints based upon this
    pokemonName = defendingPlayer[0]['name']
    initialHP = defendingPlayer[0]['current_hp']
    newHP = int(initialHP - damageDealt)

    if newHP <= 0:
        newHP = 0
        winFlag = 1

    DefendingPlayer.EditHP(newHP, pokemonName)
    print(f'{attackingPlayer[0]["name"]} attacked {defendingPlayer[0]["name"]} using {attackType}!')
    print(f'{pokemonName} initialHP: {initialHP}, HP after being attacked: {newHP}')

    if winFlag == 0:
        playerIndex = SwitchAttackingPlayer(playerIndex)

    return playerIndex, damageDealt, winFlag, attackType


def OnVictory(winFlag, Player1, Player2, playerIndex):

    if winFlag == 1:
        attackingPlayer = None
        AttackingPlayer = None
        defendingPlayer = None
        DefendingPlayer = None

        if playerIndex == 0:
            AttackingPlayer = Player1
            attackingPlayer = AttackingPlayer.GetAllData()
            DefendingPlayer = Player2
            defendingPlayer = DefendingPlayer.GetAllData()
        elif playerIndex == 1:
            AttackingPlayer = Player2
            attackingPlayer = AttackingPlayer.GetAllData()
            DefendingPlayer = Player1
            defendingPlayer = DefendingPlayer.GetAllData()

        # reset HP of both cards
        AttackingPlayer.EditHP(attackingPlayer[0]['max_hp'], attackingPlayer[0]['name'])
        DefendingPlayer.EditHP(defendingPlayer[0]['max_hp'], defendingPlayer[0]['name'])

        # get updated values of hand (hp reset)
        defendingPlayer = DefendingPlayer.GetAllData()

        # add defender's card to attacker
        AttackingPlayer.AddData([defendingPlayer[0]])
        # delete card from defender
        DefendingPlayer.DeleteLine(defendingPlayer[0]['name'])
        # rotate attacker's deck
        attackingPlayer = AttackingPlayer.GetAllData()
        attackingPlayer = deque(attackingPlayer)
        attackingPlayer.rotate(-1)
        attackingPlayer = list(attackingPlayer)
        AttackingPlayer.DestroyTable()
        AttackingPlayer, DefendingPlayer = InitialiseDeck(playerIndex)
        AttackingPlayer.AddData(attackingPlayer)

    else:
        pass


def EndGame(Player1, Player2):
    player1 = Player1.GetAllData()
    player2 = Player2.GetAllData()
    endFlag = None

    if len(player1) == 0:
        endFlag = 'Player 1'
    elif len(player2) == 0:
        endFlag = 'Player 2'

    return endFlag


def EvolvePokemon(winFlag, nextIndex, Player1, Player2):
    # take last card of the deck, check its evolution path and if is not none then delete it and replace with the fist
    # in the evolution list

    evolveFlag = 0
    evolvedCard = None

    if winFlag == 1:
        Pokedex = InitialiseDatabase()
        pokeDex = Pokedex.GetAllData()

        if nextIndex == 0:
            Player = Player1
        elif nextIndex == 1:
            Player = Player2
        else:
            Player = None

        playerDeck = Player.GetAllData()
        evolvingPokemon = playerDeck[-1]

        evolutions = evolvingPokemon['evolution_path'].split(",")

        print(evolvingPokemon['name'])

        if evolutions[0] != 'None':
            Player.DeleteLine(evolvingPokemon['name'])
            print('evolve!')
            evolveFlag = 1
            for line in pokeDex:
                if line['name'] == evolutions[0]:
                    print(f"Evolution into {line['name']}")
                    Player.AddData([line])
                    evolvedCard = line

    else:
        pass

    return evolveFlag, evolvedCard
