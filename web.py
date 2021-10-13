from flask import Flask, render_template, request
from pokemon_database import *
from api_request import *
from game_mechanics import *
from random import randint

app = Flask(__name__)


@app.route("/")
def Index():
    return render_template('welcome.html')


@app.route("/pokedex")
def PokeDex():
    Pokedex = InitialiseDatabase()
    pokeDex = Pokedex.GetAllData()
    return render_template('pokedex.html', pokeDex=pokeDex)


@app.route("/playgame")
def PlayGame():
    Player1, Player2 = InitialiseGame()
    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()
    playerIndex = random.randint(0, 1)
    attackResult = None
    nextIndex = None
    if player1Cards == [] or player2Cards == []:
        return render_template('error.html', errorType="emptydatabase")
    else:
        return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards, playerIndex=playerIndex, attackResult=attackResult, nextIndex=nextIndex)


@app.route("/playgame/attack")
def Attack():
    attType = request.args.get('attType')
    playerIndex = int(request.args.get('playerIndex'))
    Player1, Player2 = InitialiseDecks()
    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()
    nextIndex, attackResult = ComputeVictor(attType, Player1, Player2, playerIndex)
    EvolvePokemon(nextIndex, Player1, Player2)
    endFlag = EndGame(Player1, Player2)
    if endFlag is None:
        return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards, playerIndex=playerIndex, attackResult=attackResult, nextIndex=nextIndex)
    else:
        return render_template('victoryscreen.html', endFlag=endFlag)


@app.route("/playgame/newround")
def NewRound():
    playerIndex = int(request.args.get('nextIndex'))
    Player1, Player2 = InitialiseDecks()
    player1Cards = Player1.GetAllData()
    player2Cards = Player2.GetAllData()
    attackResult = None
    nextIndex = None
    return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards, playerIndex=playerIndex, attackResult=attackResult, nextIndex=nextIndex)


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


@app.route("/damage_relations")
def DamageRelations():
    return render_template('damage_relations.html')


if __name__ == "__main__": app.run()
