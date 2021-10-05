from flask import Flask, render_template, request
from pokemon_database import *
from api_request import *
from game_mechanics import *

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
    Player1, Player2, DiscardPile = InitialiseGame()
    player1 = Player1.getAllData()
    player2 = Player2.getAllData()
    print('Player 1')
    print(*player1, sep="\n")
    print('Player 2')
    print(*player2, sep="\n")
    return render_template('game.html')


@app.route("/pokedex/redownload")
def RedownloadData():
    main()
    return PokeDex()


if __name__ == "__main__": app.run()
