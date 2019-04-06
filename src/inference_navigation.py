#!/usr/bin/env python3

from src import inference
import nltk

a = inference.InferenceCrime()


def getStringResults(results):
    res = ''
    for result in results:
        for (synrep, semrep) in result:
            res += str(semrep)
    return res


def add_room_after_crime(character_name: str, une_heure_apres: int, room_after_crime: str):
    s = [character_name + ' était dans le ' + room_after_crime + ' à ' + str(une_heure_apres) + 'h']
    print(s[0])
    a.add_any_clause(getStringResults(nltk.interpret_sents(s, '635/personne_piece_heure.fcfg')))


def add_hour_of_death(victim_name: str, hour_of_death: int):
    s = [victim_name + ' est morte à ' + str(hour_of_death) + 'h']
    print(s[0])
    a.add_any_clause(getStringResults(nltk.interpret_sents(s, '635/personne_morte_heure.fcfg')))
    a.add_any_clause('HeureCrimePlusOne({})'.format(hour_of_death + 1))


def add_character_info(character_name: str, room_name: str, is_alive: bool, has_marks_on_neck: bool):
    if is_alive:
        s = [character_name + ' est vivant']
        print(s[0])
        a.add_any_clause(getStringResults(nltk.interpret_sents(s, '635/personne_vivant.fcfg')))
    else:
        s = [character_name + ' est morte']
        print(s[0])
        a.add_any_clause(getStringResults(nltk.interpret_sents(s, '635/personne_morte.fcfg')))

    if has_marks_on_neck:
        s = [character_name + ' a des marques au cou']
        print(s[0])
        a.add_any_clause(getStringResults(nltk.interpret_sents(s, '635/personne_marque.fcfg')))

    s = [character_name + ' est dans le ' + room_name]
    print(s[0])
    a.add_any_clause(getStringResults(nltk.interpret_sents(s, '635/personne_piece.fcfg')))


def add_weapon_found_fact(weapon_name: str, room_name: str):
    s = ['Le ' + weapon_name + ' est dans le ' + room_name]
    print(s[0])
    a.add_any_clause(getStringResults(nltk.interpret_sents(s, '635/arme_piece.fcfg')))


def get_found_victim_name() -> str:
    return repr(a.get_victime())


def get_found_murderer_name() -> str:
    return repr(a.get_suspect())


def get_found_room_name() -> str:
    return repr(a.get_piece_crime())


def get_found_weapon_name() -> str:
    return repr(a.get_arme_crime())
