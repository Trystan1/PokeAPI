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
    Pokedex = initialiseDatabase()
    pokeDex = Pokedex.getAllData()
    return render_template('pokedex.html', pokeDex=pokeDex)


@app.route("/playgame")
def PlayGame():
    Player1, Player2 = InitialiseGame()
    player1Cards = Player1.getAllData()
    player2Cards = Player2.getAllData()
    Players = [Player1, Player2]
    playerIndex = random.randint(0, 1)
    currentPlayer = Players[playerIndex]
    if player1Cards == [] or player2Cards == []:
        return render_template('error.html', errorType="emptydatabase", currentPlayer=currentPlayer)
    else:
        return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards)


@app.route("/playgame/nextbutton1")
def NextButton1():
    Player1, Player2 = InitialiseDecks()
    NextCard(Player1, 1)
    player1Cards = Player1.getAllData()
    player2Cards = Player2.getAllData()

    return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards)


@app.route("/playgame/nextbutton2")
def NextButton2():
    Player1, Player2 = InitialiseDecks()
    NextCard(Player2, 2)
    player1Cards = Player1.getAllData()
    player2Cards = Player2.getAllData()

    return render_template('game.html', player1Cards=player1Cards, player2Cards=player2Cards)


@app.route("/pokedex/redownload")
def RedownloadData():
    main()
    return PokeDex()


if __name__ == "__main__": app.run()
