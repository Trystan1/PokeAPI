from pokemon_types import *


class TestTypes:

    @staticmethod
    def test_fighting_with_rock():
        # Arrange
        damageModifier = PokemonTypes('fighting', ['rock'])

        # Assert
        assert damageModifier == 2

    @staticmethod
    def test_fighting_with_rock_and_grass():
        # Arrange
        damageModifier = PokemonTypes('fighting', ['rock', 'grass'])

        # Assert
        assert damageModifier == 2

    @staticmethod
    def test_fighting_with_rock_and_fairy():
        # Arrange
        damageModifier = PokemonTypes('fighting', ['rock', 'fairy'])

        # Assert
        assert damageModifier == 1

    @staticmethod
    def test_fighting_with_rock_and_fairy_and_ghost():
        # Arrange
        damageModifier = PokemonTypes('fighting', ['rock', 'fairy', 'ghost'])

        # Assert
        assert damageModifier == 0
