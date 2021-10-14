import requests
from pokemon_database import DataBase
import urllib.request

def FillPokedex():

    pokeDex, numPokemon = GetPokedex()
    if numPokemon != 151:
        print(f'Houston we have a problem, there are not enough Pokemon, returned {numPokemon}/151')

    pokeDex = CleanPokeDex(pokeDex)
    Pokedex = InitialiseDatabase()
    Pokedex.DestroyTable()
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
        pokemonHP = individualStats[0]["base_stat"]
        pokemonAttack = individualStats[1]["base_stat"]
        pokemonDefence = individualStats[2]["base_stat"]
        pokemonImage = response["sprites"]["other"]["official-artwork"]["front_default"]

        filename = f'static/Images/PokemonPNGs/{pokemonName}.png'
        urllib.request.urlretrieve(f'{pokemonImage}', filename)
        pokemonImage = f'Images/PokemonPNGs/{pokemonName}.png'

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
            {'name': pokemonName, 'evolution_path': pokemonEvolution, 'image': pokemonImage, 'max_hp': pokemonHP,
             'current_hp': pokemonHP, 'attack': pokemonAttack, 'defence': pokemonDefence, 'types': typeList})

        numPokemon += 1
        print(f'{numPokemon}/151')

    return pokeDex, numPokemon


def CleanPokeDex(pokeDex):
    # list all names from the pokeDex
    pokemonNames = []
    for line in pokeDex:
        pokemonNames.append(line['name'])

    # for each line, check the evolution path, if there is a pokemon in the evolution path which is not contained in the
    # names then remove it
    for i in range(0, len(pokeDex)):
        if pokeDex[i]['evolution_path'] is not None:
            evolutionPath = pokeDex[i]['evolution_path'].split(',')
            evolutionPathNew = ''
            for ii in range(0, len(evolutionPath)):
                if evolutionPath[ii] not in pokemonNames:
                    evolutionPath[ii] = None

                evolutionPathNew += f'{evolutionPath[ii]},'
            evolutionPathNew = evolutionPathNew[:-1]  # delete last comma

            pokeDex[i]['evolution_path'] = evolutionPathNew

    return pokeDex


def InitialiseDatabase():
    Pokedex = DataBase('Pokedex', ['name', 'evolution_path', 'image', 'max_hp', 'current_hp', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'INTEGER', 'INTEGER', 'TEXT'])
    Pokedex.CreateTable()

    return Pokedex
