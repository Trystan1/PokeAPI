from game_mechanics import *
from pokemon_database import DataBase

from api_request import *

class TestEvolutions:

    @staticmethod
    def set_up_decks():
        # Arrange
        Player1, Player2 = InitialiseGame()

        # Act
        player1Cards = Player1.GetAllData()
        player2Cards = Player2.GetAllData()
        return player1Cards, player2Cards

    @staticmethod
    def set_up_specific_pokemon_fight(pokemon1, pokemon2):
        Pokedex = InitialiseDatabase()
        pokeDex = Pokedex.GetAllData()
        Pokemon1 = [next((item for item in pokeDex if item["name"] == pokemon1), None)]
        Pokemon2 = [next((item for item in pokeDex if item["name"] == pokemon2), None)]
        if Pokemon1 is None or Pokemon2 is None:
            print("There has been an error... one of your pokemon is a fraud")
        Player1, Player2 = InitialiseDecks()
        Player1.DestroyTable(), Player2.DestroyTable()
        Player1, Player2 = InitialiseDecks()
        Player1.AddData(Pokemon1)
        Player2.AddData(Pokemon2)
        return Player1, Player2

    @staticmethod
    def test_decks_correct_size():
        player1Cards, player2Cards = TestEvolutions.set_up_decks()

        assert len(player1Cards) == 40 and len(player2Cards) == 40

    @staticmethod
    def test_bulbasaur_evolves_on_win():

        Player1, Player2 = TestEvolutions.set_up_specific_pokemon_fight('Bulbasaur', 'Squirtle')

        attackType = 'grass'
        playerIndex = 0
        nextIndex, attackResult = ComputeVictor(attackType, Player1, Player2, playerIndex)
        EvolvePokemon(nextIndex, Player1, Player2)
        player1cards = Player1.GetAllData()

        assert player1cards[1]['name'] == 'Ivysaur'

    @staticmethod
    def test_ivysaur_evolves_on_win():
        Player1, Player2 = TestEvolutions.set_up_specific_pokemon_fight('Ivysaur', 'Squirtle')

        attackType = 'grass'
        playerIndex = 0
        nextIndex, attackResult = ComputeVictor(attackType, Player1, Player2, playerIndex)
        EvolvePokemon(nextIndex, Player1, Player2)
        player1cards = Player1.GetAllData()

        assert player1cards[1]['name'] == 'Venusaur'

    @staticmethod
    def test_bulbasaur_remains_on_lose():
        Player1, Player2 = TestEvolutions.set_up_specific_pokemon_fight('Charmander', 'Bulbasaur')

        attackType = 'fire'
        playerIndex = 0
        nextIndex, attackResult = ComputeVictor(attackType, Player1, Player2, playerIndex)
        EvolvePokemon(nextIndex, Player1, Player2)
        player1cards = Player1.GetAllData()

        assert player1cards[0]['name'] == 'Bulbasaur'

    @staticmethod
    def test_bulbasaur_removed_on_win():
        Player1, Player2 = TestEvolutions.set_up_specific_pokemon_fight('Bulbasaur', 'Squirtle')

        attackType = 'grass'
        playerIndex = 0
        nextIndex, attackResult = ComputeVictor(attackType, Player1, Player2, playerIndex)
        EvolvePokemon(nextIndex, Player1, Player2)
        player1cards = Player1.GetAllData()
        player1pokemon = []
        for card in player1cards:
            player1pokemon.append(card['name'])

        assert 'Bulbasaur' not in player1pokemon