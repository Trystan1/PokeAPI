from game_mechanics import *
from pokemon_database import DataBase
from api_request import *

class TestCards:

    @staticmethod
    def set_up_decks():
        # Arrange
        Player1, Player2 = InitialiseGame()

        # Act
        player1Cards = Player1.getAllData()
        player2Cards = Player2.getAllData()
        return player1Cards, player2Cards

    @staticmethod
    def test_decks_are_created():

        player1Cards, player2Cards = TestCards.set_up_decks()

        # Assert
        assert player1Cards is not None and player2Cards is not None

    @staticmethod
    def test_decks_are_of_correct_size():

        player1Cards, player2Cards = TestCards.set_up_decks()

        # Assert
        assert len(player1Cards) == 76 and len(player2Cards) == 75
