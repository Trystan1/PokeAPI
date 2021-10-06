from game_mechanics import *
from pokemon_database import DataBase
from api_request import *

class TestCards:

    @staticmethod
    def test_decks_are_of_correct_size():

        # Arrange
        Pokedex = initialiseDatabase()
        pokeDex = Pokedex.getAllData()
        Player1, Player2, DiscardPile = InitialiseDecks()

        # Act
        DealCards(pokeDex, Player1, Player2)
        player1Cards = Player1.getAllData()
        player2Cards = Player2.getAllData()

        # Assert
        assert len(player1Cards) == 76 and len(player2Cards) == 75

    #TODO check with Dave how to get getAllData() to work within a static method
    #TODO check also how to create another test using the same body but a different assert (ie. make a function within card_tests to return player1cards, player2cards?)