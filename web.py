from flask import Flask, render_template, request
from pokemon_database import *
from api_request import *

app = Flask(__name__)



@app.route("/")
def index():
    return render_template('welcome.html')

@app.route("/pokedex")
def pokedex():
    Pokedex = initialiseDatabase()
    pokeDex = Pokedex.getAllData()
    return render_template('pokedex.html', pokeDex=pokeDex)

@app.route("/pokedex/redownload")
def redownloaddata():
    main()
    return pokedex()



if __name__ == "__main__": app.run()

