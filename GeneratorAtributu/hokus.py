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
from .Data.race_basic_atributes import *

# základní list s atributy, ze kterého se vybírá
LISTATR = ['Body', 'Agility', 'Reaction', 'Strength', 'Charisma', 'Intuition', 'Logic', 'Willpower']
usedatr = LISTATR
LISTATR = list(LISTATR)
RACE_DICT: dict = {}
final_atributes: dict = {}
chosed_tuple: tuple = ()
# TODO: adventages celkovy pocet bodu na obdareni a postizeni
adventages: int = 0

# this one is prepared for the future
metahuman_race_list = ['Human', 'Orc', 'Dwarf', 'Elf', 'Troll']


def make_decision(choosen_set, pointspool):
    # choose_destiny - urci zda je mag, technomancer, remeslnik, vagus...
    choose_destiny: int = random.randint(1, 100)
    metahuman_race_decision = random.randint(96, 100)
    match metahuman_race_decision:
        case metahuman_race_decision if metahuman_race_decision in range(96, 101):
            # this is Troll
            metahuman_race_decision = metahuman_race_list[4]
            RACE_DICT: dict = TROLL_RACE_DICT

        case metahuman_race_decision if metahuman_race_decision in range(90, 95):
            # this is Elf
            metahuman_race_decision = metahuman_race_list[3]
            RACE_DICT: dict = ELF_RACE_DICT

        case metahuman_race_decision if metahuman_race_decision in range(85, 89):
            # this is Dwarf
            metahuman_race_decision = metahuman_race_list[2]
            RACE_DICT: dict = DWARF_RACE_DICT

        case metahuman_race_decision if metahuman_race_decision in range(80, 84):
            # this is Orc
            metahuman_race_decision = metahuman_race_list[1]
            RACE_DICT: dict = ORC_RACE_DICT

        case metahuman_race_decision if metahuman_race_decision in range(0, 79):
            # this is Human
            metahuman_race_decision = metahuman_race_list[0]
            RACE_DICT: dict = HUMAN_RACE_DICT

    return RACE_DICT


class Atributes():

    def make_atributes():
        celk_atributy: dict = {}
        final_atributes: dict = {}
        # pointspool celkovy pocet bodu na postavu
        pointspool: int
        # pointspool_skills pocet bodu na skilly, Edge, rasu, Merits and Flows (neg: critters)
        pointspool_skills: int  # na platbu za edge, rasu a skilly
        # pointspool_atr_start kolik je do zacatku max na atributy - zde rozdeluji vsechny body ktere lze zakoupit (muze
        pointspool_atr_start: int  # na vypocet atributu vcetne bonusu rasy
        # pointspool/2 must be [100,150,200,250,300] and between 425 and 600 BP
        pointspool = 600
        # TODO: better way for counting atributes and so one
        pointspool_atr_start = round((pointspool / 2) + (len(usedatr) * 10))
        pointspool_skills = round(pointspool / 2)
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
            choosen_set = chosensystem_dict_four[random.randint(1, len(chosensystem_dict_four))]
            make_decision(choosen_set, pointspool)

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
            make_decision(choosen_set, pointspool)

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
            make_decision(choosen_set, pointspool)

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
            make_decision(choosen_set, pointspool)

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
            make_decision(choosen_set, pointspool)

        if pointspool_atr_start >= 425 and pointspool_atr_start <= 600:
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
            choosen_set = chosen_realy_big_pool[random.randint(1, len(chosen_realy_big_pool))]
            # 330 and 380 BP don't have combination with 4 numbers
            # 425 BP up to the 600 BP is only number of 5 in pool of 6, 600 is maximum when all 6 is set
            make_decision(choosen_set, pointspool)

        RACE_DICT = make_decision(choosen_set, pointspool)
        for char in LISTATR:
            addon = random.choice(choosen_set)
            celk_atributy[char] = [(RACE_DICT[char][3] + addon),
                                   ' min:', RACE_DICT[char][0],
                                   ' max:', RACE_DICT[char][1],
                                   ' over:', RACE_DICT[char][2],
                                   ' race modifier:', RACE_DICT[char][3]]

        for key, value in celk_atributy.items():
            if key in RACE_DICT.items():
                final_atributes[key] = value + RACE_DICT[key]
            else:
                final_atributes[key] = value

        final_atributes['Metatype'] = RACE_DICT['Metatype']
        # final_atributes['Edge'] = RACE_DICT['Edge']
        final_atributes['Initiative_Phases'] = RACE_DICT['Initiative_Phases']
        final_atributes['Metatype_Ability'] = RACE_DICT['Metatype_Ability']

        # choose_destiny - urci zda je mag, technomancer, remeslnik, vagus...
        choose_destiny: int = random.randint(1, 100)
        if choose_destiny in range(95, 101):
            atributgen = random.randint(1, 4)
            final_atributes['Magic'] = atributgen
            pointspool_skills = (pointspool + 10) - (atributgen * 10)
        elif choose_destiny in range(80, 96):
            atributgen = random.randint(1, 3)
            final_atributes['Magic'] = atributgen
            pointspool_skills = (pointspool + 10) - (atributgen * 10)
        elif choose_destiny in range(75, 81):
            atributgen = random.randint(1, 3)
            final_atributes['Resonance'] = atributgen
            pointspool_skills = (pointspool + 10) - (atributgen * 10)
        if choose_destiny in range(0, 76):
            None

        return final_atributes, pointspool_skills
