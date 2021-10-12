import requests
from pokemon_database import DataBase


def FillPokedex():

    pokeDex, numPokemon = GetPokedex()
    if numPokemon != 151:
        print(f'Houston we have a problem, there are not enough Pokemon, returned {numPokemon}/151')
    Pokedex = InitialiseDatabase()
    Pokedex.DestroyTable()    # uncomment this if want a quick table reset
    Pokedex = InitialiseDatabase()
    Pokedex.AddData(pokeDex)
    return Pokedex


def GetPokedex():

    r = requests.get(f'https://pokeapi.co/api/v2/pokemon/?offset=0&limit=151')

    response = r.json()
    pokemonObjects = response["results"]
    pokeDex = []
    numPokemon = 0

    # for each pokemon, use their url to go to another JSON Query taking you to individual stats
    for individualPokemon in pokemonObjects:

        pokemonName = individualPokemon['name']
        pokemonName = pokemonName.capitalize()      # capitalise first letter of name

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

        # get to species page
        r = requests.get(response["species"]["url"])
        response = r.json()
        # get to evolution chain page
        r = requests.get(response["evolution_chain"]["url"])
        response = r.json()

        try:
            firstEvolution = response["chain"]["evolves_to"][0]["species"]["name"]
            firstEvolution = firstEvolution.capitalize()
        except IndexError:
            firstEvolution = None

        try:
            secondEvolution = response["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
            secondEvolution = secondEvolution.capitalize()
        except IndexError:
            secondEvolution = None

        if firstEvolution == pokemonName:
            pokemonEvolution = secondEvolution
        elif secondEvolution == pokemonName:
            pokemonEvolution = None
        elif firstEvolution is not None and secondEvolution is None:
            pokemonEvolution = firstEvolution
        elif firstEvolution is not None and secondEvolution is not None:
            pokemonEvolution = f'{firstEvolution},{secondEvolution}'
        else:
            pokemonEvolution = None

        pokeDex.append(
            {'name': pokemonName, 'evolution_path': pokemonEvolution, 'image': pokemonImage, 'attack': pokemonAttack,
             'defence': pokemonDefence,
             'types': typeList})

        numPokemon += 1
        print(f'{numPokemon}/151')

    return pokeDex, numPokemon


def InitialiseDatabase():
    Pokedex = DataBase('Pokedex', ['name', 'evolution_path', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Pokedex.CreateTable()

    return Pokedex
