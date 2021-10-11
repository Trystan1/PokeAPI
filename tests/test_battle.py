from game_mechanics import *
from pokemon_database import DataBase

from api_request import *

class TestBattle:
# SCENARIO 1
    @staticmethod
    def set_up_Krabby_and_Clefable_Decks():
        Pokedex = InitialiseDatabase()
        pokeDex = Pokedex.GetAllData()
        Krabby = [next((item for item in pokeDex if item["name"] == "Krabby"), None)]
        Clefable = [next((item for item in pokeDex if item["name"] == "Clefable"), None)]
        Player1, Player2 = InitialiseDecks()
        Player1.DestroyTable(), Player2.DestroyTable()
        Player1, Player2 = InitialiseDecks()
        Player1.AddData(Krabby)
        Player2.AddData(Clefable)
        return Player1, Player2

    @staticmethod
    def test_winner_works():
        # Arrange
        # Put Krabby and Clefable at the top of the decks
        Player1, Player2 = TestBattle.set_up_Krabby_and_Clefable_Decks()

        # Act
        # Get them to fight
        attackType = 'water'
        playerIndex = 0
        playerIndex, attackResult = ComputeVictor(attackType, Player1, Player2, playerIndex)

        # Assert
        # Krabby should beat Clefable
        assert playerIndex == 0

    @staticmethod
    def test_winners_hand_increases():
        # Arrange
        # Put Krabby and Clefable at the top of the decks
        Player1, Player2 = TestBattle.set_up_Krabby_and_Clefable_Decks()

        # Act
        # Get them to fight
        attackType = 'water'
        playerIndex = 0
        ComputeVictor(attackType, Player1, Player2, playerIndex)

        # Assert
        # Player 1's hand should increase
        player1cards = Player1.GetAllData()
        player2cards = Player2.GetAllData()
        assert len(player1cards) == 2 and len(player2cards) == 0

    @staticmethod
    def test_winners_hand_increases_by_correct_pokemon():
        # Arrange
        # Put Krabby and Clefable at the top of the decks
        Player1, Player2 = TestBattle.set_up_Krabby_and_Clefable_Decks()

        # Act
        # Get them to fight
        attackType = 'water'
        playerIndex = 0
        ComputeVictor(attackType, Player1, Player2, playerIndex)

        # Assert
        # Player 1's hand should increase
        player1cards = Player1.GetAllData()
        assert player1cards[0]['name'] == 'Clefable'

#SCENARIO 2
    @staticmethod
    def set_up_Mew_and_Beedrill_Decks():
        Pokedex = InitialiseDatabase()
        pokeDex = Pokedex.GetAllData()
        Beedrill = [next((item for item in pokeDex if item["name"] == "Beedrill"), None)]
        Mew = [next((item for item in pokeDex if item["name"] == "Mew"), None)]
        Player1, Player2 = InitialiseDecks()
        Player1.DestroyTable(), Player2.DestroyTable()
        Player1, Player2 = InitialiseDecks()
        Player1.AddData(Beedrill)
        Player2.AddData(Mew)
        return Player1, Player2

    @staticmethod
    def test_right_type_attacker_wins():
        # Arrange
        # Put Beedrill and Mew at the top of the decks
        Player1, Player2 = TestBattle.set_up_Mew_and_Beedrill_Decks()

        # Act
        # Get them to fight
        attackType = 'bug'
        playerIndex = 0
        playerIndex, attackResult = ComputeVictor(attackType, Player1, Player2, playerIndex)

        # Assert
        # Beedrill should win against Mew
        assert playerIndex == 0

    @staticmethod
    def test_wrong_type_attacker_loses():
        # Arrange
        # Put Beedrill and Mew at the top of the decks
        Player1, Player2 = TestBattle.set_up_Mew_and_Beedrill_Decks()

        # Act
        # Get them to fight
        attackType = 'poison'
        playerIndex = 0
        playerIndex, attackResult = ComputeVictor(attackType, Player1, Player2, playerIndex)

        # Assert
        # Beedrill should lose against Mew
        assert playerIndex == 1
