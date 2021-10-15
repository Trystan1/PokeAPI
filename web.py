from flask import Flask, render_template, request
from pokemon_database import *
from api_request import *
from game_mechanics import *
from constants import PLAYERCHOICES

app = Flask(__name__)


@app.route("/")
def Index():
    return render_template('welcome.html')


@app.route("/pokedex")
def PokeDex():
    Pokedex = InitialiseDatabase()
    pokeDex = Pokedex.GetAllData()
    return render_template('pokedex.html', pokeDex=pokeDex)


@app.route("/gameSetUp")
def GameSetUp():
    return render_template('gamesetup.html')


@app.route("/playgame")
def PlayGame():
    NumPlayers = int(request.args.get('players'))
    Players = PLAYERCHOICES[NumPlayers]
    Player1, Player2 = InitialiseDecks()
    Player1.DestroyTable(), Player2.DestroyTable()
    Player1, Player2 = InitialiseGame()
    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()
    playerIndex = random.randint(0, 1)
    winFlag = 0
    showDefender = 'False'
    nextIndex = None
    attType = None
    if player1Cards == [] or player2Cards == []:
        return render_template('error.html', errorType="emptydatabase")
    else:
        return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards,
                               playerIndex=playerIndex, nextIndex=nextIndex,
                               players=Players, numplayers=NumPlayers, atttype=attType,
                               winFlag=winFlag, showDefender=showDefender)


@app.route("/playgame/attack")
def Attack():
    attType = request.args.get('atttype')
    playerIndex = int(request.args.get('playerIndex'))
    NumPlayers = int(request.args.get('numplayers'))
    Players = PLAYERCHOICES[NumPlayers]
    Player1, Player2 = InitialiseDecks()
    showDefender = 'True'
    # compute's damage and updates database, winFlag = 1 if defender HP hit's <= 0
    # playerIndex switches unless the attacker wins, in which case no change
    nextIndex, damageDealt, winFlag, attType = ComputeAttack(attType, Player1, Player2, playerIndex)

    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()

    # decks are rotated, cards given to the attacker and hp's are restored to max (only on winFlag == 1)
    OnVictory(winFlag, Player1, Player2, nextIndex)
    # evolution as before but will only execute on winFlag == 1, otherwise evolveFlag = 0, evolvedCard = None
    evolveFlag, evolvedCard = EvolvePokemon(winFlag, nextIndex, Player1, Player2)

    endFlag = EndGame(Player1, Player2)
    if endFlag is None:
        return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards,
                               playerIndex=playerIndex, nextIndex=nextIndex,
                               players=Players, numplayers=NumPlayers, atttype=attType, evolveFlag=evolveFlag,
                               evolvedCard=evolvedCard, winFlag=winFlag, showDefender=showDefender, damageDealt=damageDealt)
    else:
        return render_template('victoryscreen.html', endFlag=endFlag)


@app.route("/playgame/newround")
def NewRound():
    playerIndex = int(request.args.get('nextIndex'))
    NumPlayers = int(request.args.get('numplayers'))
    showDefender = request.args.get('showDefender')
    Players = PLAYERCHOICES[NumPlayers]
    Player1, Player2 = InitialiseDecks()
    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()
    winFlag = 0
    nextIndex = None
    attType = None
    return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards, playerIndex=playerIndex,
                           nextIndex=nextIndex, players=Players, numplayers=NumPlayers,
                           atttype=attType, winFlag=winFlag, showDefender=showDefender)


@app.route("/pokedex/redownload")
def RedownloadData():
    FillPokedex()
    return PokeDex()


@app.route("/error/general")
def GeneralError():
    return render_template('error.html', errorType="generalError")


@app.route("/error/database")
def DatabaseError():
    return render_template('error.html', errorType="databaseError")


@app.route("/victory")
def Victory():
    endFlag = 'Player 1'
    return render_template('victoryscreen.html', endFlag=endFlag)


@app.route("/damage_relations")
def DamageRelations():
    return render_template('damage_relations.html')


if __name__ == "__main__": app.run()
