from flask import Flask, render_template, request
# from pokemon_database import *
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


@app.route("/pokedex/redownload")
def RedownloadData():
    main()
    return PokeDex()


if __name__ == "__main__": app.run()
