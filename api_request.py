import requests
from pokemon_database import DataBase


def main():

    pokeDex, numPokemon = getPokedex()
    if numPokemon != 151:
        print(f'Houston we have a problem, there are not enough Pokemon, returned {numPokemon}/151')
    Pokedex = initialiseDatabase()
    Pokedex.destroyTable()    # uncomment this if want a quick table reset
    Pokedex = initialiseDatabase()
    Pokedex.addData(pokeDex)
    return Pokedex


def getPokedex():

    r = requests.get(f'https://pokeapi.co/api/v2/pokemon/?offset=0&limit=151')

    response = r.json()
    pokemonObjects = response["results"]
    pokeDex = []
    numPokemon = 0

    # for each pokemon, use their url to go to another JSON Query taking you to individual stats
    for individualPokemon in pokemonObjects:

        pokemonName = individualPokemon['name']

        r = requests.get(individualPokemon['url'])
        response = r.json()
        individualStats = response["stats"]
        pokemonAttack = individualStats[1]["base_stat"]
        pokemonDefence = individualStats[2]["base_stat"]
        pokemonImage = response["sprites"]["other"]["official-artwork"]["front_default"]

        individualTypes = response["types"]
        typeList = ''
        for types in individualTypes:
            typeList += f'{types["type"]["name"]},'
        typeList = typeList[:-1]    # delete last comma

        pokeDex.append(
            {'name': pokemonName, 'image': pokemonImage, 'attack': pokemonAttack, 'defence': pokemonDefence,
             'types': typeList})

        numPokemon += 1
        print(f'{numPokemon}/151')

    return pokeDex, numPokemon


def initialiseDatabase():
    Pokedex = DataBase('Pokedex', ['name', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Pokedex.createTable()

    return Pokedex


# main()
