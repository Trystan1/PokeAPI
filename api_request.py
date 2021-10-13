import requests
from pokemon_database import DataBase


def FillPokedex():

    pokeDex, numPokemon = GetPokedex()
    if numPokemon != 151:
        print(f'Houston we have a problem, there are not enough Pokemon, returned {numPokemon}/151')

    pokeDex = CleanPokeDex(pokeDex)
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

        firstEvolutionList = []
        firstCounter = False
        i = 0
        while firstCounter is False:
            try:
                firstEvolution = response["chain"]["evolves_to"][i]["species"]["name"]
                firstEvolution = firstEvolution.capitalize()
                firstEvolutionList.append(firstEvolution)
            except IndexError:
                if i == 0:
                    firstEvolution = [None]
                    firstEvolutionList = firstEvolution
                firstCounter = True
            i += 1

        secondEvolutionList = []
        for i in range(len(firstEvolutionList)):
            subSecondEvoList = []
            secondCounter = False
            ii = 0
            while secondCounter is False:
                try:
                    secondEvolution = response["chain"]["evolves_to"][i]["evolves_to"][ii]["species"]["name"]
                    secondEvolution = secondEvolution.capitalize()
                    subSecondEvoList.append(secondEvolution)
                except IndexError:
                    if ii == 0:
                        secondEvolution = [None]
                        subSecondEvoList = secondEvolution
                    secondCounter = True
                ii += 1
            secondEvolutionList.append(subSecondEvoList)

        pokemonEvolution = ",".join(firstEvolutionList) + ",".join(secondEvolutionList[0])

        pokeDex.append(
            {'name': pokemonName, 'evolution_path': pokemonEvolution, 'image': pokemonImage, 'attack': pokemonAttack,
             'defence': pokemonDefence,
             'types': typeList})

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
    Pokedex = DataBase('Pokedex', ['name', 'evolution_path', 'image', 'attack', 'defence', 'types'],
                       ['TEXT', 'TEXT', 'TEXT', 'INTEGER', 'INTEGER', 'TEXT'])
    Pokedex.CreateTable()

    return Pokedex

