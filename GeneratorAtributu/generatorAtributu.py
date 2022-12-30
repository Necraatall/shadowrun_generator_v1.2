"""
    High level: kod dokaze vygenerovat atributy, ovlivnit rasou, zapsat do atributes_dict (vcetne Magie a resonance) a vypsat je
    Deep level: kod vyrandomuje zda dotycny je magic/resonance user (a odecte je ze zbyvajicich Pointspool)
                kod vybere z ktereho listu hodnot bude pridelovat hodnoty do atributu
                kod vybere hodnoty a priradi
                kod vybere rasu a modifikuje hodnoty atributu o jeji minima a maxima
                kod vypise hodnoty do terminalu a ulozi je docasne do slovniku
    Deepest level:  kod potrebuje mit hodnotu pointspool - je to pocet bodu na celou postavu
                    kod si zjisti hodnotu poctu bodu pro generovani atributu - pointspool_atr_start (polovina pointspool) a pripocte k ni 80 (za kazdy atribut 10)
                    kod prida hodnotu 5 ke skill bodum, paklize zustal zbytek diky lichemu poctu cisel 6
                    kod si randomizuje zda je magic user, pokud ano, tak vygeneruje mu hodnotu k atributu Magic/Reason, zapise jej do dict a listu
                    kod zjisti si kolik bodu ma na skilly a vygeneruje si jeden list z ktereho bude plnit random nepouzity atribut (100, 200, 250, 300, 425 a vice do hodnoty 600)
                    kod si zavola meta cast - rasy, a upravi hodnoty v dict i v listech
                    kod vypise vysledek

"""
import random
from dataclasses import dataclass
from typing import Dict

# základní list s atributy, ze kterého se vybírá
listatr = ['Body', 'Agility', 'Reaction', 'Strength', 'Charisma', 'Intuition', 'Logic', 'Willpower']
usedatr = listatr
listatr = list(listatr)
race_dict: dict = {}

vysl_atr = []
# TODO: dopsat popisky - domyslet remeslniky a pod. 
# choose_destiny = None   # 96 - 100 is full Thaumaturgic, 91-95 is full shamanic, 86-90 is Thaumaturgy Adept, 81-85 is Shamanic Adept, 75-80 is Technomancer  
# is_mage = None          # 10 is full Thaumaturgic, 9 is full shamanic, 8 is Thaumaturgy Adept, 7 is Shamanic Adept, 6 physical Adept, 7 is Technomancer 



human_race_dict = {
    'BS': 0,
    'Metatype': "Human",
    'Body':         (1, 6, 9, 0),
    'Agility':      (1, 6, 9, 0),
    'Reaction':     (1, 6, 9, 0),
    'Strength':     (1, 6, 9, 0),
    'Charisma':     (1, 6, 9, 0),
    'Intuition':    (1, 6, 9, 0),
    'Logic':        (1, 6, 9, 0),
    'Willpower':    (1, 6, 9, 0),
    'Initiative':   (2, 12, 18),
    'Edge':         (2, 7, 10, 1),
    'Initiative_Phases': 1,
    'Metatype Ability': "+1 Edge"
}

orc_race_dict = {
    'BS': 20,
    'Metatype': "Orc",
    'Body':         (4, 9, 13, 3),
    'Agility':      (1, 6, 9, 0),
    'Reaction':     (1, 6, 9, 0),
    'Strength':     (3, 8, 12, 2),
    'Charisma':     (1, 5, 7, -1),
    'Intuition':    (1, 6, 9, 0),
    'Logic':        (1, 5, 7, -1),
    'Willpower':    (1, 6, 9, 0),
    'Initiative':   (2, 12, 18),
    'Edge':         (1, 6, 9, 0),
    'Initiative_Phases': 1,
    'Metatype Ability': "Low-Light Vision"
}

dwarf_race_dict = {
    'BS': 25,
    'Metatype': "Dwarf",
    'Body':         (2, 7, 10, 1),
    'Agility':      (1, 6, 9, 0),
    'Reaction':     (1, 5, 7, -1),
    'Strength':     (3, 8, 12, 2),
    'Charisma':     (1, 6, 9, 0),
    'Intuition':    (1, 6, 9, 0),
    'Logic':        (1, 6, 9, 0),
    'Willpower':    (2, 7, 10, 0),
    'Initiative':   (2, 11, 16),
    'Edge':         (1, 6, 9, 0),
    'Initiative_Phases': 1,
    'Metatype Ability': "Thermographic Vision, +2 dice for Body Tests to resist pathogens and toxins"
}

elf_race_dict = {
    'BS': 30,
    'Metatype': "Elf",
    'Body':         (1, 6, 9, 0),
    'Agility':      (2, 7, 10, 1),
    'Reaction':     (1, 6, 9, 0),
    'Strength':     (1, 6, 9, 0),
    'Charisma':     (3, 8, 12, 2),
    'Intuition':    (1, 6, 9, 0),
    'Logic':        (1, 6, 9, 0),
    'Willpower':    (1, 6, 9, 0),
    'Initiative':   (2, 12, 18),
    'Edge':         (1, 6, 9, 0),
    'Initiative_Phases': 1,
    'Metatype Ability': "Low-Light Vision"
}

troll_race_dict = {
    'BS': 40,
    'Metatype': "Troll",
    'Body':         (5, 10, 15, 4),
    'Agility':      (1, 5, 7, -1),
    'Reaction':     (1, 6, 9, 0),
    'Strength':     (5, 10, 15, 4),
    'Charisma':     (1, 4, 6, -2),
    'Intuition':    (1, 5, 7, -1),
    'Logic':        (1, 5, 7, -1),
    'Willpower':    (1, 6, 9, 0),
    'Initiative':   (2, 11, 16),
    'Edge':         (2, 7, 10, 1),
    'Initiative_Phases': 1,
    'Metatype Ability': "Thermographic Vision, +1 Reach, +1 natural armor (cumulative with worn armor)"
}

# this one is prepared for the future
metahuman_race_list = ['Human', 'Orc', 'Dwarf', 'Elf', 'Troll']

# metodu 
@dataclass
class Set_all_atributes(object):
    """ sets the non-main atributes
    """
    def __init__(self, race_dict: dict, metahuman_race: str, listatr: list):
        self.race_dict = race_dict
        self.metahuman_race = metahuman_race
        self.listatr = listatr
        
        celk_atributy['Metatype'] = race_dict['Metatype']
        celk_atributy['Initiative'] = atributes_dict['Reaction'] + atributes_dict['Intuition']
        # For the future Initiative_Phases
        # celk_atributy['Initiative_Phases'] = atributes_dict['Initiative_Phases']
        for char in listatr:
            celk_atributy [char] = [atributes_dict[char] + race_dict[char][3], \
                    ' min: ', race_dict[char][0], \
                        ' max: ', race_dict[char][1], \
                            'over: ', race_dict[char][2]]
        celk_atributy['Body'] = human_race_dict['Body'][1] + random.choice(chosensystem_dict_four[1])
        celk_atributy['Body'] = human_race_dict['Body'][1] + random.choice(chosensystem_dict_four[1])
        celk_atributy['Body'] = human_race_dict['Body'][1] + random.choice(chosensystem_dict_four[1])
        celk_atributy['Body'] = human_race_dict['Body'][1] + random.choice(chosensystem_dict_four[1])
        celk_atributy['Body'] = human_race_dict['Body'][1] + random.choice(chosensystem_dict_four[1])
        celk_atributy['Body'] = human_race_dict['Body'][1] + random.choice(chosensystem_dict_four[1])
        celk_atributy['Body'] = human_race_dict['Body'][1] + random.choice(chosensystem_dict_four[1])
        celk_atributy['Body'] = human_race_dict['Body'][1] + random.choice(chosensystem_dict_four[1])
        # print(celk_atributy)

def make_decision():
    # choose_destiny - urci zda je mag, technomancer, remeslnik, vagus... 
    choose_destiny: int = random.randint(1, 100)
    # atributgen promenna pro vygenerovanou hodnotu atributu
    atributgen: int
    # pointspool celkovy pocet bodu na postavu
    pointspool: int
    # pointspool_skills pocet bodu na skilly, Edge, rasu, Merits and Flows (neg: critters)
    pointspool_skills: int  # na platbu za edge, rasu a skilly
    # pointspool_atr_start kolik je do zacatku max na atributy - zde rozdeluji vsechny body ktere lze zakoupit (muze
    pointspool_atr_start: int  # na vypocet atributu vcetne bonusu rasy
    # pointspool/2 must be [100,150,200,250,300] and between 425 and 600 BP
    pointspool = 200
    pointspool_atr_start = int((pointspool/2) + (len(usedatr) * 10))
    pointspool_skills = pointspool_atr_start
    maximum: int = len(usedatr)
    print('Počáteční body na rozdělení:', (pointspool_atr_start - 80))
    metahuman_race_decision = 100 # random.randint(96, 100)
    match metahuman_race_decision:
        case metahuman_race_decision if metahuman_race_decision in range(95, 101):
            # this is Troll
            metahuman_race_decision = metahuman_race_list[4]
            race_dict: dict = troll_race_dict
            Set_all_atributes(race_dict, metahuman_race_decision, listatr)
        case metahuman_race_decision if metahuman_race_decision in range(90, 96):
            # this is Elf
            metahuman_race_decision = metahuman_race_list[3]
            race_dict: dict = elf_race_dict
            Set_all_atributes(race_dict, metahuman_race_decision, listatr)
        case metahuman_race_decision if metahuman_race_decision in range(85, 91):
            # this is Dwarf
            metahuman_race_decision = metahuman_race_list[2]
            race_dict: dict = dwarf_race_dict
            Set_all_atributes(race_dict, metahuman_race_decision, listatr)
        case metahuman_race_decision if metahuman_race_decision in range(80, 86):
            # this is Orc
            metahuman_race_decision = metahuman_race_list[1]            
            race_dict: dict = orc_race_dict
            Set_all_atributes(race_dict, metahuman_race_decision, listatr)
        case metahuman_race_decision if metahuman_race_decision in range(0, 81):
            # this is Human
            metahuman_race_decision = metahuman_race_list[0]
            race_dict: dict = human_race_dict
            Set_all_atributes(race_dict, metahuman_race_decision, listatr)

    if choose_destiny in range(95, 101):
        atributgen = random.randint(1, 4)
        atributes_dict['Magic'] = atributgen
        vysl_atr.append('Magic ' + str(atributgen))
    elif choose_destiny in range(80, 96):
        atributgen = random.randint(1, 3)
        atributes_dict['Magic'] = atributgen
        vysl_atr.append('Magic ' + str(atributgen))
    elif choose_destiny in range(75, 81):
        atributgen = random.randint(1, 3)
        atributes_dict['Resonance'] = atributgen
        vysl_atr.append('Resonance ' + str(atributgen))
    elif choose_destiny in range(75, 101):
        pointspool_skills = (pointspool + 10) - (atributgen * 10)

    if choose_destiny in range(0, 76):
            atributgen = 0

    if choose_destiny is None:
        atributgen = 0

    maximum = len(usedatr) + 1
    result = [atributgen, pointspool_atr_start, maximum, pointspool_skills]
    return result

celk_atributy = {}
def make_atributes_loop():
    decision = make_decision()
    atributgen = int(decision[0])
    pointspool_atr_start = decision[1]

    decision = make_decision()
    atributgen = int(decision[0])
    pointspool_atr_start = decision[1]
    pointspool_atr = int(decision[1])
    pointspool_skills = int(decision[3])

    if pointspool_atr_start == 180:  # 100BP
        chosensystem_dict_four = {
            1: (4, 4, 2, 2, 2, 2, 1, 1),
            2: (4, 3, 3, 3, 2, 1, 1, 1),
            3: (4, 3, 3, 2, 2, 2, 1, 1),
            4: (4, 3, 2, 2, 2, 2, 2, 1),
            5: (4, 2, 2, 2, 2, 2, 2, 2),
            6: (3, 3, 3, 3, 3, 1, 1, 1),
            7: (3, 3, 3, 3, 2, 2, 1, 1),
            8: (3, 3, 3, 2, 2, 2, 2, 1),
            9: (3, 3, 2, 2, 2, 2, 2, 2),
        }
        print("key :", [key for key in human_race_dict])
        filtered = {}
        print("filtered :", filtered)
        # value = key if keyhum in human_race_dict else None
        choosen_set = chosensystem_dict_four[random.randint(1, len(chosensystem_dict_four))]


    if pointspool_atr_start == 230:  # 150BP
        chosensystem_dict_six = {
            1: (6, 3, 3, 2, 2, 2, 2, 1),
            2: (6, 3, 2, 2, 2, 2, 2, 2),
        }
        chosensystem_dict_five = {
            1: (5, 5, 4, 3, 3, 2, 1, 1),
            2: (5, 4, 4, 3, 3, 2, 1, 1),
            3: (5, 4, 4, 3, 2, 2, 2, 1),
            4: (5, 4, 4, 2, 2, 2, 2, 2),
            5: (5, 4, 3, 3, 3, 3, 1, 1),
            6: (5, 4, 3, 3, 3, 2, 2, 1),
            7: (5, 4, 3, 3, 2, 2, 2, 2),
            8: (5, 3, 3, 3, 3, 3, 2, 1),
            9: (5, 3, 3, 3, 3, 2, 2, 2),
        }
        chosensystem_dict_four = {
            1: (4, 4, 4, 3, 3, 3, 1, 1),
            2: (4, 4, 4, 3, 3, 2, 2, 1),
            3: (4, 4, 4, 3, 2, 2, 2, 2),
            4: (4, 4, 3, 3, 3, 3, 2, 1),
            5: (4, 4, 3, 3, 3, 2, 2, 2),
            6: (4, 3, 3, 3, 3, 3, 3, 1),
            5: (4, 3, 3, 3, 3, 3, 2, 2),
            5: (3, 3, 3, 3, 3, 3, 3, 2),
        }
        choose_dict = random.randint(1, 3)
        if choose_dict == 1:
            choosen_set = chosensystem_dict_six[random.randint(1, len(chosensystem_dict_six))]
        if choose_dict == 2:
            choosen_set = chosensystem_dict_five[random.randint(1, len(chosensystem_dict_five))]
        if choose_dict == 3:
            choosen_set = chosensystem_dict_four[random.randint(1, len(chosensystem_dict_four))]

    if pointspool_atr_start == 280:  # 200 BP
        chosensystem_dict_six = {
            1: (6, 5, 4, 3, 3, 3, 1, 1),
            2: (6, 5, 4, 3, 2, 2, 2, 2),
            3: (6, 5, 4, 4, 3, 2, 1, 1),
            4: (6, 5, 4, 3, 3, 3, 1, 1),
            5: (6, 5, 4, 3, 2, 2, 2, 2),
            6: (6, 5, 3, 3, 3, 3, 2, 1),
            7: (6, 4, 4, 3, 3, 3, 2, 1),
            8: (6, 4, 3, 3, 3, 3, 3, 1),
            9: (6, 3, 3, 3, 3, 3, 3, 2)
        }
        chosensystem_dict_five = {
            1: (5, 5, 4, 4, 4, 3, 2, 1),
            2: (5, 5, 4, 4, 3, 3, 3, 1),
            3: (5, 5, 4, 4, 3, 3, 2, 2),
            4: (5, 5, 4, 3, 3, 3, 3, 2),
            5: (5, 4, 4, 4, 3, 3, 3, 2),
            6: (5, 4, 4, 3, 3, 3, 3, 3)
        }
        chosensystem_dict_four = {
            1: (4, 4, 4, 4, 3, 3, 3, 3),
            2: (4, 4, 4, 4, 3, 3, 3, 1),
            3: (4, 4, 4, 4, 4, 4, 2, 2),
            4: (4, 4, 4, 4, 4, 3, 3, 2),
        }
        choose_dict = random.randint(1, 3)
        if choose_dict == 1:
            choosen_set = chosensystem_dict_six[random.randint(1, len(chosensystem_dict_six))]
        if choose_dict == 2:
            choosen_set = chosensystem_dict_five[random.randint(1, len(chosensystem_dict_five))]
        if choose_dict == 3:
            choosen_set = chosensystem_dict_four[random.randint(1, len(chosensystem_dict_four))]

    if pointspool_atr_start == 330:  # 250 BP
        chosensystem_dict_six = {
            1: (6, 6, 5, 5, 4, 2, 1, 1),
            2: (6, 6, 5, 4, 4, 2, 2, 1),
            3: (6, 6, 5, 4, 3, 3, 2, 1),
            4: (6, 6, 5, 3, 3, 3, 3, 1),
            5: (6, 6, 5, 3, 3, 3, 2, 2),
            6: (6, 6, 4, 3, 3, 3, 3, 2),
            7: (6, 5, 5, 4, 4, 3, 3, 1),
            8: (6, 5, 5, 4, 4, 3, 2, 2),
            9: (6, 5, 5, 4, 3, 3, 3, 2),
            10: (6, 5, 4, 4, 4, 3, 3, 2),
            11: (6, 4, 4, 4, 4, 3, 3, 3)
        }
        chosensystem_dict_five = {
            1: (5, 5, 5, 4, 4, 4, 3, 3),
            2: (5, 5, 4, 4, 4, 4, 4, 3),
            3: (5, 4, 4, 4, 4, 4, 4, 4)
        }

        choose_dict = random.randint(1, 2)
        if choose_dict == 1:
            choosen_set = chosensystem_dict_six[random.randint(1, len(chosensystem_dict_six))]
        if choose_dict == 2:
            choosen_set = chosensystem_dict_five[random.randint(1, len(chosensystem_dict_five))]

    if pointspool_atr_start == 380:  # 300 BP
        chosensystem_dict_six = {
            1: (6, 6, 5, 5, 4, 4, 4, 1),
            2: (6, 6, 5, 5, 4, 4, 3, 2),
            3: (6, 6, 5, 5, 4, 3, 3, 3),
            4: (6, 6, 5, 4, 4, 4, 3, 3),
            5: (6, 6, 4, 4, 4, 4, 4, 3),
            6: (6, 5, 5, 5, 4, 4, 4, 3),
            7: (6, 5, 5, 4, 4, 4, 4, 4)
        }
        chosensystem_dict_five = {
            1: (5, 5, 5, 5, 5, 5, 4, 4)
        }
        choose_dict = random.randint(1, 2)
        if choose_dict == 1:
            choosen_set = chosensystem_dict_six[random.randint(1, len(chosensystem_dict_six))]
        if choose_dict == 2:
            choosen_set = chosensystem_dict_five[random.randint(1, len(chosensystem_dict_five))]

    if pointspool_atr_start >= 425 and pointspool_atr <= 600:
        chosen_realy_big_pool = {
            1: (6, 5, 5, 5, 5, 5, 5, 5),
            2: (6, 6, 5, 5, 5, 5, 5, 5),
            3: (6, 6, 6, 5, 5, 5, 5, 5),
            4: (6, 6, 6, 6, 5, 5, 5, 5),
            5: (6, 6, 6, 6, 6, 5, 5, 5),
            6: (6, 6, 6, 6, 6, 6, 5, 5),
            7: (6, 6, 6, 6, 6, 6, 6, 5),
            8: (6, 6, 6, 6, 6, 6, 6, 6)
        }
        choosen_set = chosensystem_dict_six[random.randint(1, len(chosensystem_dict_six))]
        # 330 and 380 BP don't have combination with 4 numbers
        # 425 BP up to the 600 BP is only number of 5 in pool of 6, 600 is maximum when all 6 is set

    if 425 <= pointspool_atr_start < 600:
        number_of_five = int((pointspool_atr_start - 80 - 400) / 25)
        choosen_set = chosen_realy_big_pool[number_of_five]

    if 180 == pointspool_atr_start:
        atributgen = 4

    if 180 < pointspool_atr_start <= 230:
        atributgen = random.randint(4, 6)

    elif pointspool_atr_start == 330 or pointspool_atr_start == 380:
        atributgen = random.randint(5, 6)

    if 180 <= pointspool_atr_start <= 230 or pointspool_atr_start == 330 or pointspool_atr_start == 380:
        match atributgen:
            case 6:
                if pointspool_atr_start != 180:
                    choose = random.randint(1, len(chosensystem_dict_six.keys()))
                    choosen_set = chosensystem_dict_six[choose]
                    match pointspool_atr_start:
                        case pointspool_atr_start if pointspool_atr_start in [230, 280]:
                            pointspool_skills = pointspool_skills + 5
                        case 330:
                            if chosensystem_dict_six[choose][1] != 6:
                                pointspool_skills = pointspool_skills + 5
                        case 380:
                            if chosensystem_dict_six[choose][1] != 6:
                                pointspool_skills = pointspool_skills + 5
                        case pointspool_atr_start if pointspool_atr_start in [425, 475, 525, 575]:
                            if chosensystem_dict_six[choose][1] != 6:
                                pointspool_skills = pointspool_skills + 5
            case 5:
                if pointspool_atr_start != 180:
                    choose = random.randint(1, len(chosensystem_dict_five.keys()))
                    choosen_set = chosensystem_dict_five[choose]
            case 4:
                    choose = random.randint(1, len(chosensystem_dict_four.keys()))
                    choosen_set = chosensystem_dict_four[choose]

    # atributgen = choosen_set[i - 1]
    
    atributgen = random.choice(choosen_set) 
    # for i in choosen_set: choosen_set[i -1]

    if atributgen == 6:
        pointspool_atr = (pointspool_atr - (atributgen * 10)) - 15
    else:
        pointspool_atr = pointspool_atr - (atributgen * 10)

    atribut2 = random.choice(usedatr)
    usedatr.remove(atribut2)
    vysl_atr.append(atribut2 + " " + str(atributgen))
    atributes_dict[atribut2] = atributgen

    # prints list of results
    print(vysl_atr)
    # to count Initiative, need reaction and Intuition divided by 2 and save it to the dictionary
    pom = atributes_dict['Reaction'] + atributes_dict['Intuition']
    atributes_dict['Initiative'] = pom
    # runs function for combining atribut values with metahuman min/max-es
    metahuman_race(atributes_dict)
    # if atributes_dict['Metatype'] == "Human":
    #     celk_atributy['Edge'] = atributes_dict['Edge'] + race_dict['Edge'][3]
    # print result
    # print(atributes_dict)




