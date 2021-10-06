import requests


def getURL(attackType):

    r = requests.get(f'https://pokeapi.co/api/v2/type/')
    response = r.json()
    typeResults = response["results"]

    modifierURL = ''

    for pokemonType in typeResults:
        typeName = pokemonType["name"]

        if typeName == attackType:
            modifierURL = pokemonType["url"]

    return modifierURL


def getModifier(modifierURL, defenceTypes):

    damageValue = int(10)

    if modifierURL != '':
        r = requests.get(modifierURL)
        response = r.json()
        damageRelations = response["damage_relations"]

        doubleFlag = getModifierFlag(damageRelations, 'double_damage_to', defenceTypes)
        halfFlag = getModifierFlag(damageRelations, 'half_damage_to', defenceTypes)
        noFlag = getModifierFlag(damageRelations, 'no_damage_to', defenceTypes)

        if doubleFlag:damageValue = damageValue*2
        if halfFlag:damageValue = damageValue*0.5
        if noFlag:damageValue = damageValue*0

    else:
        damageValue = None

    return damageValue


def getModifierFlag(damageRelations, damageTo, defenceTypes):
    damageFlag = False
    doubleDamage = damageRelations[damageTo]

    for line in doubleDamage:
        if line["name"] in defenceTypes:
            damageFlag = True

    return damageFlag


def pokemonTypes(attackType, defenseTypes):
    modifierURL = getURL(attackType)
    damageModifier = getModifier(modifierURL, defenseTypes)
    return damageModifier/10


damageModifier = pokemonTypes('fighting', ['rock', 'fairy'])
