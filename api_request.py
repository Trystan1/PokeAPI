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
            # print(f'first {response["chain"]["evolves_to"][0]["species"]}')
            firstEvolution = response["chain"]["evolves_to"][0]["species"]["name"]
            firstEvolution = firstEvolution.capitalize()
            if firstEvolution == pokemonName: firstEvolution = ''
        except IndexError:
            pass

        try:
            # print(f'second {response["chain"]["evolves_to"][0]["evolves_to"][0]["species"]}')
            secondEvolution = response["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"]
            secondEvolution = secondEvolution.capitalize()
            if secondEvolution == pokemonName: secondEvolution = ''
        except IndexError:
            pass

        if firstEvolution == '':
            pokemonEvolution = secondEvolution
        elif secondEvolution == '':
            pokemonEvolution = firstEvolution
        else:
            pokemonEvolution = f'{firstEvolution},{secondEvolution}'

        pokeDex.append(
            {'name': pokemonName, 'evolution_path': pokemonEvolution, 'image': pokemonImage, 'attack': pokemonAttack,
             'defence': pokemonDefence,
             'types': typeList})
        # print(pokeDex[numPokemon-1])
        numPokemon += 1
        print(f'{numPokemon}/151')

    return pokeDex, numPokemon


def InitialiseDatabase():
    Pokedex = DataBase('Pokedex', ['name', 'evolution_path', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Pokedex.CreateTable()

    return Pokedex


FillPokedex()