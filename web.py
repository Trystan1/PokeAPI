from flask import Flask, render_template, request
from game_mechanics import *
from api_request import *

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
def playGame():
    playerHands = InitialiseGame()
    return render_template('game.html', playerHands=playerHands)

@app.route("/pokedex/redownload")
def RedownloadData():
    main()
    return PokeDex()




if __name__ == "__main__": app.run()

