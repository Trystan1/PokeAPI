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
    attackResult = None
    nextIndex = None
    attType = None
    if player1Cards == [] or player2Cards == []:
        return render_template('error.html', errorType="emptydatabase")
    else:
        return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards, playerIndex=playerIndex, attackResult=attackResult, nextIndex=nextIndex, players=Players, numplayers=NumPlayers, atttype=attType)

@app.route("/playgame/attack")
def Attack():
    attType = request.args.get('atttype')
    playerIndex = int(request.args.get('playerIndex'))
    NumPlayers = int(request.args.get('numplayers'))
    Players = PLAYERCHOICES[NumPlayers]
    Player1, Player2 = InitialiseDecks()
    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()
    nextIndex, attackResult = ComputeVictor(attType, Player1, Player2, playerIndex)
    endFlag = EndGame(Player1, Player2)
    if endFlag is None:
        return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards, playerIndex=playerIndex, attackResult=attackResult, nextIndex=nextIndex, players=Players, numplayers=NumPlayers, atttype=attType)
    else:
        return render_template('victoryscreen.html', endFlag=endFlag)

@app.route("/playgame/newround")
def NewRound():
    playerIndex = int(request.args.get('nextIndex'))
    NumPlayers = int(request.args.get('numplayers'))
    Players = PLAYERCHOICES[NumPlayers]
    Player1, Player2 = InitialiseDecks()
    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()
    attackResult = None
    nextIndex = None
    attType = None
    return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards, playerIndex=playerIndex, attackResult=attackResult, nextIndex=nextIndex, players=Players, numplayers=NumPlayers, atttype=attType)


@app.route("/playgame/nextbutton1")
def NextButton1():
    Player1, Player2 = InitialiseDecks()
    NextCard(Player1, 0)
    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()
    playerIndex = random.randint(0, 1)
    #TODO put attacking player into 'get attacking player' function for playgame, nextbutton1, nextbutton2

    return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards, attackingPlayer=playerIndex)


@app.route("/playgame/nextbutton2")
def NextButton2():
    Player1, Player2 = InitialiseDecks()
    NextCard(Player2, 1)
    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()
    playerIndex = random.randint(0, 1)

    return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards, attackingPlayer=playerIndex)


@app.route("/pokedex/redownload")
def RedownloadData():
    FillPokedex()
    return PokeDex()


if __name__ == "__main__": app.run()
