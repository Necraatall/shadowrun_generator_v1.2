from enum import Enum, auto
import random
import re

from GeneratorAtributu.generator_atributu import *
from GeneratorJmen.Data.Gods.gods import *
from GeneratorJmen.Data.Name import (
    names,
    names_es,
    names_fi,
    names_fr,
    names_gk,
    names_hu,
    names_it,
    names_nl,
    names_no,
    names_pl,
    names_se,
    names_sk,
    names_us,
    names_vn,
    names_eg_ancient,
)

from GeneratorJmen.Data.NickName import (
    nicknames,
    # nicknames_cz for future if i find somewhere list of nicknames
)
from GeneratorJmen.Data.Surname import (
    surname,
    surname_cn,
    surname_cz,
    surname_de,
    surname_es,
    surname_fr,
    surname_gk,
    surname_hi,
    surname_ie,
    surname_il,
    surname_it,
    surname_kr,
    surname_ne,
    surname_pl,
    surname_pt,
    surname_ru,
    surname_gb,
    surname_us,
)
from GeneratorAppearance.Data.Body.body import *
from GeneratorAppearance.Data.Body.head import *
from GeneratorSocial.Data.characteristics import *
# from GeneratorAtributu.generator_atributu import *
from GeneratorAtributu.hokus import *

# TODO: asi lepe dat zdrojovy kod teto stranky a zkopnout
#    view-source:https://www.character-generator.org.uk/bio/

# TODO: nejdrive generovat gender, sexualni preference, rasu, z jake lidske rasy je,
# zemi puvodu, pak jmeno a pak dalsi
# TODO: prelozit lidske rasy a udelat zaklad na prekladac do cestiny, pokud se nebude nacitat ze souboru
# TODO: lidske/metalidske rasy predelat samostatne do enumu a dodelat Aborigince a Kapoidy
# TODO: Udalosti od 6ho roku narozeni - vymyslet jak generovat a z ceho - ? - sehnat data net ?
# TODO: ??? Predelat do souboru intenty ???? nebo rovnou vse udelat pres pydantic a nacitat z scv/excelu... ?
# TODO: rozmyslet si lepe adresarovou strukturu
# TODO: printovat bude jeden soubor k tomu urcenej - pokud soubory ci print dict
# TODO: dodelat testy a kouknout na "navrhove vzory" k priprave na dalsi verzi
# TODO: GPT chat - staci dat rozumnou frazi pred to jako:
# make me background story for shadowrun 4edition character played in post apocaliptic world afther nuclear bomb falls on earth
# see more about here:
# TODO: najit cestu jak testovat vysledne stringy ?AI?,
# slo by pres docstrings a pod kontrolory jazyka?
# - proste promyslet zda by u neceho nebylo lepsi mit jine datove typy, ci to nepostavit jinak
# zda uz nemyslet na reseni pres soubory, spoustec, linux/windows verzi a ospath pokud bude potreba
# / nabidnu at si vybere cestu
# kaslat na Os a jet pres pipenv
# ve 3. verzi mit klikacku webu kde se to bude generovat a ukladat do pdf a pod - pandas
# ve 4. zapojit tu webovku s AI co napises jakej obrazek a vygeneruje ti jej
# ve 4. zapojit tu webovku s AI (pokud je) co nahodim texty a ono mi to vygeneruje zivotni udalosti
# MEMO: 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 key for an openapi
# MEMO: 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 key for an openapi


# TODO: zakomponovat randomizer z shadowrunu ???
# http://www.miyako.pro/files/Games/Shadowrun/books/Shadowrun%204th%20Edition%20-%20Anniversary.pdf
# https://wrathofzombie.files.wordpress.com/2012/09/shadowrun-background-generator.pdf
# TODO: zapracovat radek od print(random.choice(list(Tribe_name_origin)).value)
# do radku if x in gods_egypt.intent_gods_about_eg:
# print(gods_egypt.intent_gods_about_eg[x])

###################################################
# New way
###################################################


def write_results():
    # Todays is only for set uped languages
    tribe_name_origin = tribe_name_origin_input()
    tribe_surname_origin = tribe_surname_origin_input()
    nickname = nicknames.Nickname.get_random_tribe_nickname()

    print("\n", tribe_name_origin + " \"" + nickname + "\" " + tribe_surname_origin, "\n")
    god = God.get_random_tribe_god_with_abouts()
    god_about = god
    god_about = god_about.replace("'", '"').replace("\\", "")
    god_about = god_about.split('", "')
    god_name = god_about[0].replace('("', "")
    god_about = god_about[1].replace('"),', "")
    print((f"God: \t{god_name}").replace("('", "").replace("'", "").replace("),", "").expandtabs(30))
    print((f"About God: \t{god_about}").replace("('", "").replace("'", "").replace("),", "").expandtabs(30))
    atributes = Atributes.make_atributes()[0]

    print((f"\nGender: \t{GENDER}").expandtabs(30))
    # TODO: Promyslet co vse tam dat tribe_name_origin asi jo
    # print(f"Parents origin land : {tribe_name_origin}")  # TODO: dodelat potrebuje navazat
    # print(random.choice(tuple(Tribe_name_origin)).value)
    # print(random.choice(tuple(Tribe_surname_origin)).value)
    print((f"Pleasure preferency: \t{SEXUAL_PREFERENCY_LIST}").expandtabs(30))
    print((f"Physical age: \t{Age.PHYSICAL_AGE.value}").expandtabs(30))
    if not any(s in race_choice for s in ('Caribbean', 'Latino/Hispanic', 'Caucasian', 'South_Asian', 'East_Asian', 'Mixed')):
        print((f"Human race and type: \t{race_choice}, {race_chosen[0]}").expandtabs(30))
    else:
        print((f"Human race: \t{race_choice}").expandtabs(30))
    metarace = atributes["Metatype"]
    print((f"Metahuman race: \t{metarace}").expandtabs(30))
    # TODO dict race print zakomponovat do vseho vcetne randomu vysky
    if not any(s in race_choice for s in ('Caribbean', 'Latino/Hispanic', 'Caucasian', 'South_Asian', 'East_Asian', 'Mixed')):
        print("\nOrigin:")
        original_race = race_details[race_choice][race_chosen[0]]
        for keys, value in original_race.items():
            print((f"{keys}: \t{value}").expandtabs(30))

    print("\nVisage:")
    print((f"Appearence age: \t{Age.APPEARENCE_AGE.value}").expandtabs(30))
    print((f"Social Class: \t{SOCIAL_CLASS}").expandtabs(30))
    # print((f"Height: \t{HEIGHT}").expandtabs(30))
    print(str(f"Weight: \t{WEIGHT}").expandtabs(30))
    print((f"Body: \t{BODY}").expandtabs(30))
    print((f"Body shape: \t{BODY_SHAPE}").expandtabs(30))
    print((f"Face and Hair: \t{FACE_AND_HAIR}").expandtabs(30))

    print("\nCharacter:")
    print((f"Psychical age: \t{Age.PSYCHICAL_AGE.value}").expandtabs(30))
    print((f"Positive characteristics: \t{POSITIVE_CHARACTERISTIC[0]}, {POSITIVE_CHARACTERISTIC[1]}").expandtabs(30))
    print((f"Negative characteristics: \t{NEGATIVE_CHARACTERISTIC[0]}, {NEGATIVE_CHARACTERISTIC[1]}").expandtabs(30))
    print((f"Political lean: \t{POLITICAL_LEAN}").expandtabs(30))

    print(f"\nAtributy:")
    for key, value in atributes.items():
        print(((f"{key}: \t{value}").replace("'", "").replace("[", "").replace("]", "")).expandtabs(30))


@staticmethod
def tribe_name_origin_input():
    chosen_tribe_name = random.randint(1, 18)
    gender = GENDER
    if gender == "female":
        gender_name = 1
    else:
        gender_name = 0
    match chosen_tribe_name:
        case 1:
            tribe_name_origin = "Polish"
            result_name = random.choice(names_pl.intent_names_pl)
        case 2:
            tribe_name_origin = "Neaderlanden"
            result_name = random.choice(names_nl.intent_names_nl)
        case 3:
            tribe_name_origin = "Spanish"
            result_name = random.choice(names.intent_names_es[random.randint(0, 2)])
        case 4:
            tribe_name_origin = "French"
            result_name = random.choice(names.intent_names_fr[random.randint(0, 2)])
        case 5:
            tribe_name_origin = "Greek"
            result_name = random.choice(names_gk.intent_names_gk)
        case 6:
            tribe_name_origin = "Italien"
            result_name = random.choice(names_it.intent_names_it)
        case 7:
            tribe_name_origin = "US. American"
            result_name = random.choice(names_us.intent_names_us)
        case 8:
            tribe_name_origin = "Finlanden"
            result_name = random.choice(names_fi.intent_names_fi)
        case 9:
            tribe_name_origin = "Hungarian"
            result_name = random.choice(names_hu.intent_names_hu)
        case 10:
            tribe_name_origin = "Norish"
            result_name = random.choice(names_no.intent_names_no)
        case 11:
            tribe_name_origin = "Sveedish"
            result_name = random.choice(names_se.intent_names_se)
        case 12:
            tribe_name_origin = "Slovakian"
            result_name = random.choice(names_sk.intent_names_sk)
        case 13:
            tribe_name_origin = "Vietnamees"
            result_name = random.choice(names_vn.intent_names_vn)
        case 14:
            tribe_name_origin = "Czech"
            result_name = random.choice(names.intent_names_cz[gender_name])
        case 15:
            tribe_name_origin = "Anglish"
            result_name = random.choice(names.intent_names_gb_scotish[gender_name])
        case 16:
            tribe_name_origin = "Aboriginal"
            result_name = random.choice(names.intent_names_au_aboriginal[random.randint(0, 2)])
        case 17:
            tribe_name_origin = "Australian"
            result_name = random.choice(names.intent_names_au[random.randint(0, 2)])
        case 18:
            tribe_name_origin = "Ancient Egypt"
            result_name = random.choice(names_eg_ancient.intent_names_eg_ancient)
    return result_name


@staticmethod
def tribe_surname_origin_input():
    tribe_surname_origin = random.randint(1, 17)
    match tribe_surname_origin:
        case 1:
            tribe_surname_origin = random.choice(surname_cn.intent_surname_cn)
        case 2:
            tribe_surname_origin = random.choice(surname_cz.intent_surname_cz)
        case 3:
            tribe_surname_origin = random.choice(surname_de.intent_surname_de)
        case 4:
            tribe_surname_origin = random.choice(surname_es.intent_surname_es)
        case 5:
            tribe_surname_origin = random.choice(surname_fr.intent_surname_fr)
        case 6:
            tribe_surname_origin = random.choice(surname_gk.intent_surname_gk)
        case 7:
            tribe_surname_origin = random.choice(surname_hi.intent_surname_hi)
        case 8:
            tribe_surname_origin = random.choice(surname_ie.intent_surname_ie)
        case 9:
            tribe_surname_origin = random.choice(surname_il.intent_surname_il)
        case 10:
            tribe_surname_origin = random.choice(surname_it.intent_surname_it)
        case 11:
            tribe_surname_origin = random.choice(surname_kr.intent_surname_kr)
        case 12:
            tribe_surname_origin = random.choice(surname_ne.intent_surname_ne)
        case 13:
            tribe_surname_origin = random.choice(surname_pl.intent_surname_pl)
        case 14:
            tribe_surname_origin = random.choice(surname_pt.intent_surname_pt)
        case 15:
            tribe_surname_origin = random.choice(surname_ru.intent_surname_ru)
        case 16:
            tribe_surname_origin = random.choice(surname_gb.intent_surname_gb)
        case 17:
            tribe_surname_origin = random.choice(surname_us.intent_surname_us)
    return tribe_surname_origin
